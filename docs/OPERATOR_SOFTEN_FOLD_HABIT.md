# Operator Soften-fold habit (Method Operator)

A short working habit. It does not change how claims are scored. It does **not** change the Material Admission Check, Amb scoring, or Soften Critic hire.

## The habit

After the Operator Soften / Harden / Kill **ADMIT**s a Lab board, fold that admit into docs **this way**. Eight standing rules (A–D original; E–H 2026-09-07 after golf WC idle-breach + docs-fold latency).

### A. One Soften-fold lane (no parallel Soften PRs)

For a given Amb, launch **at most one** Soften docs fold cloud agent / PR at a time.

- Do **not** open N Soften day/pulse PRs in parallel for the same Amb. The lane stays **one-at-a-time** so the Illustrator Softened index does **not** race parallel Soften PRs.
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
- Rejected/PARKED (not Softened)
- HOLD Soften (only if Founder call open)
- Docs fold PR#
- Master Softened SoT path
- Box-lab Softened SoT path (mid-run write-back; list both paths)
- Edge Softened/established? (default **N** for ops tracks)

Fill-in stub: [`templates/OPERATOR_STATUS_STAMP.md`](../templates/OPERATOR_STATUS_STAMP.md). State vocab / idle / admit-pass: [`docs/operator_ops/README.md`](operator_ops/README.md).

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

### E. State vocabulary

Use these stamps. Do **not** invent a fifth live state.

| Stamp | Meaning |
|-------|---------|
| **ADMITTED** | Operator Soften / Harden / Kill / dated-record admit is on the record. |
| **REJECTED** | Founder (or Operator under idle) rejected the board. **Not Softened.** |
| **PARKED** | Board is parked (often with REJECTED). **Not Softened.** |
| **HOLD Soften** | Founder GO vs reject is still **open**. Temporary only. |

Rules:

- **HOLD Soften** only while the Founder GO vs reject call is open.
- After Founder **reject**, the stamp says **REJECTED/PARKED** — never **HOLD Soften** pending GO.
- Lab waiting Soften on a **REJECTED** board is an Operator **hard-stop**. Do not leave the Lab queued on a rejected board.

Short table: [`templates/OPERATOR_STATE_VOCAB.md`](../templates/OPERATOR_STATE_VOCAB.md). Full text: [`docs/operator_ops/STATE_VOCAB.md`](operator_ops/STATE_VOCAB.md).

### F. Idle latch

When idle is **ON**:

- `SOFTENED_SET.md` **and** the Operator STATUS stamp both say **Idle ON** plus the **reject rule** (new Lab PROPOSED under idle = idle-breach REJECT, not Softened).
- Any new Lab **PROPOSED** under idle → **REJECT as idle-breach** (**not Softened**).
- **Soften Hard NO** under idle. Do not Soften the breach board to “clear the chatter.”
- Clear idle **only** on a fresh Founder **GO** that **names the next invent** (example: WC3+ on a **new settled week**). Restating park facts is not a GO.

Golf WC2 (2026-09-07) was this latch: second weekly invent without fresh Founder GO = idle-breach. CONFLICT cleared by parking the PROPOSED board, not by Softening WC2.

Short list: [`templates/OPERATOR_IDLE_LATCH.md`](../templates/OPERATOR_IDLE_LATCH.md). Full text: [`docs/operator_ops/IDLE_LATCH.md`](operator_ops/IDLE_LATCH.md).

### G. Docs-fold latency

On a dated-record **ADMIT**, write the Softened SoT **then** launch the docs fold in the **same pass**. Do **not** wait for a second Founder ping.

- Same-pass order: Softened SoT write → stamp + `SOFTENED_SET.md` → docs-fold PR.
- Auto-merge docs-only **CLEAN**: mark the PR ready if it is still draft, then **squash-merge**.
- Section A still holds: one Soften-fold lane. If a prior fold is in flight, **queue** this fold — but do not wait for a new Founder ping to *start* the queue.

Full text: [`docs/operator_ops/DOCS_FOLD_LATENCY.md`](operator_ops/DOCS_FOLD_LATENCY.md). Admit-pass: [`templates/OPERATOR_ADMIT_PASS_CHECKLIST.md`](../templates/OPERATOR_ADMIT_PASS_CHECKLIST.md).

### H. Ops-beside-method (golf / Kalshi)

Ops tracks (golf weekly claims, Kalshi Micro / 15-min researcher, and kin) are **dated records only**.

Hard NO:

- banked-edge / “edge established”
- invent finishes (or invent settles)
- demo-as-edge / Kalshi-demo fills as settles
- cash deposit-withdraw scopes

Dual Softened path (list **both** on the stamp):

- **Box-lab twin** — mid-run write-back so Lab invent carry is not chat-only.
- **Master path** — after the docs fold lands; this is post-fold authority.

Kalshi Micro / 15-min researcher **never self-admits**. Softened admits stay **Operator-owned** (`lab_admits=false`). Soften Critic stays **deferred** (not hired).

**Edge Softened/established?** defaults to **N** on ops tracks.

Full text: [`docs/operator_ops/OPS_BESIDE_METHOD.md`](operator_ops/OPS_BESIDE_METHOD.md).

### Softened-set ledger (required)

On every Soften / Kill / park DIGEST ADMIT, the Operator updates the Amb’s `SOFTENED_SET.md` (**not** chat-only). Lab reads Softened carry from that file at invent start **and** before finalize.

Template: [`templates/SOFTENED_SET_TEMPLATE.md`](../templates/SOFTENED_SET_TEMPLATE.md).

Do **not** rely on chat Softened lists for Lab invent carry.

### Illustrator Softened-state hygiene (Founder lock)

- The **Soften-fold** is the authoritative Softened state for living viz + suite. Illustrator does **not** invent Softened state.
- Illustrator keeps the Amb `viz/softened_index.json` updated **from Soften-folds**.
- On park DIGEST ADMIT, the Operator pings Illustrator with the path **or** updates `viz/PARK_DIGEST_PATH.md`.
- Lab Soften-flip races are a **no-op** if the index is already Softened.
- Soften-fold lane stays **one-at-a-time** (section A) so the Illustrator index does **not** race parallel Soften PRs.

This does **not** hire a Soften Critic. It does **not** Soften usefulness / verdict. It does **not** authorize elevate / skill-met.

## Why

Parallel Soften PRs rewrite the same STATUS as if each fold owns the whole Amb. A stamp the folds point to, one lane, one idle handshake, and a thin checklist keep the record honest without hiring a Soften Critic.

Golf WC1/WC2 (2026-09-07) added four more standing rules: named state vocabulary so REJECTED is not left as HOLD Soften; an idle latch that rejects new invent as idle-breach; same-pass docs fold so dated-record ADMIT is not chat-only until a second ping; and ops-beside-method Hard NOs so a dated FAIL cannot be read as banked edge.

## What this does not do

- Does **not** change the Material Admission Check or Amb scoring.
- Does **not** hire a Soften Critic.
- Does **not** Soften parent usefulness or verdict.
- Does **not** auto-GO C2/C4 (or Amb equivalents).
- Does **not** authorize elevate / skill-met / productize language.
- Does **not** let Digestor or Lab Soften / Harden / Kill.
- Does **not** treat REJECTED/PARKED as HOLD Soften pending GO.
- Does **not** Soften under idle, or clear idle without a Founder GO that names the next invent.
- Does **not** bank edge, invent finishes, treat demo as edge, or open cash deposit-withdraw scopes on ops tracks.

## Related

Ops index (state vocab, idle latch, same-pass fold, admit-pass): [`docs/operator_ops/README.md`](operator_ops/README.md).

When you switch to a **brand-new claim**, write up what the last string taught you first: [`docs/DIGESTION_HABIT.md`](DIGESTION_HABIT.md).

**Related — Digestor living spine / index:** Digestor keeps a living spine/index board per Amb (`LIVING_SPINE_INDEX.md`). Write a true `DIGESTION_PARK_WHAT_TAUGHT.md` only after Operator **LAST-live ADMIT** or **TABLE**. Authority order: Operator ADMIT chat → master `STATUS.md` / `OPERATOR_STATUS_STAMP.md` → Founder/Lab paraphrase. Digestor never Soften / Harden / Kill. Habit: [`docs/DIGESTOR_LIVING_SPINE_INDEX_HABIT.md`](DIGESTOR_LIVING_SPINE_INDEX_HABIT.md). Template: [`templates/LIVING_SPINE_INDEX_TEMPLATE.md`](../templates/LIVING_SPINE_INDEX_TEMPLATE.md).
