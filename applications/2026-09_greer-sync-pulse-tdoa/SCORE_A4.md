# A4 phase-flip detection jitter — score (Operator-gated Soften X/σ_t)

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**String:** A4 — honest 50 kHz phase-flip detection jitter vs GEOM0 1 ns; **Soften X/σ_t**  
**Parent:** abstract ingest **ADMITTED** · **A1 Soften carried** ([`SCORE_A1.md`](SCORE_A1.md)) · **A2 Soften-conditional** ([`SCORE_A2.md`](SCORE_A2.md)) · **A3 Soften** ([`SCORE_A3.md`](SCORE_A3.md); mild/intermittent LE ~0.5–1 m / `f≈0.25` survives ≤1 m; persistent `B_lb` / `B_dense` fail) · prior SYNC/JOINT/DRIFT/GATE = **partial** sync-fragility  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Digestion (this pulse):** [`DIGESTION_A4.md`](DIGESTION_A4.md)  
**Suite scaffold:** [`DIGESTION_A1A4_SUITE.md`](DIGESTION_A1A4_SUITE.md)  
**A1 (carried):** [`SCORE_A1.md`](SCORE_A1.md) · [`DIGESTION_A1.md`](DIGESTION_A1.md)  
**Copy gate:** [`COPY_GATE.md`](COPY_GATE.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit.

Lab scratch / Lab DIGEST was **not** on this fold VM. Metrics and class names below are copied from the **Operator gate** (authoritative). Hunt scripts / Lab notebooks are **not** on master. Operator may follow-on when Lab DIGEST lands.

**What this is not:** A locator. Claim clearance. Hardware **X**. Skill-met. RF / ML / fingerprint invent. An RF bench. GPS/DGPS as the mobile fix. Claim-language product copy. A send to Greer. A Harden of GEOM0 1 ns. A wholesale Kill of the laptop model. Reopening cell-tower as live. Reopening BIA. SkyMirr invent reopen. A p90 bar.

---

## 0. Plain-language framing

**What this is:** The A4 leftover after A1–A3. GEOM0 locked **sim X = 0.50 m** at **σ_t = 1 ns**. This pulse asks whether a **50 kHz phase-flip** detection story can honestly carry that 1 ns, or whether **X / σ_t** must be Softened.

**What this settles:** **Soften X/σ_t.** Kill is **not** wholesale (the laptop model **remains**). Honest 50 kHz phase-flip detection jitter is **≫ GEOM0 1 ns**. Mid-class **J_mid ~100–500 ns** maps to **tens of meters**. Optimistic **J_stretch ~10 ns** maps to **~3.8 m** and **fails ≤1 m**. **JOINT1 does not cancel detection jitter.** **Harden unsupported.** **RF bench PARKED.**

**What this is not:** Not a field locator. Not a hardware bar. Not a reason to build an RF bench this fold. Not a claim that 1 ns is an honest phase-flip detector. Not a send.

---

## 1. Board (gated)

| Field | Gated record |
|-------|----------------|
| Leftover | **A4** phase-flip detection jitter / **Soften X/σ_t** |
| Pulse class | Honest **50 kHz** phase-flip detection (Operator-named) |
| GEOM0 contrast | **1 ns** RX noise was the X basis (median **0.361 m**; **X = 0.50 m** perfect-ref) |
| A1 carried | **Soften** — patent-facing **≤1 m xy**; **X = 0.50 m** **perfect-ref**; **RN floor named** |
| A2 carried (gate) | **Soften-conditional** — JOINT1 + ~2.5 ns; **Kill** bare Chan / commodity |
| A3 carried (gate) | **Soften** — mild/intermittent **LE** only for **≤1 m**; persistent **B_lb** fails |
| JOINT1 vs jitter | **Does not cancel** detection jitter (per-measurement; not a shared-τ offset) |
| GPS / DGPS | never the mobile fix (place/time refs only, if used at all) |

This fold does **not** re-run the sim. Numbers are the gated Operator summary. No new GEOM0 median at 10 ns / 100–500 ns is invented beyond the gate’s **~3.8 m** / **tens of meters**.

---

## 2. Lab / Operator score (copied from the gate)

| Class | Honest detection jitter | Map (Operator-named) | vs bars |
|-------|-------------------------|----------------------|---------|
| GEOM0 X basis | **1 ns** (model) | median **0.361 m**; **X = 0.50 m** perfect-ref | **not** an honest 50 kHz phase-flip detector |
| **J_stretch** (optimistic) | **~10 ns** | **~3.8 m** | **fails ≤1 m**; fails perfect-ref **X = 0.50 m** |
| **J_mid** | **~100–500 ns** | **tens of meters** | **fails** both bars |
| JOINT1 on detection jitter | — | does **not** cancel | shared-τ is not a detector-jitter soak |
| RF bench | — | **PARKED** | no radio campaign this fold |

**Soften X/σ_t. Kill not wholesale. Harden unsupported.**

- Honest 50 kHz phase-flip detection jitter **≫ GEOM0 1 ns**.
- **J_mid ~100–500 ns → tens of meters.**
- **J_stretch ~10 ns → ~3.8 m fails ≤1 m.**
- **JOINT1 does not cancel detection jitter.**
- **Not Kill wholesale** — laptop model **remains**.
- **Harden unsupported.**
- **RF bench PARKED.**

---

## 3. Combined bars / named window (standing)

**A1 Soften carried. A2 Soften-conditional carried (gate). A3 Soften carried (gate).**

| Bar | Meaning after A1–A4 |
|-----|---------------------|
| **≤1 m xy** | Patent-facing / collaboration object. **J_stretch ~10 ns (~3.8 m)** already **fails** it. Commercial 1PPS does **not** clear it (A2). Persistent **B_lb** fails it (A3). |
| **sim X = 0.50 m** | **Perfect-ref** scoped sim bar @ **σ_t = 1 ns**. **Softened** as an honest phase-flip detector. **Not** a patent promise. **Not** an absolute bar under the RN floor (A1). |
| **σ_t honesty** | GEOM0 **1 ns** is a **named model**, **not** an honest 50 kHz phase-flip detection floor. **Soften X/σ_t.** |
| **RN floor** | Named **DGPS ~0.4–0.5 m** (A1). |

**Fails / out of this budget (do not invent a rescue):**

- Treating GEOM0 **1 ns** as an honest 50 kHz phase-flip detector.
- Treating **J_stretch ~10 ns (~3.8 m)** as a pass of **≤1 m**.
- Treating **J_mid ~100–500 ns** as in-band for either bar.
- Treating **JOINT1** as a cancel of detection jitter.
- Unparking an **RF bench** to Harden 1 ns.

Do **not** invent fingerprint / ML / RF to rescue detection jitter.

---

## 4. Operator gate (authoritative)

**Soften X/σ_t.**

> Honest 50 kHz phase-flip detection jitter ≫ GEOM0 1 ns (J_mid ~100–500 ns → tens of meters; J_stretch ~10 ns → ~3.8 m fails ≤1 m). JOINT1 does not cancel detection jitter. Not Kill wholesale (laptop model remains). Harden unsupported. RF bench PARKED.

**Suite Soften wrap (A1→A4):**

- **A1 Soften:** abs ≤1 m under RN floor; X=0.50 perfect-ref only; DGPS floor named
- **A2 Soften-conditional:** JOINT1+~2.5 ns Soften; Kill bare Chan/commodity
- **A3 Soften:** mild/intermittent LE only for ≤1 m; persistent B_lb fails
- **A4 Soften:** Soften X/σ_t; RF PARKED

**Greer send HOLD** until DIGEST + Founder fold. **No** claim-language product copy.

**PARK** hardware **X**. **PARK** RF bench. **Lab HOLD invent.** Link/map stays **PARKED**.

**Honesty locks**

- Soften X/σ_t is **not** a wholesale Kill of the laptop model.
- GEOM0 **1 ns** remains the **named model** that produced perfect-ref **X = 0.50 m**. It is **not** Harden-as-honest phase-flip detection.
- **J_stretch ~10 ns → ~3.8 m** is Operator-named. It **fails ≤1 m**.
- **J_mid ~100–500 ns → tens of meters** is Operator-named.
- **JOINT1** still stands as the **fixed-offset** shared-τ window. It does **not** soak detector jitter.
- **A1 Soften** still stands (≤1 m poseable under RN floor; perfect-ref X; RN floor named).
- **A2 Soften-conditional** still stands (JOINT1+~2.5 ns; Kill bare Chan/commodity).
- **A3 Soften** still stands (mild/intermittent LE only for ≤1 m; persistent B_lb fails).
- Prior SYNC/JOINT/DRIFT/GATE stay **partial** sync-fragility evidence.
- **GEOM0 HARDEN** still stands as geometry-not-bottleneck under the **named 1 ns model**. Silent “1 ns is honest phase-flip” is **Softened**.
- **MULTIPATH1 Soften** still stands (not a substitute for A3).
- Path-shared **batch**, **not** free per-epoch realtime. Ingest A4 realtime leftover is **not** Hardened.
- GPS is **never** the mobile fix.
- This is **not** claim clearance.
- This is **not** a locator.
- This is **not** skill-met.
- No fingerprint / ML / RF invent.
- **No** claim-language product copy.

US10135667B1 — owner-requested **collaboration framing**. Published abstract is the Amb spine. **No claim-language copy.** Not a product embodiment.

Cell-tower Amb stays **PARKED**. BIA→weight portfolio stays **CLOSED**. SkyMirr stays its own Amb.

---

## 5. Hard NO

- Do **not** treat GEOM0 **1 ns** as an honest 50 kHz phase-flip detector.
- Do **not** treat **J_stretch ~10 ns (~3.8 m)** as a pass of **≤1 m** or of **X = 0.50 m**.
- Do **not** treat **J_mid ~100–500 ns** as in-band.
- Do **not** treat JOINT1 as a cancel of detection jitter.
- Do **not** Kill the laptop model wholesale.
- Do **not** Harden 1 ns / RF-bench 1 ns.
- Do **not** unpark an **RF bench**.
- Do **not** treat **0.50 m** as the patent-facing bar, a p90 bar, a multipath-robust bar, a free per-epoch realtime bar, or a hardware bar.
- Do **not** invent fingerprint / ML / RF to rescue detection jitter.
- Do **not** use GPS / DGPS as the mobile fix.
- Do **not** copy US10135667B1 claim language.
- Do **not** commit Lab scratch / hunt scripts as established.
- Do **not** write skill-met / elevated language.
- Do **not** send [`GREER_WRITEUP.md`](GREER_WRITEUP.md) until DIGEST + Founder fold.
- Do **not** unpark hardware **X** or link/map.
- Do **not** reopen cell-tower as live. Do **not** reopen BIA. Do **not** reopen SkyMirr invent.

---

## 6. Admission check (compact `04`)

**Targeted gap:** A4 phase-flip detection jitter vs GEOM0 1 ns; risk of reading perfect-ref **X = 0.50 m** as if a 50 kHz phase-flip detector already carried 1 ns.

**Relevance:** Yes — Operator-named J_mid / J_stretch vs the already-scored GEOM0 1 ns board constrain the leftover. They do **not** establish a locator.

**Cons:** Compatible with CLAIM LOCK, ingest, A1 Soften, A2 Soften-conditional, A3 Soften, GEOM0 HARDEN (geometry-not-bottleneck under the named model), GPS-never-mobile-fix, no claim copy.

**Decision:** Operator **ADMIT Soften X/σ_t**. Expected Amb effect: A4 **Soften**; 1 ns detector **not** Harden; RF bench **PARKED**; laptop model **remains**. **Amb drop ≠ clearance.** Prod: none invented.

**Establishment-stop drill:** Would honest `04` declare established? **No.** Stop not triggered.

---

*Docs only. Soften X/σ_t ≠ claim clearance. Not Kill wholesale ≠ 1 ns Harden. J_stretch ~10 ns ≠ ≤1 m. JOINT1 ≠ detector-jitter cancel. RF bench PARKED. A1–A3 Soften carried. Not skill-met. Not a patent-product claim. Not rithm. Lab does not self-admit. Lab scratch / Lab DIGEST was not on this VM; summary copied from the Operator gate. Greer send HOLD until DIGEST + Founder fold.*
