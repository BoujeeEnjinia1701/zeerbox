---
doc_id: ZBX-DEC-001
title: ZeerBox design decisions register
project: ZeerBox
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-02'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
---

# ZeerBox design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design for construction | Accept the changes C1 to C10 as made; or ask for any of them to be redone | Accept | Every making sketch and step of the build plan | ZBX-DDR-003, Table 1 |
| 2 | Fan position | (a) ceiling fan box at the door end, as modelled; (b) wall fans above the door, with the room raised about 250 mm; (c) wall fans beside a door narrowed to about 600 mm | (a) | Fan box (build plan 3.10, steps 11 and 13), door, wall height | ZBX-DDR-003, A1 |
| 3 | Exhaust into the roof space | (a) accept, check at TRL 4 that moist air does not drift back to the pad; (b) add a short duct past the roof edge at the door end | (a) | Fan box top; a duct would add a part | ZBX-DDR-003, A2 |
| 4 | Wall material | Fired brick (working choice), mud brick, or block | None stated; fired brick is modelled | Walls, footing width, brick count, lintel bearing | ZBX-DDR-001, item 9 |
| 5 | First co-design partner, region and crop mix | Per-area partner chosen later | None yet | Site, wind speed, crate size, wall material | ZBX-DDR-001, item 10 |
| 6 | Clear window in the controller lid and power box door (appearance model) | Keep both; keep the controller window only; neither | Keep the controller window; plain power box door if the partner prefers | Bought boxes (build plan 3.19) | REVIEW.md, 2026-09-26, item 2 |
| 7 | Mode lamp position | On top of the controller box beside the door (appearance model); elsewhere by the door | Accept on the controller box, and add it to the model | Controller box drilling | REVIEW.md, 2026-09-26, item 3 |
| 8 | Outside sensor shield shape | Stacked round plates 46 mm across; the 40 x 40 x 60 mm block of the model | Accept the plates | Sensor arm | REVIEW.md, 2026-09-26, item 4 |
| 9 | Plinth render band | A 10 mm cement render 300 mm high round the base; none | Optional finish, the mason's choice | Walls, finish only | REVIEW.md, 2026-09-26, item 5 |
| 10 | Hose and conduit routing | Routing as sketched in the build plan wiring and plumbing; the partner's routing | Accept as a sketch; route on site | Hoses and conduit (build plan 3.19.1, step 24) | REVIEW.md, 2026-09-26, item 6 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The fan frame is no wider than 290 mm and fits a 250 mm hole | The fan box bay is 310 mm between joists | ZBX-DDR-003, C1 |
| 2 | The fan curve and the pad's pressure drop and effectiveness from supplier data | The airflow of about 560 m³/h and the 10.7 K drop rest on assumed curves | ZBX-CAL-001, sections 1 and 3 |
| 3 | The panel frame has mounting holes on its back flange that the top rails can reach | The panel bolts to the mounting frames through them | ZBX-DDR-003, C8 |
| 4 | Hurricane ties are rated 2 kN or more in uplift | Each purlin crossing sees about 1.1 kN at a 30 m/s gust | ZBX-CAL-001, Table 6a |
| 5 | A durable, pest-proof rice husk supply near the site; otherwise dry sand | The fill's insulation and the wall heat gain depend on it | ZBX-DDR-002, item 12 |
| 6 | The local design wind speed, confirmed with a builder | The roof footings and ties are sized for a 30 m/s gust | ZBX-DDR-002, item 13 |
| 7 | The pump gives about 3.6 L/min at 2 m head and has a float switch | The pad must stay wet and the pump must not run dry | ZBX-CAL-001, section 8 |
| 8 | The charge controller is set for 12.8 V lithium iron phosphate and the BMS takes 10 A of charge | Battery safety and life | ZBX-CAL-001, section 7 |

## Value engineering

Value-engineering target: USD 300 for the cooling equipment kit (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 299 for the kit (USD 1 under the target). The structure is costed separately at USD 574, and the whole store at USD 873, crates excluded. Main cost drivers and savings worth trying:

- The largest kit lines are the 150 W panel (USD 62), the power box with its battery (USD 62), the pad with its frame, header and gutter (USD 50), the two fans (USD 30) and the controller (USD 30).
- Making the design constructable added USD 22 for the two panel mounting frames and USD 10 for the pad frame, lining, bars and brackets, less USD 3 for the roof clamps they replace: the kit rose from USD 270 to USD 299.
- The structure rose from USD 355 to USD 574 because the concept did not price the strip footing (USD 35), the roof beams and purlins (USD 70) or the door lining and fan box (USD 25), and underpriced the framed ceiling and the racks.
- Savings worth trying: galvanized steel angle in place of aluminium for the panel frames (about USD 8 less, needs painting at cut ends); a 100 W panel is not one (6 % short on energy, ZBX-CAL-001 section 7); in the structure, mud brick or stabilized block if decision 4 allows, and racks of local poles in place of sawn timber.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items 1 to 8: the USD 300 budget covers the cooling kit with the structure costed separately; 150 W panel; keep the battery; forced air through a pad; exhaust fans with the pad opposite; wet sand cavity pending the heat balance; 24 crates; control thresholds as starting values | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | ZBX-DDR-001 |
| 2026-09-25 | Items 11 to 13: 150 mm pad, R3 relaxed to 80 % with covered or lined crates; dry rice husk fill in place of wet sand (dry sand as fallback); 500 x 500 x 600 mm roof footings as a minimum | Amish: "i accept all your recommendations, go with them across all repos." | ZBX-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | ZBX-DDR-003 (the changes themselves await his review, open decision 1) |
| 2026-09-30 | Open decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | This register |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a spending limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | ZBX-CAL-001 v0.3, section 11 |
