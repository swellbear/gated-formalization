# BATCH_SIGNAL
**Sibling 2/3 of authorized batch**
- New FP shape outside LOCK-001…004? **No**
- New lock? **No**
- New pattern tag? **No**
- Signal: **keep-rule / transfer success**

## Early-pause check (b)
Sibling 1 (serverless) and Sibling 2 (graphql) are **two consecutive** pure keep-rule / no new lock / no new pattern → **PAUSE. Skip sibling 3.**
