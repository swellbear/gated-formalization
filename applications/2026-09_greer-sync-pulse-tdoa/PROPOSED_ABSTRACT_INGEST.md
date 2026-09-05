# Proposed abstract ingest — US10135667B1 as Amb spine (Operator-gated)

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**lab_admits:** false  
**Operator:** **ADMIT ingest** (SOURCE + this sheet + [`ABSTRACT_INGEST_SUMMARY.md`](ABSTRACT_INGEST_SUMMARY.md)). Still **not** claim clearance.  
**Copy gate:** [`COPY_GATE.md`](COPY_GATE.md) **PASS**  
**SOURCE:** [`SOURCE.md`](SOURCE.md)  
**Digestion:** [`DIGESTION_ABSTRACT_INGEST.md`](DIGESTION_ABSTRACT_INGEST.md)

Lab proposed the ingest sheet. Lab does **not** self-admit. The gate below is copied from the Operator.

**What this is not:** Claim clearance. A locator. Hardware **X**. A patent-product embodiment. Claim-language product copy. A send to Greer. Skill-met. RF / ML / fingerprint invent. Reopening cell-tower as live. Reopening BIA. SkyMirr invent reopen.

---

## 0. Plain-language framing

**What this is:** Fold the **published abstract** of US10135667B1 in as the Amb spine — the named problem set we are collaborating on — without copying claims and without treating our prior sim string as if it already understood that set.

**What this settles (gated):** Two bars. Patent-facing **≤1 m xy**. Scoped **sim X = 0.50 m** stays only under ideal refs + named GEOM0 noise — **not** a patent promise. **DGPS ~0.4–0.5 m** is named as the absolute floor. Prior SYNC/JOINT/DRIFT/GATE = **sync-fragility evidence (partial)**. Geometry-not-bottleneck under our noise model **HARDENS**. Rank-1 next = **A1** (ref-floor honesty). Link/map **PARKED**. Greer send **HOLD** until this ingest **and preferably A1** (or A1+A2).

**What this is not:** Not claim clearance. Not a rewrite of the Founder sim claim into a patent promise. Not a send. Not Lab invent of A1 this fold (A1 is **opened**, not scored).

---

## 1. Amb spine (paraphrase of the published abstract)

From [`SOURCE.md`](SOURCE.md) — paraphrase, not claims:

1. **GPS-denied / indoor / enclosed** target (buildings or enclosed structures).
2. **Multiple reference nodes** each transmitting a **synchronization pulse** to body-worn or device-mounted receivers.
3. Receiver **high-speed clock** measuring **TDOA** of those sync pulses to the resolution needed for precise positioning.
4. **Central compute** of receiver position **relative to a fixed reference**.
5. **Realtime** monitor of receivers as they move in the target area.
6. Display **overlaid on GIS / building CAD** — **PARKED** (link/map).

That list is the Amb spine. Our prior string scored geometry + mild NLOS + inter-ref sync fragility on a laptop sim. It did **not** ingest this spine.

---

## 2. Success-bar Soften/Harden (Operator)

| Bar | Role | Honesty |
|-----|------|---------|
| Patent-facing **≤1 m xy** | Collaboration / description-typical horizontal object (≥3 refs) | **Not** a p90 promise. **Not** claim copy. **Not** hardware **X**. |
| Scoped **sim X = 0.50 m** | GEOM0 median @ 1 ns under **ideal known refs** + named noise (JOINT1 fixed-offset + DRIFT1 batch α + GATE1 refuse-belt + mild NLOS; **median-not-p90**) | **Not** the patent promise. Keep only as the scoped sim bar. |
| **DGPS ~0.4–0.5 m** | Named **absolute floor** (description-typical survey-quality DGPS on refs) | Absolute mobile error is floored by how refs are placed/timed. GPS/DGPS stay **refs-only** — **never** the mobile fix. |

**Soften:** do **not** read 0.50 m as the patent-facing bar.  
**Harden:** the two-bar split + named DGPS floor.

---

## 3. Prior-string Soften / HARDEN (Operator)

| Prior | After ingest |
|-------|----------------|
| **SYNC1 Soften** · **JOINT1 Soften** · **DRIFT1 HARDEN** · **GATE1 Soften** | **Soften** to **sync-fragility evidence (partial)**. Useful. **Not** the full patent hard-problem set. |
| Claim that we fully understood the patent hard-problem set | **Soften.** We did not. Abstract leftovers A1–A4 remain. |
| **GEOM0 HARDEN** (geometry-not-bottleneck under our noise model) | **HARDEN stands.** |
| **MULTIPATH1 Soften** | Still stands as **our** additive-NLOS scope. **Not** A3 (indoor first-arrival leftover). **Later.** |

Prior write-up ([`GREER_WRITEUP.md`](GREER_WRITEUP.md) + Lab [`GREER_WRITEUP_DRAFT.md`](GREER_WRITEUP_DRAFT.md)) = **sync-fragility evidence only**.

---

## 4. Rank-1 leftovers (locked order)

| ID | Leftover | Disposition |
|----|----------|-------------|
| **A1** | **Ref-floor honesty** — absolute vs relative; named **DGPS ~0.4–0.5 m** floor vs our ideal-known-refs sim | Later **A1 Soften** — [`SCORE_A1.md`](SCORE_A1.md). Not scored on this ingest sheet. |
| **A2** | **Clock-count / TDOA-resolution honesty** — abstract’s high-speed receiver clock “to the resolution needed,” distinct from our inter-ref SYNC/JOINT/DRIFT/GATE string | Named. **GO A2** next after A1 Soften. |
| **A3** | **Indoor / first-arrival / denied-box radio** — GPS-denied buildings / enclosed structures; not our additive mild-NLOS Soften | Named. After A2. |
| **A4** | **Realtime / central-compute / motion** — abstract names realtime as they move; our JOINT1/DRIFT1 wins were path-batch | Named. After A2 (with A3). |
| **Link/map** | GIS / CAD overlay | **PARKED** |

---

## 5. Operator gate (authoritative)

**ADMIT ingest** of US10135667B1 **published abstract** as Amb spine.

- Still **not** claim clearance.
- **No** claim-language product copy. [`COPY_GATE.md`](COPY_GATE.md) **PASS**.
- Patent-facing bar → **≤1 m xy**.
- Keep **X = 0.50 m** only as scoped sim bar under ideal refs + named noise (GEOM0) — **not** a patent promise.
- Name **DGPS ~0.4–0.5 m** absolute floor.
- Prior string Soften: SYNC/JOINT/DRIFT/GATE = sync-fragility evidence (**partial**). Soften the claim we fully understood the patent hard-problem set. **HARDEN:** geometry-not-bottleneck under our noise model stands.
- Rank-1 next **locked:** **A1** (ref-floor honesty) first, then **A2**, then **A3/A4**. Link/map **PARKED**.
- **Greer send HOLD** until this ingest fold **+ preferably A1** (or A1+A2). Prior write-up = sync-fragility evidence only.
- **Lab invent HOLD** except **A1 opened** by Operator.
- Hardware **X** stays **PARKED**. Cell-tower **PARKED**. BIA **CLOSED**. SkyMirr stays its own Amb (not this fold).

---

## 6. Hard NO

- Do **not** copy US10135667B1 claim language or write a product embodiment.
- Do **not** send [`GREER_WRITEUP.md`](GREER_WRITEUP.md) as if it covered the patent hard-problem set.
- Do **not** treat **0.50 m** as the patent-facing bar, a p90 bar, a multipath-robust bar, a free per-epoch realtime bar, or a hardware bar.
- Do **not** invent A2 / A3 / A4 / link-map this fold.
- Do **not** invent fingerprint / ML / RF.
- Do **not** use GPS / DGPS as the mobile fix.
- Do **not** unpark hardware **X**.
- Do **not** reopen cell-tower as live. Do **not** reopen BIA.
- Do **not** write skill-met / elevated language.

---

## 7. Admission check (compact `04`)

**Targeted gap:** Amb spine was bibliographic-only; success bar was treated as if 0.50 m were the collaboration bar; prior string was easy to over-read as “we understood the patent hard-problem set.”

**Relevance:** Yes — published abstract + Operator-named description-typical numbers constrain the spine and the bars. They do **not** establish a locator.

**Cons:** Compatible with CLAIM LOCK, C1–C3, GEOM0 HARDEN, prior Soften/HARDEN pulses, GPS-never-mobile-fix, no claim copy.

**Decision:** Operator **ADMIT** ingest. Expected Amb effect: spine **named** (A1–A4 + parked link/map); 0.50 m **narrowed** to scoped sim bar; patent-facing **≤1 m xy** named. **Amb drop ≠ clearance.** Prod: none invented.

**Establishment-stop drill:** Would honest `04` declare established? **No.** Stop not triggered.

---

*Docs only. ADMIT ingest ≠ claim clearance. Lab does not self-admit. No RF / ML. Later A1 Soften is on SCORE_A1.md.*
