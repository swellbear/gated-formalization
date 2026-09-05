# Digestion — Track B invent→test / solve-loop string (2026-09-05)

A plain-English write-up of a stalled string. This does **not** score a new claim. It does **not** authorize new invent. Lab stays held.

**What this is:** A digestion of **Track B** — the oil **spot** 21-day-ahead vs “just keep going” (continuation) hunt. That is a **separate** object from the futures leftover (**R-F-SKILL**, the still-open “does a named futures recipe beat last settlement?” job). Parent leftover-ambiguity stays **1.0**. Habit: [`docs/DIGESTION_HABIT.md`](../../docs/DIGESTION_HABIT.md). The solve-loop habit stays live as a habit, not as a current Lab ticket: [`docs/SOLVE_LOOP_HABIT.md`](../../docs/SOLVE_LOOP_HABIT.md).

---

## What this string was trying to do

See whether a cheap, named rule could beat a simple continuation baseline on EIA spot WTI and Brent over a 21-day horizon. First we invented direction and overlay “horses” (named candidates) and tested them cheaply. After that hunt was parked, we named one missing piece at a time and ran a cheap check that could move the fog.

It was **not** trying to prove the futures leftover, pick a trade, or clear the parent slogan (“a predictive oil-futures model works”).

---

## What it taught

- **Finding a direction is not confirming it.** Across Lab batches 1–4, many direction and overlay classes burned. Among the new skill horses, none confirmed. A strong discovery hit, or a near-miss on one window, is not a keep. Do not pick the least-bad miss.
- **One scoped survivor is not a class win.** Brent month-of-year continuation (**H-SPOT-MOY-CONT** — a Brent rule that follows that calendar month’s usual pattern versus continuation) passed a scoped confirm, then was marked **FRAGILE** after a 2023 leave-one-year-out fail (batch 4). That is **not** skill-met, **not** class-met (the seasonality class **C-SPOT-SEAS** is **not** established), **not** WTI-met, and **not** a reason to burn the horse as a null.
- **Stop minting more lookalike direction horses.** Founder/user pick **P3=B** ([PR #32](https://github.com/swellbear/gated-formalization/pull/32)): park the all-day directional hunt. The leftover that is still live is **vehicle + cutoff fragility** on that Brent horse — not a new direction class.
- **Cutoff fog moved a little, then overlapped.** Probe **P1** ([PR #33](https://github.com/swellbear/gated-formalization/pull/33)): on FRED Brent, among the 2018 / 2020 / 2023 cutoffs the confirm is not a single-cutoff artifact; 2015 dies at discovery. Confirm windows overlap, so those three survives are partly redundant. WTI was 0/4.
- **Vehicle fog moved a little.** Probe **P2** ([PR #33](https://github.com/swellbear/gated-formalization/pull/33)): EIA copies the 2023 year-out fail (not a FRED-only packaging quirk). EIA also breaks the full confirm at the last-750 window, so the FRED confirm is vehicle-sensitive there.
- **The 2023 year-break looks toward real, not a thin stub.** Probe **P4** ([PR #35](https://github.com/swellbear/gated-formalization/pull/35)): both halves of late-2023 fail; October is the blow-up; November/December are ties; not thin-stub-only and not single-month-only. That **HARDEN**s the year-stability fog (tightens it toward “2023 really broke”). It is still **not** skill-met.
- **New checks that only restate “still fragile” should stop.** Lab’s one allowed year-fragility probe is **done**. Invent is paused for digest ([PR #36](https://github.com/swellbear/gated-formalization/pull/36)). The solve-loop habit is the right tool if a *new named gap* is later locked — it is **not** a license to invent now.

---

## What is still foggy / parked unfinished

Park these clearly so they do not vanish:

- **Brent month-of-year continuation stays scoped and FRAGILE.** It is on the record. It is **not** skill-met. It is **not** burned as a null. Do not promote it. Do not erase it to keep a queue “empty.”
- **Vehicle + cutoff fragility is the live leftover** on that horse. P1/P2 tightened those constraints; they did not clear them. FRED confirm among {2018, 2020, 2023} is not a single-cutoff artifact, but windows overlap. EIA last-750 flips. The 2023 year-out fail is not FRED-only.
- **Year-stability is HARDENED toward “2023 really broke,”** not cleared. We still do not have a skill pass. It is still **not** skill-met.
- **The all-day directional hunt stays parked** (P3=B). Do not mint new beat-continuation / direction horses.
- **Track B invent is paused.** Lab’s one-probe allotment is done. Reopen invent only if Founder/user locks a **new named-gap** string. This write-up does not lock one.
- **The futures leftover (R-F-SKILL) is unchanged** and still separate. Track B is not that leftover. Parent leftover-ambiguity stays **1.0**.

---

## What we refuse to claim

- Track B spot-trend skill is **not** skill-met.
- Seasonality as a class (**C-SPOT-SEAS**) is **not** established.
- WTI is **not** met.
- Brent month-of-year continuation is **not** elevated and is **not** a null-burn.
- A scoped confirm is **not** slogan clearance. **FRAGILE** is **not** elevated. An Ambiguity **HARDEN** is **not** skill-met.
- Discovery is **not** confirm. Volume of burned classes is **not** a refute of every possible recipe, and it is **not** a reason to keep the least-bad miss.
- This digestion does **not** authorize new invent. It does **not** change parent leftover-ambiguity. It is **not** a trade.

---

## Where invent sits now

**Paused.** Lab remains held. No new invent authorization lives in this note.

Reopen only if Founder/user locks a **new named-gap** solve string. Until then, do not mint new beat-continuation horses, do not revive burned classes, and do not treat this write-up as a green light.

The solve-loop habit ([`docs/SOLVE_LOOP_HABIT.md`](../../docs/SOLVE_LOOP_HABIT.md)) stays on the shelf for a later named gap. It is live as a habit, not as a current Lab ticket.

---

## Pointers to the key pulses

| Pulse | What it did |
|-------|-------------|
| [#32](https://github.com/swellbear/gated-formalization/pull/32) | **P3=B** — park the all-day directional hunt |
| [#33](https://github.com/swellbear/gated-formalization/pull/33) | **P1 / P2** — cutoff-sweep and vehicle Ambiguity constraints (**not** skill-met) |
| [#35](https://github.com/swellbear/gated-formalization/pull/35) | **P4** — 2023 year-break decomp **HARDEN** (**not** skill-met) |
| [#36](https://github.com/swellbear/gated-formalization/pull/36) | Pause invent after P4; digest |

Batch records (docs only; scripts not on master): [`PULSE_Lab_TrackB_Batch1.md`](PULSE_Lab_TrackB_Batch1.md) · [`PULSE_Lab_TrackB_Batch2.md`](PULSE_Lab_TrackB_Batch2.md) · [`PULSE_Lab_TrackB_Batch3.md`](PULSE_Lab_TrackB_Batch3.md) · [`PULSE_Lab_TrackB_Batch4.md`](PULSE_Lab_TrackB_Batch4.md) · [`PULSE_Lab_TrackB_Deep1_P1P2.md`](PULSE_Lab_TrackB_Deep1_P1P2.md) · [`PULSE_Lab_TrackB_P4_LOY2023.md`](PULSE_Lab_TrackB_P4_LOY2023.md)
