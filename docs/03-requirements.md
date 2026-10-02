---
doc_id: ZBX-REQ-001
title: ZeerBox requirements
project: ZeerBox
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-10-02'
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
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R3 relaxed to 80 %; status from ZBX-CAL-001 v0.2 (150 mm pad, dry rice husk fill)
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: Status from ZBX-CAL-001 v0.3 after the design for construction (ZBX-DDR-003); R12 reported against the value-engineering target
---

# ZeerBox requirements

These requirements are checked by calculation in ZBX-CAL-001 v0.3 at TRL 3, after the design was made constructable (ZBX-DDR-003). Seven are met (three of them by design or logic review only), the kit cost (R12) is USD 1 under its value-engineering target, **R3 is at risk**, none is not met, and R6, R10 and R11 cannot be verified at TRL 3. Targets are not yet validated with users and will be revised after co-design sessions (see ZBX-PRB-001).

The **design point** used throughout is outside air at 35 °C and 30 % RH (wet bulb 21.5 °C), a full store of 480 kg of mixed vegetables, and 100 kg of fresh produce loaded per day at 32 °C.

*Table 1. Requirements and TRL 3 status. Values are central estimates from ZBX-CAL-001 v0.3, with the favorable to unfavorable range where it matters.*

| ID | Requirement | Target | Verification | TRL 3 status (ZBX-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Storage capacity | 20 or more standard 20 kg crates (400 kg or more) on shelves; one adult can walk in and reach every crate without lifting any crate above 1.6 m | Layout model; later loading trial | Met: 24 crates, 480 kg; top shelf 1.40 m above the floor |
| R2 | Cooling at the design point | Mean store air temperature 8 K or more below outside air | Psychrometric and heat balance calculation; later logged field data | Met: 10.7 K (9.8 to 11.4 K); store 24.3 °C |
| R3 | Humidity for produce | Store RH 80 % or more while cooling, to limit water loss; covered or lined crates for leafy and water-sensitive produce | Calculation; later logged field data | **At risk:** 81 % (77 to 85 %) |
| R4 | Behavior in humid weather | Controller detects outside air too humid to cool (wet-bulb depression under 4 K) and switches to night ventilation or hold, with a visible mode indicator | Controller logic review; later bench test with sensors | Met by logic review: 30 °C and 75 % RH gives 3.7 K and switches to hold |
| R5 | Mold and condensation guard | Pad pump stops if store RH stays above 95 % for 60 min; store air changes at least once per hour whenever produce is inside | Controller logic review | Met by logic review: hold mode gives about 8 air changes an hour at about 2 W |
| R6 | Shelf life | Tomato shelf life at least 1.5 times that of ambient storage in the dry season (for example 6 days to 9 days or more) | Literature comparison; later paired storage trial with the partner | Not verifiable at TRL 3; ZECC data (about 1.8 times) come from a cooler, more humid chamber |
| R7 | Solar operation | Fans, pump and controller run from one PV panel with no grid for a full design day: 10 h of cooling plus 2 h of evening ventilation | Energy balance | Met: 372 Wh needed, 525 Wh from the 150 W panel (41 % margin) |
| R8 | Water use | 70 L or less of water per design day, including pad and wall cavity; sump holds at least one day | Water balance | Met: about 36 L (no cavity water); 60 L sump for 36 L of pad and bleed water |
| R9 | Low-voltage and safe | All electrical parts at 12 V DC nominal, fused at the battery; fans guarded; door opens from inside without a key | Design review | Met by design review |
| R10 | Local build and repair | Walls, roof, door and shelves built by a local mason and carpenter; every fan, pump, sensor and pad replaceable in 30 min or less with generic parts | Design review; parts availability survey with the partner | Not verifiable at TRL 3 |
| R11 | Durability | Structure 10 years or more; pad 3 years or more with cleaning; fans and pump 3 years or more in dust | Material review; supplier data | Not verifiable at TRL 3; roof footings 1.8 times the uplift at 30 m/s, 500 mm kept as a minimum (ZBX-DDR-002); roof beams and purlins sized (ZBX-CAL-001 v0.3) |
| R12 | Affordable | Cooling equipment kit (pad, sump and pump, fans, controller, solar panel, power box, wiring and panel frames: BOM items 6 to 11, 14 and 18) priced against the USD 300 value-engineering target (`project.yaml` budget). The structure (items 1 to 5, 12, 15, 16 and 17) is built from local materials and costed separately | Priced BOM (`bom/bom.csv`) | Value-engineering target: USD 300 for the kit. Estimated cost of the constructable design: USD 299 (USD 1 under the target); structure USD 574, reported separately |

R12 was redefined on 2026-09-25 by Amish's decision to go with the TRL 2 recommendation (ZBX-DDR-001 item 1). Its earlier target, the complete store for $300, was not met at about $575. Since 2026-10-01 the USD 300 figure is a hypothetical value-engineering target, not a limit (Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens"), so R12 is reported as over or under the target.

R3 was relaxed from 85 % to 80 % on 2026-09-25 by Amish's decision to go with the TRL 3 recommendation (ZBX-DDR-002, item 11), together with a 150 mm pad and produce-level measures (covered or lined crates). At 85 % R3 would still not be met: the store averages 81 % and 85 % needs a pad about 185 mm deep or more.

## Assumptions

- Direct evaporative pad effectiveness of 75 % for a 100 mm cellulose pad at 0.6 m/s face velocity, scaled for velocity and depth in ZBX-CAL-001; about 88 % for the decided 150 mm pad at 0.52 m/s. Manufacturer data for deeper pads show 90 % or more ([CELdek specification](https://piec.com/celdek/)); 70 to 80 % is assumed for 100 mm.
- The fans are taken as a straight-line curve from 400 m³/h free air to a 50 to 70 Pa shut-off; pad pressure drop is 15 Pa at 1.0 m/s. Both need supplier data.
- The heat load at the design point is 442 W (376 to 558 W), from the heat balance in ZBX-CAL-001 v0.2.
- Dry rice husk in the wall cavity conducts about 0.06 W/(m·K) and is kept dry and pest-free (assumption).
- Dry-season solar resource of about 5 peak sun hours, with 30 % combined losses for heat, dust, PWM charging and wiring.
- Tomato shelf life gains are taken from zero energy cool chamber trials, which run cooler and more humid than a forced-air store; R6 may be optimistic.
- Recommended produce conditions follow the UC Davis Postharvest Center (tomato 12.5 to 15 °C for mature green, 90 to 95 % RH). ZeerBox cannot reach these temperatures in the design case; R2 is set on temperature drop, not absolute temperature.

## Requirements not met or at risk at TRL 3

- **R3 (humidity), at risk:** the 150 mm pad supplies air at 87 % RH, and the store averages 81 % in the central case but 77 % in the unfavorable case, against 80 %. The air loses about 4 to 5 percentage points of RH per kelvin as it warms across the store. Covered or lined crates hold humidity near the produce; field data will show whether they are enough.
- No requirement is not met. R2 moved from at risk to met (10.7 K, 9.8 K unfavorable) with the 150 mm pad and dry rice husk fill (ZBX-DDR-002, items 11 and 12).
