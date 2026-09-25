---
doc_id: ZBX-CAL-001
title: ZeerBox sizing and first-principles checks
project: ZeerBox
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (psychrometrics, fan and pad operating point, heat balance, humidity, off-design weather, energy, water, electrical, structure, cost) against every requirement
---

# ZeerBox sizing and first-principles checks

On paper the store cools as the concept claims, but with less margin and at lower humidity than a produce store should have. At the design point of 35 °C and 30 % RH, the two 250 mm fans deliver about 584 m³/h (344 cfm) through the 100 mm pad, the supply air leaves the pad at 24.8 °C and 75 % RH, and the store averages **25.9 °C, 9.1 K below the outside air**. Seven of the twelve requirements are met (three of them by design review or logic review only), one is at risk, one is **not met** and three cannot be verified at TRL 3. **R3 (store RH 85 % or more) is not met:** the store averages about 71 % RH, and no direct evaporative pad of practical depth reaches 85 % once the air picks up the store's heat. R2 is at risk because the unfavorable case gives 8.0 K, on the limit. The heat balance also shows that the wet sand cavity, decided in ZBX-DDR-001 item 6, buys only about 0.15 K over a dry cavity for about 12 L of water a day; a dry insulating fill does as well without water (open item 12).

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry from `PARAMS` in `cad/src/model.py`, the prices from `bom/bom.csv` and the budget from `project.yaml`, so the model, drawing ZBX-DWG-001 and this note agree. All values are first-principles estimates; nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design unless marked as decided.*

| Input | Value | Basis |
| --- | --- | --- |
| Architecture | Forced air, exhaust fans with the pad on the opposite wall, wet sand cavity, 24 crates, 150 W panel with a LiFePO4 battery | Decided, ZBX-DDR-001 items 2 to 7 |
| Design point | 35 °C, 30 % RH, sea-level pressure (101.325 kPa); 480 kg of produce inside; 100 kg loaded per day at 32 °C | ZBX-REQ-001 |
| Psychrometrics | ASHRAE saturation pressure over water and the ASHRAE humidity-ratio relation for the thermodynamic wet bulb | ASHRAE *Fundamentals* (2017), chapter 1 |
| Pad | 100 mm cellulose, 0.6 x 0.5 m (0.3 m²); saturation effectiveness 80, 75 or 70 % at 0.6 m/s, scaled with depth and with face velocity to the power -0.2 (NTU model); wet pressure drop 15 Pa at 1.0 m/s, proportional to depth and to velocity to the power 1.8 | TRL 2 assumption for effectiveness; pressure drop is an assumption to confirm with the pad supplier's chart |
| Fans | Two 250 mm 12 V DC axial fans, each 400 m³/h free air and 12 W; straight-line fan curve to a shut-off pressure of 70, 60 or 50 Pa | BOM line 8; shut-off pressure is an assumption to confirm with the fan's curve |
| Other airflow losses | Gravity shutters 5 Pa to hold open; guards and shutters four velocity heads at the fan openings | Allowance |
| Walls | Two 115 mm fired-brick leaves, k 0.70 W/(m·K); 75 mm cavity of wet sand (k 1.5) or dry sand (k 0.30); inside and outside film resistances 0.13 and 0.04 m²·K/W | Typical handbook values |
| Wet cavity | Cavity held at the outside temperature minus 60, 50 or 30 % of the wet-bulb depression | ZECC field data show 4 to 7 K below ambient; the fraction is an assumption |
| Ceiling, floor, door | 50 mm straw (k 0.06) on boards, air under the shade roof at 38, 40 or 43 °C; brick floor on sand to ground at 28, 30 or 32 °C; door with 50 mm insulation (k 0.04) | Allowance for a shaded, ventilated roof space |
| Produce | Respiration heat 0.10, 0.15 or 0.25 W/kg near 26 °C (mixed tomatoes, peppers and greens); water loss 0.5, 1 or 2 % of mass per day; specific heat 3.9 kJ/(kg·K); field heat removed over 8 h | Respiration heat of about 3 mW per mg CO₂/(kg·h) from glucose oxidation |
| Door openings and leaks | 30, 50 or 80 W; sun on the end walls at low sun angles 0, 20 or 60 W | Allowance |
| Solar | 5 peak sun hours; 30 % combined loss (heat, dust, PWM charging, wiring) | As TRL 2 |
| Loads | Fans 12 W each at full speed (taken as constant), pump 6 W for the 10 h of cooling, controller 1 W for 24 h | As TRL 2, controller now counted all day |
| Structure | Brick 1,800 kg/m³, wet sand 1,900 kg/m³, concrete 23.5 kN/m³; roof uplift at a 30 m/s gust with a net pressure coefficient of 1.5 on an open canopy | Assumptions; confirm the local design wind speed |

Three scenarios bracket the result: **favorable**, **central** and **unfavorable**, taking the first, second and third value where Table 1 gives three. Central values are quoted unless a range is given.

## 2. Geometry and capacity (R1)

The room is 2,400 x 1,500 x 2,000 mm inside (7.2 m³) and 3,010 x 2,110 mm outside. Two racks, 2,200 x 450 mm, carry three shelves each with tops at 0.30, 0.85 and 1.40 m above the floor, four crates per shelf, so the store holds **24 crates (480 kg)** with a 600 mm aisle. The top crate reaches 1.70 m and leaves 0.30 m to the ceiling. Each shelf is carried by two 50 x 75 mm timber rails spanning 1.05 m between legs; four loaded crates (22 kg each) give 196 N/m, a bending stress of 0.58 MPa and a deflection of 0.20 mm, well inside softwood limits. R1 is **met**.

## 3. Fan and pad operating point

With both fans against the pad, the shutters and the guards, the operating point is **584 m³/h at 16.2 Pa** (556 to 605 m³/h), not the 650 m³/h assumed at TRL 2. Face velocity at the pad falls to 0.54 m/s, which raises the pad effectiveness slightly to 75.7 % (71.1 to 80.4 %). The air changes about 81 times an hour. Each fan delivers about 290 m³/h, 73 % of its free-air rating, which is a normal operating point for a small axial fan but must be checked against the chosen fan's curve.

## 4. Design point, heat balance and store temperature (R2)

*Table 2. Air states at the design point, central case.*

| State | Temperature | RH | Humidity ratio |
| --- | --- | --- | --- |
| Outside | 35.0 °C | 30 % | 10.5 g/kg |
| Wet bulb | 21.5 °C | | depression 13.5 K |
| Supply, after the pad | 24.8 °C | 75 % | |
| Store mean | 25.9 °C | 71 % | |
| Exhaust | 27.0 °C | 67 % | |

*Table 3. Heat gains at the design point, central case.*

| Gain | W | Basis |
| --- | --- | --- |
| Walls, wet cavity at 28.3 °C | 103 | U 3.13 W/(m²·K) from cavity to room over 13.8 m² net |
| Sun on the end walls | 20 | Allowance |
| Ceiling | 42 | U 0.82 W/(m²·K), 3.6 m², air under the roof at 40 °C |
| Floor | 40 | U 2.68 W/(m²·K), 3.6 m², ground at 30 °C |
| Door leaf | 8 | U 0.62 W/(m²·K), 1.44 m² |
| Produce respiration | 72 | 480 kg x 0.15 W/kg |
| Field heat | 83 | 100 kg from 32 °C, over 8 h |
| Door openings and leaks | 50 | Allowance |
| **Total** | **418** | 333 W favorable, 598 W unfavorable |

The 418 W warms the 584 m³/h airstream by 2.15 K, so the store averages 25.9 °C, **9.1 K below the outside air** (8.0 to 10.0 K). R2 (8 K or more) is **at risk**: met in the central and favorable cases, and on the limit (7.96 K) in the unfavorable case. The TRL 2 estimate (about 550 W and 9 K) had a larger load but assumed more airflow; the result is nearly the same.

A 150 mm pad on the same fans would lift the effectiveness to 88 % at 563 m³/h and give a 10.5 K drop, which restores margin on R2. This is open item 11 in ZBX-DDR-001.

### 4.1 Wet cavity against a dry fill

*Table 4. Wall options at the design point.*

| Cavity fill | Wall gain, central | Store drop, central | Store drop, unfavorable | Cavity water |
| --- | --- | --- | --- | --- |
| Wet sand (decided) | 103 W | 9.13 K | 7.96 K | about 12 L/day |
| Dry sand | 165 W | 8.98 K | 8.01 K | none |
| Dry rice husk, k 0.06 W/(m·K) | 72 W | 9.20 K | 8.22 K | none |

Wet sand conducts about five times better than dry sand, so the wet cavity helps only as long as evaporation keeps it well below the outside temperature. In the central case it saves about 60 W against dry sand, worth 0.15 K; in the unfavorable case, with the cavity only 30 % of the way to the wet bulb, it is slightly worse than dry sand. A dry insulating fill such as rice husk beats both without any water, but it must be kept dry and protected from termites and rodents. The wet cavity stays in the design as decided; the comparison goes to Amish as open item 12.

## 5. Humidity (R3)

The store averages about **71 % RH** (66 to 76 %) while cooling, against a target of 85 %. R3 is **not met**, and the calculation shows why no simple fix reaches it:

- Even the supply air leaving a 100 mm pad is only 75 % RH.
- A 150 mm pad raises the supply to 87 % RH, but the store still averages 81 %.
- To average 85 % at the central temperature rise of 2.15 K, the pad would need about 92 % effectiveness, which takes a pad about 180 mm deep or more.
- Produce transpiration adds only about 0.3 g/kg to the airstream at this airflow, worth about 1 percentage point of RH in the store, so the produce cannot humidify the store itself.

The limit is the architecture: a once-through airstream that must carry the store's heat warms as it goes, and its RH falls about 4 to 5 percentage points per kelvin. Options (proposed, awaiting Amish, open item 11) are a deeper pad, a relaxed R3 target, and produce-level measures such as covered or lined crates that hold humidity near the produce.

## 6. Off-design weather and control (R4, R5)

*Table 5. Store in evaporative mode at other outside conditions, central case.*

| Outside | Wet-bulb depression | Supply | Store | Drop | Store RH | Controller mode |
| --- | --- | --- | --- | --- | --- | --- |
| 35 °C, 30 % RH | 13.5 K | 24.8 °C | 25.9 °C | 9.1 K | 71 % | Evaporative cooling |
| 38 °C, 15 % RH | 18.8 K | 23.8 °C | 25.0 °C | 13.0 K | 61 % | Evaporative cooling |
| 32 °C, 50 % RH | 8.3 K | 25.7 °C | 26.6 °C | 5.4 K | 81 % | Evaporative cooling |
| 30 °C, 60 % RH | 6.2 K | 25.3 °C | 26.2 °C | 3.8 K | 84 % | Evaporative cooling |
| 30 °C, 75 % RH | 3.7 K | 27.2 °C | 27.9 °C | 2.1 K | 90 % | Hold by day, night ventilation |

The proposed 4 K wet-bulb depression threshold switches the store to hold at 30 °C and 75 % RH, where the pad would give only about 2 K of cooling at 90 % RH. R4 is **met** by logic review. In hold mode one fan at 30 % speed moves about 57 m³/h, about 8 air changes an hour, for about 2 W including driver losses, so the minimum of one air change an hour in R5 is easy to hold. With the 95 % RH pump stop, R5 is **met** by logic review. Both need a bench test with sensors later (TRL 4, on hold).

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

The pad evaporates 2.82 kg/h, **28 L** over the 10 h cooling day (25 to 31 L). Holding the wet cavity at 28.3 °C takes about 649 W through the outer leaf, which evaporates about **12 L/day** over a 12 h equivalent day, less than the 20 L allowed at TRL 2. With 4 L of bleed and cleaning the total is **about 44 L/day**, and R8 (70 L or less) is **met**. The sump holds 68 L gross and 60 L working, which covers the 32 L of pad and bleed water for a full day.

The pad needs about 3.6 L/min to stay wet (6 L/min per m of pad length, a typical supplier figure to confirm). Lifting that 2 m takes 1.2 W of hydraulic power, or about 6 W at a small pump's 20 % efficiency, which matches the 6 W pump in the BOM.

## 9. Electrical (R9, R10)

The full load draws 2.4 A at 12.8 V and the panel charges at up to 8.3 A; the 15 A fuse at the battery terminal sits above both and below the cable ratings. Every electrical part runs at 12 V DC, the fans are guarded on both faces and the door opens from inside. R9 is **met** by design review. R10 (local build and 30 min part swaps) depends on a parts survey and swap trials with a partner and is **not verifiable at TRL 3**.

## 10. Structure (R11)

The walls need about 1,977 bricks with 10 % waste (1,677 for the walls, 120 for the floor), 3.9 m³ of brickwork weighing about 7.1 t, and 1.3 m³ of wet sand weighing about 2.4 t. That puts about 9.3 kN/m on the foundations, or about 21 kPa on a 450 mm strip, well below the 100 kPa or more of firm soils.

The shade roof is the structural risk. At a 30 m/s gust the net uplift on the 11.7 m² roof is about 9.5 kN, or 2.23 kN per post after the sheet weight. A 400 x 400 x 600 mm concrete footing weighs only 2.26 kN, a factor of 1.01. The model and BOM now use **500 x 500 x 600 mm footings** (3.52 kN, a factor of 1.58). The local design wind speed must be confirmed with a builder; squall lines in the Sahel can exceed 30 m/s. Pad, fan and pump life depend on supplier data and dust exposure, so R11 is **not verifiable at TRL 3**.

## 11. Cost (R12)

*Table 7. Cost groups from `bom/bom.csv` (indicative 2026 USD).*

| Group | Items | Cost |
| --- | --- | --- |
| Cooling equipment kit | 6 to 11 and 14 | **$260** |
| Structure, costed separately | 1 to 5 and 12 | $360 |
| Store total, crates excluded | | $620 |
| Crates, user supplied | 13 | $96 if bought |

R12 was redefined by ZBX-DDR-001 item 1 to cover the cooling equipment kit, with the structure costed separately. The kit costs **$260 against $300**, 87 % of the budget, and R12 is **met**. The kit rose by $27 from TRL 2 for the 150 W panel, the 20 A charge controller and the heavier PV cable; the structure rose by $20 for the larger post footings.

## 12. Results against requirements

*Table 8. Every requirement, value and status. Not met and at risk first.*

| ID | Quantity | Value (central, with range) | Target | Status |
| --- | --- | --- | --- | --- |
| R3 | Mean store RH while cooling | 71 % (66 to 76 %) | 85 % or more | **Not met** |
| R2 | Mean store air below outside air | 9.1 K (8.0 to 10.0 K); store 25.9 °C | 8 K or more | **At risk** |
| R1 | Crates on shelves; highest shelf | 24 crates (480 kg); top shelf 1.40 m | 20 or more; no lift above 1.6 m | Met |
| R4 | Humid-weather detection and mode change | 4 K threshold; 30 °C and 75 % RH gives 3.7 K and switches to hold; lamp shows mode | Detect under 4 K and switch, with indicator | Met (logic review) |
| R5 | Guard and minimum ventilation | Pump stop at 95 % RH for 60 min; hold mode about 8 air changes an hour at about 2 W | Pump stop rule; 1 air change an hour or more | Met (logic review) |
| R7 | Design-day energy from one panel | 372 Wh needed; 525 Wh from 150 W (41 % margin) | 10 h cooling plus 2 h evening, no grid | Met |
| R8 | Water per design day; sump | 44 L/day (pad 28, cavity 12, bleed 4); 60 L sump for 32 L | 70 L or less; sump one day | Met |
| R9 | Low voltage and safe | 12.8 V, 15 A terminal fuse, guards, inside release | As stated | Met (design review) |
| R12 | Cooling equipment kit cost | Kit $260; structure $360 separate | Kit $300 or less | Met |
| R6 | Tomato shelf life | No calculation basis; ZECC data come from a cooler, more humid chamber | 1.5 times ambient or more | Not verifiable at TRL 3 |
| R10 | Local build; 30 min part swaps | Needs a parts survey and swap trials with a partner | Local trades; 30 min | Not verifiable at TRL 3 |
| R11 | Durability | Wall bearing 21 kPa; post footings 1.6 times uplift at 30 m/s; pad and fan life unknown | 10 years structure; 3 years pad, fans, pump | Not verifiable at TRL 3 |

Counts: 7 met (R1, R4, R5, R7, R8, R9, R12), 1 at risk (R2), 1 not met (R3), 3 not verifiable at TRL 3 (R6, R10, R11).

## 13. Corrections to earlier figures

- Airflow is 584 m³/h at the fan and pad operating point, not 650 m³/h; the TRL 2 figure sized airflow from the load without a fan curve.
- The heat load is 418 W, not about 550 W. The TRL 2 wall figure (about 250 W) was high for a wet cavity, and its 75 W margin is replaced by the scenario range.
- Store RH is about 71 %, inside the TRL 2 range of 65 to 75 %.
- Water is about 44 L/day, not 55 L; the cavity needs about 12 L, not 20 L.
- Daily energy is 372 Wh, not 350 Wh, because the controller runs all day. A 100 W panel would have been 6 % short, not "no margin".
- About 1,980 bricks are needed, not 2,200, and 1.3 m³ of sand, not 1.5 m³.
- The 10 A charge controller was undersized for a 150 W panel; the BOM now has 20 A.

> **Safety:** These figures do not cover entrapment, air quality, *Legionella* in the sump, mold, the LiFePO4 battery or roof uplift beyond section 10. See ZBX-PRC-001, Safety. The roof footings must be sized for the local design wind speed by a competent builder.
