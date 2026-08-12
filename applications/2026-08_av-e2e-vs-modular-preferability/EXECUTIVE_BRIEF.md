# Executive Brief (≤1 page)

**Default share artifact.** Full audit trail: `DISSERTATION.md`.  
**Glossary:** [`docs/READER_GLOSSARY.md`](../../docs/READER_GLOSSARY.md)

**Application:** `2026-08_av-e2e-vs-modular-preferability`  
**Date:** 2026-08-12  

---

## Claim

End-to-end neural nets are preferable to modular (perception–planning–control) stacks for self-driving cars because they alone avoid cascading errors from hand-built interfaces, and they can keep improving with data and scale in a way modular stacks structurally cannot.

---

## Plain verdict

The strong package **does not hold**. Architecture choice is a **spectrum** (modular / hybrid / more end-to-end), not a clean either/or. Modular stacks **can** learn from data — the “structurally cannot improve” line is **false as stated**. End-to-end is **not** uniquely free of cascading-style problems, and avoiding hand-built interfaces does **not** eliminate error cascades. Unrestricted “E2E is preferable” is **not established**. Under one agreed comparison lock, some technical questions are well-posed but still need matching evidence.

---

## Established

- Comparison is a spectrum, not an exclusive binary.  
- Preferability depends on multiple criteria — not a single automatic win.  
- Interface-composition errors vs end-to-end compounding/shift errors are different kinds of problems.  
- Joint learning across hard module cuts is a weak design-asymmetry / mechanism candidate only.  
- Under one strong comparison lock: certain scoped technical questions are well-posed; empirical closure still needs package-matching evidence.  

---

## Not established

- Modular stacks **structurally cannot** improve with data/scale — **refuted**.  
- End-to-end **alone** avoids cascading-interface problems — uniqueness fails.  
- Avoiding hand-engineered interfaces **eliminates** cascading errors — **refuted**.  
- Unrestricted preferability of end-to-end over modular.  
- Empirical closure of the locked technical questions (still open).  

---

## Action implications

**Stop saying:** End-to-end is preferable because it alone avoids cascading interface errors; modular stacks structurally cannot improve with data/scale; that locking a comparison or “getting clearer” clears the original slogan.

**Keep saying:** Architecture choice is a spectrum; modular stacks can learn from data; cascading-interface vs end-to-end compounding/shift errors are different problems; under the agreed lock, the technical questions are well-posed but empirically open.

**Test next (only if authorized):** Matching evidence under the agreed lock after settling remaining either/or choices; or a different lock / revised claim.

**Residual-branch menu:** Offered (`RESIDUAL_BRANCH_MENU.md`) — R-EVID needs OR-slots first. **No branch authorized.**

---

## For the record (technical)

| Item | Value |
|------|--------|
| Method verdict | Stable Provisional — original not well-constrained |
| Amb | ≈ 4 |
| Locks / proxy IDs | R4 = P-Strong-Both; OR-slots unpaid; R1/R2 evidence open |
| Scope label | Scoped technical well-posedness; unrestricted slogan fail |

---

## Full write-up

→ [`DISSERTATION.md`](DISSERTATION.md)

---

*Mandatory at closeout. Plain verdict first; method labels secondary. No silent softening.*
