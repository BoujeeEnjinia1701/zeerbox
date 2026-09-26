---
doc_id: ZBX-CAL-001
title: ZeerBox sizing and first-principles checks
project: ZeerBox
doc_type: Calculation note
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (psychrometrics, fan and pad operating point, heat balance, humidity, off-design weather, energy, water, electrical, structure, cost) against every requirement
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). 150 mm pad, dry rice husk cavity fill, R3 at 80 %; all figures rerun
---

# ZeerBox sizing and first-principles checks

On paper the store cools as the concept claims, with margin on temperature and humidity close to the relaxed target. This version (v0.2) applies the decisions in ZBX-DDR-002: a 150 mm pad in place of 100 mm, a dry rice husk cavity fill in place of wet sand, and R3 relaxed from 85 % to 80 %. At the design point of 35 °C and 30 % RH, the two 250 mm fans deliver about 563 m³/h (331 cfm) through the 150 mm pad, the supply air leaves the pad at 23.1 °C and 87 % RH, and the store averages **24.3 °C, 10.7 K below the outside air** (v0.1: 25.9 °C and 9.1 K). Eight of the twelve requirements are met (three of them by design review or logic review only), one is at risk, none is not met, and three cannot be verified at TRL 3. **R3 (store RH 80 % or more) is at risk:** the store averages about 81 % RH in the central case but 77 % in the unfavorable case. R2 is now met in every case (9.8 to 11.4 K). The dry fill also removes the cavity's water use, so the store needs about 36 L of water a day (v0.1: 44 L).

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry from `PARAMS` in `cad/src/model.py`, the prices from `bom/bom.csv` and the budget from `project.yaml`, so the model, drawing ZBX-DWG-001 and this note agree. All values are first-principles estimates; nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design unless marked as decided.*

| Input | Value | Basis |
| --- | --- | --- |
| Architecture | Forced air, exhaust fans with the pad on the opposite wall, dry rice husk cavity fill, 24 crates, 150 W panel with a LiFePO4 battery | Decided, ZBX-DDR-001 items 2 to 5 and 7; ZBX-DDR-002 item 12 (fill) |
| Design point | 35 °C, 30 % RH, sea-level pressure (101.325 kPa); 480 kg of produce inside; 100 kg loaded per day at 32 °C | ZBX-REQ-001 |
| Psychrometrics | ASHRAE saturation pressure over water and the ASHRAE humidity-ratio relation for the thermodynamic wet bulb | ASHRAE *Fundamentals* (2017), chapter 1 |
| Pad | 150 mm cellulose (decided, ZBX-DDR-002 item 11), 0.6 x 0.5 m (0.3 m²); saturation effectiveness of a 100 mm pad 80, 75 or 70 % at 0.6 m/s, scaled with depth and with face velocity to the power -0.2 (NTU model); wet pressure drop 15 Pa at 1.0 m/s, proportional to depth and to velocity to the power 1.8 | TRL 2 assumption for effectiveness; pressure drop is an assumption to confirm with the pad supplier's chart |
| Fans | Two 250 mm 12 V DC axial fans, each 400 m³/h free air and 12 W; straight-line fan curve to a shut-off pressure of 70, 60 or 50 Pa | BOM line 8; shut-off pressure is an assumption to confirm with the fan's curve |
| Other airflow losses | Gravity shutters 5 Pa to hold open; guards and shutters four velocity heads at the fan openings | Allowance |
| Walls | Two 115 mm fired-brick leaves, k 0.70 W/(m·K); 75 mm cavity of dry rice husk (k 0.06, decided), dry sand (k 0.30, fallback) or wet sand (k 1.5, v0.1); inside and outside film resistances 0.13 and 0.04 m²·K/W | Typical handbook values; the rice husk conductivity is an assumption |
| Wet cavity (comparison only) | Cavity held at the outside temperature minus 60, 50 or 30 % of the wet-bulb depression | ZECC field data show 4 to 7 K below ambient; the fraction is an assumption |
| Ceiling, floor, door | 50 mm straw (k 0.06) on boards, air under the shade roof at 38, 40 or 43 °C; brick floor on sand to ground at 28, 30 or 32 °C; door with 50 mm insulation (k 0.04) | Allowance for a shaded, ventilated roof space |
| Produce | Respiration heat 0.10, 0.15 or 0.25 W/kg near 26 °C (mixed tomatoes, peppers and greens); water loss 0.5, 1 or 2 % of mass per day; specific heat 3.9 kJ/(kg·K); field heat removed over 8 h | Respiration heat of about 3 mW per mg CO₂/(kg·h) from glucose oxidation |
| Door openings and leaks | 30, 50 or 80 W; sun on the end walls at low sun angles 0, 20 or 60 W | Allowance |
| Solar | 5 peak sun hours; 30 % combined loss (heat, dust, PWM charging, wiring) | As TRL 2 |
| Loads | Fans 12 W each at full speed (taken as constant), pump 6 W for the 10 h of cooling, controller 1 W for 24 h | As TRL 2, controller now counted all day |
| Structure | Brick 1,800 kg/m³, dry rice husk 120 kg/m³, concrete 23.5 kN/m³; roof uplift at a 30 m/s gust with a net pressure coefficient of 1.5 on an open canopy | Assumptions; confirm the local design wind speed |

Three scenarios bracket the result: **favorable**, **central** and **unfavorable**, taking the first, second and third value where Table 1 gives three. Central values are quoted unless a range is given.

## 2. Geometry and capacity (R1)

The room is 2,400 x 1,500 x 2,000 mm inside (7.2 m³) and 3,010 x 2,110 mm outside. Two racks, 2,200 x 450 mm, carry three shelves each with tops at 0.30, 0.85 and 1.40 m above the floor, four crates per shelf, so the store holds **24 crates (480 kg)** with a 600 mm aisle. The top crate reaches 1.70 m and leaves 0.30 m to the ceiling. Each shelf is carried by two 50 x 75 mm timber rails spanning 1.05 m between legs; four loaded crates (22 kg each) give 196 N/m, a bending stress of 0.58 MPa and a deflection of 0.20 mm, well inside softwood limits. R1 is **met**.

## 3. Fan and pad operating point

With both fans against the 150 mm pad, the shutters and the guards, the operating point is **563 m³/h at 17.8 Pa** (534 to 585 m³/h). The deeper pad adds pressure drop, so airflow falls from the 584 m³/h of the 100 mm pad in v0.1. Face velocity at the pad is 0.52 m/s and the pad effectiveness rises to 88.2 % (84.7 to 91.5 %), against 75.7 % for 100 mm. The air changes about 78 times an hour. Each fan delivers about 280 m³/h, 70 % of its free-air rating, which is a normal operating point for a small axial fan but must be checked against the chosen fan's curve.

## 4. Design point, heat balance and store temperature (R2)

*Table 2. Air states at the design point, central case.*

| State | Temperature | RH | Humidity ratio |
| --- | --- | --- | --- |
| Outside | 35.0 °C | 30 % | 10.5 g/kg |
| Wet bulb | 21.5 °C | | depression 13.5 K |
| Supply, after the pad | 23.1 °C | 87 % | |
| Store mean | 24.3 °C | 81 % | |
| Exhaust | 25.5 °C | 77 % | |

*Table 3. Heat gains at the design point, central case.*

| Gain | W | Basis |
| --- | --- | --- |
| Walls, dry rice husk cavity | 84 | U 0.57 W/(m²·K) from outside air to room over 13.8 m² net |
| Sun on the end walls | 20 | Allowance |
| Ceiling | 46 | U 0.82 W/(m²·K), 3.6 m², air under the roof at 40 °C |
| Floor | 55 | U 2.68 W/(m²·K), 3.6 m², ground at 30 °C |
| Door leaf | 10 | U 0.62 W/(m²·K), 1.44 m² |
| Produce respiration | 72 | 480 kg x 0.15 W/kg |
| Field heat | 104 | 100 kg from 32 °C, over 8 h |
| Door openings and leaks | 50 | Allowance |
| **Total** | **442** | 376 W favorable, 558 W unfavorable |

The 442 W warms the 563 m³/h airstream by 2.35 K, so the store averages 24.3 °C, **10.7 K below the outside air** (9.8 to 11.4 K). R2 (8 K or more) is **met** in every case. The heat load is higher than in v0.1 (418 W) because the cooler store draws more heat through the ceiling and floor and from the day's warm produce; the deeper pad more than makes up for it.

### 4.1 Pad depth and cavity fill

*Table 4. Pad and wall options at the design point.*

| Option | Wall gain, central | Store drop, central (range) | Store RH, central (range) | Cavity water |
| --- | --- | --- | --- | --- |
| 100 mm pad, wet sand (v0.1) | 103 W | 9.1 K (8.0 to 10.0 K) | 71 % (66 to 76 %) | about 12 L/day |
| 100 mm pad, rice husk | 72 W | 9.2 K (8.2 to 10.0 K) | 71 % (67 to 76 %) | none |
| 150 mm pad, wet sand | 163 W | 10.5 K (9.4 to 11.3 K) | 81 % (75 to 85 %) | about 12 L/day |
| 150 mm pad, dry sand (fallback) | 192 W | 10.5 K (9.6 to 11.1 K) | 80 % (76 to 84 %) | none |
| **150 mm pad, rice husk (decided)** | **84 W** | **10.7 K (9.8 to 11.4 K)** | **81 % (77 to 85 %)** | **none** |

The deeper pad does most of the work: it adds about 1.5 K of cooling and 10 percentage points of RH. The dry rice husk fill adds a further 0.2 to 0.4 K over wet or dry sand and needs no water. Wet sand conducts about five times better than dry sand, so a wet cavity helps only while evaporation holds it well below the outside air, and with the cooler store of the 150 mm pad it lets in more heat than the husk. The husk must stay dry and be protected from termites and rodents: it sits on a damp-proof course, is mixed with hydrated lime, and is capped with mortar (BOM line 2). If no durable, pest-proof husk supply exists locally, dry sand is the fallback at a cost of about 0.3 K.

## 5. Humidity (R3)

R3 was relaxed from 85 % to 80 % by ZBX-DDR-002 (item 11). The store averages about **81 % RH** (77 to 85 %) while cooling. R3 is **at risk**: met in the central and favorable cases, short by about 3 percentage points in the unfavorable case.

- The supply air leaving the 150 mm pad is 87 % RH (v0.1: 75 % with 100 mm).
- To average 85 % at the central temperature rise of 2.35 K, the pad would need about 93 % effectiveness, a pad about 185 mm deep or more, before the lower airflow of a deeper pad.
- Produce transpiration adds only about 0.3 g/kg to the airstream at this airflow, worth about 1 percentage point of RH in the store, so the produce cannot humidify the store itself.

The limit is the architecture: a once-through airstream that must carry the store's heat warms as it goes, and its RH falls about 4 to 5 percentage points per kelvin. The accepted recommendation pairs the deeper pad with produce-level measures: covered or lined crates for leafy and water-sensitive produce, which hold humidity near the produce. These are an operating practice with user-supplied liners and are not costed in the kit.

## 6. Off-design weather and control (R4, R5)

*Table 5. Store in evaporative mode at other outside conditions, central case.*

| Outside | Wet-bulb depression | Supply | Store | Drop | Store RH | Controller mode |
| --- | --- | --- | --- | --- | --- | --- |
| 35 °C, 30 % RH | 13.5 K | 23.1 °C | 24.3 °C | 10.7 K | 81 % | Evaporative cooling |
| 38 °C, 15 % RH | 18.8 K | 21.4 °C | 22.8 °C | 15.2 K | 75 % | Evaporative cooling |
| 32 °C, 50 % RH | 8.3 K | 24.6 °C | 25.6 °C | 6.4 K | 87 % | Evaporative cooling |
| 30 °C, 60 % RH | 6.2 K | 24.5 °C | 25.5 °C | 4.5 K | 89 % | Evaporative cooling |
| 30 °C, 75 % RH | 3.7 K | 26.7 °C | 27.5 °C | 2.5 K | 93 % | Hold by day, night ventilation |

The decided 4 K wet-bulb depression threshold switches the store to hold at 30 °C and 75 % RH, where the pad would give only about 2.5 K of cooling at 93 % RH. R4 is **met** by logic review. In hold mode one fan at 30 % speed moves about 57 m³/h, about 8 air changes an hour, for about 2 W including driver losses, so the minimum of one air change an hour in R5 is easy to hold. With the 95 % RH pump stop, R5 is **met** by logic review. Both need a bench test with sensors later (TRL 4, on hold).

## 7. Energy and solar (R7)

*Table 6. Design-day energy.*

| Load | Energy |
| --- | --- |
| Fans, 24 W for 10 h of cooling and 2 h of evening ventilation | 288 Wh |
| Pump, 6 W for 10 h | 60 Wh |
| Controller and sensors, 1 W for 24 h | 24 Wh |
| **Total** | **372 Wh/day**, peak load 31 W |

The decided 150 W panel yields 525 Wh/day, a **41 % margin**; R7 is **met**. The 100 W panel of TRL 2 would fall 6 % short once the controller is counted all day. After sunset the evening ventilation and the controller need 62 Wh, half of the battery's usable 123 Wh (12.8 V x 12 Ah x 80 %). Full-speed night ventilation can therefore run only about 2.5 h beyond the evening run; the controller must run night ventilation at reduced speed or limit its hours.

Two sizing corrections follow from the larger panel and are now in the BOM:

- The 150 W panel's short-circuit current is about 9 A, and 1.25 x Isc is 11.2 A, so the 10 A PWM charge controller of TRL 2 is too small. The BOM now specifies 20 A.
- On a 6 m run, 1.5 mm² cable drops 1.14 V (6.5 % of Vmp) and loses 9.5 W at 8.3 A; 2.5 mm² cable drops 0.69 V (3.9 %). The BOM now specifies 2.5 mm² for the panel run.

The charge current of up to 8.3 A is 0.69 C for the 12 Ah battery, so its BMS must allow at least 10 A of charge.

## 8. Water (R8)

The 150 mm pad evaporates 3.19 kg/h, **32 L** over the 10 h cooling day (29 to 35 L), about 4 L more than the 100 mm pad because it cools the air further. The dry rice husk cavity needs no water (v0.1: about 12 L/day for the wet sand). With 4 L of bleed and cleaning the total is **about 36 L/day** (v0.1: 44 L), and R8 (70 L or less) is **met**. The sump holds 68 L gross and 60 L working, which covers the 36 L of pad and bleed water for a full day.

The pad needs about 3.6 L/min to stay wet (6 L/min per m of pad length, a typical supplier figure to confirm). Lifting that 2 m takes 1.2 W of hydraulic power, or about 6 W at a small pump's 20 % efficiency, which matches the 6 W pump in the BOM.

## 9. Electrical (R9, R10)

The full load draws 2.4 A at 12.8 V and the panel charges at up to 8.3 A; the 15 A fuse at the battery terminal sits above both and below the cable ratings. Every electrical part runs at 12 V DC, the fans are guarded on both faces and the door opens from inside. R9 is **met** by design review. R10 (local build and 30 min part swaps) depends on a parts survey and swap trials with a partner and is **not verifiable at TRL 3**.

## 10. Structure (R11)

The walls need about 1,977 bricks with 10 % waste (1,677 for the walls, 120 for the floor), 3.9 m³ of brickwork weighing about 7.1 t, and 1.3 m³ of dry rice husk weighing about 0.15 t (v0.1: 2.4 t of wet sand). That puts about 7.1 kN/m on the foundations, or about 16 kPa on a 450 mm strip, well below the 100 kPa or more of firm soils.

The shade roof is the structural risk. At a 30 m/s gust the net uplift on the 11.7 m² roof is about 9.5 kN, or 2.23 kN per post after the sheet weight. A 400 x 400 x 600 mm concrete footing weighs only 2.26 kN, a factor of 1.01. The model and BOM use **500 x 500 x 600 mm footings** (3.52 kN, a factor of 1.58), kept as a minimum by ZBX-DDR-002 (item 13). The local design wind speed must be confirmed with a builder at the chosen site; squall lines in the Sahel can exceed 30 m/s. Pad, fan and pump life depend on supplier data and dust exposure, so R11 is **not verifiable at TRL 3**.

## 11. Cost (R12)

*Table 7. Cost groups from `bom/bom.csv` (indicative 2026 USD).*

| Group | Items | Cost |
| --- | --- | --- |
| Cooling equipment kit | 6 to 11 and 14 | **$270** |
| Structure, costed separately | 1 to 5 and 12 | $355 |
| Store total, crates excluded | | $625 |
| Crates, user supplied | 13 | $96 if bought |

R12 was redefined by ZBX-DDR-001 item 1 to cover the cooling equipment kit, with the structure costed separately. The kit costs **$270 against $300**, 90 % of the budget, and R12 is **met**. The kit rose by $10 from v0.1 for the 150 mm pad ($260 to $270); the structure fell by $5 for the rice husk fill with lime, mesh and damp-proof course in place of sand and a wetting pipe ($360 to $355).

## 12. Results against requirements

*Table 8. Every requirement, value and status. Not met and at risk first.*

| ID | Quantity | Value (central, with range) | Target | Status |
| --- | --- | --- | --- | --- |
| R3 | Mean store RH while cooling | 81 % (77 to 85 %) | 80 % or more (relaxed from 85 %, DDR-002) | **At risk** |
| R1 | Crates on shelves; highest shelf | 24 crates (480 kg); top shelf 1.40 m | 20 or more; no lift above 1.6 m | Met |
| R2 | Mean store air below outside air | 10.7 K (9.8 to 11.4 K); store 24.3 °C | 8 K or more | Met |
| R4 | Humid-weather detection and mode change | 4 K threshold; 30 °C and 75 % RH gives 3.7 K and switches to hold; lamp shows mode | Detect under 4 K and switch, with indicator | Met (logic review) |
| R5 | Guard and minimum ventilation | Pump stop at 95 % RH for 60 min; hold mode about 8 air changes an hour at about 2 W | Pump stop rule; 1 air change an hour or more | Met (logic review) |
| R7 | Design-day energy from one panel | 372 Wh needed; 525 Wh from 150 W (41 % margin) | 10 h cooling plus 2 h evening, no grid | Met |
| R8 | Water per design day; sump | 36 L/day (pad 32, cavity 0, bleed 4); 60 L sump for 36 L | 70 L or less; sump one day | Met |
| R9 | Low voltage and safe | 12.8 V, 15 A terminal fuse, guards, inside release | As stated | Met (design review) |
| R12 | Cooling equipment kit cost | Kit $270; structure $355 separate | Kit $300 or less | Met |
| R6 | Tomato shelf life | No calculation basis; ZECC data come from a cooler, more humid chamber | 1.5 times ambient or more | Not verifiable at TRL 3 |
| R10 | Local build; 30 min part swaps | Needs a parts survey and swap trials with a partner | Local trades; 30 min | Not verifiable at TRL 3 |
| R11 | Durability | Wall bearing 16 kPa; post footings 1.6 times uplift at 30 m/s; pad and fan life unknown | 10 years structure; 3 years pad, fans, pump | Not verifiable at TRL 3 |

Counts: 8 met (R1, R2, R4, R5, R7, R8, R9, R12), 1 at risk (R3), none not met, 3 not verifiable at TRL 3 (R6, R10, R11).

## 13. Corrections to earlier figures

Changes in v0.2 (ZBX-DDR-002): pad 100 to 150 mm; cavity fill wet sand to dry rice husk; R3 target 85 to 80 %; airflow 584 to 563 m³/h; store 25.9 to 24.3 °C; drop 9.1 to 10.7 K; store RH 71 to 81 %; heat load 418 to 442 W; water 44 to 36 L/day; kit $260 to $270; structure $360 to $355.

Changes in v0.1 against the TRL 2 estimates:


- Airflow is 584 m³/h at the fan and pad operating point, not 650 m³/h; the TRL 2 figure sized airflow from the load without a fan curve.
- The heat load is 418 W, not about 550 W. The TRL 2 wall figure (about 250 W) was high for a wet cavity, and its 75 W margin is replaced by the scenario range.
- Store RH is about 71 %, inside the TRL 2 range of 65 to 75 %.
- Water is about 44 L/day, not 55 L; the cavity needs about 12 L, not 20 L.
- Daily energy is 372 Wh, not 350 Wh, because the controller runs all day. A 100 W panel would have been 6 % short, not "no margin".
- About 1,980 bricks are needed, not 2,200, and 1.3 m³ of sand, not 1.5 m³.
- The 10 A charge controller was undersized for a 150 W panel; the BOM now has 20 A.

> **Safety:** These figures do not cover entrapment, air quality, *Legionella* in the sump, mold, the LiFePO4 battery or roof uplift beyond section 10. See ZBX-PRC-001, Safety. The roof footings must be sized for the local design wind speed by a competent builder.
