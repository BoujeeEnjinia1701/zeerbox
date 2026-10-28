---
doc_id: ZBX-PRS-001
title: ZeerBox product requirements and specifications
project: ZeerBox
doc_type: Product requirements and specifications
version: "0.6"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold (as ZBX-REQ-001)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, design point and status against the concept
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Redefine R12 as the cooling equipment kit (ZBX-DDR-001 item 1); R7 on the decided 150 W panel; TRL 3 status from ZBX-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R3 relaxed to 80 %; status from ZBX-CAL-001 v0.2 (150 mm pad, dry rice husk fill)
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: Status from ZBX-CAL-001 v0.3 after the design for construction (ZBX-DDR-003); R12 reported against the value-engineering target
- version: "0.6"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: ZBX-REQ-001 becomes ZBX-PRS-001; R1 to R12 migrated to PR-001 to PR-012 with the same targets, each traced to a user requirement in ZBX-URS-001, with tolerance, units and verification TRL; PR-009 names the 5 A load fuse (ZBX-DEC-001 D1); PR-012 at the target after it"
---

# ZeerBox product requirements and specifications

What the design must do, each traced to a user need in ZBX-URS-001 and checked by calculation in ZBX-CAL-001 v0.4 on the constructable design (option A, ZBX-OPT-001). Seven are met on paper (three of them by design or logic review only), the kit cost (PR-012) is at its value-engineering target, **PR-003 is at risk**, none is not met, and PR-006, PR-010 and PR-011 can only be verified at TRL 4. Targets are proposals and are not yet validated with users; they will be revised after co-design sessions with the partner (ZBX-PRB-001). The "Was" column gives the requirement's number in ZBX-REQ-001, which the calculation note still uses. Method: STANDARDS section 22.

The **design point** used throughout is outside air at 35 °C and 30 % RH (wet bulb 21.5 °C), a full store of 480 kg of mixed vegetables, and 100 kg of fresh produce loaded per day at 32 °C.

Table 1. Product requirements and specifications. Values are central estimates from ZBX-CAL-001 v0.4, with the favorable to unfavorable range where it matters.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001, UR-002 | Physical architecture | Storage capacity and reach | The store shall hold standard 20 kg crates on shelves, every crate reachable by one adult walking in, with no crate lifted above 1.6 m | 20 crates (400 kg); top shelf 1.6 m | min; max | crates; m | Analysis of the model (CAL-001 s2), TRL 3; loading trial, TRL 4 | Met on paper: 24 crates, 480 kg; top shelf 1.40 m | R1 |
| PR-002 | UR-003 | Performance | Cooling at the design point | Mean store air shall be below outside air at the design point by at least the target | 8 | min, unfavorable case | K | Psychrometric and heat balance (CAL-001 s4), TRL 3; logged field data, TRL 4 | Met on paper: 10.7 K (9.8 to 11.4 K); store 24.3 °C | R2 |
| PR-003 | UR-004 | Performance | Humidity for produce | Mean store RH while cooling shall reach the target; leafy and water-sensitive produce goes in covered or lined crates | 80 | min, unfavorable case | % RH | Calculation (CAL-001 s5), TRL 3; logged field data, TRL 4 | At risk: 81 % (77 to 85 %) | R3 |
| PR-004 | UR-005 | Software | Humid-weather detection and mode lamp | The controller shall detect outside air too humid to cool and switch to night ventilation or hold, showing the mode on a lamp by the door | Switch below 4 K wet-bulb depression | +-1 K sensing error | K | Logic review (CAL-001 s6), TRL 3; bench test with sensors, TRL 4 | Met by logic review: 30 °C and 75 % RH gives 3.7 K and switches to hold; sensing error 0.5 K (STM S32) | R4 |
| PR-005 | UR-006 | Safety | Mold and air-quality guard | The pad pump shall stop if store RH stays above 95 % for 60 min, and the store air shall change at least once an hour whenever produce is inside | 1 | min | air changes per hour | Logic review (CAL-001 s6), TRL 3; bench test, TRL 4 | Met by logic review: hold mode about 8 air changes an hour at about 2 W; with no power for more than about 40 h the fans stop (STM S36, ZBX-DEC-001 D3) | R5 |
| PR-006 | UR-007 | Performance | Shelf life | Tomato shelf life shall be at least the target multiple of ambient storage in the dry season (for example 6 days to 9 days or more) | 1.5 | min | x ambient | Literature comparison, TRL 3; paired storage trial with the partner, TRL 4 | To verify at TRL 4: ZECC data (about 1.8 times) come from a cooler, more humid chamber | R6 |
| PR-007 | UR-008 | Electrical | Solar operation | Fans, pump and controller shall run from one PV panel with no grid for a full design day: 10 h of cooling plus 2 h of evening ventilation | 372 | min, energy available | Wh/day | Energy balance (CAL-001 s7), TRL 3 | Met on paper: 525 Wh from the 150 W panel (41 % margin) | R7 |
| PR-008 | UR-009 | Performance | Water use and sump | Water use per design day, pad and any wall cavity included, shall not exceed the target; the sump shall hold at least one day of pad and bleed water | 70 | max | L/day | Water balance (CAL-001 s8), TRL 3 | Met on paper: about 43 L (no cavity water; 11 L bleed, ZBX-DEC-001 D5); 60 L sump for 43 L | R8 |
| PR-009 | UR-010 | Safety | Low voltage and safe | All electrical parts shall run at 12 V DC nominal, the battery leads fused at the terminal and the load circuit fused within its cable's capacity; fans guarded both faces; the door shall open from inside without a key | 12 V DC; fuse at or below the derated cable capacity | as stated | V; A | Design review (CAL-001 s9), TRL 3 | Met by design review: 15 A battery fuse on 2.5 mm² leads, 5 A load fuse on the 1.5 mm² load circuit, both DC rated (ZBX-DEC-001 D1, D5) | R9 |
| PR-010 | UR-011, UR-012 | Physical architecture | Local build and repair | Walls, roof, door and shelves shall be built by a local mason and carpenter; every fan, pump, sensor and pad shall be replaceable with generic parts in the target time | 30 | max per part | min | Design review, TRL 3; parts survey and swap trials with the partner, TRL 4 | To verify at TRL 4 | R10 |
| PR-011 | UR-013 | Materials | Durability | The structure shall last the target life; pad, fans and pump at least 3 years with cleaning, in dust | 10 | min, structure | years | Material review and structural checks (CAL-001 s10), TRL 3; supplier data and field life, TRL 4 | To verify at TRL 4; roof footings 1.8 times the uplift at 30 m/s; beams and purlins sized | R11 |
| PR-012 | UR-014 | Cost | Affordable kit | The cooling equipment kit (pad, sump and pump, fans, controller, solar panel, power box, wiring and panel frames: BOM items 6 to 11, 14 and 18) shall be priced against the value-engineering target in `project.yaml`; the structure (items 1 to 5, 12, 15, 16 and 17) is built from local materials and costed separately | 300 | value-engineering target, not a limit | USD | Priced BOM (`bom/bom.csv`), CAL-001 s11, TRL 3 | At the target: kit USD 300; structure USD 574, reported separately | R12 |

Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

PR-012 (R12) was redefined on 2026-09-25 by Amish's decision to go with the TRL 2 recommendation (ZBX-DDR-001 item 1). Its earlier target, the complete store for $300, was not met at about $575. Since 2026-10-01 the USD 300 figure is a hypothetical value-engineering target, not a limit (Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens"), so PR-012 is reported as over, under or at the target.

PR-003 (R3) was relaxed from 85 % to 80 % on 2026-09-25 by Amish's decision to go with the TRL 3 recommendation (ZBX-DDR-002, item 11), together with a 150 mm pad and produce-level measures (covered or lined crates). At 85 % it would still not be met: the store averages 81 % and 85 % needs a pad about 185 mm deep or more.

## Assumptions

- Direct evaporative pad effectiveness of 75 % for a 100 mm cellulose pad at 0.6 m/s face velocity, scaled for velocity and depth in ZBX-CAL-001; about 88 % for the decided 150 mm pad at 0.52 m/s. Manufacturer data for deeper pads show 90 % or more ([CELdek specification](https://piec.com/celdek/)); 70 to 80 % is assumed for 100 mm.
- The fans are taken as a straight-line curve from 400 m³/h free air to a 50 to 70 Pa shut-off; pad pressure drop is 15 Pa at 1.0 m/s. Both need supplier data (STEM check S3 and S5).
- The heat load at the design point is 443 W (376 to 559 W), from the heat balance in ZBX-CAL-001.
- Dry rice husk in the wall cavity conducts about 0.06 W/(m·K) and is kept dry and pest-free; measured values of 0.065 to 0.075 W/(m·K) add about 15 W of wall gain (STEM check S23).
- Dry-season solar resource of about 5 peak sun hours, with 30 % combined losses for heat, dust, PWM charging and wiring.
- Tomato shelf life gains are taken from zero energy cool chamber trials, which run cooler and more humid than a forced-air store; PR-006 may be optimistic.
- Recommended produce conditions follow the UC Davis Postharvest Center (tomato 12.5 to 15 °C for mature green, 90 to 95 % RH). ZeerBox cannot reach these temperatures in the design case; PR-002 is set on temperature drop, not absolute temperature.

## Requirements not met or at risk at TRL 3

- **PR-003 (humidity), at risk:** the 150 mm pad supplies air at 87 % RH, and the store averages 81 % in the central case but 77 % in the unfavorable case, against 80 %. The air loses about 4 to 5 percentage points of RH per kelvin as it warms across the store. Covered or lined crates hold humidity near the produce; field data will show whether they are enough.
- No requirement is not met. PR-005 holds only while the battery has charge: after about 40 h with no sun the fans stop and the room is sealed (STEM check S36); a passive vent for that case is proposed to Amish (ZBX-DEC-001 D3).
