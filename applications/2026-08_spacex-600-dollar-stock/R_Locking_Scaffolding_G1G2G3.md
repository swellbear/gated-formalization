# Locking Scaffolding — G1 / G2 / G3 Choice Set

**Date:** 2026-08-11  
**Application:** `2026-08_spacex-600-dollar-stock`  
**Dominant blocker ID(s):** **G1** (modal bar), **G2** (share count), **G3** (horizon)  
**Dependents blocked:** **G4** (path to equity value ≈ $600 × shares) — G2-dependent; difficulty scales with G1×G3  

**Explicit dependency statement:**  
G4 is currently blocked primarily by the unset status of G2 (required equity value = $600 × share count). G1 and G3 further determine how hard G4 is (tighter “potential” bar and shorter horizon raise the burden). Reverse-split-only paths remain **excluded by default** (L1e) unless the operator widens G5.

**Original claim (verbatim, for deviation comparison):**  
“SpaceX has potential to become a $600 stock.”

**Carry-forward defaults (already admitted, not re-opened unless operator overrides):**  
- G5 = reverse-split-only **excluded** (L1e)  
- G6 = SPCX Class A / continuous successor unless corporate action  

---

## 0. Plain-language framing (required)

**What decision is being made right now:**  
Choosing what “potential,” which **share count**, and which **time window** mean for the $600 claim — so “$600 stock” becomes a definite equity-value target we can test.

**Why this decision is required before further work:**  
Without those locks, any story about Starlink, Starship, or AI can be waved at $600 without knowing whether we mean ~$8T of firm value, a cosmetic reverse split, “someday maybe,” or “likely within five years.”

**What becomes testable once the decision is made:**  
Whether there is a coherent business/market path (G4) to **EquityValue ≈ $600 × locked shares** inside the locked horizon, under the locked “potential” bar.

**What still cannot be settled by this decision alone:**  
That SpaceX *will* hit $600; that it is a buy; fair value today; or the parent-style investment recommendation. Locking only makes the upside claim **well-posed**.

---

## 1. Decision points

| Point ID | Question (plain language) |
|----------|---------------------------|
| **M** (G1) | How strong is “potential”? |
| **S** (G2) | Which share count turns $600 into a company-value target? |
| **H** (G3) | By when must the $600 print count? |
| **X** (G5) | Do reverse-split-only paths count? *(default already No)* |

---

## 2. Options per decision point

### Point M — “Potential” bar
| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| **M1 P-Logical** | Not ruled out; a path exists on paper | Weak modal reading of “potential” |
| **M2 P-NonNegligible** | A live upside path with real (non-vanishing) chance — not a base case, not a joke | Ordinary investor/analyst use of “has potential” |
| **M3 P-BaseCase** | Central / expected path reaches $600 in the window | Forecast-strength reading (stronger than the bare wording) |

### Point S — Share count
| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| **S1 IPO-scale freeze** | Use share base consistent with IPO math ($135 ↔ ~$1.77T ⇒ ~**13.1B** shares). Then $600 ⇒ ~**$7.9T** equity value | L1f working package; prospectus/IPO pricing identity |
| **S2 Horizon fully diluted** | Same idea, but count shares expected outstanding at the horizon (dilution, issuance, conversions). $600 target **rises** with dilution | Standard fully-diluted discipline |
| **S3 Rebase to market-cap slogan** | Drop per-share fixation; test “potential for ~$8T equity value” (or another named cap) | Cleaner economics; **leaves the $600 words** |

### Point H — Horizon
| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| **H1 5 years** | $600 by ~2031 | Near-term mega-cap test |
| **H2 10 years** | $600 by ~2036 | Long-cycle infrastructure / AI build |
| **H3 20 years** | $600 by ~2046 | Generational / Mars-optional narrative space |
| **H4 Open** | No deadline | Matches bare text; couples with M1 toward vacuity (L1g) |

### Point X — Reverse split
| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| **X1 Exclude** *(default)* | Cosmetic reverse split alone does **not** count | L1e |
| **X2 Include** | Any path to a $600 print counts | Trivializes claim |

**Incoherent / weak combos (do not package as top ranks):**  
M1+H4 (near-vacuous); S3 if operator wants to keep “$600 stock” as the literal claim without marking revision; X2 with any serious economic package.

---

## 3–5. Ranked packages (most → least powerful for resolving G4)

### Rank 1 — **P-NonNegligible / IPO-scale / 10y** (`M2+S1+H2+X1`)

**What this package concretely means:**  
Treat “potential” as a **real upside chance**, not a guarantee. Freeze shares at **IPO-scale** (~13.1B). Ask whether SpaceX can reach about **$8T** equity value with a **$600** print by ~**2036**, without counting reverse-split tricks.

**If chosen, the next phase can check:**  
Whether disclosed businesses + credible growth/multiple paths make ~$8T by 2036 a non-negligible scenario (or not).

**It still cannot settle (vs original claim):**  
That $600 *will* happen; that one should buy SPCX; open-ended “someday” stories outside 10 years.

**Relevance warning:** Partial — adds share count and horizon **not in the claim text**; this is what makes the slogan testable.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** “Potential” kept as non-negligible (not collapsed to “will”). “$600 stock” kept as per-share.  
2. **Problem-identity check:** Same claim family (SpaceX upside to a $600 print).  
3. **Scope / baseline / metric shift:** Adds IPO-scale share freeze and 10-year window.  
4. **Deviation summary:** **Moderate deviation**

---

### Rank 2 — **P-NonNegligible / fully-diluted-at-horizon / 10y** (`M2+S2+H2+X1`)

**What this package concretely means:**  
Same “real upside” bar and 10-year window, but the share count is whatever is **fully diluted by ~2036**. If SpaceX issues a lot of stock, hitting $600 gets **harder** (needs even larger firm value).

**If chosen, the next phase can check:**  
G4 under a dilution-aware equity-value target (must estimate or bound future share count).

**It still cannot settle:** Buy advice; certainty; sub-5-year path.

**Relevance warning:** Partial — more realistic, but “fully diluted at horizon” is extra machinery.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** “Potential” and “$600” kept; share path made stricter.  
2. **Problem-identity check:** Same family; anti-games dilution.  
3. **Scope / baseline / metric shift:** Future diluted shares not in text.  
4. **Deviation summary:** **Moderate deviation**

**OR-slot if selected:** must specify how future dilution is bounded (e.g. “≤ IPO-scale × 1.25” or “use street FD shares when available”).

---

### Rank 3 — **P-NonNegligible / IPO-scale / 5y** (`M2+S1+H1+X1`)

**What this package concretely means:**  
Real upside chance of ~**$8T** / $600 by ~**2031**. Much tougher compounding from today’s mega-cap starting point.

**If chosen, the next phase can check:**  
Near-term scenario plausibility; easier to falsify as non-negligible.

**It still cannot settle:** Longer-run potential outside five years (explicitly out of scope).

**Relevance warning:** Partial — short horizon is a strong add-on vs bare “potential.”

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** “Potential” kept; timing tightened hard.  
2. **Problem-identity check:** Same family, compressed.  
3. **Scope / baseline / metric shift:** 5-year cap not in text.  
4. **Deviation summary:** **Moderate deviation** (timing add-on is large)

---

### Rank 4 — **P-BaseCase / IPO-scale / 10y** (`M3+S1+H2+X1`)

**What this package concretely means:**  
Not just “has a shot” — the **central expected path** is that SPCX is about $600 by ~2036 (~$8T equity value).

**If chosen, the next phase can check:**  
Whether base-case forecasts / underwriter-style paths actually center near that outcome (likely severe Amb / Cons pressure).

**It still cannot settle:** That “potential” in the ordinary weak sense — this **strengthens** the claim.

**Relevance warning:** **Weak overlap with bare wording** — “potential” is weaker than “expected to.” Risk of testing a stronger claim than written.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** “Potential” **strengthened** to base-case forecast.  
2. **Problem-identity check:** Same topic; **over-strong** vs text.  
3. **Scope / baseline / metric shift:** Share freeze + 10y + forecast bar.  
4. **Deviation summary:** **Substantial deviation**

---

### Rank 5 — **P-Logical / IPO-scale / open horizon** (`M1+S1+H4+X1`)

**What this package concretely means:**  
Only ask whether ~$8T / $600 is **not ruled out** someday. Closest to the bare words; least useful.

**If chosen, the next phase can check:**  
Almost nothing decisive — hard to falsify; L1g vacuity applies.

**It still cannot settle:** Whether the claim is interesting or action-guiding.

**Relevance warning:** **Partial / weak as a test** — preserves words, sacrifices bite.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** “Potential” kept weak; no horizon added.  
2. **Problem-identity check:** Same words; economically thin.  
3. **Scope / baseline / metric shift:** Still adds IPO-scale share freeze.  
4. **Deviation summary:** **Moderate deviation** (share freeze) / **low practical power**

---

## 6. Choice prompt

Pick **one** package by name, **or** list à-la-carte option IDs.

```
Package: Rank 1 / P-NonNegligible / IPO-scale / 10y (M2+S1+H2+X1)

OR-slots: none — complete singleton lock
```

**Status:** **SELECTED** — Rank 1. Lock record: `Lock_Rank1_M2S1H2X1.md`. G4 re-opened under **Under Rank 1 (M2+S1+H2+X1) only.**

---

## 7. Forced-deviation extraction

**Condition met?** Every package that usefully unblocks G4 is **Moderate** or higher on the original wording (no **Minimal deviation** package that both stays faithful *and* makes G4 well-posed): **Yes**

1. **Extracted terms/clauses that force deviation:**  
   - bare **“potential”** (no modal bar)  
   - bare **“$600 stock”** (no share count / capital-structure lock)  
   - missing **time horizon**
2. **Record as under-specified in the claim as written:** FD-M1 “potential”; FD-S1 “$600 stock” as per-share without shares; FD-H1 silent horizon.  
3. **Carry forward IDs:** **FD-M1**, **FD-S1**, **FD-H1** into claim-freeze / agenda / any later Original-Claim Assessment.  
4. **Closeout note (draft):** These terms could not be tested in non-derivative form without adding locks; that is a property of the claim text relative to valuation tools, not merely temporary lack of data.
