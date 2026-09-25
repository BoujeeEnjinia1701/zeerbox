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
