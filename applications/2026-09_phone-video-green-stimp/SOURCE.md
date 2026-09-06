# SOURCE — USGA Stimpmeter + Sommer cellphone-video BRD + physics pointers

**Date:** 2026-09-06  
**Application:** `2026-09_phone-video-green-stimp`  
**Role:** notes summary. Operator **ADMIT Soften S0** locks the board as poseable/citable — [`DIGESTION_S0.md`](DIGESTION_S0.md). **NOT** Soften of the green-speed claim. **X unset.**  
**Copy gate:** [`COPY_GATE.md`](COPY_GATE.md)  
**Proposed pulse:** [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md)

This file holds **bibliographic pointers** plus a short paraphrase of definition, procedure, and named objects. It does **not** hold a product specification. It does **not** hold Amb **X**. It is **not** claim-language product copy. Long USGA booklet text and Sommer methods-as-product stay [`COPY_GATE.md`](COPY_GATE.md) blocked.

**Method practice only.** Do **not** build a Stimpmeter. Do **not** treat Sommer’s 6.4 in 95% CI as Amb **X**.

---

## 1. USGA Stimpmeter (definition / procedure)

| Field | Value |
|-------|--------|
| Name | **Stimpmeter** (USGA) |
| What the number is | Green speed = **average ball-roll distance (BRD) in feet** under the USGA procedure |
| Instrument (typical) | Extruded aluminum bar, **36 in**; **145°** V-groove supporting the ball at two points **0.5 in** apart; tapered end to reduce bounce |
| 1X notch | ~**30 in** from the tapered end (full-length run) |
| 2X notch (2013 update) | ~**14 in** from the tapered end (half-length run; **double** the measured roll) |
| Release | Bar raised to ~**20°** (some USGA notes ~22°); gravity releases the ball from the notch |
| Exit velocity (physics pointer) | Repeatable **~6.00 ft/s** (**72 in/s**; **1.83 m/s**) — Holmes 1986; not a casual-putt speed |
| Official booklet Sommer cites | USGA, *Stimpmeter Instruction Booklet* (**2012**) |
| 2013 update | USGA two-sided Stimpmeter (1X + 2X) for shorter level areas |
| Public pointers | [USGA 2013 update](https://www.usga.org/articles/2013/01/usga-introduces-updated-stimpmeter-21474853935.html); booklet archive [wayback](https://web.archive.org/web/20070619004415/www.usga.org/turf/articles/management/greens/stimpmeter.html) |

### Procedure (short paraphrase; not the booklet)

1. Choose a **level** area (~10 ft × 10 ft when using 1X).
2. Equipment named: Stimpmeter, **three** golf balls, **three** tees, 10– or 12-foot tape, data sheet.
3. Roll **three** balls in one direction from a fixed tee / tapered-end spot. Same-direction rests should cluster within **8 in** (USGA validation tolerance).
4. Roll **three** balls the **opposed** direction along the same line.
5. Green speed = **average** of the two direction means, in **feet**.
6. USGA booklet: the device is a management tool; it is **not** intended for course-to-course comparisons.
7. Opposed-direction difference: official Stimpmeter practice keeps the two directions close (commonly cited **≤18 in**); larger slope → Brede correction is a **physics pointer**, not a silent substitute for the USGA procedure.

### Named objects (S0 target list)

| Object | Why it is named |
|--------|-----------------|
| Stimpmeter bar (36 in, V-groove, 1X / 2X notches) | The launch instrument this Amb does **not** build |
| Release angle (~20°) | Makes exit velocity repeatable |
| Exit velocity ~6 ft/s | Launch-class freeze (S2); Holmes |
| Three + three opposed rolls | What a “real Stimpmeter reading” *is* |
| 8-inch same-direction cluster | Literature kinship / validation tolerance — **not** Amb **X** |
| BRD in feet | The unit of green speed and of later **X** |
| Level area | Official procedure object; slope is Brede, not silent |

---

## 2. Sommer et al. — cellphone-video BRD (abstract)

| Field | Value |
|-------|--------|
| Title | *Video Measurement of Golf Green Putting Speed Using a Cellphone* |
| Authors | H. Joseph Sommer; Timothy T. Lulis; John E. Kaminski (Penn State) |
| Venue | WSCG abstract (public PDF) |
| URL | https://www.me.psu.edu/sommer/workarea/WSCG_abstract.pdf |

### Named facts (paraphrase; literature only)

- **Purpose:** measure deceleration of a golf ball on a green from cellphone video and **predict BRD** that correlates to Stimpmeter readings.
- **Ground truth:** 36 Stimpmeter tests on flat A4 bentgrass; readings **9.5–11.5 ft**; 216 rolls (six per test).
- **Video:** iPhone 6 rear camera, 1920×1080, 30 fps; **fixed level base**, **42 in** above turf; ~40 in FOV; ~48 pixels/inch. FOV placed along the expected roll; **Stimpmeter end not in frame**.
- **Launch:** Stimpmeter-launched. Invert assumed **constant exit 72 in/s** (Holmes 1986).
- **Method class:** threshold / blob centroid + photogrammetry; Savitzky–Golay velocity; constant-decel model, then extra nonlinear terms.
- **Numbers:** constant-decel vs actual BRD **r² = 0.644**; three-parameter fit **r² = 0.822**; video predicted 36 equivalent Stimpmeter values with **SD 3.2 in**; authors state **95% CI = 6.4 in** (comparable, they say, to the USGA 8-inch same-direction tolerance).
- **Honesty the authors named:** deceleration is **not** constant (they confirm Hubbard & Alaways 1999). **Handheld / not-level** “additional tests should be conducted.” Better ball-diameter → camera-height still needed.

### What this SOURCE licenses

- Bibliographic citation of a **fixed-mount, Stimpmeter-launched** cellphone-video BRD result.
- The number **~6.4 in 95% CI** as **literature only** — kinship / prior-art note, **not** Amb **X**.

### What this SOURCE does not license

- Treating 6.4 in as handheld **X** or as this Amb’s error bar.
- Treating Sommer’s MATLAB / iPhone-6 / 42-inch mount recipe as a product spec.
- Treating a casual putt as Holmes 72 in/s.
- Porting to a real-time phone app (authors’ “practical application” line is **not** this Amb).

---

## 3. Physics pointers (bibliographic)

| Pointer | Cite | What it names |
|---------|------|----------------|
| **Holmes 1986** | Brian Holmes, “Dialogue concerning the Stimpmeter,” *The Physics Teacher* **24**, 401–404 (1986). [DOI 10.1119/1.2342065](https://doi.org/10.1119/1.2342065) | Stimpmeter exit **1.83 m/s = 6.00 ft/s = 72 in/s**. Launch-class freeze. |
| **Brede 1991** | A. Douglas Brede, “Correction for Slope in Green Speed Measurement of Golf Course Putting Greens,” *Agronomy Journal* **83**(2) (1991). [DOI 10.2134/agronj1991.00021962008300020032x](https://doi.org/10.2134/agronj1991.00021962008300020032x) | Slope correction \(S = 2 S_\uparrow S_\downarrow / (S_\uparrow + S_\downarrow)\). Pointer only; not a silent rewrite of the USGA procedure. |
| **Hubbard & Alaways 1999** | M. Hubbard and L. W. Alaways, “Mechanical interaction of the golf ball with putting greens,” *Proceedings of the 1998 World Scientific Congress of Golf* (Human Kinetics, 1999), pp. 429–439 | Rolling deceleration **not constant** (~10% variation over a putt). Sommer confirms. Constant-decel invert is a **named idealization**, not a free lunch. |

These are **pointers**, not ingested papers and not a product physics engine.

---

## 4. Honesty locks that sit on SOURCE

- **X unset.** Name **X** (ft) vs a real Stimpmeter reading before Soften / Harden.
- Sommer **6.4 in 95% CI** = fixed-mount + Stimpmeter-launched **only**.
- USGA **8-inch** cluster = same-direction validation tolerance, **not** **X**.
- Scale must be **known approx or recoverable**.
- Launch must be **named** (Stimpmeter ~6 ft/s vs unknown casual putt).
- Handheld / non-level is **first-class Soften** vs Sommer’s fixed level mount.

S0 is **Operator Soften** (poseable/citable). This is **not** green-speed Soften. **X** stays unset. **Hold S2.**
