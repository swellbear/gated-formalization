# Named-gap ledger — cell-tower geometry

Habit: [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). One line per open gap. This is a problem-solving scoreboard, **not** a trained map and **not** a GPS-replacement claim.

**Opened:** 2026-09-05 — Founder opens a **new** Amb: location from public mast maps + radio observations via geometry / path-loss, without fingerprint training. Lab proposes three cheap first-pulse peeks. Method Operator gates.

**Last check:** 2026-09-05 — Founder **STOP** / user pivot. Amb **PARKED**. Cheap checks A→B **halted mid-flight**. Peek #61 + provisional **X = 300 m** remain **on record**; Amb is **not live**. Park digestion: [`DIGESTION_PARK.md`](DIGESTION_PARK.md). Peek record: [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md).

**What this is not:** This is **not** rithm. GPS replacement is **not** claimed. Peek succeed is **not** claim clearance. Training is **not** started and is **not** established. Estimator invent is **halted** (A→B mid-flight) and is **not** this fold. Skill-met is **not** claimed. This Amb is **not live** and is **not** reopened as live. The BIA→weight portfolio is **CLOSED** and is **not** reopened here.

**Process:** Lab invented 2–3 ranked peek probes. Operator admits, rejects, or parks. Lab does **not** self-admit. After this park Lab does **not** invent estimators here. Do **not** reopen this Amb as live.

**Greer-style sync-pulse TDOA** is a **separate OPEN** scaffold (`2026-09_greer-sync-pulse-tdoa`). This park is **not** that Amb and does **not** invent its models.  
**BIA→weight portfolio** is **CLOSED** (human #59 ship demo + kill of the accurate-weight claim; animal parks stay). This app does **not** reopen it.  
**Collatz playground** is **done** (#45). Lab HOLD there (unchanged).  
**Track B invent** remains **paused** (unchanged).  
**llm-gwt R-REPL** remains **parked** (unchanged).

## Claim line (parent; X on record; Amb PARKED)

`geometry / path-loss from public mast coordinates + cell IDs (optional RSSI / TA) hits median error ≤ 300 m on held-out drives, without GPS-fingerprint training` → kill vs succeed: fail closed if the live pack is RSSI-only **or** fog-as-honesty (OpenCelliD / MLS as the mast map); succeed later would need a held-out median ≤ **300 m** with GPS used only as eval labels and non-fog masts → last check: 2026-09-05 Founder **STOP** / user pivot — Amb **PARKED** (not live); peek #61 + provisional **X = 300 m** remain on record; peek succeed ≠ claim clearance → status: **paused** / **PARKED** (on-record **X** only; **not** a live string)

## Honest-fog lines

`mast-map lineage honesty (regulatory vs OpenCelliD / MLS)` → kill vs succeed: only GPS-crowdsourced mast maps are usable → “no GPS in the map lineage” stays untestable; a regulatory list is usable **and** can be matched to the radio site heard → honesty hardens → last check: 2026-09-05 Peek2 **MIXED** — prefer FCC ASR (`r_tower.zip` structure lat/lon) and Austrian Senderkataster; OpenCelliD / MLS = GPS-crowdsourced fog (**ablation only**); ASR has **no CID** → status: **restated** / **MIXED**

`CID ↔ ASRN join (regulatory mast ↔ cell ID)` → kill vs succeed: a non-crowdsourced join that maps heard CID to an ASR / Senderkataster record vs only a GPS-crowdsourced join → last check: 2026-09-05 **PARKED** (no crowdsourced GPS join) → status: **paused** / **PARKED**

`US ASR geography` → kill vs succeed: join honesty cleared so US ASR can sit on the same bar as EU packs vs stay Soften → last check: 2026-09-05 Operator **Soften** US ASR until CID↔ASRN join honesty-cleared; **EU packs first** → status: **paused** / **Soften**

`ceiling is coarse location, not GPS replacement` → kill vs succeed: this is standing honesty, not a hunt — rural sparse towers imply huge uncertainty; ~2–5 m GPS replacement is **out of scope** → last check: named at scaffold; restated at peek → status: **open** (constraint; do not silently upgrade)

`Timing Advance or equivalent ranging in public traces` → kill vs succeed: TA (or equivalent) missing **and** RSSI+ID alone cannot clear a stated weaker bar → **fail closed**; TA present → ranging limb stays live → last check: 2026-09-05 Peek3 **PASS** — TA present in Edinburgh / Vienna / DoNext; **not** fail-closed on TA absence → status: **hardened** (ranging limb live)

## First-pulse data line

`public drive / walk traces with phone-visible cell IDs (+ optional RSSI / TA) and GPS only as held-out eval labels` → kill vs succeed: no usable public traces / schema / license → **DATA-BLOCKED park**; a citable public source + schema + license with those columns (docs/schema peek; no bulk dump in-repo) → peek succeed (**not** claim clearance) → last check: 2026-09-05 Peek1 **PASS** — primary Vienna (Zenodo CC-BY 4.0, `timing_advance`; concept [DOI 10.5281/zenodo.18322065](https://doi.org/10.5281/zenodo.18322065)) + DoNext Dortmund (CC-BY 4.0, `ta`; [DOI 10.17877/tudodata-2026-t6mypo](https://doi.org/10.17877/tudodata-2026-t6mypo)); Soften secondary Edinburgh Melrose MNRUL (~102k, `ta`, research/non-commercial); Soften/RSSI-only Malaysia GNetTrack (no TA documented) → status: **killed** / **PASS** (peek succeed; **not** claim clearance)

## Next pulse (halted; not live)

`ranked pure geometry / path-loss estimators on the admitted EU packs` → kill vs succeed: Lab invents 2–3 ranked estimators; Operator admits, rejects, or parks. Cheap checks A→B **halted mid-flight**. This fold does **not** invent. → last check: 2026-09-05 Founder **STOP** / user pivot — A→B halted; no estimator results on this record → status: **paused** / **PARKED** (halted mid-flight)
