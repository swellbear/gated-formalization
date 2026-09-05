# A2 residual sync vs commercial 1PPS — score (Operator-gated Soften, conditional)

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**String:** A2 — residual sync vs commercial 1PPS (clock-count / TDOA-resolution honesty)  
**Parent:** abstract ingest **ADMITTED** · **A1 Soften carried** ([`SCORE_A1.md`](SCORE_A1.md); abs ≤1 m poseable; X=0.50 perfect-ref only; RN floor named; do **not** Harden absolute **X**) · prior SYNC/JOINT/DRIFT/GATE = **partial** sync-fragility  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Digestion:** [`DIGESTION_A2.md`](DIGESTION_A2.md)  
**Copy gate:** [`COPY_GATE.md`](COPY_GATE.md)  
**A1 (carried):** [`SCORE_A1.md`](SCORE_A1.md) · [`DIGESTION_A1.md`](DIGESTION_A1.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit.

Lab scratch was **not** on this fold VM. Metrics and class names below are copied from the **Operator gate** (authoritative). Hunt scripts / Lab notebooks are **not** on master.

**What this is not:** A locator. Claim clearance. Hardware **X**. Skill-met. RF / ML / fingerprint invent. GPS/DGPS as the mobile fix. Claim-language product copy. A product embodiment of a 1PPS box. A send to Greer. Reopening cell-tower as live. Reopening BIA. SkyMirr invent reopen. A p90 bar.

---

## 0. Plain-language framing

**What this is:** The A2 leftover after A1 Soften. The published abstract names a high-speed receiver clock “to the resolution needed.” Our prior string already showed inter-ref sync fragility. This pulse asks whether **commercial 1PPS / public timing residuals** can carry the named bars, or only a **named differential relative-clock** window can.

**What this settles:** **Soften (conditional).** Kill is **not** a full-string kill. The named window is **JOINT1 + differential ~2.5 ns (F9T-class) path-shared relative-clock**. Bare Chan at that class **fails**. Commodity / common-view / absolute-only public classes **fail both curves**. **Harden** that public residuals are `≪ 0.3 ns` is **unsupported**.

**What this is not:** Not a field locator. Not a hardware bar. Not a claim that an F9T was used. Not a claim that patent “simultaneous via DGPS 1PPS” equals commercial 1PPS reality. Not a send.

---

## 1. Board (gated)

| Field | Gated record |
|-------|----------------|
| Leftover | **A2** clock-count / TDOA-resolution honesty vs commercial 1PPS |
| A1 carried | **Soften** — abs **≤1 m** poseable (Chan abs **0.832 m** @ `σ_ref=0.5`); **X = 0.50 m** **perfect-ref only**; RN floor named; abs ≤0.50 **not**; JOINT1 scrape **0.449** rides floor — do **not** Harden absolute **X** |
| Chan-alone (SYNC1) | Near-ideal window `σ_sync ≲ 0.3 ns` → **0.382 m**; 1 ns scrapes **0.513 m**; ≥3 ns fails |
| JOINT1 (fixed_trial) | **0.231 m** @ 1 ns; **0.439 m** @ 3 ns ≤ X; **1.816 m** @ 10 ns fails |
| Named Soften window | **JOINT1 + differential ~2.5 ns (F9T-class) path-shared relative-clock** |
| GPS / DGPS | never the mobile fix (place/time refs only, if used at all) |

This fold does **not** re-run the sim. Numbers are the gated Lab / Operator summary. No new JOINT1 median at exactly 2.5 ns is invented: ~2.5 ns sits inside the already-scored JOINT1 **≲ 3 ns** window (**0.439 m** @ 3 ns ≤ X).

---

## 2. Lab / Operator score (copied from the gate)

| Class | Chan-alone | JOINT1 (path-shared relative-clock) |
|-------|------------|-------------------------------------|
| Differential **~2.5 ns (F9T-class)** | **Kill** — ~**1.14 m** ≫ **X = 0.50 m** | **Soften (conditional)** — named path-shared relative-clock; inside JOINT1 **≲ 3 ns** (**0.439 m** @ 3 ns ≤ X) |
| Commodity **20–50 ns** | **Kill** | **Kill** |
| Common-view **~10 ns** | **Kill** | **Kill** (JOINT1 @ 10 ns = **1.816 m** fails **X** and **≤1 m**) |
| Absolute-only **~5–15 ns** | **Kill** | **Kill** |
| Public residuals **ns–tens-of-ns** | **Harden unsupported** — not `≪ 0.3 ns` | **Harden unsupported** — not `≪ 0.3 ns` |

**Soften (conditional). Kill not a full-string kill.**

- **Soften** only under **JOINT1 + differential ~2.5 ns (F9T-class) path-shared relative-clock** **named**.
- **Kill** bare Chan at ~2.5 ns (~**1.14 m** ≫ X).
- **Kill** commodity **20–50 ns** / common-view **~10 ns** / absolute-only **~5–15 ns** for **both** curves (Chan and JOINT1).
- **Harden unsupported:** public residuals are **ns–tens-of-ns**, **not** `≪ 0.3 ns` (the Chan-alone SYNC1 window).

**Brutal lock:** patent **simultaneous-via-DGPS-1PPS** ≠ commercial 1PPS reality.

---

## 3. Combined bars / named window (standing)

**A1 Soften carried.**

| Bar | Meaning after A1 + A2 |
|-----|------------------------|
| **≤1 m xy** | Patent-facing / collaboration object. Poseable under DGPS-class RN survey (A1 Chan abs **0.832 m** @ `σ_ref=0.5`). **Not** cleared by commercial 1PPS. |
| **sim X = 0.50 m** | **Perfect-ref** scoped sim bar. Honest under **JOINT1 + differential ~2.5 ns (F9T-class) path-shared relative-clock** + prior mild-NLOS + named DRIFT1 batch α + GATE1 refuse-belt. **Median-not-p90**. **Not** a patent promise. **Not** an absolute bar under the RN floor. |
| **RN floor** | Named **DGPS ~0.4–0.5 m** (A1). Abs ≤0.50 m **not**. JOINT1 scrape **0.449** rides the floor — do **not** Harden absolute **X**. |

**Fails / out of this budget (do not invent a rescue):**

- Bare **Chan** at ~2.5 ns (~**1.14 m**).
- Commodity **20–50 ns**, common-view **~10 ns**, absolute-only **~5–15 ns** — **both** Chan and JOINT1.
- JOINT1 `σ_sync` = **10 ns** → **1.816 m**.
- Treating patent simultaneous-via-DGPS-1PPS as if it were commercial 1PPS.

Do **not** invent fingerprint / ML / RF to rescue commodity 1PPS.

---

## 4. Operator gate (authoritative)

**Soften (conditional).**

- Soften under **JOINT1 + differential ~2.5 ns (F9T-class) path-shared relative-clock** **named**.
- **Kill** bare Chan at ~2.5 ns (~**1.14** ≫ X).
- **Kill** commodity **20–50 ns** / common-view **~10 ns** / absolute-only **~5–15 ns** for **both** curves.
- **Harden unsupported** (public residuals **ns–tens-of-ns**, **not** `≪ 0.3 ns`).

**Brutal lock:** patent simultaneous-via-DGPS-1PPS ≠ commercial 1PPS reality.

**A1 Soften carried** (≤1 m; X=0.50 perfect-ref; RN floor named).

**Next (user override suite):** **GO A3** then **A4**; Soften/Harden each. Greer send **HOLD** until the suite digests.

**PARK** hardware **X**. **Lab HOLD invent** except **A3 opened**. Link/map stays **PARKED**.

**Honesty locks**

- Conditional Soften is **not** a Chan-alone pass at F9T-class.
- F9T-class is an **Operator-named public timing class**, **not** a product embodiment and **not** a claim that this folder used an F9T.
- Public 1PPS residuals stay **ns–tens-of-ns**. They do **not** Harden the Chan-alone `≲ 0.3 ns` window.
- Patent simultaneous-via-DGPS-1PPS is **Operator-named brutal-lock paraphrase**. It is **not** claim-language product copy. It is **not** commercial 1PPS reality.
- **A1 Soften** still stands (≤1 m; perfect-ref X; RN floor named).
- Prior SYNC/JOINT/DRIFT/GATE stay **partial** sync-fragility evidence.
- **GEOM0 HARDEN** still stands.
- **MULTIPATH1 Soften** still stands (not A3).
- Path-shared **batch**, **not** free per-epoch realtime (A4 leftover).
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

- Do **not** treat commercial 1PPS as the named Soften window.
- Do **not** collapse patent simultaneous-via-DGPS-1PPS into commercial 1PPS reality.
- Do **not** treat bare Chan at ~2.5 ns (~**1.14 m**) as a pass.
- Do **not** treat commodity **20–50 ns**, common-view **~10 ns**, or absolute-only **~5–15 ns** as a pass on **either** curve.
- Do **not** Harden “public residuals `≪ 0.3 ns`.”
- Do **not** write F9T / 1PPS product copy or a patent-claim embodiment.
- Do **not** treat **0.50 m** as the patent-facing bar, a p90 bar, a multipath-robust bar, a free per-epoch realtime bar, or a hardware bar.
- Do **not** invent fingerprint / ML / RF to rescue commodity 1PPS.
- Do **not** use GPS / DGPS as the mobile fix.
- Do **not** copy US10135667B1 claim language.
- Do **not** commit Lab scratch / hunt scripts as established.
- Do **not** write skill-met / elevated language.
- Do **not** send [`GREER_WRITEUP.md`](GREER_WRITEUP.md) until the A1–A4 suite digests.
- Do **not** invent **A4** before **A3**.
- Do **not** unpark hardware **X** or link/map.
- Do **not** reopen cell-tower as live. Do **not** reopen BIA. Do **not** reopen SkyMirr invent.

---

## 6. Admission check (compact `04`)

**Targeted gap:** A2 clock-count / TDOA-resolution honesty vs commercial 1PPS; risk of reading patent simultaneous-via-DGPS-1PPS as if commodity 1PPS already carried the bars.

**Relevance:** Yes — already-scored Chan / JOINT1 medians plus Operator-named public timing classes constrain the leftover. They do **not** establish a locator.

**Cons:** Compatible with CLAIM LOCK, ingest, A1 Soften, GEOM0 HARDEN, GPS-never-mobile-fix, no claim copy.

**Decision:** Operator **ADMIT Soften (conditional)**. Expected Amb effect: A2 **named-window Soften**; Chan-alone at F9T-class **killed**; commodity / common-view / absolute-only **killed** on both curves; Harden of `≪ 0.3 ns` public residuals **unsupported**. **Amb drop ≠ clearance.** Prod: none invented.

**Establishment-stop drill:** Would honest `04` declare established? **No.** Stop not triggered.

---

*Docs only. Soften (conditional) ≠ claim clearance. Kill bare Chan ≠ full-string kill. F9T-class named ≠ product used. Patent simultaneous-via-DGPS-1PPS ≠ commercial 1PPS. A1 Soften carried. Not skill-met. Not a patent-product claim. Not rithm. Lab does not self-admit. Lab scratch was not on this VM; summary copied from the Operator gate. Greer send HOLD until the suite digests.*
