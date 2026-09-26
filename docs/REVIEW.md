# Review note: ZeerBox

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (ZBX-PRB-001 v0.2): problem with cited loss figures, three gaps (cost of refrigeration, small passive coolers, humid-weather failure), users, operating environment, constraints, out of scope, prior work with sources (zeer, ZECC, MIT D-Lab Mali and Kenya, fan and pad practice, solar cold rooms), open questions, and a co-design checklist (none existed before; added in the portfolio's standard form).
- `docs/03-requirements.md` (ZBX-REQ-001 v0.2): 12 measurable requirements (R1 to R12) with a defined design point, a TRL 2 status column and a list of requirements not met.
- `docs/02-concept.md` (ZBX-PRC-001 v0.2): how it works, four control modes, numbered components, psychrometric and heat balance estimates, airflow, water, solar energy, humid-weather performance, cost, design choices, safety and open questions.
- `cad/src/concept_media.py`: massing model of the store (double brick walls and floor, wet sand cavity, insulated ceiling, shade roof on posts, door, pad assembly, sump and pump, fans, controller, solar panel, power box, racks, crates), with a hand-placed 1.75 m person in front of the long wall so no roof post hides the figure.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with callouts 1 to 13, `cutaway.png` along the aisle, `flow.png` (air and water path, estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 14 lines with indicative USD prices, numbered to match the exploded view (item 14, wiring and plumbing, has no callout). `bom/bom-notes.md` gives the structure and equipment subtotals.
- `README.md`: hero image and links line before "## Problem"; problem, concept and key components brought in line with the precis; short safety section added.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml` is unchanged. Its pitch and problem remain accurate.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Store size and capacity | 2.4 x 1.5 x 2.0 m inside; 24 crates, about 480 kg | R1 met |
| Supply air at 35 °C, 30 % RH | about 24.9 °C, 74 % RH (75 % pad effectiveness) | |
| Mean store temperature | about 26 °C, about 9 K below ambient | R2 met |
| Store RH | about 65 to 75 % | **R3 not met** (85 %) |
| Heat gain | about 550 W (walls 250 W, respiration 70 W, field heat 80 W, other 150 W) | |
| Airflow | about 650 m³/h (380 cfm), 0.6 m/s at the pad, about 90 air changes per hour | |
| Water | about 55 L/day (31 L pad, 20 L cavity, 4 L bleed) | R8 met |
| Electrical load | about 31 W cooling; about 350 Wh/day | |
| Solar yield, 100 W panel | about 350 Wh/day | **R7 at risk, no margin** |
| Humid season, 30 °C and 75 % RH | about 1.5 K of cooling | R4 handled by mode change |
| Parts cost, crates excluded | about $575 (structure about $340, equipment kit about $233) | **R12 not met, about 90 % over $300** |

Requirements not met or at risk:

- **R3 (store RH 85 %) not met:** forced air warms by about 2.6 K across the store and its RH falls to about 65 to 75 %.
- **R7 (solar) at risk:** the 100 W panel just matches the design-day load.
- **R12 (cost) not met:** about $575 against $300. The structure alone is over budget.
- **R6 (shelf life), R10 and R11 unverified:** R6 relies on ZECC data from cooler, more humid chambers and may be optimistic.

### Proposed, awaiting Amish

1. **Budget.** Options: (a) redefine the $300 budget as the cooling equipment kit (about $233), with the structure built from local materials and costed separately, as SunSpoke does for its pack; (b) raise `budget_usd` to about $600 for the complete store; (c) shrink the store to about 12 crates to cut the structure cost by about a third, which would still exceed $300. Recommendation: (a), and redefine R12 as "equipment kit $300 or less; structure costed separately". `project.yaml` is unchanged.
2. **Solar panel size.** 100 W (no margin) or 150 W (about $20 more, about 50 % margin). Recommendation: 150 W.
3. **Battery.** Keep a 12.8 V 12 Ah LiFePO4 battery for evening ventilation, or run PV-direct and save about $50. Recommendation: keep it.
4. **Forced air through a pad** rather than a passive ZECC-style chamber. Recommendation: forced air (this is the pitch).
5. **Exhaust fans with the pad on the opposite wall** rather than blowing air in through the pad. Recommendation: exhaust.
6. **Wet sand cavity walls** rather than a single insulated wall. Recommendation: wet cavity, pending a TRL 3 heat balance.
7. **Store size** of 24 crates rather than a smaller single-farm store or a larger group store. Recommendation: keep 24 until a partner confirms the need.
8. **Control thresholds:** 20 °C set point, 4 K wet-bulb depression, 95 % RH guard. Recommendation: use as starting values.
9. **Fired brick** rather than mud brick or block for the walls.
10. **First partner, region and crop mix** for co-design (for example a dry-season vegetable area in the Sahel, or a group already using D-Lab designs in Kenya).

### Safety concerns

- A walk-in room: entrapment and stale air. The door must open from inside with no outside lock that can shut someone in.
- Warm recirculating water in the pad and sump can grow *Legionella* and other bacteria; weekly draining and cleaning, a covered sump and no reuse of sump water are part of the design.
- Mold in a damp store; guard mode and cleaning routine.
- LiFePO4 battery (154 Wh): BMS, terminal fuse, shaded and ventilated box.
- Fans: guards on both faces; isolate before cleaning.
- Masonry and roof: competent mason, roof anchored against uplift, footings protected from the wet cavity.
- The store is not cold chain and must not be used for meat, fish, milk or medicines.

### Problems and notes

- No SwapCell pack is used; the 12 V load of about 31 W does not justify a 48 V pack.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- In the hero view the door and fans face away from the camera; they appear in the exploded view, the cutaway, the blueprint's right view and the 3D viewer.
- In the exploded view the controller (9) and power box (11) are small at this scale and partly hidden by their callouts.
- The co-design checklist in PRB-001 is new in this session (there was none to keep); remove it if Amish prefers.

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to check the heat balance (including a wet cavity), the pad and fan selection, the RH problem (R3) and the solar sizing by calculation, and to produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

Amish reviewed the TRL 2 points on 2026-09-25 and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." This session advanced ZeerBox to TRL 3 and stopped there. **TRL 4 is on hold by Amish's instruction.**

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (ZBX-DDR-001 v0.1): records items 1 to 8 as decided by Amish, 2026-09-25 (go with recommendation), the cross-cutting approvals, and the open items 9 to 13.
- `docs/04-calcs/01-sizing.md` (ZBX-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: psychrometrics, fan and pad operating point, heat balance with three scenarios, humidity, wet cavity against dry fills, off-design weather, energy and solar, water, electrical, structure (bricks, bearing, roof uplift) and cost, with a results table for R1 to R12. The script reads `cad/src/model.py`, `bom/bom.csv` and `project.yaml`, prints every quoted number and writes `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d model (all 13 modeled BOM lines) with `PARAMS` and `derived()`; exports `cad/step/zeerbox-assembly.step`, `zeerbox-structure.step`, `zeerbox-cooling-kit.step` and matching STL files.
- `cad/src/sheets.py` and `cad/drawings/ZBX-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:50, third-angle, with key dimensions, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet keeps ZBX-DWG-010, so DWG-001 was the next free number.
- `bom/bom.csv` and `bom/bom-notes.md`: every line priced with a supplier type; 150 W panel, 20 A PWM controller, 2.5 mm² PV cable, 500 mm post footings, brick and sand quantities from the calculation.
- `cad/src/concept_media.py` now builds from the model; `media/` refreshed (hero, blueprint, exploded, cutaway, flow, `model.glb`, `viewer.html`). All images were inspected; temporary `media/_views*` folders were deleted.
- ZBX-PRB-001, ZBX-PRC-001 and ZBX-REQ-001 raised to v0.3 with the decisions and the checked figures; R12 redefined as the cooling equipment kit. `README.md` updated (TRL 3, 150 W, costs, links). `project.yaml`: `trl: 3`, `trl_target: 3`, evidence list extended. The pitch and problem lines are unchanged (no rewording was recommended).
- PDFs of all controlled documents rebuilt in `docs/pdf/`.

### Requirements (ZBX-CAL-001), not met first

| ID | Status | Value (central, range) |
| --- | --- | --- |
| R3 | **Not met** | Store RH 71 % (66 to 76 %) against 85 % |
| R2 | **At risk** | 9.1 K below ambient (8.0 to 10.0 K); store 25.9 °C |
| R6, R10, R11 | Not verifiable at TRL 3 | Shelf life, local repair times and component life need field data or a partner |
| R1, R7, R8, R12 | Met | 24 crates, top shelf 1.40 m; 372 Wh/day against 525 Wh (41 % margin); 44 L/day; kit $260 against $300 |
| R4, R5, R9 | Met by logic or design review | Mode switch at 3.7 K depression; about 8 air changes an hour in hold; 12 V, fused, guarded, inside release |

Key numbers: airflow 584 m³/h at 16 Pa (not 650 m³/h); heat load 418 W (not 550 W); supply air 24.8 °C and 75 % RH; about 44 L of water per day (not 55 L); 372 Wh/day (the 100 W panel of TRL 2 would have been 6 % short); structure about $360 and store total about $620, crates excluded.

Other findings: the 10 A charge controller was too small for a 150 W panel (1.25 x Isc is 11.2 A), so the BOM now has 20 A; and the wet sand cavity is worth only about 0.15 K over dry sand in the central case and is slightly worse than dry sand in the unfavorable case.

### Decisions recorded

Decided by Amish, 2026-09-25, go with recommendation (ZBX-DDR-001): (1) keep `budget_usd: 300` for the cooling equipment kit, structure costed separately, R12 redefined; (2) 150 W panel; (3) keep the battery; (4) forced air through a pad; (5) exhaust fans with the pad opposite; (6) wet sand cavity walls, pending the TRL 3 heat balance; (7) 24 crates; (8) control thresholds as starting values. Cross-cutting: SwapCell interface v0.3 and shared-pack pricing do not apply (no SwapCell pack); partners are picked per area later.

### Still awaiting Amish

9. Wall material: fired brick, mud brick or block. No recommendation was stated; fired brick is the working choice.
10. First partner, region and crop mix (left open by the per-area partner rule).
11. R3 not met and R2 at risk. **Decided by Amish, 2026-09-25: go with recommendation (ZBX-DDR-002).** Options: 150 mm pad (10.5 K, 81 % RH, about $10 more), a relaxed R3, produce-level measures. Recommendation: a 150 mm pad and R3 at 80 %.
12. Wet cavity against a dry insulating fill. **Decided by Amish, 2026-09-25: go with recommendation (ZBX-DDR-002).** Dry rice husk gives 9.2 K (8.2 K unfavorable) with no cavity water. Recommendation: dry fill, if a durable, pest-proof fill is available locally. This reopens the substance of decided item 6, because the heat balance it was waiting for does not support it.
13. Roof footings and design wind speed: **Decided by Amish, 2026-09-25: go with recommendation (ZBX-DDR-002).** 500 x 500 x 600 mm footings are in the model; confirm the local design wind speed.

### Safety concerns

- Roof uplift is the main structural hazard: about 2.2 kN per post at a 30 m/s gust. The footings were enlarged to 500 x 500 x 600 mm; a 400 mm footing would have had no margin.
- Walk-in room: the door opens from inside with no outside lock; air the store out before entering after a long hold.
- *Legionella* and other bacteria in the warm sump and pad: covered sump, weekly drain and clean, no reuse of sump water.
- LiFePO4 battery (154 Wh): BMS rated for at least 10 A of charge, terminal fuse, shaded and ventilated box; charge controller sized to 1.25 x Isc.
- Fans guarded on both faces; isolate before cleaning. Heavy masonry (about 7 t of brick and 2.4 t of wet sand) needs a competent mason, and the wet cavity must not undermine the footings.
- Not cold chain; not for meat, fish, milk or medicines.

### Problems and notes

- No TRL 4 material exists in the repo; none was created. `build-log/` holds only its README. STANDARDS section 9 asks for a build-log entry on a TRL change; none was added because build-log work is outside this brief, so the TRL change is recorded here and in `project.yaml`.
- No citations were flagged as unchecked in the TRL 2 review; no new sources were added.
- Pad pressure drop, pad effectiveness at 0.54 m/s and the fan curve are assumptions; supplier data for the chosen parts should replace them.
- As at TRL 2, the hero view shows the pad end, and the small controller (9) and power box (11) are partly hidden by their callouts in the exploded view.

### Recommended next step

Decide items 11 and 12 (pad depth, the R3 target and the cavity fill), then items 9 and 13. These are paper changes that can be made at TRL 3: update `PARAMS`, rerun `sizing.py`, and reissue the drawing at Rev P2.

TRL 4 is on hold by Amish's instruction. For reference only, TRL 4 would need: a pad and fan test article with measured airflow, pressure drop and pad effectiveness; a bench test of the controller logic with sensors; a lab test report (TST with `environment: lab`); and build-log entries. None of this has been started.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25, in chat: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (ZBX-DDR-002 v0.1). The repo stays at TRL 3.

### Decisions applied and what changed

- **Item 11 (R3 not met, R2 at risk):** option (c). Pad 100 to 150 mm (`PAD_T` in `cad/src/model.py`; BOM line 6 $30 to $40); R3 target 85 to 80 %; covered or lined crates for leafy and water-sensitive produce as an operating practice. Pad effectiveness 75.7 to 88.2 %; airflow 584 to 563 m³/h; supply air 24.8 °C and 75 % RH to 23.1 °C and 87 % RH.
- **Item 12 (wet cavity against a dry fill):** option (b). Dry rice husk fill, lime-treated, on a damp-proof course and capped with mortar; dry sand is the fallback if no durable, pest-proof supply exists locally. Supersedes ZBX-DDR-001 item 6. BOM line 2 $20 to $15 (wetting pipe removed); cavity water 12 to 0 L/day; fill mass 2.4 to 0.15 t; wall line load 9.3 to 7.1 kN/m.
- **Item 13 (roof footings):** keep 500 x 500 x 600 mm footings as a minimum and confirm the local design wind speed with a builder at the chosen site. No geometry change.
- Combined result: store 25.9 to 24.3 °C; drop 9.1 K (8.0 to 10.0 K) to 10.7 K (9.8 to 11.4 K); store RH 71 % to 81 % (77 to 85 %); heat load 418 to 442 W; water 44 to 36 L/day; kit $260 to $270; structure $360 to $355; store total $620 to $625.
- **Budget:** `budget_usd` unchanged at $300 for the cooling equipment kit (no budget change was recommended). Pitch and problem lines unchanged (no rewording was recommended).
- Files: `cad/src/model.py` (and STEP, STL re-exported), `docs/04-calcs/sizing.py` and `results.csv`, ZBX-CAL-001 v0.2, ZBX-REQ-001 v0.4, ZBX-PRC-001 v0.4, ZBX-PRB-001 v0.4, ZBX-DDR-001 v0.2, `bom/bom.csv`, `bom/bom-notes.md`, drawing ZBX-DWG-001 at Rev P2 (`cad/src/sheets.py`), `cad/src/concept_media.py` and all of `media/`, `README.md`, `project.yaml` (DDR-002 added to the evidence list). All PDFs in `docs/pdf/` rebuilt; the drawing and media were regenerated so no generated file shows the old site address.
- `README.md` gained "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea" (the Bah Abba pot-in-pot cooler, northern Nigeria, 1990s).

### Requirements (ZBX-CAL-001 v0.2), not met first

| ID | Status | Value (central, range) |
| --- | --- | --- |
| (none) | Not met | No requirement is not met |
| R3 | **At risk** | Store RH 81 % (77 to 85 %) against 80 % |
| R6, R10, R11 | Not verifiable at TRL 3 | Shelf life, local repair times and component life need field data or a partner |
| R1, R2, R7, R8, R12 | Met | 24 crates; 10.7 K (9.8 to 11.4 K); 41 % solar margin; 36 L/day; kit $270 against $300 |
| R4, R5, R9 | Met by logic or design review | Mode switch at 3.7 K depression; about 8 air changes an hour in hold; 12 V, fused, guarded, inside release |

### Still awaiting Amish

9. Wall material: fired brick, mud brick or block. No recommendation; fired brick remains the working choice.
10. First co-design partner, region and crop mix. No recommendation; partners are picked per area later.

### Cross-repo actions

None. No decision needs another repo to change.

### Safety concerns

- Dry rice husk is combustible: keep the cavity capped with mortar, keep hot work and flames away from the walls during building, and run solar wiring in conduit where it passes the wall top (added to ZBX-PRC-001 v0.4).
- The husk must stay dry and closed to termites and rodents; a wet or infested fill loses its insulation and can harbor mold.
- All earlier concerns stand: roof uplift, inside door release, *Legionella* in the sump, battery, fan guards, not for cold-chain products.

### TRL 4

TRL 4 remains on hold by Amish's instruction. No TRL 4 work was created. Confirming the husk supply and the local design wind speed, crate liner trials, and a pad and fan test article all wait for a partner and for TRL 4 to be released.

## Session 2026-09-26: sources strengthened

Amish asked for the weaker sources to be fixed. Every replacement below was fetched and checked against the claim it supports.

| Where | Claim | Old source | New source |
| --- | --- | --- | --- |
| README, Northern Nigeria row; ZBX-PRB-001 gap 1 | ColdHubs pay-per-crate solar cold rooms at markets and farm clusters | Wikipedia, "ColdHubs" | [ColdHubs](https://coldhubs.com/) official site and [IFPRI](https://www.ifpri.org/blog/coldhubs-addressing-crucial-problem-food-loss-nigeria-solar-powered-refrigeration/) (about $0.50 per crate per day); zeer revival cited to *TIME* |
| README, Australia row | Coolgardie safe | Wikipedia, "Coolgardie safe" | [Western Australian Museum](https://visitwanderland.com.au/explore/golden-outback/warden-finnertys-residence/coolgardie-safe). The unverified "3 to 9 °C below the air" figure and the uncited remote supply claim were removed |
| README, What sparked the idea; ZBX-PRB-001 prior work | Bah Abba pot-in-pot cooler | Wikipedia, "Pot-in-pot refrigerator" | Verploegen, Sanogo and Chagomoka, [MIT D-Lab Mali evaluation](https://d-lab.mit.edu/sites/default/files/inline-files/GHTC%20-%20Evaluation%20of%20Low-Cost%20Evaporative%20Cooling%20Technologies%20for%20Improved%20Vegetable%20Storage%20in%20Mali.pdf) (popularized in Nigeria from 1995) and [*TIME*, Best Inventions of 2001](https://content.time.com/time/specials/packages/article/0,28804,1936165_1936254_1936632,00.html). The unverified "first batch of 5,000" and the award year were dropped; the name now follows the Rolex and D-Lab spelling, Mohammed |
| ZBX-PRB-001 gap 3 | Evaporative cooling weakens in humid air | Wikipedia, "Evaporative cooling chambers" (25 °C, 40 % RH rule of thumb) | MIT D-Lab Mali evaluation: peak cooling up to 10.4 °C below 40 % RH, 4.2 °C above 70 % RH |
| README, Mali row; ZBX-PRB-001 prior work | Brick chamber cooling in Mali | MIT News only | MIT D-Lab paper added as the primary source alongside MIT News |

The inspiration event is unchanged; its line in the portfolio `INSPIRATIONS.md` was corrected to the verified facts. ZBX-PRB-001 moved to v0.5. No budget change for ZeerBox.
