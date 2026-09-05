# Failure-Mode Log

Record cases in which the method:

- blocked something that later proved well-supported, or
- allowed something that later collapsed,
- or hit a clear **method pressure point** worth recording.

## Cadence

After every **closed application**, or after every **N ≥ 5** REJECT/HOLD decisions that share a recurring pattern (whichever comes first), add or update an entry when there is anything to learn. Lightweight; skip empty ceremony. See `.cursor/rules/applications-gated-method.mdc`.

## Entry Format

```
### YYYY-MM-DD | Domain | Short claim/layer name
- **Gate outcome at the time:** 
- **Later evidence:** 
- **Direction of error:** blocked-but-later-supported / allowed-but-later-collapsed / method-pressure-point
- **Which rule or judgment contributed:** 
- **Adjustment made (if any):** 
- **Notes:** 
```

## Entries

### 2026-09-05 | Markets / oil Track B (spot) | 2023 LOY decomp HARDEN — Oct blow-up vs late ties; not thin-stub-only — P4
- **Gate outcome at the time:** Brent **H-SPOT-MOY-CONT** already on record as a **scoped confirm pass** marked **FRAGILE** (batch 3 + batch 4). Year-stability Amb already constrained toward fragile (2023 LOY fail 0.374 vs 0.582, n=91 on FRED; EIA replicate). Deep1 P1/P2 already recorded as Amb constraints (cutoff/vehicle). Spot-trend skill **not established**. Separate from R-F-SKILL / F-CC futures. P3=B held (see #32). One allowed year-fragility probe after P1/P2.
- **Later evidence:** **P4** C-SPOT-LOY2023-DECOMP, **ADMIT HARDEN as Amb constraint only**. FRED Brent primary; eligible **2023-08-22..2023-12-31**; n=91. Aggregate **0.374 vs 0.582 FAIL**. Half A n=45 **0.222 vs 0.533 FAIL**. Half B n=46 **0.522 vs 0.630 FAIL**. Months: Sep BEATS 0.333>0.143; Oct FAIL 0.136 vs 0.864; Nov TIE 0.955=0.955 (FAIL strict); Dec TIE 0.158=0.158 (FAIL strict) → 3/4 months not-strict-beat. Binomial p_gt≈1.0 (cannot claim beat); p_lt≈4.8e-5 (horse below cont). EIA same HARDEN pattern (agg 0.352 vs 0.582; both halves fail; 3/4 months). Gatekeeper: Amb HARDEN recorded. Still **not** skill-met. Does **not** elevate. Does **not** null-burn. **NOT RESTATE**.
- **Direction of error:** **method-pressure-point** — a recorded 2023 LOY fail is easy to dismiss as a thin stub or a single-month wreck. Decomp shows agg + both halves FAIL and 3/4 months not-strict-beat ⇒ HARDEN toward “2023 really broke year-stability,” not thin-stub-only / not single-month-only. Honesty: **Oct is the blow-up**; Nov/Dec are **ties** (MOY-CONT ≡ continuation); Sep beats. Month-level Sep beat does not rescue year-stability. None of this is skill-met, elevate, or a null burn.
- **Which rule or judgment contributed:** Amb constraint ≠ skill-met; Amb HARDEN ≠ skill-met; FRAGILE ≠ elevated; Track B ≠ F-SKILL; do not treat a scoped survivor as a null; do not revive burned direction classes; one-probe allotment then hold.
- **Adjustment made (if any):** None to parent Amb math (held 1.0). Year-stability leftover HARDENED as Amb constraint only. Lab one-probe allotment **DONE**. Tracker fold only; Lab hunt scripts not merged.
- **Notes:** Live scoped horse stays Brent **H-SPOT-MOY-CONT** (**FRAGILE**). Open residual: fragility/vehicle Amb (year-stability slice HARDENED). P3=B held. Invent held unless Founder locks a new named missing constraint. **NOT RESTATE**.

### 2026-09-05 | Markets / oil Track B (spot) | Multi-cutoff confirm redundancy; EIA vehicle-sensitive last-750; LOY fail not FRED-only — Deep1 P1/P2
- **Gate outcome at the time:** Brent **H-SPOT-MOY-CONT** already on record as a **scoped confirm pass** marked **FRAGILE** (batch 3 + batch 4). Spot-trend skill **not established**. Year-stability Amb already constrained toward fragile (2023 LOY fail on FRED). Separate from R-F-SKILL / F-CC futures. P3=B held (see #32).
- **Later evidence:** Deep1 probes **P1** C-SPOT-CUTOFF-SWEEP and **P2** C-SPOT-VEHICLE, **ADMIT as Amb constraint only**. P1 (pre-registered {2015,2018,2020,2023}-08-21; FRED Brent primary; WTI info-only): 2015 disc **KILL** (0.494≤0.540); 2018/2020/2023 disc+confirm **SURVIVE** (FULL last-500/250/750). Brent confirm-survive 3/4; WTI 0/4. Confirm windows are FULL-file last-N and overlap across cutoffs. Batch-4 LOY fragility **untouched** by the sweep alone. P2 (EIA v2 `petroleum/pri/spt` DEMO_KEY OK): EIA Brent confirm last-500 Y / last-250 Y / last-750 **N** (0.514667 vs 0.517333) ⇒ all-windows FAIL. EIA LOY 2023 **FAIL** 0.352 vs 0.582; 2024–26 beat (replicates FRED). Gatekeeper: Amb constraints recorded. Still **not** skill-met. Does **not** elevate. Does **not** null-burn.
- **Direction of error:** **method-pressure-point** — (1) Surviving three of four cutoffs is easy to misread as independent-era robustness. Confirm windows are FULL-file last-N and overlap ⇒ multi-cutoff confirm is **partly redundant**, not independent eras. (2) A FRED-scoped confirm is easy to treat as vehicle-invariant. EIA last-750 flips ⇒ vehicle-sensitive at last-750. (3) A 2023 LOY fail on FRED is easy to dismiss as packaging. EIA replicates that fail ⇒ **not** FRED-only. None of these is skill-met, elevate, or a null burn.
- **Which rule or judgment contributed:** Amb constraint ≠ skill-met; FRAGILE ≠ elevated; Track B ≠ F-SKILL; WTI-met ≠ Brent-met; do not treat a scoped survivor as a null; do not revive burned direction classes.
- **Adjustment made (if any):** None to parent Amb math (held 1.0). Cutoff/vehicle leftover tightened as Amb constraints only. Tracker fold only; Lab hunt scripts not merged.
- **Notes:** Live scoped horse stays Brent **H-SPOT-MOY-CONT** (**FRAGILE**). Open residual: fragility/vehicle Amb. P3=B held (see #32). Lab held from new direction classes unless Founder locks a new named missing constraint.

### 2026-09-05 | Markets / oil Track B (spot) | Dead-definition QUANT; FRAGILE scoped survivor ≠ elevate — Lab batch 4
- **Gate outcome at the time:** Track B named invent queue already **empty** after #15–#19 and Lab batch 1–3. Spot-trend skill **not established**. Brent **H-SPOT-MOY-CONT** already on record as a **scoped confirm pass** (not skill-met). Separate from R-F-SKILL / F-CC futures.
- **Later evidence:** Lab invent→test batch 4 (protocol `Lock_Hunt_Spot_Trend`; FRED EIA `DCOILWTICO` / `DCOILBRENTEU`; disc n=500 ≤2023-08-21; cont WTI=0.5080 Brent=0.5060). **C-SPOT-SHRINK** SHRINK25/50 both boards: shrunk momentum **worsens** RMSE vs 0-forecast; no confirm. **C-SPOT-VOLTGT** MAG/ABS05 both boards lose to always-predict-1; VOLTGT ABS05 is **vol-target**, not the burned direction-THRESH ABS05. **C-SPOT-QUANT** definitional collapse: hr ≡ continuation; `noncont_calls=0` — dead definition, not a near-miss. Confirm survivors among new skill horses: **NONE**. ROBUST on Brent **H-SPOT-MOY-CONT**: (a) discovery cutoff 2018-08-21 last-500 still beats cont; (b) leave-one-year-out post-2023-08-21 **2023 FAIL** 0.374 vs 0.582 (n=91); 2024/25/26 beat. Gatekeeper: burns listed; scoped survivor stays on record as **FRAGILE**. Spot-trend skill still **not established**.
- **Direction of error:** **method-pressure-point** — (1) QUANT: a horse that is definitionally continuation (`noncont_calls=0`; hr ≡ continuation) is easy to misread as a tautology-near-miss or as a keep. Dead definition ≠ near-miss. Burn. (2) Year-stability fail on a scoped confirm survivor is easy to misread as either skill-met (because 2024/25/26 beat) or as a null burn (because 2023 fails). FRAGILE ≠ elevated. Scoped confirm ≠ skill-met. Do **not** promote. Do **not** burn the scoped survivor as a null to keep the invent queue “empty.” Year-stability Amb constrained **toward fragile**, not clearance.
- **Which rule or judgment contributed:** Confirm windows on survivors only; Track B ≠ F-SKILL; dead definition ≠ near-miss; FRAGILE ≠ elevated; WTI-met ≠ Brent-met; class-met needs the class, not one board; do not revive burned SHRINK/VOLTGT/QUANT (or prior FLIP/REV, INV, CROSS, LOGIT, MAG, PERSIST, BREAK, DXY, SHORT, VOTE, RATES, SPREAD, VIX, THRESH, SKEW). VOLTGT ABS05 ≠ direction-THRESH ABS05.
- **Adjustment made (if any):** None to parent Amb math (held 1.0). Year-stability leftover constrained toward fragile, not clearance. Tracker fold only; Lab hunt scripts not merged.
- **Notes:** Burned-class invent queue **empty**. Live scoped horse: Brent **H-SPOT-MOY-CONT** (**FRAGILE**). Lab may invent **new** classes after merge — must not revive the burned set (now including SHRINK/VOLTGT/QUANT); must not treat Brent MOY-CONT as a null; must not promote it to skill-met.

### 2026-09-05 | Markets / oil Track B (spot) | VIX/DGS10 disc-then-collapse; first scoped confirm ≠ slogan clearance — Lab batch 3
- **Gate outcome at the time:** Track B named queue already **empty** after #15–#19 and Lab batch 1 + batch 2. Spot-trend skill **not established**. Separate from R-F-SKILL / F-CC futures.
- **Later evidence:** Lab invent→test batch 3 (protocol `Lock_Hunt_Spot_Trend`; FRED EIA `DCOILWTICO` / `DCOILBRENTEU`; **VIXCLS**; disc n=500 ≤2023-08-21; cont WTI=0.5080 Brent=0.5060; confirm 250/500/750 survivors only). **C-SPOT-VIX** VIX-INV burned both boards; VIX-ALIGN disc **strong** then confirm kill — same pattern as DGS10-ALIGN. **C-SPOT-THRESH** ABS05 / ABS10 both boards (WTI ABS05 disc survivor → confirm kill; Brent both disc kill). **C-SPOT-SKEW** UPFRAC ≡ UPFRAC-GATE burned as one family both boards. **C-SPOT-SEAS** MOY-DIR confirm kill both boards; WTI MOY-CONT killed disc. **Brent H-SPOT-MOY-CONT** survived confirm (last_500 0.5440>0.5100; last_250 0.5600>0.5200; last_750 0.5253>0.5147). Gatekeeper: burns listed; Brent MOY-CONT = **scoped confirm pass**, **not** a null. Spot-trend skill still **not established**. C-SPOT-SEAS **not** established. WTI-met ≠ Brent-met.
- **Direction of error:** **method-pressure-point** — (1) VIX-ALIGN / DGS10-ALIGN: a strong discovery hit is easy to misread as a live horse; disc-then-collapse is the pattern, not a near-miss to keep. (2) First scoped confirm is easy to misread as Track B skill-met, C-SPOT-SEAS class-met, WTI-met, or parent-slogan clearance. Scoped confirm ≠ skill-met. Amb ≠ clearance. Do **not** burn the scoped survivor as a null to keep the queue “empty.”
- **Which rule or judgment contributed:** Confirm windows on survivors only; Track B ≠ F-SKILL; WTI-met ≠ Brent-met; class-met needs the class, not one board; do not revive burned VIX/THRESH/SKEW (or prior FLIP/REV, INV, CROSS, LOGIT, MAG, PERSIST, BREAK, DXY, SHORT, VOTE, RATES, SPREAD).
- **Adjustment made (if any):** None to Amb math. Tracker fold only; Lab hunt scripts not merged.
- **Notes:** Burned-class invent queue **empty**. Live scoped horse: Brent **H-SPOT-MOY-CONT**. Lab may invent **new** classes after merge — must not revive the burned set; must not treat Brent MOY-CONT as a null.

### 2026-09-05 | Markets / oil Track B (spot) | Strong discovery / last-750 near-miss ≠ least-bad — Lab batch 2 REJECT
- **Gate outcome at the time:** Track B named queue already **empty** after #15–#19 and Lab batch 1. Spot-trend skill **not established**. Separate from R-F-SKILL / F-CC futures.
- **Later evidence:** Lab invent→test batch 2 (protocol `Lock_Hunt_Spot_Trend`; FRED EIA `DCOILWTICO` / `DCOILBRENTEU`; disc n=500 ≤2023-08-21; cont WTI=0.5080 Brent=0.5060; confirm 500/250/750 survivors only). **C-SPOT-SHORT** SIGN5/SIGN10 disc survivors both boards → all killed confirm. **C-SPOT-VOTE** VOTE3 disc survivors → killed confirm; VOTE-STRICT both boards killed disc (tautology: 0 noncont / always continuation). **C-SPOT-RATES** DGS10-INV killed disc both; DGS10-ALIGN disc **strong** (~0.61–0.62) → killed confirm (WTI **tie** on last-500). **C-SPOT-SPREAD** SPREAD-FADE WTI disc→confirm kill; SPREAD-CATCH Brent disc→confirm kill (**500/250 yes, 750 no**); opposite horse killed disc on each board. Not CROSS. Vehicles: **DGS10** (not DXY); spread Brent−WTI z expanding past-only. Gatekeeper **REJECT / burn** SHORT/VOTE/RATES/SPREAD all horses both boards. Confirm survivors: **NONE**. Named Track B queue still **empty**.
- **Direction of error:** **method-pressure-point** — a strong discovery hit, or a confirm miss that fails only the last-750 window, is easy to misread as a live horse or as a reason to keep the least-bad. Discovery ≠ confirm. Near-miss confirm ≠ least-bad. Tie ≠ pick. Nothing admitted.
- **Which rule or judgment contributed:** Confirm windows on survivors only; all three must pass; Track B ≠ F-SKILL; do not revive burned SHORT/VOTE/RATES/SPREAD (or prior FLIP/REV, INV, CROSS, LOGIT, MAG, PERSIST, BREAK, DXY).
- **Adjustment made (if any):** None to Amb math. Tracker fold only; Lab hunt scripts not merged.
- **Notes:** Spot-trend skill still **not established**. Lab may invent **new** classes after merge — must not revive the burned set.

### 2026-09-05 | Markets / oil Track B (spot) | Discovery survivors die at confirm — Lab batch 1 REJECT
- **Gate outcome at the time:** Track B named queue already **empty** after #15–#19. Spot-trend skill **not established**. Separate from R-F-SKILL / F-CC futures.
- **Later evidence:** Lab invent→test batch 1 (protocol `Lock_Hunt_Spot_Trend`; FRED EIA `DCOILWTICO` / `DCOILBRENTEU`; disc n=500 ≤2023-08-21; cont WTI=0.5080 Brent=0.5060; DXY=DTWEXBGS). MAG-STRONG both killed disc; MAG-WEAK WTI killed disc; MAG-WEAK Brent disc survivor then confirm fail (250 no). PERSIST both killed disc; FRESH both disc survivors then confirm fail (WTI 500/250 no; Brent 250 no). BREAK63/42 both boards disc ties → killed. DXY-INV both disc survivors then confirm fail; DXY-ALIGN both killed disc. Gatekeeper **REJECT / burn** MAG/PERSIST/BREAK/DXY all variants both boards. Confirm survivors: **NONE**. Named Track B queue still **empty**.
- **Direction of error:** **method-pressure-point** — a discovery beat is easy to misread as a live horse or as a reason to keep the least-bad confirm miss. Discovery beat ≠ confirm. Do **not** pick least-bad. Nothing admitted.
- **Which rule or judgment contributed:** Confirm windows on survivors only; tie ≠ pick; Track B ≠ F-SKILL; do not revive burned MAG/PERSIST/BREAK/DXY (or prior FLIP/REV, INV, CROSS, LOGIT).
- **Adjustment made (if any):** None to Amb math. Tracker fold only; Lab hunt scripts not merged.
- **Notes:** Spot-trend skill still **not established**. Lab may invent **new** classes after merge — must not revive the burned set.

### 2026-09-05 | Markets / oil futures | Long null hunt cascade after hard stop (residuals live)
- **Gate outcome at the time:** Hard stop (residuals live); Amb 1.0; **H-LAG-WF** F-CC loss; **R-F-SKILL** pursue.
- **Later evidence:** Named Yahoo CL cascade (PRs #10–#14, #20–#22) and a **separate** Track B EIA spot 21-day cascade (PRs #15–#19) all burned or failed confirm. Named Yahoo CL queue **empty**. Track B named queue **empty** separately. F-SKILL still **not established**. H-KS still not run.
- **Direction of error:** **method-pressure-point** — a long string of honest nulls after hygiene is sealed is easy to misread as either refute-of-all-skill or a reason to pick the least-bad horse. Volume of nulls ≠ refute of every recipe. Discovery beat ≠ confirm. Tiny F-DAY ≠ F-CC promote. Track B ≠ F-SKILL. Empty named queue ≠ leftover closed.
- **Which rule or judgment contributed:** Named-class pulse (test runs; establishment still stops); Amb≠clearance; stand-in ≠ live; do not pick least-bad; leftover `pursue` survives an emptied named Yahoo queue.
- **Adjustment made (if any):** None to Amb math. Tracker fold only; hunt scripts and stacked PRs #9–#22 not merged.
- **Notes:** Skill leftover remains `name horse …` or `live CME / curve tape`. Park/spot-21d stays parked relative to F-SKILL.

### 2026-08-12 | Official outlook / FOMC June 2026 SEP | Brochure cannot clear P-BaseCase
- **Gate outcome at the time:** Stable Provisional (split) hard stop (Amb ≈ 1). Census vehicle L3–L10 + G4/G5/G7 **established**. F-ML-BAR on 2026 medians **not established** (L13; not a refute). C-APPROP as vote and F-LR as 2026-on-target **not met**. July 29 **OUT**.
- **Later evidence:** Named-class pulse L17 (SPF Q2 2026): PCE/core Q4/Q4 **print-match** 3.6 / 3.3; GDP concept mismatch; U 4.5 vs 4.3; bar still **not established**.
- **Direction of error:** **method-pressure-point** — an official table that *poses* figures as “most likely” is easy to misread as the economy’s expected path once Amb falls from census and meaning freezes. A later independent survey printing the same inflation numbers is a second pressure point (kinship ≠ clearance).
- **Which rule or judgment contributed:** LOCK-010 posed≠clearance; conflicted-source (SEP may census itself, may not solely meet F-ML-BAR); L11 policy-mix (18 conditionings ≠ one expected path); Amb≠clearance; live vs stand-in (July 29 kept out); named-class pulse (test runs; establishment still stops).
- **Adjustment made (if any):** None new to Amb math. Pattern map + calibration record the official-table case as the same FD/LOCK-010 lesson, not a new tag. Print-match ≠ met recorded at L17.
- **Notes:** Keep saying what 18 people submitted. Stop saying “the Fed forecasts 3.6%” and “SPF also printed 3.6 so the path is cleared.” Hit vs later actuals still would not, by itself, mean the June median *was* the expected path on June 17.

### 2026-08-12 | Equity seasonality | Sell in May / S&P / May–Oct 2026
- **Gate outcome at the time:** Stable Provisional hard stop (Amb ≈ 2.5) under Rank 1. G1* seasonality **established** (~3.52 pp); G4* Sharpe vs B&H **fails**; G5*/G6* “should” **not established**. FD1–FD5 on record. Contrastive Alt A–C recorded, not selected.
- **Later evidence:** n/a (closeout).
- **Direction of error:** **method-pressure-point** — folklore “because seasonality → should exit / improves risk-adjusted / do it this year” packages easily over-read once Amb falls from locks + one established descriptive leg.
- **Which rule or judgment contributed:** Soft-modal fork + Amb≠clearance + accuracy-first Phase 2 (workbook) prevented slogan clearance; Contrastive Recommendation separated descriptive core from failed elevation.
- **Adjustment made (if any):** None new; reinforces existing hygiene (Amb≠clearance; already-included seasonality leg does not rescue Sharpe/should).
- **Notes:** Keep saying seasonal gap; stop saying obligatory exit / Sharpe edge / 2026 mandate under Rank 1.

### 2026-08-11 | Method hygiene | Amb≠clearance, Phase 2 accuracy, soft-modal, conflicted sources, scenario legs, lock-time Amb warning
- **Gate outcome at the time:** n/a (standing-rule upgrade after debt-limit + SpaceX pressure points).
- **Later evidence:** Operator authorized implementing recommendations 1–6 as domain-general methodology.
- **Direction of error:** **method-pressure-point** — low Amb misread as success; Phase 2 could be read as substantiation-seeking; soft modals and conflicted pitch curves under-specified in templates; scenario “omission” confusion.
- **Which rule or judgment contributed:** Practice ahead of explicit text on Amb≠clearance / accuracy posture.
- **Adjustment made (if any):** Standing rule + templates/workflow updated: Amb≠clearance; Phase 2 accuracy default; soft-modal fork; conflicted-source rule; already-included legs (`S_Scenario_Pass`); lock-time Amb warning.
- **Notes:** General methodology, not application-specific patches.

### 2026-08-11 | Public equity / SpaceX | “Potential” to become a $600 stock (SPCX)
- **Gate outcome at the time:** Stable Provisional closeout (Amb ≈ 2) under Rank 1 (M2+S1+H2+X1). Well-posed ~$7.9T / $600-by-2036 target; M2 not established after scenario + deep evidence (accuracy-first). FD-M1/S1/H1 on bare wording.
- **Later evidence:** n/a at closeout.
- **Direction of error:** **method-pressure-point** — low Amb after locks can be misread as claim success; Amb≠M2 clearance. Per-share slogans force Moderate+ deviation to become testable.
- **Which rule or judgment contributed:** Locking-scaffolding + forced-deviation; scoped Rank 1 honesty; accuracy-first Phase 2 (not substantiation-seeking).
- **Adjustment made (if any):** None required beyond existing Amb-vs-clearance discipline; closeout states distinction explicitly.
- **Notes:** Starlink already included as strongest demonstrated leg; does not close multi-trillion gap alone.

### 2026-08-11 | Federal fiscal / debt limit | Scorekept pairing recommendation (Rank 1 revision of equal-cuts claim)
- **Gate outcome at the time:** Stable Provisional closeout (Amb ≈ 4). Descriptive well-posed scorekept pairing constrained; soft “should” open (normative); FRA 2023 fails C≥H under freeze; other episodes untested; parent FD1–FD5 remain on parent record.
- **Later evidence:** Post-closeout QI full path: implication C* ≈ $4.7T (~3.6×); counterfactual stipulated balance only; G1 still open. Failed instance not upgraded.
- **Direction of error:** **method-pressure-point** (positive) — Claim-Revision Scaffolding Rank 1 removed forced-deviation blockers for the *successor* claim; instance evidence then cleanly failed C≥H without settling N1; QI mode separates implication/counterfactual from claim support.
- **Which rule or judgment contributed:** Claim-Revision Scaffolding (authorization-gated); scoped-result honesty on FRA episode; soft “should” kept Normative (L1c); Quantitative Implication & Counterfactual Benefit mode (new).
- **Adjustment made (if any):** Claim-Revision Scaffolding and QI modes added to standing rule; applied end-to-end on successor.
- **Notes:** No second episode required for clean closeout; G1 optional / lower priority.

### 2026-08-11 | Federal fiscal / debt limit | Equal spending cuts with any debt-limit increase (H.R.10078-aligned)
- **Gate outcome at the time:** Stable Provisional closeout (Amb ≈ 4). Strong must/equal/irresponsible/should-not package not well-constrained; FD1–FD5 forced-deviation; P-Score-Strict+R2 well-posed but no public C≥H instance; FRA/BCA analogues only.
- **Later evidence:** Authorized Rank 1 revision application closed Stable Provisional separately; parent FD1–FD5 unchanged. FRA under revision freeze fails C≥H (does not salvage parent original wording).
- **Direction of error:** **method-pressure-point** — claim text forces Moderate+ lock deviation on every realistic package; non-derivative testing impossible.
- **Which rule or judgment contributed:** Forced-deviation extraction after G2+G3 scaffolding; scoped-result honesty under package lock.
- **Adjustment made (if any):** Standing rule already includes forced-deviation carry-forward into Original-Claim Assessment (applied here). Later: Claim-Revision Scaffolding mode added and used for Rank 1 successor.
- **Notes:** Keep original wording on parent; successor is a marked revision, not a silent rewrite.

### 2026-08-11 | AV architectures | E2E vs modular preferability (R1/R2 vs R4)
- **Gate outcome at the time:** Phase 2 Attempt 1 marked general R1/R2 currently intractable; reopen mentioned R4/matching but dependency was easy to read as ordinary evidence-gap rather than **dominant blocker**.
- **Later evidence:** Corrective pass showed R1/R2 were blocked primarily by unset R4; locking-scaffolding + package selection made dependents well-posed without answering them empirically.
- **Direction of error:** **method-pressure-point** (under-specified dependency / soft reopen), not a false ADMIT of the original slogan.
- **Which rule or judgment contributed:** Intractability reopen listed as trailing condition; inter-parameter dependency not yet first-class; no locking-scaffolding / OR-slot rule yet.
- **Adjustment made (if any):** Standing rule updated: explicit inter-parameter dependency; locking-scaffolding with ranked packages + relevance warnings; OR-slot resolution; scoped-result honesty; Original-Claim Assessment + revision-vs-continuation fork; evidence-intake template; compact no-admit mandatory; canonical `.mdc` as sole full rule text.
- **Notes:** AV application closed Stable Provisional. P-Strong-Both left B1|B2 and D5|D1 as OR-slots — under the new OR-slot rule those must be singled or formally “either”-accepted going forward.

### Prior note
*Conscience sketch and 2026 Fox News opinion article on democratic socialism: no confirmed blocked-but-later-supported or allowed-but-later-collapsed entries; remain consistent with currently available material.*
