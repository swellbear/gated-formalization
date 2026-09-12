# Tesla method-viz prototypes — 2026-09-07 (EXAMPLE DATA ONLY)

> **EXAMPLE DATA — NOT LIVE CAR DATA.** Every number, state, date, and quoted-looking
> line in these two charts was written by hand for layout review. Nothing here was
> scraped from Teslascope, read off a window sticker, or taken from any real vehicle.
> If you want to see what these charts would say about a real car, the answer is:
> nothing yet. These are picture prototypes, not findings.

Two large prototype charts for showing gated-formalization-style questions about a
car's own logs. They exist to test whether the *layout* reads cold on a phone. They
do not establish anything about any vehicle, any log service, or any manufacturer.

## What is in this folder

| File | What it is |
| --- | --- |
| `ghost_strip.png` | Chart 1, 2560 x 1440 |
| `overnight_court.png` | Chart 2, 2560 x 1440 |
| `render_ghost_strip.py` | Regenerates chart 1 |
| `render_overnight_court.py` | Regenerates chart 2 |
| `viz_style.py` | Shared dark-card palette, type scale, and card/caption helpers |

## Regenerating

```bash
python3 -m pip install matplotlib
cd docs/viz/tesla_prototypes_2026-09-07
python3 render_ghost_strip.py
python3 render_overnight_court.py
```

No network access, no input files, no randomness: the example numbers are literals at
the top of each script, so the same PNGs come out every time. Both scripts write
2560 x 1440 px on the `#0b0f14` background and use exactly three data colors.

## Chart 1 — Ghost Strip

`ghost_strip.png` puts 28 invented after-charge readings ("displayed rated miles" at a
charge to full) against an invented published range window, and sorts each reading
into one of three buckets:

- **IN-WINDOW** — inside the example sticker / EPA window (`370–400 mi` here).
- **MARKETING-ONLY** — above that window but inside an example "up to" headline number
  (`400–415 mi` here), so the only published number it matches is the marketing one.
- **NOWHERE** — under every example published number (`under 370 mi` here).

The vehicle is labelled as a **stand-in profile** (2020 Model S Long Range Plus). The
window bounds are *not* that car's real EPA or window-sticker figures; they are round
placeholders picked to make the three bands legible. Swap the literals in
`render_ghost_strip.py` and the bucket counts recompute themselves.

**Honesty caption, as printed on the chart:**

- *What this chart does:* it counts where example after-charge numbers land — inside the
  published window, only inside a marketing "up to" number, or under every published
  number. Sorting is the whole job.
- *What it does not do:* it is not a verdict and not a method call of any kind. It does
  not say a car is bad or that anyone lied. It is not buy, sell, sue, or repair advice.
  A dot in one bucket is a reading, not a fault.

## Chart 2 — Overnight Court

`overnight_court.png` shows one invented night (10 pm to 7 am): displayed rated miles
stepping down from 268 to 249, with the state the example log claims the car was in
layered underneath in the same three colors:

- **asleep** — the ordinary parked case.
- **awake + feature** — awake with a feature named in the log (security camera mode,
  climate, app wake-ups).
- **awake, no feature** — awake with nothing named.

Alongside it sits a **paraphrase panel**: short plain-English stand-ins for the sort of
standby / parked-loss guidance a maker publishes ("losing some range while parked is
normal and expected"; "leaving things like security camera mode or climate on uses
more"). These are **hand-written EXAMPLE paraphrases, not quotations**, and the chart
labels them that way on its face. No real published text is reproduced here.

The chart then names one gap where the example log and the example wording do not line
up, using the one-line form from [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../NAMED_GAP_LEDGER_HABIT.md):

> **Named mismatch hole (EXAMPLE): `G-EX-AWAKE-DRAIN-01`** — in this example night, 11
> of the 19 lost miles land while the log says the car was awake with no feature named.
> The paraphrased wording covers sleep loss and feature-on loss — not this stretch.
> *What would close it:* a log field naming a feature that was on. *What would harden
> it:* the same shape on repeat example nights.

**Honesty caption, as printed on the chart:** a hole is a place where the log and the
wording do not line up. That is all it is. It is not a verdict, not a method call, and
it does not say the car is bad or that anyone lied. It is not buy, sell, sue, or repair
advice.

## What these charts are not

- **Not a method artifact.** No Soften, no admit, no verdict, no usefulness score, no
  gate scoring. Nothing in this folder scores or clears anything, and nothing here is
  an application run. It is docs-only prototype art.
- **Not a claim about a car.** "NOWHERE" and "the hole" are names for *where a number
  sits* and *where two texts disagree*. Neither is a statement that a vehicle is
  defective, degraded beyond spec, or misdescribed.
- **Not advice.** Nothing here recommends buying, selling, keeping, suing, servicing,
  or repairing anything.
- **Not sourced from Teslascope.** No scraping, no API calls, no logs. The name appears
  only to describe the *kind* of after-charge / overnight log these layouts are shaped
  for.
- **Not real published wording.** The paraphrase panel is invented plain English.

## If someone later wants to run these on real data

Then the honesty captions have to change with the data, and the "EXAMPLE" stamps have
to come off only when every literal in the scripts has been replaced by a sourced
number with a stated provenance — including the window bounds, the "up to" figure, and
the exact published standby text (quoted and cited, not paraphrased). Until then these
files stay marked as examples.
