"""Operating-path ingest. Real sources only. Never calls mock feeds."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from golf_offshoot.data_feeds.base import (
    FallbackChain,
    FeedError,
    MockOnOperatingPathError,
    assert_operating_quality,
    unavailable_quality,
)
from golf_offshoot.data_feeds.bovada import BovadaOddsFeed
from golf_offshoot.data_feeds.hardrock import HardRockBetOddsFeed, resolve_odds_book
from golf_offshoot.data_feeds.datagolf import DataGolfRecentSgFeed
from golf_offshoot.data_feeds.espn import (
    EspnClient,
    EspnFieldFeed,
    _finish_place,
    _place_display,
    _score_to_par,
    _status_name,
    _thru_holes,
    espn_course_weather,
    iter_competitors,
    parse_course,
    parse_event_payload,
    parse_season_rankings,
    parse_tournament,
)
from golf_offshoot.data_feeds.history import (
    HistoryIndex,
    event_from_espn,
    quality_for_feature,
)
from golf_offshoot.data_feeds.http import HttpCache
from golf_offshoot.data_feeds.odds_api import OddsApiFeed
from golf_offshoot.data_feeds.openings import merge_archived_openings, persist_prematch_openings
from golf_offshoot.data_feeds.openmeteo import OpenMeteoClient, OpenMeteoWeatherFeed
from golf_offshoot.config import HISTORY_YEARS
from golf_offshoot.data_feeds.asof_sg import AsOfSgIndex, asof_coverage_report, scale_recent_sg_quality
from golf_offshoot.data_feeds.pga_sg import PgaTourSgFeed, SgTable
from golf_offshoot.market.coverage import market_coverage_report
from golf_offshoot.market.freshness import apply_odds_freshness, odds_ttl_seconds
from golf_offshoot.models.enums import DataRole, RunMode, SourceKind
from golf_offshoot.models.schemas import (
    DataQuality,
    FieldSnapshot,
    MarketQuote,
    PlayerInputs,
    SourceInventoryItem,
    StrokesGainedProfile,
    Tournament,
)


class RealIngestor:
    """Build a tournament field from ESPN + Open-Meteo + Bovada/Odds API + PGA SG."""

    def __init__(
        self,
        cache: HttpCache | None = None,
        refresh: bool = False,
        history_years: tuple[int, ...] = HISTORY_YEARS,
    ) -> None:
        self.cache = cache or HttpCache()
        self.refresh = refresh
        self.espn = EspnClient(self.cache, refresh=refresh)
        self.meteo = OpenMeteoClient(self.cache, refresh=refresh)
        self.history_years = history_years
        self._history: HistoryIndex | None = None
        self._asof: AsOfSgIndex | None = None

    def load_history(self, *, include_in_progress: bool = False) -> HistoryIndex:
        if self._history is not None:
            return self._history
        idx = HistoryIndex()
        seen: set[str] = set()
        for year in self.history_years:
            for season_type in (2, 3):
                try:
                    ids = self.espn.season_event_ids(year, season_type)
                except FeedError:
                    continue
                for eid in ids:
                    if eid in seen:
                        continue
                    seen.add(eid)
                    try:
                        payload = self.espn.event_leaderboard(eid, live=False)
                        ev = event_from_espn(payload)
                    except (FeedError, AttributeError, TypeError, KeyError, ValueError) as exc:
                        print(f"skip {eid}: {exc}", flush=True)
                        continue
                    if ev.status_state != "post" and not include_in_progress:
                        continue
                    if ev.field_size < 10:
                        continue
                    idx.events.append(ev)
                    if len(idx.events) % 10 == 0:
                        print(f"history: {len(idx.events)} completed events cached", flush=True)
        idx.sorted()
        self._attach_historical_weather(idx)
        self._history = idx
        return idx

    def load_asof(self, year: int) -> AsOfSgIndex:
        if self._asof is not None and self._asof.year == year:
            return self._asof
        idx = AsOfSgIndex(PgaTourSgFeed(self.cache, refresh=self.refresh), year=year)
        idx.load_pills()
        idx.bind_history(self.load_history().events)
        self._asof = idx
        return idx

    def _attach_historical_weather(self, idx: HistoryIndex) -> None:
        weather_feed = OpenMeteoWeatherFeed(self.meteo)
        for ev in idx.events:
            if ev.wind_kph is not None:
                continue
            if not (ev.start_date or "").startswith("2026"):
                continue
            payload, q = weather_feed.quality_or_missing(
                city=ev.city,
                region=ev.state,
                start_date=ev.start_date,
                end_date=ev.start_date,
                historical=True,
            )
            if payload and not q.missing:
                ev.wind_kph = payload.get("wind_kph")
                ev.rain_mm = payload.get("rain_mm")

    def current_event_id(self) -> str:
        payload = self.espn.current_leaderboard()
        event = parse_event_payload(payload)
        return str(event["id"])

    def ingest(
        self,
        event_id: str | None = None,
        *,
        mode: RunMode = RunMode.PRE_TOURNAMENT,
        include_season_stats: bool = True,
        include_odds: bool = True,
        odds_book: str = "auto",
    ) -> tuple[Tournament, FieldSnapshot, list[MarketQuote], list[SourceInventoryItem]]:
        live_board = event_id is None
        payload = (
            self.espn.current_leaderboard()
            if live_board
            else self.espn.event_leaderboard(str(event_id), live=True)
        )
        event = parse_event_payload(payload)
        eid = str(event["id"])
        course, course_q = parse_course(event)
        tournament = parse_tournament(event, course)
        assert_operating_quality(course_q, context="course")

        espn_wx, espn_wx_q = espn_course_weather(event)
        addr = ((event.get("courses") or [{}])[0].get("address") or {})
        om_feed = OpenMeteoWeatherFeed(self.meteo)
        om_payload, om_q = om_feed.quality_or_missing(
            city=addr.get("city") or "",
            region=addr.get("state") or "",
            historical=False,
        )
        weather, weather_q = _pick_weather(espn_wx, espn_wx_q, om_payload, om_q)
        wind_kph = None
        if weather:
            if weather.get("wind_kph") is not None:
                wind_kph = float(weather["wind_kph"])
            elif weather.get("wind_mph") is not None:
                wind_kph = float(weather["wind_mph"]) * 1.609

        history = self.load_history(include_in_progress=False)
        sg_feed = PgaTourSgFeed(self.cache, refresh=self.refresh)
        sg_year = int(str(tournament.start_date)[:4]) if tournament.start_date else 2026
        asof = self.load_asof(sg_year)
        asof_bundle = asof.bundle_for(
            before=tournament.start_date,
            exclude_event_id=tournament.espn_event_id,
            exclude_name=tournament.name,
        )
        sg_cur, sg_cur_q = sg_feed.quality_or_missing(year=sg_year)
        sg_prev, sg_prev_q = sg_feed.quality_or_missing(year=sg_year - 1)
        comps = [c for c in iter_competitors(event) if c.get("athlete")]
        players: list[PlayerInputs] = []
        sg_missing = 0
        sg_prior_season = 0
        sg_through_event = 0
        recent_sg_n = 0
        season_n = 0
        sg_unmatched: list[str] = []
        for comp in comps:
            pi = self._player_inputs(
                comp,
                tournament,
                history,
                wind_kph,
                mode=mode,
                include_season_stats=include_season_stats,
                sg_feed=sg_feed,
                sg_current=sg_cur if isinstance(sg_cur, SgTable) else None,
                sg_current_q=sg_cur_q,
                sg_prior=sg_prev if isinstance(sg_prev, SgTable) else None,
                sg_prior_q=sg_prev_q,
                asof_bundle=asof_bundle,
            )
            if pi.sg.quality is None or pi.sg.quality.missing:
                sg_missing += 1
                sg_unmatched.append(pi.player.name)
            elif "prior season" in (pi.sg.quality.notes or "").lower():
                sg_prior_season += 1
            elif "THROUGH_EVENT" in (pi.sg.quality.notes or ""):
                sg_through_event += 1
            if pi.recent_sg is not None and pi.recent_sg.quality is not None and not pi.recent_sg.quality.missing:
                recent_sg_n += 1
            if pi.sg.driving_distance_yd is not None:
                season_n += 1
            players.append(pi)

        name_to_id = {p.player.name: p.player.player_id for p in players}
        quotes, odds_q = self._fetch_odds(
            name_to_id,
            tournament.name,
            include_odds=include_odds,
            live=mode == RunMode.LIVE,
            event_id=eid,
            odds_book=odds_book,
        )
        dg_feed = DataGolfRecentSgFeed(self.cache)
        _, dg_q = dg_feed.quality_or_missing(refresh=self.refresh)
        recent_sg_q = asof_bundle.recent_q
        if recent_sg_q.missing and not dg_q.missing:
            recent_sg_q = dg_q
        asof_cov = asof_coverage_report(
            asof_bundle, [p.player.name for p in players], sg_feed
        )
        asof_cov["datagolf"] = {
            "available": not dg_q.missing,
            "source_kind": dg_q.source_kind.value,
            "notes": dg_q.notes,
        }
        asof_cov["players_with_recent_sg"] = recent_sg_n

        wx_summary = ""
        if weather:
            wx_summary = str(weather.get("summary") or weather.get("condition") or "")
            if weather.get("wind_mph") is not None:
                wx_summary = wx_summary or f"wind {weather['wind_mph']:.0f} mph"
        win_n = sum(1 for q in quotes if q.bet_type.value == "win" and q.line_role != "opening")
        t10_n = sum(1 for q in quotes if q.bet_type.value == "top_10" and q.line_role != "opening")
        notes = (
            f"operating ingest event={eid} sources=espn,open-meteo,bovada|odds_api|hardrockbet,pga_sg,datagolf "
            f"odds_book={resolve_odds_book(odds_book)} "
            f"odds={win_n}/{len(players)} top10={t10_n} sg_missing={sg_missing}/{len(players)} "
            f"sg_through_event={sg_through_event} "
            f"recent_sg={'yes' if not recent_sg_q.missing else 'unavailable'} "
            f"recent_sg_players={recent_sg_n}/{len(players)}"
        )
        if asof_bundle.long_term is not None and not asof_bundle.long_term_q.missing:
            sg_q_inv = asof_bundle.long_term_q
        else:
            sg_q_inv = sg_cur_q if sg_cur_q and not sg_cur_q.missing else (
                sg_prev_q if sg_prev_q and not sg_prev_q.missing else unavailable_quality(
                    "strokes_gained",
                    "PGA Tour GraphQL SG unavailable; not mocked",
                )
            )
        inv = build_inventory(
            n=len(players),
            course_q=course_q,
            weather_q=weather_q,
            odds_q=odds_q,
            sg_q=sg_q_inv,
            sg_missing=sg_missing,
            sg_prior_season=sg_prior_season,
            sg_unmatched=sg_unmatched,
            season_n=season_n,
            has_cut=tournament.has_cut,
            history_events=len(history.completed()),
            odds_matched=win_n,
            recent_sg_q=recent_sg_q,
            market_coverage=market_coverage_report(quotes, len(players)),
            asof_coverage=asof_cov,
            sg_through_event=sg_through_event,
        )
        field = FieldSnapshot(
            tournament_id=tournament.tournament_id,
            mode=mode,
            players=players,
            weather_summary=wx_summary,
            notes=notes,
            inventory=inv,
            operating=True,
            extra={"asof_coverage": asof_cov, "odds_book": resolve_odds_book(odds_book)},
        )
        _guard_field(field)
        if weather:
            _apply_wind_exposure(tournament, weather)
        return tournament, field, quotes, inv

    def _fetch_odds(
        self,
        name_to_id: dict[str, str],
        tournament_name: str,
        *,
        include_odds: bool,
        live: bool = False,
        event_id: str | None = None,
        odds_book: str = "auto",
    ) -> tuple[list[MarketQuote], DataQuality]:
        if not include_odds:
            return [], unavailable_quality("market_odds", "odds fetch skipped")
        ttl = odds_ttl_seconds(live=live)
        book = resolve_odds_book(odds_book)
        if book == "hardrockbet":
            chain = FallbackChain([HardRockBetOddsFeed(cache=self.cache)])
        elif book == "bovada":
            chain = FallbackChain([BovadaOddsFeed(cache=self.cache, refresh=self.refresh)])
        else:
            chain = FallbackChain(
                [
                    OddsApiFeed(cache=self.cache),
                    BovadaOddsFeed(cache=self.cache, refresh=self.refresh),
                ]
            )
        payload, odds_q, used = chain.fetch(
            name_to_id=name_to_id,
            tournament_name=tournament_name,
            live=live,
            refresh=self.refresh,
            ttl_seconds=ttl,
        )
        quotes = list(payload or [])
        if odds_q.source_kind == SourceKind.MOCK:
            raise MockOnOperatingPathError("odds")
        persist_prematch_openings(event_id, tournament_name, quotes, book_family=book)
        quotes = merge_archived_openings(quotes, event_id, book_family=book)
        quotes, odds_q = apply_odds_freshness(quotes, odds_q, live=live)
        if quotes and not odds_q.missing:
            extra = ""
            if book == "hardrockbet":
                extra = " odds_book=hardrockbet (Bovada not used as a substitute);"
            odds_q = odds_q.model_copy(
                update={
                    "notes": (
                        f"{odds_q.notes}; feed={used};{extra} unmatched players have no invented price; "
                        "de-juice is proportional (implied_fair = implied_raw / Σimplied_raw); "
                        "decision layer requires model_p > 1/decimal (beat the posted number); "
                        "place/top-10 never synthesized from winner odds"
                    )
                }
            )
            return quotes, odds_q
        if book == "hardrockbet":
            q = unavailable_quality(
                "market_odds",
                f"no usable Hard Rock Bet outrights (not filled from Bovada) ({odds_q.notes})",
            )
        else:
            q = unavailable_quality(
                "market_odds",
                f"no usable real outrights: Odds API and Bovada missing or live-stale "
                f"({odds_q.notes})",
            )
        q.lag_hours = odds_q.lag_hours
        q.as_of = odds_q.as_of
        return [], q

    def _player_inputs(
        self,
        comp: dict[str, Any],
        tournament: Tournament,
        history: HistoryIndex,
        wind_kph: float | None,
        *,
        mode: RunMode,
        include_season_stats: bool,
        sg_feed: PgaTourSgFeed | None = None,
        sg_current: SgTable | None = None,
        sg_current_q: DataQuality | None = None,
        sg_prior: SgTable | None = None,
        sg_prior_q: DataQuality | None = None,
        asof_bundle=None,
    ) -> PlayerInputs:
        from golf_offshoot.data_feeds.espn import competitor_to_player

        player = competitor_to_player(comp)
        feats = history.features_for(
            player.player_id,
            before=tournament.start_date,
            course_id=tournament.course.course_id,
            event_wind_kph=wind_kph,
            exclude_event_id=tournament.espn_event_id,
        )
        player.is_lesser_known = feats.is_lesser_known
        player.owgr = None
        sq: dict[str, DataQuality] = {}
        sq["talent_prior"] = quality_for_feature(
            n=feats.n_starts,
            source="espn_leaderboard_history",
            kind=SourceKind.DERIVED_FROM_REAL,
            notes="decaying finish-percentile skill from events that started before this tournament",
            missing=feats.n_starts == 0,
            score_if_present=min(0.88, 0.35 + 0.04 * feats.n_starts),
        )
        if feats.recent_form is not None:
            sq["recent_form"] = quality_for_feature(
                n=feats.n_form,
                source="espn_leaderboard_history",
                kind=SourceKind.DERIVED_FROM_REAL,
                notes="last-5 residual vs own longer-run finish skill; pre-event only; not a last-N SG window",
                missing=False,
                score_if_present=min(0.80, 0.40 + 0.08 * feats.n_form),
            )
        if feats.trend is not None:
            sq["short_term_trend"] = quality_for_feature(
                n=feats.n_trend,
                source="espn_leaderboard_history",
                kind=SourceKind.DERIVED_FROM_REAL,
                notes="last-2 vs prior-3 finish skill; pre-event only",
                missing=False,
                score_if_present=0.52,
            )
        if feats.course_history is not None:
            sq["course_history"] = quality_for_feature(
                n=feats.course_history_rounds,
                source="espn_same_course_history",
                kind=SourceKind.DERIVED_FROM_REAL,
                notes="prior finishes at this ESPN course id",
                missing=False,
                score_if_present=min(0.85, 0.30 + 0.06 * feats.course_history_rounds),
            )
        if feats.weather_fit is not None:
            sq["weather_suitability"] = quality_for_feature(
                n=feats.n_weather,
                source="open_meteo+espn_history",
                kind=SourceKind.DERIVED_FROM_REAL,
                notes="player residual vs historical event wind (Open-Meteo archive)",
                missing=False,
                score_if_present=min(0.62, 0.28 + 0.04 * feats.n_weather),
            )
        st_name = _status_name(comp)
        withdrawn = "WITHDRAW" in st_name
        health = -1.2 if withdrawn else 0.0
        if withdrawn:
            sq["health_setup"] = quality_for_feature(
                n=1,
                source="espn_leaderboard_status",
                kind=SourceKind.REAL_LIVE,
                notes="STATUS_WITHDRAW on ESPN leaderboard",
                missing=False,
                score_if_present=0.90,
            )
        else:
            sq["health_setup"] = unavailable_quality(
                "injury_wire",
                "no public injury feed connected; health left unavailable (not treated as healthy)",
            )
            sq["health_setup"].role = DataRole.PRIMARY

        sg = StrokesGainedProfile(
            quality=unavailable_quality(
                "strokes_gained",
                "no PGA Tour / ShotLink / Data Golf SG row for this player; not mocked",
            )
        )
        course_fit = feats.course_history
        if include_season_stats:
            try:
                overview = self.espn.athlete_overview(player.player_id)
                ranks = parse_season_rankings(overview)
            except FeedError:
                ranks = {}
            if ranks:
                dist = ranks.get("yardsPerDrive")
                acc = ranks.get("driveAccuracyPct")
                putt_gir = ranks.get("puttsGirAvg")
                earn_rank = ranks.get("amount_rank")
                season_q = quality_for_feature(
                    n=1,
                    source="espn_athlete_season_rankings",
                    kind=SourceKind.REAL_LIVE,
                    notes="season-to-date ESPN ranking categories; not used as calibration targets; not SG",
                    missing=False,
                    score_if_present=0.68,
                )
                if dist is not None:
                    sg.driving_distance_yd = dist
                    sq["driving_distance"] = season_q
                if acc is not None:
                    sg.driving_accuracy_pct = acc
                    sq["driving_accuracy"] = season_q
                if putt_gir is not None:
                    # lower putts/GIR is better; center ~1.75
                    sg.putt = (1.75 - putt_gir) / 0.08
                    sq["putting"] = quality_for_feature(
                        n=1,
                        source="espn_putts_per_gir",
                        kind=SourceKind.DERIVED_FROM_REAL,
                        notes="inverted putts-per-GIR vs 1.75; not SG:PUTT",
                        missing=False,
                        score_if_present=0.50,
                    )
                if earn_rank is not None and earn_rank > 125:
                    player.is_lesser_known = True
                if dist is not None and tournament.course.yardage:
                    length = ((dist - 295) / 12.0) * ((tournament.course.yardage - 7200) / 450.0)
                    if course_fit is None:
                        course_fit = float(max(-3, min(3, length)))
                    else:
                        course_fit = float(max(-3, min(3, 0.65 * course_fit + 0.35 * length)))
                    sq["course_fit"] = quality_for_feature(
                        n=max(feats.course_history_rounds, 1),
                        source="espn_course+season_distance",
                        kind=SourceKind.DERIVED_FROM_REAL,
                        notes="blend of same-course finish skill and length-vs-yardage",
                        missing=False,
                        score_if_present=0.50,
                    )

        sg_profile, sg_origin = _sg_profile_for(
            player.name,
            sg_feed,
            sg_current,
            sg_current_q,
            sg_prior,
            sg_prior_q,
            asof_bundle=asof_bundle,
        )
        recent_sg = None
        if asof_bundle is not None and sg_feed is not None:
            rec = sg_feed.profile_for(player.name, asof_bundle.recent, asof_bundle.recent_q) if asof_bundle.recent else None
            rec = scale_recent_sg_quality(rec)
            if rec is not None and rec.quality is not None and not rec.quality.missing:
                recent_sg = rec
                sq["recent_form"] = rec.quality
        if sg_profile is not None:
            dist, acc = sg.driving_distance_yd, sg.driving_accuracy_pct
            sg = sg_profile
            sg.driving_distance_yd = dist
            sg.driving_accuracy_pct = acc
            sq["putting"] = sg.quality.model_copy(
                update={
                    "notes": (
                        f"PGA Tour SG:Putting Avg ({sg_origin}); not putts/GIR. "
                        f"{sg.quality.notes}"
                    ).strip()
                }
            ) if sg.quality else sq.get("putting")

        live_score = None
        live_holes = 0
        live_cut = None
        live_place = None
        live_place_disp = ""
        if mode == RunMode.LIVE:
            live_score = _score_to_par(comp)
            live_holes = _thru_holes(comp, tournament.n_rounds)
            live_place = _finish_place(comp)
            live_place_disp = _place_display(comp)
            if st_name == "STATUS_CUT":
                live_cut = False
            elif st_name in ("STATUS_FINISH", "STATUS_FINAL") and not tournament.has_cut:
                live_cut = True
            sq["live_position"] = quality_for_feature(
                n=max(live_holes, 1),
                source="espn_leaderboard_live",
                kind=SourceKind.REAL_LIVE,
                notes="score-to-par and holes from ESPN competitor status",
                missing=live_score is None,
                score_if_present=0.95,
            )

        for q in sq.values():
            assert_operating_quality(q, context=player.player_id)
        if sg.quality:
            assert_operating_quality(sg.quality, context="sg")
        if recent_sg and recent_sg.quality:
            assert_operating_quality(recent_sg.quality, context="recent_sg")

        return PlayerInputs(
            player=player,
            talent_prior=feats.talent_prior,
            talent_prior_sd=feats.talent_prior_sd,
            sg=sg,
            recent_sg=recent_sg,
            course_history_rounds=feats.course_history_rounds,
            course_history_sg=feats.course_history,
            recent_form_sg=feats.recent_form,
            short_term_trend=feats.trend,
            weather_fit=feats.weather_fit,
            health_flag=health,
            narrative_momentum=0.0,
            rest_days=feats.rest_days,
            live_score_to_par=live_score,
            live_holes_completed=live_holes,
            live_place=live_place,
            live_place_display=live_place_disp,
            live_status_name=st_name,
            live_made_cut=live_cut,
            withdrawn=withdrawn,
            source_qualities=sq,
            course_fit_signal=course_fit,
        )


def _sg_profile_for(
    espn_name: str,
    feed: PgaTourSgFeed | None,
    current: SgTable | None,
    current_q: DataQuality | None,
    prior: SgTable | None,
    prior_q: DataQuality | None,
    asof_bundle=None,
) -> tuple[StrokesGainedProfile | None, str | None]:
    if feed is None:
        return None, None
    if asof_bundle is not None and asof_bundle.long_term is not None and not asof_bundle.long_term_q.missing:
        profile = feed.profile_for(espn_name, asof_bundle.long_term, asof_bundle.long_term_q)
        if profile is not None:
            return profile, "THROUGH_EVENT as-of last completed PGA pill"
    if current is not None and current_q is not None and not current_q.missing:
        profile = feed.profile_for(espn_name, current, current_q)
        if profile is not None:
            return profile, "current season StatDetails fallback"
    if prior is not None and prior_q is not None and not prior_q.missing:
        profile = feed.profile_for(espn_name, prior, prior_q)
        if profile is not None:
            if profile.quality is not None:
                profile.quality = profile.quality.model_copy(
                    update={
                        "score": min(profile.quality.score, 0.70),
                        "notes": profile.quality.notes
                        + "; prior season fallback (current-season row missing)",
                    }
                )
            return profile, "prior season StatDetails"
    return None, None


def _pick_weather(espn_wx, espn_q, om_wx, om_q):
    chain_notes = []
    if espn_wx and not espn_q.missing:
        assert_operating_quality(espn_q, context="espn_weather")
        payload = dict(espn_wx)
        if om_wx and not om_q.missing:
            payload["forecast"] = om_wx
            payload["summary"] = (
                f"ESPN now: {espn_wx.get('condition')}, wind {espn_wx.get('wind_mph')} mph; "
                f"{om_wx.get('summary')}"
            )
        return payload, espn_q
    chain_notes.append(espn_q.notes)
    if om_wx and not om_q.missing:
        assert_operating_quality(om_q, context="open_meteo")
        return om_wx, om_q
    q = unavailable_quality("weather", "ESPN course weather and Open-Meteo both missing")
    q.notes = "; ".join(x for x in chain_notes + [om_q.notes] if x)
    return None, q


def _apply_wind_exposure(tournament: Tournament, weather: dict[str, Any]) -> None:
    mph = weather.get("wind_mph")
    if mph is None and weather.get("wind_kph") is not None:
        mph = float(weather["wind_kph"]) / 1.609
    if mph is None:
        return
    tournament.course.wind_exposure = float(min(1.0, max(0.0, float(mph) / 25.0)))


def _guard_field(field: FieldSnapshot) -> None:
    for p in field.players:
        if p.sg.quality:
            assert_operating_quality(p.sg.quality, context=p.player.player_id)
        if p.recent_sg and p.recent_sg.quality:
            assert_operating_quality(p.recent_sg.quality, context=f"{p.player.player_id}:recent_sg")
        for k, q in p.source_qualities.items():
            assert_operating_quality(q, context=f"{p.player.player_id}:{k}")
        for st in p.factors.values():
            if st.quality:
                assert_operating_quality(st.quality, context=st.factor_id)


def build_inventory(
    *,
    n: int,
    course_q: DataQuality,
    weather_q: DataQuality,
    odds_q: DataQuality,
    sg_q: DataQuality,
    sg_missing: int,
    sg_prior_season: int,
    sg_unmatched: list[str],
    season_n: int,
    has_cut: bool,
    history_events: int,
    odds_matched: int,
    recent_sg_q: DataQuality | None = None,
    market_coverage: dict | None = None,
    asof_coverage: dict | None = None,
    sg_through_event: int = 0,
) -> list[SourceInventoryItem]:
    def row(name, q: DataQuality, coverage: str, impact: str) -> SourceInventoryItem:
        return SourceInventoryItem(
            field_name=name,
            source_kind=q.source_kind,
            source_name=q.source_name,
            quality_score=q.score,
            coverage=coverage,
            notes=q.notes,
            impact_if_missing=impact,
        )

    owgr_q = unavailable_quality("owgr", "ESPN rankings endpoint empty; OWGR not connected")
    health_q = unavailable_quality("injury_wire", "no injury wire; WD status only")
    setup_q = unavailable_quality(
        "course_setup_agronomy",
        "firmness/rough/green speed not published on ESPN; left unconstrained",
    )
    unmatched_note = ""
    if sg_unmatched:
        sample = ", ".join(sg_unmatched[:8])
        extra = f" (+{len(sg_unmatched) - 8} more)" if len(sg_unmatched) > 8 else ""
        unmatched_note = f"; unmatched: {sample}{extra}"
    sg_notes = (
        f"{sg_q.notes}; THROUGH_EVENT attached {sg_through_event}/{n}; "
        f"prior-season fallback {sg_prior_season}/{n}{unmatched_note}"
    ).strip("; ")
    sg_item = sg_q.model_copy(update={"notes": sg_notes})
    sg_have = n - sg_missing
    odds_cov = f"{odds_matched}/{n}" if not odds_q.missing else "0"
    if recent_sg_q is None:
        recent_sg_q = unavailable_quality(
            "pga_tour_sg_event_only",
            "true as-of recent SG windows not connected; not inferred from season tables",
        )
    cov = market_coverage or {}
    by_mkt = cov.get("by_market") or {}
    t10 = by_mkt.get("top_10") or {}
    t5 = by_mkt.get("top_5") or {}
    t20 = by_mkt.get("top_20") or {}
    mc = by_mkt.get("make_cut") or {}
    opening_n = int(cov.get("opening_quotes") or 0)
    unavailable_mkts = ", ".join(cov.get("unavailable_markets") or ["top_5", "top_10", "top_20", "make_cut"])
    asof = asof_coverage or {}
    recent_cov = asof.get("recent_coverage") or ("0" if recent_sg_q.missing else f"{recent_sg_q.n_observations}/{n}")
    recent_events = ", ".join(asof.get("recent_events_used") or []) or "none"
    cats = asof.get("by_category") or {}
    cat_note = "; ".join(
        f"{k} long={v.get('long_term', 0)} recent={v.get('recent', 0)}"
        for k, v in cats.items()
    )
    return [
        row("player_identification_field", course_q.model_copy(update={"source_name": "espn_field", "score": 0.92, "source_kind": SourceKind.REAL_LIVE, "notes": "ESPN leaderboard competitors"}), f"{n}/{n}", "cannot rank without a field"),
        row("long_term_talent", DataQuality(score=0.80, source_name="espn_leaderboard_history", as_of=datetime.now(timezone.utc), n_observations=history_events, source_kind=SourceKind.DERIVED_FROM_REAL, notes=f"finish-skill from {history_events} completed ESPN events"), "all players with prior starts", "new players stay near 0 with wide SD"),
        row("owgr", owgr_q, "0", "no official world rank; talent is finish-derived only"),
        row(
            "strokes_gained_categories",
            sg_item,
            f"{sg_have}/{n} (missing {sg_missing})",
            "SG match/approach/ARG/putting unconstrained for unmatched players",
        ),
        row(
            "strokes_gained_recent_window",
            recent_sg_q.model_copy(
                update={
                    "notes": (
                        f"{recent_sg_q.notes}; events={recent_events}; "
                        f"median_events_per_player={asof.get('recent_median_events_per_player', 0)}; "
                        f"p10={asof.get('recent_p10_events_per_player', 0)} "
                        f"p90={asof.get('recent_p90_events_per_player', 0)}; "
                        f"window_requested={asof.get('recent_window_requested', 0)}; "
                        f"{cat_note or 'no per-category counts'}"
                    ).strip("; ")
                }
            ),
            recent_cov if not recent_sg_q.missing else "0",
            "recent SG stays unconstrained; finish-residual form is not a last-N SG window",
        ),
        row("season_driving_putts", DataQuality(score=0.68 if season_n else 0.0, source_name="espn_athlete_season_rankings", as_of=datetime.now(timezone.utc), n_observations=season_n, missing=season_n == 0, source_kind=SourceKind.REAL_LIVE if season_n else SourceKind.UNAVAILABLE, notes="yards/drive, accuracy %; putts/GIR only if SG:PUTT missing"), f"{season_n}/{n}", "length/accuracy/putting proxies weaker"),
        row("recent_form_trend", DataQuality(score=0.70, source_name="espn_leaderboard_history", as_of=datetime.now(timezone.utc), source_kind=SourceKind.DERIVED_FROM_REAL, notes="pre-event residuals from prior events only"), "players with ≥1 prior start", "form unconstrained"),
        row("course_history", DataQuality(score=0.55, source_name="espn_same_course_history", as_of=datetime.now(timezone.utc), source_kind=SourceKind.DERIVED_FROM_REAL, notes="same ESPN course id across loaded seasons"), "thin if course not in 2025–26 sample", "course history unconstrained; reliability down"),
        row("course_identity", course_q, "1", "yards/par real; agronomy unavailable"),
        row("course_setup_agronomy", setup_q, "0", "tightness/rough/stimp not evidence"),
        row("weather", weather_q, "event", "weather suitability unconstrained"),
        row(
            "market_odds",
            odds_q,
            odds_cov,
            "no edges; strategy cannot size into a book; unmatched names are unavailable not invented",
        ),
        row(
            "market_odds_place_top10",
            DataQuality(
                score=0.78 if t10.get("available") else 0.0,
                source_name=odds_q.source_name,
                as_of=odds_q.as_of,
                n_observations=int(t10.get("n") or 0),
                missing=not bool(t10.get("available")),
                source_kind=SourceKind.REAL_LIVE if t10.get("available") else SourceKind.UNAVAILABLE,
                notes=(
                    f"top10={t10.get('coverage', '0')} top5={t5.get('coverage', '0')} "
                    f"top20={t20.get('coverage', '0')} make_cut={mc.get('coverage', '0')}; "
                    f"unavailable={unavailable_mkts}; never synthesized from winner odds"
                ),
            ),
            t10.get("coverage") or "0",
            "place/top-10 edges stay unavailable unless a real coupon exists",
        ),
        row(
            "market_odds_opening",
            DataQuality(
                score=0.72 if opening_n else 0.0,
                source_name=odds_q.source_name,
                as_of=odds_q.as_of,
                n_observations=opening_n,
                missing=opening_n == 0,
                source_kind=SourceKind.REAL_LIVE if opening_n else SourceKind.UNAVAILABLE,
                notes=(
                    f"distinct prematch coupons tagged line_role=opening n={opening_n}; "
                    "current in-play Winner Live is not treated as an opening line; "
                    "archived prematch is used only if captured before the market flipped live"
                ),
            ),
            str(opening_n) if opening_n else "0",
            "no open-to-current movement; live prices are not claimed as opens",
        ),
        row("health_injury", health_q, "WD only", "injury rumours cannot move θ"),
        row("cut_rule", DataQuality(score=0.9, source_name="espn_tournament_cutRound", as_of=datetime.now(timezone.utc), source_kind=SourceKind.REAL_LIVE, notes="has_cut from ESPN cutRound"), "event", f"has_cut={has_cut}"),
    ]
