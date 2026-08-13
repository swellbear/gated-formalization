# Probability-object pilot — design (not standing rule)

**Status:** Brainstorming / pilot only. **Not** canonical method. **Not** a standing-rule change. Does **not** alter Amb weights, thresholds, clearance, lock semantics, or any application folder.

This note records a **Version 2 router**: classify the constraint state, then say which probability-*object* would be legal. This dry-run **emits no percents, odds, or ranges**. Success is **legal when, silent when not, killed if a number becomes the headline** — not “optimal confidence.”

Current best guesses, not gospel.

---

## What this is for

The method already answers:

- How unset the question still is (**Amb**)
- Whether a **locked bar** is **established / not established / refuted** (the **triad**)
- Gate verdict (**Admissible / Provisional / Not admissible**)
- **Reliability of this scoring pass** (high / medium / low)

A “probability of the slogan” is a **different** object. This pilot only asks: *when would any numeric credence even be legal?* If not legal, the honest extra is **nothing**.

---

## One-question test

**All** of the following must pass. Any fail → this instance is **not** one question → **no slogan-P** (no numeric credence on the original slogan or on “the claim as a blob”).

1. **One ordinary sentence.** You can say the instance in one sentence: object, time, place, what would count as yes.
2. **Not a mixed blob.** If the claim is mixed, split it. A number may attach only to a **descriptive** piece that itself passes this test — never to the unsplit slogan.
3. **Bar height locked when strength-words carry the claim.** If could / likely / should / potential / live-shot (or close analogues) do real work, **how strong you mean** is already locked (P-Logical / P-NonNegligible / P-BaseCase, or an explicit numerical bar). That lock is a **bar height**, not a credence.
4. **No live rival reading inside the yes.** This-Saturday vs every-Saturday, this branch vs all branches, census vs expected-path, etc. must be resolved or the unused reading parked **outside** this instance.
5. **Leftovers locked or parked outside.** Remaining free parameters are either frozen or explicitly **not part of what would count as yes** for this instance (park-until-trigger / out of package / unnamed class left unnamed and therefore **blocking**, which is a **fail**, not a pass).

If the test fails, stop. Use Amb, leftovers, triad, and verdict. Do not invent a percent that averages several questions.

---

## Legal-object table (inspectable router)

Apply **after** the one-question test. First matching row wins. Still **no numbers in this dry-run**.

| Run state | Legal object | Not allowed |
|-----------|--------------|-------------|
| Meaning still moves (one-question test fail) | **Silent.** Constraint state + leftovers only. | Any slogan percent |
| Locked bar, triad = **established** | **Triad-only.** The bar is met. | A high percent as a gold star |
| Locked bar, triad = **refuted** | **Triad-only.** | A cute low percent |
| Locked bar, triad = **not established** | **Triad-only** is the headline. A number is legal **only** if it answers a **different named question** (see next-print row). | “We’re 40% of the way to established”; untagged credence on the unmet bar |
| Named future print / named series, parked until it exists | **Next-print-only** (legal *later*, still not emitted now). Must name the print. | Using today’s stand-in ¢ or kinship print as that number |
| One-question **pass**, descriptive, **no** locked modal/numerical bar | **Instance-range-would-be-legal-later** (still not emitted in this dry-run). | Treating that future range as slogan-true |
| Normative / should / preferability / uniqueness elevation | **N/A-normative** for slogan-P. Split off any descriptive core and route that core separately. | A percent on “should” |
| Live vs stand-in / conflicted source | Any later number must be **tagged**. | Untagged percent |
| Low Amb + unmet bar (`Amb ≠ clearance`) | Triad **not established** stays primary. | A percent that reads as “the question is clear, so it’s probably true” |

**Never compute:** Amb weighted sum → percent. Severity weights rank leftovers; they are not likelihood ratios.

---

## Naming (do not collide)

- **P-Logical / P-NonNegligible / P-BaseCase** = **how strong you mean** (bar height). Never “the probability.”
- If a credence were ever shown, **do not prefix it with `P-`.** Put the locked height next to it in words: “We *mean* a real shot. That bar is **not established**. This number is not that bar.”
- A number must **never** upgrade merely-possible into expected-path.
- **Reliability of this scoring pass** stays **high / medium / low** plus why: one question or not; evidence thin / stand-in / conflicted or not; single pass or not. **No second 0–100.** Show it **before** any future percent.

---

## Kill tests

Withdraw the feature (or never ship) if:

- Cold readers treat a number as **the original slogan is true** and drop the leftover list.
- Amb, locks, or hard stops start moving **to make room** for a percent.
- Established / not established / refuted is replaced by a percent.
- Conflicted ¢ or print-match are laundered into a credence.

---

## If it ever ships (step 3 — not this pass)

Optional closeout mode, QI-shaped: operator asks, **default off**, does not write Amb / locks / verdicts. **Not** folded into QI (QI = numerical implication after a failed numerical instance bar). In-chat picker may offer **“no number” / “run the optional instance-credence mode”** — never a menu of percents.

**Step 4 (later):** calibration only after some legal instances **resolve in the world**, with a tiny resolution log and a scoring rule. Not before.

**Step 5 (permanent aim):** legal when, silent when not, killed if it becomes the headline. Not “optimal confidence.”

---

## This pass

Dry-run: [`PROBABILITY_OBJECT_DRY_RUN.md`](PROBABILITY_OBJECT_DRY_RUN.md). Ten sealed apps. Legal yes/no only. Then **stop for discussion**.
