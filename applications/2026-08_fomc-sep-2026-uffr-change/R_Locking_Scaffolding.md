# Locking Scaffolding — Dominant Blocker Choice Set

**Operator selection (2026-08-12):** **Rank 3** + URL, then **`live shots`** = **M3**, then **`leave unnamed`**, then **`closeout`**. Hard stop sealed. `Lock_Rank3_Q3O2L1M3B1.md`. `Phase1_Endpoint_Readout.md`. `SHARE_PACK.md`.

**Date:** 2026-08-12  
**Application:** `2026-08_fomc-sep-2026-uffr-change`  
**Dominant blocker ID(s):** **G1** speech act · **G2** displayed options / venue · **G4** live vs stand-in · **G5** forecast wait  
**Dependents blocked:** D-RULES census; F-PRINT; any odds pulse; named-class pulse

**Explicit dependency statement:**  
Until we lock whether this is a **contract census**, a **September print forecast**, or an **odds** claim — and what to do about missing brackets — there is no well-posed proposition to admit or refute. June SEP conclusions do **not** transfer.

**Original claim (verbatim, for deviation comparison):**  
The pasted market rules (upper-bound change vs pre-September 2026 meeting; FOMC statement Sep 15–16 2026; round up to 25; fallback No change).

---

## 0. Plain-language framing

**What decision is being made right now:**  
What we are actually testing: the **rules**, the **September rate-change print**, or a **market price**.

**Why this decision is required:**  
Without that, “yes” can mean “the contract says that,” “they will cut 25,” or “the market implies a cut.” Those are different questions. The paste also never lists the **displayed brackets** or the **market page**.

**What becomes testable once the decision is made:**  
Either a census of the rules as written, and/or a later read of the September FOMC statement’s upper-bound change.

**What still cannot be settled by this decision alone:**  
That the FOMC **will** cut, hike, or hold; that any market price is the expected path; June SEP medians. **Lock ≠ clearance.**

---

## 1. Decision points

| Point ID | Question (plain language) |
|----------|---------------------------|
| **Q** (G1) | Are we scoring the **contract**, the **September print**, or **odds**? |
| **O** (G2) | What do we do about missing displayed options / venue? |
| **L** (G4) | What is the live source for the print? |
| **M** (G5) | If we forecast now, how strong is the claim? |
| **B** (G3) | What is “prior to the September meeting”? |

---

## 2. Options per decision point

### Point Q — Speech act
| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| **Q1 Census-rules** | Test only what the pasted rules **say** | Contract as intake |
| **Q2 Forecast-print** | Test what the Sep 15–16 **statement** will print as upper-bound **change** | Market’s own resolution object |
| **Q3 Odds** | Use a named market’s **published price** as a modal bar for that same event | Odds fork; needs named venue + matching event |

### Point O — Displayed options
| Option ID | What it means | Provenance |
|-----------|----------------|------------|
| **O1 Unset** | Record rounding schema; do not invent brackets | Honest to the paste |
| **O2 Operator-supply** | You paste the option list / market URL | Completes the contract |
| **O3 Invent-typical** | Assume ±0 / 25 / 50 … | **Disallowed** (invented class) |

### Point L — Live source
| Option ID | What it means | Provenance |
|-----------|----------------|------------|
| **L1 Statement** | FOMC statement after Sep 15–16 2026 meeting | Named in the paste |
| **L2 Openmarket** | Fed openmarket.htm as live | Named as also-published |
| **L3 Either-accepted** | Statement **or** openmarket if they agree; conflict → HOLD | Formal either |
| **L4 This-paste** | The rules text as proof of the print | Circular / stand-in |

### Point M — Forecast bar (only if Q2 or Q3)
| Option ID | What it means | Provenance |
|-----------|----------------|------------|
| **M1 Park-until-print** | Do not claim a bracket now; wait for the statement | Data not yet existent |
| **M2 P-BaseCase** | A named series’ central path **is** the expected change | Needs named class; not June SEP brochure |
| **M3 P-NonNegligible** | A named series shows a live shot at a named bracket | Weaker; still needs named class |
| **M4 P-Logical** | Some rounded 25 bp move is possible | Near-vacuous |

### Point B — Baseline
| Option ID | What it means | Provenance |
|-----------|----------------|------------|
| **B1 Pre-meeting in-force** | Upper bound in force immediately before the Sep meeting | Ordinary “prior to” |
| **B2 Last-statement-only** | Only the previous FOMC **statement**’s range | Narrower |

**Incoherent / weak:** O3; L4 as live for F-PRINT; Q3 without a named market URL; M2 using June SEP Table 1 (different object; funds-rate was **off** that bar); M4+open horizon.

---

## 3–5. Ranked packages

### Rank 1 — **Rules census + wait for the statement** (`Q1+O1+L1+M1+B1`)

**What this package concretely means:**  
Score the pasted **rules** as a contract (upper-bound **change**, 25 bp round-up schema, Sep statement as source, fallback No change). Do **not** pick a winning bracket. The actual September print waits until that statement exists.

**If chosen, the next phase can check:**  
Whether the contract text is internally well-posed under those freezes (D-RULES). F-PRINT parks until the Sep 15–16 2026 statement.

**It still cannot settle:** Who wins the market; that a cut is likely; June SEP path.

**Relevance warning:** Partial if you wanted a **prediction** now — this package refuses to invent one.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** “Will resolve to the change” kept as **contract**, not as a filled-in bps number.  
2. **Problem-identity check:** Same market object.  
3. **Scope / baseline / metric shift:** Adds wait-for-print; leaves displayed options unset.  
4. **Deviation summary:** **Minimal deviation** (intake is the rules)

---

### Rank 2 — **Forecast the print, still wait** (`Q2+O1+L1+M1+B1`)

**What this package concretely means:**  
The claim under test **is** the September upper-bound **change** (mapped to 25 bp brackets). We still **do not** guess a number today. After the statement, we read the change vs the pre-meeting upper bound.

**If chosen, the next phase can check:**  
Nothing until the statement (or fallback clock). Then a named-class pulse on the locked live statement.

**It still cannot settle:** Odds; a named bracket as P-BaseCase today.

**Relevance warning:** Stronger as a **prediction market object**; still no winner now.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** “Will resolve to the change” read as a **future print**, not a filled bracket.  
2. **Problem-identity check:** Same event.  
3. **Scope / baseline / metric shift:** Elevates F-PRINT over D-RULES.  
4. **Deviation summary:** **Minimal deviation** relative to a market whose object **is** that print

---

### Rank 3 — **Odds on a named market** (`Q3+O2+L1+M2 or M3+B1`)

**What this package concretely means:**  
You supply the **market URL and displayed options**. We freeze that venue’s **published price** (named central statistic) as a modal bar for the **same** upper-bound-change event.

**If chosen, the next phase can check:**  
Whether that price meets the locked bar — **not** whether the FOMC will actually print that change (different leftover). Conflicted-source: the market is interest-aligned with trading.

**It still cannot settle:** The September print itself; June SEP.

**Relevance warning:** Needs **O2**. Without a URL this package is incomplete. Print-match of price to a forecast ≠ the statement.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** Adds “likely/odds” not in the paste.  
2. **Problem-identity check:** Same event **if** the named market matches; else substitution.  
3. **Scope / baseline / metric shift:** Price ≠ print.  
4. **Deviation summary:** **Moderate deviation** (odds fork)

---

## 6. Choice prompt

**Resolved (2026-08-12):** Rank 3 + M3 + **`leave unnamed`** + **`closeout`**. Hard stop sealed. See `SHARE_PACK.md`.

- **What we’re doing:** The file is closed.  
- **What we need from you:** Nothing required. Optional: `run UX` / `run CX` / `run CR` / later `name source class C2: …`.  
- **What a “yes” means:** Independent live-shot affirmation stays not established.  
- **What this does *not* mean:** That a hike or hold is a live shot. **33¢ is not P-NonNegligible met.** Leave-unnamed ≠ unlikely. **Low Amb ≠ clearance.**

```
Package: ________

OR à-la-carte:
- Point Q = Option __
- Point O = Option __
- Point L = Option __
- Point M = Option __
- Point B = Option __

OR-slots:
  - [ ] Pick single: ____
  - [ ] Formally accept either: { ____ , ____ }
```

**Details:** Rank 1 = `Q1+O1+L1+M1+B1` · Rank 2 = `Q2+O1+L1+M1+B1` · Rank 3 = `Q3+O2+L1+M2/M3+B1` (incomplete without URL)

**Recommended (not locked):** Rank 1 if you want the **rules** well-posed; Rank 2 if you want the **September print** as the claim but still wait. Do **not** pick Rank 3 until you name the market.

**Dependents re-open only after selection + OR-slot resolution.**

**Lock-time Amb warning:** Selecting a package **drops Amb by fixing meanings**. That does **not** establish a cut, hike, or hold.

---

## 7. Forced-deviation extraction

**Condition met?** Every realistic package is Moderate+ (no Minimal): **No**

Ranks 1 and 2 are **Minimal deviation** relative to the paste as rules / as print-object. Rank 3 is Moderate. No forced-deviation extraction.

---

*Domain-general template. See `.cursor/rules/applications-gated-method.mdc`.*
