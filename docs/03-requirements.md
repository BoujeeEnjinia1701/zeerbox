---
doc_id: ZBX-REQ-001
title: ZeerBox requirements
project: ZeerBox
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, design point and status against the concept
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Redefine R12 as the cooling equipment kit (ZBX-DDR-001 item 1); R7 on the decided 150 W panel; TRL 3 status from ZBX-CAL-001
---

# ZeerBox requirements

These requirements are checked by calculation in ZBX-CAL-001 at TRL 3. Seven are met (three of them by design or logic review only), R2 is at risk, **R3 is not met**, and R6, R10 and R11 cannot be verified at TRL 3. Targets are not yet validated with users and will be revised after co-design sessions (see ZBX-PRB-001).

The **design point** used throughout is outside air at 35 °C and 30 % RH (wet bulb 21.5 °C), a full store of 480 kg of mixed vegetables, and 100 kg of fresh produce loaded per day at 32 °C.

*Table 1. Requirements and TRL 3 status. Values are central estimates from ZBX-CAL-001, with the favorable to unfavorable range where it matters.*

| ID | Requirement | Target | Verification | TRL 3 status (ZBX-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Storage capacity | 20 or more standard 20 kg crates (400 kg or more) on shelves; one adult can walk in and reach every crate without lifting any crate above 1.6 m | Layout model; later loading trial | Met: 24 crates, 480 kg; top shelf 1.40 m above the floor |
| R2 | Cooling at the design point | Mean store air temperature 8 K or more below outside air | Psychrometric and heat balance calculation; later logged field data | **At risk:** 9.1 K (8.0 to 10.0 K); store 25.9 °C |
| R3 | Humidity for produce | Store RH 85 % or more while cooling, to limit water loss | Calculation; later logged field data | **Not met:** 71 % (66 to 76 %) |
| R4 | Behavior in humid weather | Controller detects outside air too humid to cool (wet-bulb depression under 4 K) and switches to night ventilation or hold, with a visible mode indicator | Controller logic review; later bench test with sensors | Met by logic review: 30 °C and 75 % RH gives 3.7 K and switches to hold |
| R5 | Mold and condensation guard | Pad pump stops if store RH stays above 95 % for 60 min; store air changes at least once per hour whenever produce is inside | Controller logic review | Met by logic review: hold mode gives about 8 air changes an hour at about 2 W |
| R6 | Shelf life | Tomato shelf life at least 1.5 times that of ambient storage in the dry season (for example 6 days to 9 days or more) | Literature comparison; later paired storage trial with the partner | Not verifiable at TRL 3; ZECC data (about 1.8 times) come from a cooler, more humid chamber |
| R7 | Solar operation | Fans, pump and controller run from one PV panel with no grid for a full design day: 10 h of cooling plus 2 h of evening ventilation | Energy balance | Met: 372 Wh needed, 525 Wh from the 150 W panel (41 % margin) |
| R8 | Water use | 70 L or less of water per design day, including pad and wall cavity; sump holds at least one day | Water balance | Met: about 44 L; 60 L sump for 32 L of pad and bleed water |
| R9 | Low-voltage and safe | All electrical parts at 12 V DC nominal, fused at the battery; fans guarded; door opens from inside without a key | Design review | Met by design review |
| R10 | Local build and repair | Walls, roof, door and shelves built by a local mason and carpenter; every fan, pump, sensor and pad replaceable in 30 min or less with generic parts | Design review; parts availability survey with the partner | Not verifiable at TRL 3 |
| R11 | Durability | Structure 10 years or more; pad 3 years or more with cleaning; fans and pump 3 years or more in dust | Material review; supplier data | Not verifiable at TRL 3; roof footings sized for uplift at 30 m/s |
| R12 | Affordable | Cooling equipment kit (pad, sump and pump, fans, controller, solar panel, power box, wiring: BOM items 6 to 11 and 14) $300 or less in parts (`project.yaml` budget). The structure (items 1 to 5 and 12) is built from local materials and costed separately | Priced BOM (`bom/bom.csv`) | Met: kit about $260; structure about $360, reported separately |

R12 was redefined on 2026-09-25 by Amish's decision to go with the TRL 2 recommendation (ZBX-DDR-001 item 1). Its earlier target, the complete store for $300, was not met at about $575.

## Assumptions

- Direct evaporative pad effectiveness of 75 % for a 100 mm cellulose pad at 0.6 m/s face velocity, scaled for velocity and depth in ZBX-CAL-001. Manufacturer data for deeper pads show 90 % or more ([CELdek specification](https://piec.com/celdek/)); 70 to 80 % is assumed for 100 mm.
- The fans are taken as a straight-line curve from 400 m³/h free air to a 50 to 70 Pa shut-off; pad pressure drop is 15 Pa at 1.0 m/s. Both need supplier data.
- The heat load at the design point is 418 W (333 to 598 W), from the heat balance in ZBX-CAL-001.
- Dry-season solar resource of about 5 peak sun hours, with 30 % combined losses for heat, dust, PWM charging and wiring.
- Tomato shelf life gains are taken from zero energy cool chamber trials, which run cooler and more humid than a forced-air store; R6 may be optimistic.
- Recommended produce conditions follow the UC Davis Postharvest Center (tomato 12.5 to 15 °C for mature green, 90 to 95 % RH). ZeerBox cannot reach these temperatures in the design case; R2 is set on temperature drop, not absolute temperature.

## Requirements not met or at risk at TRL 3

- **R3 (humidity), not met:** the supply air leaves a 100 mm pad at only 75 % RH and loses RH as it warms by 2.15 K across the store. A 150 mm pad gives 81 %; 85 % needs a pad about 180 mm deep or more. Options (a 150 mm pad, a relaxed target, produce-level measures) are proposed, awaiting Amish (ZBX-DDR-001 item 11).
- **R2 (cooling), at risk:** met in the central case (9.1 K) but on the limit in the unfavorable case (8.0 K). A 150 mm pad (10.5 K) or a dry insulating cavity fill (8.2 K unfavorable) restores margin (items 11 and 12).
