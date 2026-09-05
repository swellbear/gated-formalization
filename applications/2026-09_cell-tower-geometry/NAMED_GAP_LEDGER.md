# Named-gap ledger — cell-tower geometry

Habit: [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). One line per open gap. This is a problem-solving scoreboard, **not** a trained map and **not** a GPS-replacement claim.

**Opened:** 2026-09-05 — Founder opens a **new** Amb: location from public mast maps + radio observations via geometry / path-loss, without fingerprint training. Lab proposes three cheap first-pulse peeks. Method Operator gates. Last check: **none**.

**What this is not:** This is **not** rithm. GPS replacement is **not** claimed. Opening the scaffold does **not** show a geometry locator and is **not** clearance. Training is **not** started and is **not** established. Proposed peeks are **not** admitted yet. The BIA→weight portfolio is **CLOSED** and is **not** reopened here.

**Process:** Lab invents 2–3 ranked peek probes for the named gaps (why / cost / kill-vs-succeed). Operator admits, rejects, or parks. Lab does **not** self-admit.

**BIA→weight portfolio** is **CLOSED** (human #59 ship demo + kill of the accurate-weight claim; animal parks stay). This app does **not** reopen it.  
**Collatz playground** is **done** (#45). Lab HOLD there (unchanged).  
**Track B invent** remains **paused** (unchanged).  
**llm-gwt R-REPL** remains **parked** (unchanged).

## Claim line (parent; X unset)

`geometry / path-loss from public mast coordinates + cell IDs (optional RSSI / TA) hits median error ≤ X m on held-out drives, without GPS-fingerprint training` → kill vs succeed: fail closed if TA (or equivalent ranging) is missing **and** RSSI+ID alone cannot clear a stated weaker bar; succeed later would need a frozen **X** plus a held-out median ≤ X with GPS used only as eval labels → last check: none → status: **open** / **awaiting admit** · **X** TBD (non-heroic urban bar likely 100–500 m median)

## Honest-fog lines

`mast-map lineage honesty (FCC ASR vs OpenCelliD / MLS)` → kill vs succeed: only GPS-crowdsourced mast maps are usable → “no GPS in the map lineage” stays untestable; a regulatory list (e.g. FCC ASR) is usable **and** can be matched to the radio site heard → honesty hardens (map may still be sparse / messy) → last check: none → status: **open**

`ceiling is coarse location, not GPS replacement` → kill vs succeed: this is standing honesty, not a hunt — rural sparse towers imply huge uncertainty; ~2–5 m GPS replacement is **out of scope** → last check: named at scaffold → status: **open** (constraint; do not silently upgrade)

`Timing Advance or equivalent ranging in public traces` → kill vs succeed: TA (or equivalent) missing **and** RSSI+ID alone cannot clear a stated weaker bar → **fail closed**; TA present (or a weaker RSSI+ID bar is stated and later tested) → ranging limb stays live → last check: none → status: **open**

## First-pulse data line

`public drive / walk traces with phone-visible cell IDs (+ optional RSSI / TA) and GPS only as held-out eval labels` → kill vs succeed: no usable public traces / schema / license → **DATA-BLOCKED park**; a citable public source + schema + license with those columns (docs/schema peek; no bulk dump in-repo) → peek succeed (**not** claim clearance) → last check: none → status: **open**
