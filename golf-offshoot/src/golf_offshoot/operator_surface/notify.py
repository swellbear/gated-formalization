"""One optional ntfy ping when an operator-triggered run finishes. Off if no topic."""

from __future__ import annotations

import os
from dataclasses import dataclass

from golf_offshoot.strategy.watch import WatchConfigError, ntfy_topic, publish_ntfy


@dataclass(frozen=True)
class CompletionNotice:
    sent: bool
    reason: str
    url: str | None = None


def notify_run_complete(
    *,
    command: str,
    ok: bool,
    event_id: str = "",
    detail: str = "",
    topic: str | None = None,
    dry_run: bool = False,
    environ: dict[str, str] | None = None,
    lane: str = "",
) -> CompletionNotice:
    """Ping once on completion. Does not run on progress lines. Safe when topic absent."""
    env = environ if environ is not None else os.environ
    raw = (topic if topic is not None else env.get("NTFY_TOPIC") or "").strip()
    if not raw:
        return CompletionNotice(sent=False, reason="NTFY_TOPIC absent; notify off")
    try:
        name = ntfy_topic(raw)
    except WatchConfigError as exc:
        return CompletionNotice(sent=False, reason=str(exc))
    status = "ok" if ok else "failed"
    from golf_offshoot.learning_lane_15m.paths import LANE_15M
    from golf_offshoot.operator_surface.lanes import parse_lane

    lane_id = parse_lane(lane) if lane else ""
    if lane_id == LANE_15M:
        title = f"golf-offshoot learning_lane_15m {command} {status}"
        if event_id:
            title = f"{title} {event_id}"
        posture = (
            "LEARNING LANE. KXBTC15M. PAPER OBSERVATION ONLY.",
            "PHASE 1 OBSERVATION. Trading NOT ARMED.",
            "AI NEVER DEPOSITS / WITHDRAWS / TRANSFERS CASH",
        )
    else:
        title = f"golf-offshoot {command} {status}"
        if event_id:
            title = f"{title} {event_id}"
        posture = (
            "PHASE 1 OBSERVATION. Trading NOT ARMED.",
            "AI NEVER DEPOSITS / WITHDRAWS / TRANSFERS CASH",
        )
    body = "\n".join(
        [
            title,
            *posture,
            detail.strip(),
        ]
    ).strip()
    try:
        url = publish_ntfy(body, topic=name, title=title[:120], dry_run=dry_run)
    except WatchConfigError as exc:
        return CompletionNotice(sent=False, reason=str(exc))
    return CompletionNotice(sent=not dry_run, reason="dry_run" if dry_run else "sent", url=url)
