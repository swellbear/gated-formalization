# Operator Soften-fold habit (Method Operator)

A short working habit. It does not change how claims are scored. It does **not** change the Material Admission Check, Amb scoring, or Soften Critic hire.

## The habit

After the Operator Soften / Harden / Kill **ADMIT**s a Lab board, fold that admit into docs **this way**. Four standing rules.

### A. One Soften-fold lane (no parallel Soften PRs)

For a given Amb, launch **at most one** Soften docs fold cloud agent / PR at a time.

- Do **not** open N Soften day/pulse PRs in parallel for the same Amb.
- The next Soften fold launches only after the prior Soften PR is **CLEAN + squash-merged** (or closed).
- Lab may still invent the next board while a fold lands. The Operator may Soften-admit that board in chat. **Queue** the docs fold until the lane is free.
- **Exception:** a tiny VIZ-pointer-only amend to an already-merged Soften may ride as its own short PR **only if** it does not rewrite `STATUS.md` as “this fold.” Prefer amending the in-flight Soften PR before merge.

### B. Operator-owned STATUS stamp

Each Amb keeps a short **Operator STATUS stamp** (file or section). Soften folds **point to** it. They do **not** re-author it as the canonical “where am I?”

Soften digests may update Softened-set bullets and DIGESTION pointers. They must **not** rewrite the stamp’s authoritative lines as if this Soften PR alone owns corpus-complete / park DIGEST state.

Minimum stamp fields:

- Softened set (IDs / days)
- Digestor park DIGEST: `none` | `interim` | `ADMITTED` + PR#
- Amb: `OPEN` | `TABLE` | `hard-stop`
- Hold C2/C4 (or Amb equivalents)
- Parent usefulness Softened? Y/N
- Success bar set? Y/N
- Soften Critic hired? Y/N
- Operator idle until Founder GO? Y/N

Fill-in stub: [`templates/OPERATOR_STATUS_STAMP.md`](../templates/OPERATOR_STATUS_STAMP.md).

### C. Founder done / idle handshake

When park DIGEST is **ADMITTED + MERGED** and available Soften folds for the live set are on master, the Operator sends the Founder **one** done line, then goes **idle**.

- Do **not** re-reply park STATUS to repeat Founder/Lab pings that only restate the same facts.
- Further Operator action on that Amb requires Founder/user **GO** (C2/C4, TABLE, reopen, Soften Critic hire, or conflict).
- Digestor/Lab must treat master `OPERATOR_STATUS_STAMP.md` (or the STATUS pointer to it) as **authoritative** for park-DIGEST-complete questions. Do **not** re-ask the Operator for a second admit of an already-merged park DIGEST.

### D. Soften-PR pre-merge honesty checklist

Every Soften docs PR must include this checklist in DIGESTION or the PR body (thin; Soften Critic is still **not** hired):

- [ ] media≠certified (or Amb SOURCE honesty)
- [ ] day≠certified / closings≠evidence as applicable
- [ ] no elevate / skill-met / productize language
- [ ] parent usefulness / verdict **NOT** Softened this fold
- [ ] Hold C2/C4 (or Amb holds) unless Founder GO
- [ ] Digestor never Soften/Harden/Kill; `lab_admits=false`
- [ ] Soften Critic not hired (unless Founder hired)
- [ ] Operator STATUS stamp pointed/updated correctly (not rewritten as sole owner of park DIGEST)

Short template: [`templates/SOFTEN_PR_HONESTY_CHECKLIST.md`](../templates/SOFTEN_PR_HONESTY_CHECKLIST.md).

## Why

Parallel Soften PRs rewrite the same STATUS as if each fold owns the whole Amb. A stamp the folds point to, one lane, one idle handshake, and a thin checklist keep the record honest without hiring a Soften Critic.

## What this does not do

- Does **not** change the Material Admission Check or Amb scoring.
- Does **not** hire a Soften Critic.
- Does **not** Soften parent usefulness or verdict.
- Does **not** auto-GO C2/C4 (or Amb equivalents).
- Does **not** authorize elevate / skill-met / productize language.
- Does **not** let Digestor or Lab Soften / Harden / Kill.

## Related

When you switch to a **brand-new claim**, write up what the last string taught you first: [`docs/DIGESTION_HABIT.md`](DIGESTION_HABIT.md).

**Related — Digestor living spine / index:** Digestor keeps a living spine/index board per Amb (`LIVING_SPINE_INDEX.md`). Write a true `DIGESTION_PARK_WHAT_TAUGHT.md` only after Operator **LAST-live ADMIT** or **TABLE**. Authority order: Operator ADMIT chat → master `STATUS.md` / `OPERATOR_STATUS_STAMP.md` → Founder/Lab paraphrase. Digestor never Soften / Harden / Kill. Habit: [`docs/DIGESTOR_LIVING_SPINE_INDEX_HABIT.md`](DIGESTOR_LIVING_SPINE_INDEX_HABIT.md). Template: [`templates/LIVING_SPINE_INDEX_TEMPLATE.md`](../templates/LIVING_SPINE_INDEX_TEMPLATE.md).
