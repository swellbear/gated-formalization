# Residual Branch Menu

**Date:** 2026-08-13  
**Application:** `2026-08_india-heat-mortality-mitigation-show`  
**Offering ≠ running.** Parent closeout unchanged.

**Glossary:** [`docs/READER_GLOSSARY.md`](../../docs/READER_GLOSSARY.md)

---

## Index

| ID | One-line | Disposition |
|----|----------|-------------|
| [R-DOC](#r-doc) | Census of the arXiv HTML | **executed** (D-DOC admitted) |
| [R-CITY](#r-city) | City- or district-level heat-death series | **park-until-trigger** (unnamed) |
| [R-POL](#r-pol) | Real mitigation / HAP evaluation class | **park-until-trigger** (unnamed) |
| [R-INDEP](#r-indep) | Independent CMIP6/ARIMAX rerun | **park-until-trigger** (OUT of object unless named) |
| [R-REV](#r-rev) | Rewrite wrapping to match §4/§5 | **park-90d** (CR offered) |

**Authorize:** `authorize branch R-…` · `name source class …` · `decline residual menu`

---

<a id="r-doc"></a>
### R-DOC — Document census

| Field | Content |
|-------|---------|
| What it is | Admit what the page prints |
| Named source class | arXiv:2603.24244 HTML, 2026-08-13 |
| Disposition | executed — D-DOC admitted; E-DEM not met |
| What it does not do | Clear the abstract slogan |

<a id="r-city"></a>
### R-CITY — City deaths

| Field | Content |
|-------|---------|
| What it is | Replace national-death + city-SMT proxy with a named city/district death series |
| Named source class | **unnamed** — stop until `name source class C-CITY: …` |
| Disposition | park-until-trigger |
| What authorizing does | New evidence pass under Rank 1; does **not** auto-meet E-DEM |
| Trigger | Operator names a public city/district heat-mortality class matching the freeze |

<a id="r-pol"></a>
### R-POL — Real mitigation

| Field | Content |
|-------|---------|
| What it is | Test a named policy (statute, carbon price, HAP evaluation) rather than SSP labels |
| Named source class | **unnamed** |
| Disposition | park-until-trigger |
| Trigger | `name source class C-POL: …` |

<a id="r-indep"></a>
### R-INDEP — Independent rerun

| Field | Content |
|-------|---------|
| What it is | Reproduce ARIMAX/CMIP6 numbers from public inputs |
| Named source class | **unnamed** (CDS/IMD/NDMA stack would need naming) |
| Disposition | park-until-trigger |
| What it does not do | By itself meet “mitigation demonstrated” |

<a id="r-rev"></a>
### R-REV — Claim revision

| Field | Content |
|-------|---------|
| What it is | Successor wording aligned to scenario contrast + “could” |
| Disposition | park-90d (CR offered, not run) |
| What it does not do | Silently fix the parent abstract |

---

*Standing rule: Residual-branch offering. No automatic branch for unnamed class.*
