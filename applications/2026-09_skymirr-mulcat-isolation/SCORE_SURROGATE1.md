# SURROGATE1 score — smoke-class even/odd surrogate (Operator-gated Soften Rank1)

**Date:** 2026-09-05  
**Application:** `2026-09_skymirr-mulcat-isolation`  
**String:** SURROGATE1 — documented surrogate (scikit-rf class) with-vs-without isolation peek; Rank1 = **SURR_EO_COUPLED**; Rank2/3 = Soften-carry peeks only  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Digestion:** [`DIGESTION_SURROGATE1.md`](DIGESTION_SURROGATE1.md)  
**Fog peek (prior Soften):** [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md) · [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit.

Lab scratch was **not** on this fold VM. Metrics below are copied from the **Operator gate** (authoritative). Hunt scripts / Lab notebooks are **not** on master. **No invent scripts** merged this fold.

**What this is not:** Isolation shown. Claim clearance. PCB isolation. A measured S21 campaign. Rank1 bar-met. Amb Harden. Training established. Skill-met. Commercial clearance. Fingerprint-style nonsense. HFSS. A product copied from US12,719,158 B2. A vanity-freeze of bibliographic ~12 dB. A vanity Ze/Zo chase. Reopening Greer invent. Sending the Greer write-up. Reopening cell-tower as live. Reopening BIA→weight. Rithm.

---

## 0. Plain-language framing

**What this is:** A cheap smoke-class surrogate pulse on the fog-peek board. Live path stays **surrogate-first**. Rank1 is even/odd coupled (**SURR_EO_COUPLED**). Rank2/3 are peeks only — they do **not** Amb Harden and they do **not** clear Rank1.

**What this settles:** Operator **ADMIT Soften Rank1**. Kill did **not** fire. Provisional **Δ = 5 dB** **stands** and is **unmet** on Rank1. Rank1 ΔS21 sits in the Soften band 3–5. Surrogate ≠ PCB. Peek succeed is **not** isolation shown.

**What this is not:** Not isolation shown. Not PCB clearance. Not a reason to retune Ze/Zo until 3.32 crosses 5. Not a reason to promote Rank2/3 into Rank1. Not invent of a model. Not HFSS.

---

## 1. Board (gated)

| Field | Gated record |
|-------|----------------|
| Live path | **surrogate-first** (scikit-rf class; **not** PCB; **not** full-wave) |
| Rank1 object | **SURR_EO_COUPLED** — smoke-class mild even/odd |
| Rank1 condition | Ze=70 / Zo=36 @ **2 GHz** |
| Metric | ΔS21 (with-vs-without isolation improvement) |
| Locked bar | provisional **Δ = 5 dB** (Soften; do **not** vanity-freeze 12) |
| Soften band | **3–5 dB** (Rank1 sitting here is Soften, **not** bar-met) |
| Alternate Harden | **Δ = 10** held (not locked) |
| Rank2 / Rank3 | Soften-carry **peeks only** — do **not** Amb Harden / Rank1 clearance |

This fold does **not** re-run the surrogate. Numbers are the gated Lab summary copied from the Operator gate.

---

## 2. Lab score (copied from the gate)

| Rank | Object | ΔS21 (gated) | Gate |
|------|--------|--------------|------|
| **1** | **SURR_EO_COUPLED** — smoke-class mild EO (Ze=70 / Zo=36) @ 2 GHz | **3.32 dB** | **Soften Rank1** — Soften band 3–5; locked **Δ = 5** bar **unmet**. No Soften-param vanity Ze/Zo chase |
| 2 (peek only) | **SURR_NEUTRAL_DN** | **54.19 dB** | Soften-peek / **park as Amb path** — textbook lumped cancel; **wrong object** for MuLCAT multi-layer. Do **not** Amb Harden / Rank1 clearance |
| 3 (peek only) | **SURR_DGS_EQ** | **6.24 dB** | **Formal DGS Hold** — meets bar on eq-circuit; **fragile to detune**; **not** Amb clear; **not** PCB / claim clearance. Do **not** Amb Harden / Rank1 clearance |

**Soften Rank1 (Operator).** Locked Δ = 5 **unmet**.

- Rank1 **3.32 dB** is inside the Soften band **3–5**. That is Soften, **not** bar-met, **not** Harden, **not** isolation shown.
- Do **not** chase Ze/Zo as a Soften-param vanity to push Rank1 over 5.
- Rank2 **54.19 dB** is the wrong object (textbook lumped cancel ≠ MuLCAT multi-layer). **Park** as an Amb path.
- Rank3 **6.24 dB** can pose an eq-circuit alternate. It is **fragile to detune**. **Formal DGS Hold** — **not** Amb clear, **not** PCB clearance, **not** Rank1 clearance.

Surrogate ≠ PCB. Peek succeed ≠ isolation shown.

---

## 3. Operator gate (authoritative)

**Soften Rank1 SURR_EO_COUPLED:** ΔS21=3.32 dB @ 2 GHz under smoke-class mild EO (Ze=70/Zo=36) — Soften band 3–5; locked Δ=5 bar **unmet**. No Soften-param vanity Ze/Zo chase.

**Rank2/3 Soften-carry peeks only** (do NOT Amb Harden / Rank1 clearance):
- SURR_NEUTRAL_DN Δ=54.19 — textbook lumped cancel; wrong object for MuLCAT multi-layer → Soften-peek / park as Amb path.
- SURR_DGS_EQ Δ=6.24 — meets bar on eq-circuit; fragile to detune → **Formal DGS Hold**; **not** Amb clear; not PCB/claim clearance.

**Locks:** provisional Δ=5 Soften stands (alt 10 held; **do not drop bar to 3.32**); surrogate-first Soften; **Lab HOLD invent**; further surrogate invent parked; Formal DGS Hold (not Amb clear); full-wave parked; HFSS Hard NO; AI optimizer later; Greer HOLD; write-up hold-send; BIA CLOSED; cell-tower PARKED. Surrogate ≠ PCB. Peek succeed ≠ isolation shown. Reopen later **only** for openEMS / toolchain or user override.

**Honesty locks**

- Provisional **Δ = 5 dB** Soften **stands**. **Do not drop the bar to 3.32.** Alternate Harden **Δ = 10** held.
- Live path = **surrogate-first**. **Lab HOLD invent.** Further surrogate invent **PARKED**. Full-wave stays **PARKED**. **HFSS Hard NO.**
- **Formal DGS Hold** — **not** Amb clear.
- AI / design-optimizer claims stay a **later wave**.
- US12,719,158 B2 / SkyMirr MuLCAT = bibliographic prior art only. **No claim-language copy.**
- Surrogate ≠ PCB.
- Peek succeed ≠ isolation shown.
- This is **not** claim clearance.
- This is **not** skill-met.
- This is **not** commercial clearance.

---

## 4. Hard NO

- Do **not** treat **3.32 dB** as isolation shown, as PCB isolation, as bar-met, or as a new **Δ**.
- Do **not** drop locked **Δ = 5** to Rank1 **3.32**.
- Do **not** vanity-chase Ze/Zo until Rank1 crosses 5.
- Do **not** treat Formal DGS Hold as Amb clear.
- Do **not** invent further surrogate classes while **Lab HOLD invent** is in force (reopen later only for openEMS / toolchain or user override).
- Do **not** Amb Harden or Rank1-clear from Rank2 **SURR_NEUTRAL_DN** (wrong object) or Rank3 **SURR_DGS_EQ** (eq-circuit; fragile; not PCB).
- Do **not** vanity-freeze bibliographic ~12 dB as **Δ**.
- Do **not** unpark full-wave / 3D fine-mesh.
- Do **not** require or run commercial HFSS.
- Do **not** invent antenna / coupling-structure models as a product embodiment.
- Do **not** train a fingerprint / ML / design-optimizer model.
- Do **not** copy US12,719,158 B2 claim language.
- Do **not** commit Lab scratch / hunt scripts as established.
- Do **not** write skill-met / commercial-clearance / elevated language.
- Do **not** reopen Greer sync-locate invent (`2026-09_greer-sync-pulse-tdoa`), including draft REOPEN #68.
- Do **not** send or rewrite the Greer-facing write-up (stays **hold-send**).
- Do **not** reopen `2026-09_cell-tower-geometry` as live.
- Do **not** reopen the BIA→weight portfolio.

---

*Docs only. Soften Rank1 ≠ bar-met. Soften ≠ isolation shown. Surrogate ≠ PCB. Peek succeed ≠ isolation shown. Locked Δ = 5 unmet. Not a product. Not skill-met. Not commercial clearance. Not a patent-product claim. Not rithm. Lab does not self-admit. Lab scratch was not on this VM; summary copied from the Operator gate. No invent scripts this fold.*
