---
doc_id: ZBX-REQ-001
title: ZeerBox requirements
project: ZeerBox
doc_type: Requirements
version: "0.2"
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
---

# ZeerBox requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3 and revised after co-design sessions (see ZBX-PRB-001). The status column gives the TRL 2 estimate from ZBX-PRC-001; every value there is an estimate.

The **design point** used throughout is outside air at 35 °C and 30 % RH (wet bulb about 21.5 °C), a full store of 480 kg of mixed vegetables, and 100 kg of fresh produce loaded per day at 32 °C.

| ID | Requirement | Target | Verification (TRL 3 or later) | TRL 2 status (estimate) |
| --- | --- | --- | --- | --- |
| R1 | Storage capacity | 20 or more standard 20 kg crates (400 kg or more) on shelves; one adult can walk in and reach every crate without lifting any crate above 1.6 m | Layout model; later loading trial | Met: 24 crates, about 480 kg; top shelf at about 1.45 m |
| R2 | Cooling at the design point | Mean store air temperature 8 K or more below outside air | Psychrometric and heat balance calculation; later logged field data | Met: about 9 K (store about 26 °C) |
| R3 | Humidity for produce | Store RH 85 % or more while cooling, to limit water loss | Calculation; later logged field data | **Not met:** about 65 to 75 % at the full airflow |
| R4 | Behavior in humid weather | Controller detects outside air too humid to cool (wet-bulb depression under 4 K) and switches to night ventilation or hold, with a visible mode indicator | Controller logic review; later bench test with sensors | Met by design, unverified |
| R5 | Mold and condensation guard | Pad pump stops if store RH stays above 95 % for 60 min; store air changes at least once per hour whenever produce is inside | Controller logic review | Met by design, unverified |
| R6 | Shelf life | Tomato shelf life at least 1.5 times that of ambient storage in the dry season (for example 6 days to 9 days or more) | Literature comparison; later paired storage trial with the partner | Plausible (ZECC data show about 1.8 times), unverified |
| R7 | Solar operation | Fans, pump and controller run from one PV panel with no grid for a full design day: 10 h of cooling plus 2 h of evening ventilation | Energy balance | **At risk:** about 350 Wh needed, about 350 Wh available from 100 W; no margin |
| R8 | Water use | 70 L or less of water per design day, including pad and wall cavity; sump holds at least one day | Water balance | Met: about 55 L; 60 L sump |
| R9 | Low-voltage and safe | All electrical parts at 12 V DC nominal, fused at the battery; fans guarded; door opens from inside without a key | Design review | Met by design |
| R10 | Local build and repair | Walls, roof, door and shelves built by a local mason and carpenter; every fan, pump, sensor and pad replaceable in 30 min or less with generic parts | Design review; parts availability survey with the partner | Met by design, unverified |
| R11 | Durability | Structure 10 years or more; pad 3 years or more with cleaning; fans and pump 3 years or more in dust | Material review; supplier data | Unverified |
| R12 | Affordable | Complete store, including structure, $300 or less in parts (from `project.yaml` budget) | Priced BOM (`bom/bom.csv`) | **Not met:** about $575 in total; the equipment kit alone is about $235 |

## Assumptions

- Direct evaporative pad effectiveness of 75 % for a 100 mm cellulose pad at about 0.6 m/s face velocity. Manufacturer data for deeper pads show 90 % or more ([CELdek specification](https://piec.com/celdek/)); 70 to 80 % is assumed for 100 mm.
- The produce and the store fabric together gain about 550 W at the design point (heat balance in ZBX-PRC-001).
- Dry-season solar resource of about 5 peak sun hours, with 30 % combined losses for heat, dust, PWM charging and wiring.
- Tomato shelf life gains are taken from zero energy cool chamber trials, which run cooler and more humid than a forced-air store; R6 may be optimistic.
- Recommended produce conditions follow the UC Davis Postharvest Center (tomato 12.5 to 15 °C for mature green, 90 to 95 % RH). ZeerBox cannot reach these temperatures in the design case; R2 is set on temperature drop, not absolute temperature.

## Requirements not met at TRL 2

- **R3 (humidity):** forced air at the flow needed to carry 550 W warms by about 2.6 K from supply to exhaust, and RH falls as it warms. Options for TRL 3: wet the inner brick leaf as well as the cavity, cut airflow at night, or add a humidifying wet curtain inside the pad.
- **R7 (solar):** the 100 W panel matches the design-day load with no margin. Options: 150 W panel (about $20 more), cooling only while the sun is up, or fan speed control.
- **R12 (cost):** the walk-in structure costs more than the whole budget. Options are in `docs/REVIEW.md`, proposed, awaiting Amish.
