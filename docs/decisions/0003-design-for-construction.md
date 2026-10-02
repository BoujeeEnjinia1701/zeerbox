---
doc_id: ZBX-DDR-003
title: ZeerBox design for construction
project: ZeerBox
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-02'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-02
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The questions in Table 3 are proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo to get an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of ZBX-DDR-002 showed what ZeerBox does, and its calculations hold, but many of its parts were massing shapes: a roof sheet on four posts with nothing under it, a solid ceiling slab, openings cut through a cavity wall with no lintels or linings, fan holes that left 50 mm brick piers, shelves that the rack posts passed through, and a solar panel floating 150 mm above the roof.

Each component was reviewed for how it is made (cast, laid, sawn, bent, welded, bought) and how it joins the parts next to it. The model now builds every component with the faces it sits on (`cad/src/model.py`) and runs 7,816 constructability checks with build123d (`python cad/src/model.py --check`): no two components share volume except a post cast into its footing, 39 named joints touch, no piece floats, and seven clearances hold (fan shutters to the roof framing, the door in its lining, the air path above the top crates, and others). All pass.

The changes keep what ZeerBox does: the same 2.4 x 1.5 x 2.0 m room, double brick walls with a dry rice husk cavity, 150 mm pad on the back wall, two 250 mm exhaust fans at the door end, sump, controller, 150 W panel, battery, racks and 24 crates. The calculated store temperature, humidity, airflow, water and energy are unchanged (ZBX-CAL-001 v0.3). Nothing here changes the pitch or the safety case.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| C1 | The two 250 mm fan holes in the front wall, 575 mm each side of the door axis, left about 50 mm of brick between each hole and the door opening and 50 mm to the inner corners: piers too narrow to lay or to carry a lintel. | Both fans sit in one plywood fan box (310 x 640 mm, 150 mm deep, 18 mm plywood) dropped into a joist bay of the ceiling, centred 1,000 mm from the store's centre toward the door, over the aisle. They blow up into the shaded 450 mm roof space through gravity shutters. | The fans still exhaust at the door end with the pad opposite, so the air still sweeps the aisle and crates. A ceiling bay needs no lintel and no brick cut, the shutters close by gravity when lying flat, and rain cannot reach them under the roof. The wall gains 0.1 m² and the heat load 1 W. See A1. |
| C2 | The roof sheet sat on the four post tops with nothing under it (a 3.9 x 3.0 m sheet cannot span between posts), and the posts ran into the sheet. | Two 75 x 150 mm beams across the store on the post lines, five 50 x 150 mm purlins along it at 700 mm, sheets screwed to the purlins. Each post is an 89 mm galvanized pipe with a 150 x 150 x 6 mm cap plate welded at the 4° roof slope and a 12 mm anchor bar through its foot; two M10 coach screws hold each beam; a hurricane tie holds each purlin crossing. | Purlins 100 mm deep would be over-stressed at 11.6 MPa under uplift; 150 mm deep gives 5.2 MPa (ZBX-CAL-001 Table 6a). The framing weight lowers the uplift per post from 2.23 to 1.94 kN, so the decided 500 mm footings now have a factor of 1.81. |
| C3 | The walls stood on bare ground; the calculation assumed a 450 mm strip footing that was neither modelled nor priced. | A concrete strip footing 450 mm wide and 250 mm deep, top at ground level, with a damp-proof strip on top under both leaves and the cavity (BOM line 15). | Matches the calculation's bearing check (16 kPa) and gives the husk fill its dry base. |
| C4 | Door and pad openings were cut straight through the cavity wall: no lintels, the husk fill open at every reveal, no door frame or hinges, and a 50 mm door leaf where the calculation's U value assumes 50 mm of insulation between two 12 mm skins. | One 115 x 100 mm hardwood lintel over each leaf at both openings (150 mm bearing). A 20 mm board lining on every reveal closes the cavity; the brick openings are 40 mm wider and taller to keep the clear sizes (door 800 x 1,800 mm, pad 600 x 500 mm). The door gets stop beads with a seal, three hinges, a 74 mm leaf, and opens outward with an inside push latch and no outside lock. | Lintels were already in BOM line 1; now they are drawn and priced. The linings keep the husk in and dry. An outward door keeps the racks and aisle clear and cannot be held shut by produce inside. |
| C5 | The ceiling was a solid 120 mm slab. | Nine 50 x 100 mm joists across the wall tops with 25 x 25 mm cleats, 50 mm insulation and a vapor sheet on the cleats, 20 mm boards nailed on top, a galvanized strap at each joist end. The wall top is a brick capping course over both leaves and the cavity. | The same 120 mm build-up and U value as the calculation; joist spacing (410 mm or less) leaves one 310 mm bay for the fan box. |
| C6 | The rack posts passed through the shelf boards, and the shelves had no rails. | Each rack: six 50 x 50 mm posts, six 50 x 75 mm rails screwed to the inside faces of the posts, 15 slats per shelf across the rails with gaps for air, two steel angle brackets tying the end posts to the wall. | The rail size is the one the calculation checked (0.58 MPa); slat gaps let the air pass up through the crates; the brackets stop a loaded rack tipping. |
| C7 | The pad frame was a ring with nothing to hold the pad in or the frame on the wall; the drip header floated 14 mm above the frame; the gutter had no brackets. | Frame of 25 mm boards on two wall battens, two bottom bars the pad stands on, two front retaining bars; the header lies on top of the pad through holes in the frame sides; the gutter sits on two strip brackets 20 mm below the pad. | Every piece is screwed or plugged to the one beside it; the pad slides out from the front for cleaning. |
| C8 | The solar panel floated 150 mm above the roof with no mount. | Two aluminium frames (angle base rail screwed through sheet crests into two purlins, two flat-bar legs, angle top rail bolted to the panel frame). The panel centre moves 50 mm down the slope and 100 mm higher so both base rails cross two purlins. Replaces the roof clamps of BOM line 10. | The panel keeps its 15° tilt and size; the fixing reaches the purlins, not just the thin sheet. |
| C9 | The sump drum stood half outside the roof edge, in the sun. | Moved 190 mm toward the store, fully under the roof; hoses routed from the pump to the header end and from the gutter outlet to the drum lid. | Keeps the recirculating water shaded (cooler water, slower bacterial growth). |
| C10 | The outside sensor's radiation shield floated 40 mm off the wall. | A short bent strip arm screws it to the wall. | A fixing. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Calculations | ZBX-CAL-001 v0.3: heat load 442 to 443 W; bricks 1,977 to 1,973; husk 1.3 to 1.2 m³; uplift per post 2.23 to 1.94 kN, footing factor 1.58 to 1.81; roof and ceiling members checked. Temperature, humidity, airflow, water and energy unchanged. | Follows the model. |
| Cost | Value-engineering target: USD 300 for the kit (`budget_usd`, unchanged). Estimated cost of the constructable design: kit USD 299 (USD 1 under the target); structure USD 574, costed separately (was USD 355); store USD 873. | New BOM lines 15 to 18; lines 1, 3, 4, 6, 10 and 12 repriced. |
| BOM | Lines 15 (strip footing), 16 (door lining, stops, fan box), 17 (roof beams and purlins), 18 (panel frames) added; lines 1, 3, 4, 5, 6, 8, 10, 12 respecified. | Parts added for construction. |
| Drawings | ZBX-DWG-001 Rev P3; making sketches ZBX-DWG-101 to 118 added. | Follows the model. |
| Documents | ZBX-REQ-001 v0.5 and ZBX-PRC-001 v0.5 updated for the ceiling fans, cost and structure figures. No requirement changed status except R12, now reported against the value-engineering target. | Follows the model. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Fan position. The concept put the fans in the front wall beside the door, which leaves piers too narrow to build. | (a) ceiling fan box at the door end, as modelled; (b) keep wall fans by raising the room about 250 mm so they fit above the door (more brick, a taller room, a new heat balance); (c) narrow the door to about 600 mm to widen the piers. | (a): no change to the room, the airflow or the door. |
| A2 | Moist exhaust air now leaves into the roof space, about 2.5 m from the pad intake. | (a) accept, and check at TRL 4 that it does not drift back to the pad; (b) add a short duct to carry it out past the roof edge at the door end. | (a); the roof space is open on all four sides. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan ZBX-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open questions are in the design decisions register ZBX-DEC-001.
- Requirement status: 7 met (3 by design or logic review), R12 USD 1 under its value-engineering target, 1 at risk (R3), none not met, 3 not verifiable at TRL 3 (ZBX-CAL-001 v0.3).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the fans in the front wall, the old panel legs and the concept racks; they need updating on Amish's Mac. The concept media in `media/` have been regenerated from the constructable model.
- The concept views (hero, exploded, cutaway, blueprint) leave out the below-ground footings; the general arrangement and the build plan show them.
