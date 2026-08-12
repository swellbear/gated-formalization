# Failure-Mode Log

Record cases in which the method:

- blocked something that later proved well-supported, or
- allowed something that later collapsed,
- or hit a clear **method pressure point** worth recording.

## Cadence

After every **closed application**, or after every **N ≥ 5** REJECT/HOLD decisions that share a recurring pattern (whichever comes first), add or update an entry when there is anything to learn. Lightweight; skip empty ceremony. See `.cursor/rules/applications-gated-method.mdc`.

## Entry Format

```
### YYYY-MM-DD | Domain | Short claim/layer name
- **Gate outcome at the time:** 
- **Later evidence:** 
- **Direction of error:** blocked-but-later-supported / allowed-but-later-collapsed / method-pressure-point
- **Which rule or judgment contributed:** 
- **Adjustment made (if any):** 
- **Notes:** 
```

## Entries

### 2026-08-11 | AV architectures | E2E vs modular preferability (R1/R2 vs R4)
- **Gate outcome at the time:** Phase 2 Attempt 1 marked general R1/R2 currently intractable; reopen mentioned R4/matching but dependency was easy to read as ordinary evidence-gap rather than **dominant blocker**.
- **Later evidence:** Corrective pass showed R1/R2 were blocked primarily by unset R4; locking-scaffolding + package selection made dependents well-posed without answering them empirically.
- **Direction of error:** **method-pressure-point** (under-specified dependency / soft reopen), not a false ADMIT of the original slogan.
- **Which rule or judgment contributed:** Intractability reopen listed as trailing condition; inter-parameter dependency not yet first-class; no locking-scaffolding / OR-slot rule yet.
- **Adjustment made (if any):** Standing rule updated: explicit inter-parameter dependency; locking-scaffolding with ranked packages + relevance warnings; OR-slot resolution; scoped-result honesty; Original-Claim Assessment + revision-vs-continuation fork; evidence-intake template; compact no-admit mandatory; canonical `.mdc` as sole full rule text.
- **Notes:** AV application closed Stable Provisional. P-Strong-Both left B1|B2 and D5|D1 as OR-slots — under the new OR-slot rule those must be singled or formally “either”-accepted going forward.

### Prior note
*Conscience sketch and 2026 Fox News opinion article on democratic socialism: no confirmed blocked-but-later-supported or allowed-but-later-collapsed entries; remain consistent with currently available material.*
