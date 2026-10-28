---
doc_id: ZBX-DEC-001
title: ZeerBox design decisions register
project: ZeerBox
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-02'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: Amish approved the recommendations for open items 1 to 10 on 2026-10-02 (ZBX-DDR-003 accepted with A1 and A2, fired brick, MIT D-Lab and Mali as first candidates, appearance items); moved to decisions made
  - version: "0.3"
    date: '2026-10-24'
    author: Amish Chadha
    change: "Kit 1.9.1 upgrade: D1 load fuse and D5 review fixes made under the standing instruction of 2026-10-23 (STEM check S16, S27, S30, S37); D2 concept selection, D3 no-power ventilation, D6 battery location, D7 design gust and D8 sump disinfection proposed to Amish; D4 details added in the D3 model listed; kit USD 300"
---

# ZeerBox design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision | Options | Recommendation | Status | Record |
| --- | --- | --- | --- | --- | --- |
| D2 | Concept choice | A forced-air pad store (190 of 235); B passive wet-wall chamber (173); C charcoal-wall wind cooler (173) | None: all three within 10 %, so all go to Amish without a pick (STANDARDS section 21). Option A stays the design of record until he decides; it is the only option that meets PR-002 and PR-004 | Proposed, awaiting Amish | ZBX-OPT-001, ZBX-DDR-004 |
| D3 | Ventilation when the battery is flat | (a) keep as is: the safety notes say to air the store before entering; (b) an always-open meshed vent low in the back wall and a 110 mm stack through the ceiling with a turbine ventilator head (the graft from options B and C); (c) a battery-low alarm only | (b): keeps at least a trickle of air through a closed store with no power (a sealed store reaches about 2.3 % CO₂ in 12 h, STM S36; the independent review also found that in hold mode one fan at 30 % against a 3 m/s wind can stall or reverse, which makes a passive path more useful), at the cost of some cooled air lost on design days, to be sized at TRL 4; a safety trade-off, so Amish's call | Proposed, awaiting Amish | ZBX-STM-001 S36, ZBX-RSK-001 H2 |
| D6 | Where the battery and power box sit | (a) as now: shaded steel box on the outside of the door-end wall; (b) inside the store, low on the door-end wall in the same ventilated box; (c) under the roof overhang on the shaded side, with a white shade board | (b): the store runs at about 24 °C, inside the 0 to 45 °C charging window, where the outside box in 35 to 40 °C air with the pack self-heating at 0.69 C may make the BMS stop charging at midday (STM S31, independent review); the trade-off is a lithium battery inside a room people enter, which is a safety call | Proposed, awaiting Amish | ZBX-STM-001 S31 |
| D7 | Design gust and roof pressure zones | (a) keep the 30 m/s gust and mean net Cp 1.5 until the site is known; (b) design now for a 35 to 40 m/s squall gust and edge-zone Cp of about 2: larger post footings (about 600 x 600 x 700 mm) or ground anchors, ties rated 3 kN on the edge purlins | (a) with a hold point: confirm the local design gust before the roof is built (to confirm 6); at 30 m/s the footing factor is 1.8 but it falls below 1.5 above about 32 m/s, and edge-zone purlins reach about 6.9 MPa against 7 MPa (independent review). Changing the footings changes the structure cost and is a safety margin choice | Proposed, awaiting Amish | ZBX-STM-001 S17, S18, S20 |
| D8 | Disinfection of the sump water | (a) none beyond the daily bleed, daily pad dry-out and weekly drain and clean (D5); (b) add a weekly shock dose of chlorine (household bleach) after cleaning, rinsed before refilling; (c) a slow-release chlorine tablet in the sump | (b): WHO guidance treats disinfection as part of controlling *Legionella* in warm recirculating water; a weekly dose after cleaning keeps chlorine away from produce and the pad's normal running; it adds a chemical to handle, so it is a safety trade-off | Proposed, awaiting Amish | ZBX-STM-001 S27, ZBX-REG-001 G9 |

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

Value-engineering target: USD 300 for the cooling equipment kit (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 300 for the kit (at the target; USD 299 before the USD 1 load fuse of D1). The structure is costed separately at USD 574, and the whole store at USD 874, crates excluded. Main cost drivers and savings worth trying:

- The largest kit lines are the 150 W panel (USD 62), the power box with its battery (USD 62), the pad with its frame, header and gutter (USD 50), the two fans (USD 30) and the controller (USD 30).
- Making the design constructable added USD 22 for the two panel mounting frames and USD 10 for the pad frame, lining, bars and brackets, less USD 3 for the roof clamps they replace: the kit rose from USD 270 to USD 299.
- The structure rose from USD 355 to USD 574 because the concept did not price the strip footing (USD 35), the roof beams and purlins (USD 70) or the door lining and fan box (USD 25), and underpriced the framed ceiling and the racks.
- Savings worth trying: galvanized steel angle in place of aluminium for the panel frames (about USD 8 less, needs painting at cut ends); a 100 W panel is not one (6 % short on energy, ZBX-CAL-001 section 7); in the structure, mud brick or stabilized block if decision 4 allows, and racks of local poles in place of sawn timber.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-24 | D1: load-circuit cable protection. The STEM check found the 1.5 mm² load cable protected only by the 15 A battery fuse, above its 13.8 A capacity derated for a 45 °C roof space (S16). Options weighed: (a) a 5 A fuse on the load circuit and 2.5 mm² battery leads, about USD 1; (b) all load wiring in 2.5 mm² behind the 15 A fuse, about USD 4 more cable and stiffer cable at the small terminals; (c) relying on the charge controller's electronic load protection, not certain for every generic controller. Chosen: (a), the cheapest fix that is certain with generic parts. Made in BOM line 11, ZBX-CAL-001 s9, PR-009, the build plan's wiring section and the model (fuse holder in the power box) | Claude, under Amish's standing instruction of 2026-10-23 ("when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session"); Amish can reverse it | ZBX-STM-001 S16, ZBX-CAL-001 v0.4 s9 |
| 2026-10-24 | D4: details added in the D3 model, no design dimension changed. Pipe wall of the roof posts 3.2 mm; box-profile roof sheets 0.5 mm thick, 190 mm pitch, 24.5 mm deep, in four sheets across the 3.9 m; door built up from 12 mm plywood skins, a 50 x 50 mm frame and two insulation boards inside the 74 mm leaf; three 100 mm butt hinges; joist straps 30 x 2 mm, 300 mm long; hurricane ties 35 mm wide, 1.5 mm; coach screws M10 x 100 at 58 mm either side of each post on the cap plates; M8 stainless bolts on the panel frames; fixings and screws sized in the model's part names; outside sensor arm moved above the six-plate shield (it passed through the fourth plate as one solid in the TRL 3 model); inside sensor on the aisle face of the right rack's middle post, 1.5 m up, as the build plan's wiring section places it | Modelling detail within the decided design; recorded so Amish can see every new size | `cad/src/model.py`, `cad/src/zbx_parts.py` |
| 2026-10-24 | D5: fixes from the independent review of the STEM check. (a) Sump bleed sized for at most 4 cycles of concentration, 10.6 L a day in place of 4 L, so hard or silty water does not scale the pad; total water 43 L a day, still within PR-008 (STM S37; options weighed: a larger bleed, which costs only water, against softened or rain water, which the site may not have). (b) Both fuses DC rated with a breaking capacity above the battery's short-circuit current, the load fuse at the source end of its run (STM S16). (c) EPDM isolating washers under every stainless bolt on the aluminium panel frames (STM S30). (d) Controller logic: the pad pump stops for the last 60 min of each cooling day so the pad dries, and the fans run 10 min before anyone goes in (STM S27). No BOM price changes: (a) and (d) are operating rules, (b) and (c) are specifications within lines 11 and 18 (estimates, not quoted) | Claude, under Amish's standing instruction of 2026-10-23; Amish can reverse any item | ZBX-STM-001 Independent review, ZBX-CAL-001 v0.4 s8 and s9 |
| 2026-09-25 | TRL 2 review items 1 to 8: the USD 300 budget covers the cooling kit with the structure costed separately; 150 W panel; keep the battery; forced air through a pad; exhaust fans with the pad opposite; wet sand cavity pending the heat balance; 24 crates; control thresholds as starting values | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | ZBX-DDR-001 |
| 2026-09-25 | Items 11 to 13: 150 mm pad, R3 relaxed to 80 % with covered or lined crates; dry rice husk fill in place of wet sand (dry sand as fallback); 500 x 500 x 600 mm roof footings as a minimum | Amish: "i accept all your recommendations, go with them across all repos." | ZBX-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | ZBX-DDR-003 (the changes themselves await his review, open decision 1) |
| 2026-09-30 | Open decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | This register |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a spending limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | ZBX-CAL-001 v0.3, section 11 |
| 2026-10-02 | Design for construction accepted: the changes C1 to C10 of ZBX-DDR-003, as made | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | ZBX-DDR-003, Table 1 |
| 2026-10-02 | Fan position: the two fans stay in the ceiling fan box at the door end, as modelled | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | ZBX-DDR-003, A1 |
| 2026-10-02 | Exhaust into the roof space accepted, with a check at TRL 4 that moist air does not drift back to the pad; a short duct past the roof edge is added only if it does | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | ZBX-DDR-003, A2 |
| 2026-10-02 | Wall material: fired brick, as modelled and calculated | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | ZBX-DDR-001, item 9 |
| 2026-10-02 | First co-design partner, region and crop mix: a group that has already field-tested evaporative cooling chambers with vegetable growers; the first candidate to approach is MIT D-Lab's evaporative cooling team, with a dry-season vegetable area of Mali as the first candidate region and tomatoes, peppers and okra as the crop mix, leafy greens on a separate rack | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | ZBX-DDR-001, item 10 |
| 2026-10-02 | Clear window in the controller lid only; the power box has a plain door | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | REVIEW.md, 2026-09-26, item 2 |
| 2026-10-02 | Mode lamp on top of the controller box beside the door, added to the model | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | REVIEW.md, 2026-09-26, item 3 |
| 2026-10-02 | Outside sensor shield: stacked round plates 46 mm across | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | REVIEW.md, 2026-09-26, item 4 |
| 2026-10-02 | Plinth render band: an optional 10 mm finish 300 mm high, the mason's choice | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | REVIEW.md, 2026-09-26, item 5 |
| 2026-10-02 | Hose and conduit routing accepted as sketched in the build plan, routed on site | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | REVIEW.md, 2026-09-26, item 6 |
