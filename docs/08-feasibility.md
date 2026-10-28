---
doc_id: ZBX-FEA-001
title: ZeerBox feasibility assessment
project: ZeerBox
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First assessment (kit 1.9.1 upgrade) of the constructable design, option A
---

# ZeerBox feasibility assessment

On paper ZeerBox is feasible: the store cools about 10.7 K below the outside air on a hot, dry day with every number inside known science (ZBX-STM-001), it is built from bricks, timber and sheet by a mason and a carpenter, and its cooling kit costs about USD 300 against a USD 300 value-engineering target; the weakest points are humidity at the low end of its target, the assumed fan and pad curves, and the fact that nobody who would use it has yet been asked. Method: STANDARDS section 23.

Table 1. Feasibility by aspect (option A, the constructable design).

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Forced air through a 150 mm pad and an insulated store; 10.7 K drop (9.8 to 11.4 K), 24 crates, 43 L of water and 372 Wh a day | High | Store RH 81 % against 80 % (PR-003 at risk); the store runs at about 24 °C, well above the 12.5 to 15 °C tomatoes prefer, so it slows spoilage rather than stopping it | ZBX-STM-001 S1 to S9, ZBX-CAL-001 s3 to s5 |
| Materials | Fired brick, dry rice husk with lime, sawn timber, galvanised steel, a bought cellulose pad | High | Rice husk must be supplied dry and pest-free (dry sand is the fallback, about 0.3 K warmer); timber must be termite-treated; measured husk conductivity is a little above the assumed value (STM S23) | ZBX-DEC-001 to confirm 5, BOM lines 1 to 3 |
| Manufacturing and assembly | Masonry, carpentry and a 12 V installation in 26 build steps; no welding on site except the post cap plates, which a workshop does | High | Fan frame must fit the 310 mm fan box bay (to confirm 1); hurricane ties must be rated 2 kN (to confirm 4) | ZBX-BLD-001, ZBX-DDR-003 |
| Power and controls | One 150 W panel (41 % energy margin), a 154 Wh LiFePO4 battery, a microcontroller with two temperature and RH sensors and four modes | Medium | Fan curve and pad pressure drop are assumed (STM S3, S5); after about 40 h without sun the fans stop (STM S36, ZBX-DEC-001 D3); firmware is a labelled sketch only at TRL 3; load fuse corrected (D1) | ZBX-CAL-001 s6, s7, s9 |
| Structure | Wall bearing 16 kPa; post footings 1.8 times the uplift at a 30 m/s gust; beams and purlins at 5.2 to 5.3 MPa against about 7 MPa | High | Local design wind speed not confirmed (to confirm 6); the purlins work at about 74 % of their allowed stress (STM S18), the least margin in the frame | ZBX-CAL-001 s10 |
| Water and hygiene | 43 L a day, including an 11 L bleed against scale, from a 60 L covered sump; daily pad dry-out, weekly drain and clean (ZBX-DEC-001 D5) | Medium | *Legionella* and mold controls depend on users keeping the routine (RSK H3, H4) | ZBX-PRC-001 Safety, ZBX-REG-001 G9 |
| Supply of parts | Bricks, cement, timber and sheet locally; 12 V fans, pump, panel and battery from regional towns; cellulose pads from poultry or greenhouse suppliers, perhaps only in a regional city | Medium | Pad supply and price in Mali to assess; cited Indian listings put a 150 mm pad at about INR 460 a square foot (ZBX-MKT-001) | BOM, ZBX-MKT-001 |
| Users and partner | First candidate partner and region chosen (MIT D-Lab's evaporative cooling team, Mali); not yet approached | Low | Every requirement is a proposal until co-design sessions; whether users want a store for one farm or a group, and whether they need it in the rainy season, is unknown | ZBX-PRB-001, ZBX-URS-001 |

Ratings: High, Medium, Low.

Options B and C (ZBX-OPT-001) are more feasible to build and power (no electrics) but less feasible on performance: option B holds a full store only about 3 K below outside air at first order, and option C depends on wind and on a turbine ventilator whose airflow is to assess.
