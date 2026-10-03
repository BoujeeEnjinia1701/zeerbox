---
doc_id: ZBX-PRC-001
title: ZeerBox design precis
project: ZeerBox
doc_type: Design precis
version: "0.7"
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
  change: Populate to TRL 2 (architecture, control modes, first-order numbers, cost, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3; record the decisions in ZBX-DDR-001, replace the estimates with ZBX-CAL-001 figures (airflow, heat load, humidity, water, energy, cost), 150 W panel and 20 A charge controller, parametric model and drawing ZBX-DWG-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). 150 mm pad, dry rice husk cavity fill, R3 at 80 % with covered or lined crates; figures from ZBX-CAL-001 v0.2; drawing ZBX-DWG-001 Rev P2
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Design made constructable (ZBX-DDR-003): fans in a ceiling fan box, footings, lintels, linings, framed ceiling and roof; cost against the value-engineering target; build plan ZBX-BLD-001 and register ZBX-DEC-001; drawing Rev P3"
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: Design for construction, wall material and partner recorded from Amish's decisions of 2026-10-02 (ZBX-DEC-001)
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: Controller parts list names the clear-lid box, mode lamp position and plate shield (ZBX-DEC-001, decisions 6 to 8)
---

# ZeerBox design precis

ZeerBox is a walk-in store, 2.4 x 1.5 x 2.0 m inside, with double brick walls around a dry rice husk cavity, a shade roof, a 150 mm cellulose pad in the back wall, and two 12 V exhaust fans in the ceiling at the door end that pull outside air through the pad and along the aisle between two shelving racks. A controller reads temperature and humidity inside and outside and chooses between evaporative cooling, night ventilation and hold, and a 150 W solar panel with a small LiFePO4 battery powers it all. The TRL 3 calculation (ZBX-CAL-001 v0.3) shows that on a 35 °C, 30 % RH day the store holds 480 kg of produce at about 24.3 °C, 10.7 K below the outside air, using about 36 L of water and 372 Wh of solar energy. Store humidity is about 81 %, just above the 80 % target (R3, at risk in the unfavorable case). Value-engineering target: USD 300 for the cooling equipment kit. Estimated cost of the constructable design: USD 299 for the kit (USD 1 under the target); the structure, about USD 574 in local materials, is costed separately. How to build it is in the prototype build plan ([ZBX-BLD-001](05-build-plan.md)).

![Hero render](../media/hero.png)

*Figure 1. ZeerBox from the TRL 3 parametric model, with the pad and sump on the back wall, the 150 W panel on the shade roof and a 1.75 m person for scale. The door is on the far end, with the fan box in the ceiling above it.*

## How it works

1. **Wet.** A 12 V pump in a 60 L sump drum lifts about 3.6 L/min to a perforated header on top of the pad. Water runs down through the 150 mm cellulose pad and drains back to the sump through a gutter. The wall cavity is filled with dry rice husk, which insulates the store and needs no water.
2. **Cool.** Two 250 mm fans in a plywood fan box in the ceiling at the door end exhaust air from the store up into the shaded roof space, which pulls outside air in through the wetted pad on the opposite wall. At the fan and pad operating point of about 563 m³/h, evaporation cools the air from 35 °C toward its wet-bulb temperature of 21.5 °C; with a pad effectiveness of about 88 %, it enters at 23.1 °C and 87 % RH.
3. **Store.** Air sweeps along the 0.6 m aisle and across 24 crates on two three-level timber racks, picking up about 440 W from the walls, ceiling, floor, produce and the day's warm field produce, and leaves through the fans at about 25.5 °C. Leafy and water-sensitive produce goes in covered or lined crates, which hold humidity near the produce.
4. **Decide.** A controller compares the inside and outside readings every minute and runs one of four modes (below). A three-color lamp by the door shows the mode, so users know when to keep the door shut and when the store is not cooling.
5. **Power.** A 150 W panel on the shade roof charges a 12.8 V, 12 Ah LiFePO4 battery through a 20 A PWM charge controller. The battery covers cloud and about 2 h of evening ventilation.

The shade roof sits 450 mm above an insulated ceiling so that sun never falls on the storage room, and its overhang shades the walls for most of the day.

![Air and water path](../media/flow.png)

*Figure 2. Air and water path on the design day, 35 °C and 30 % RH. Values from ZBX-CAL-001; all are estimates.*

### Control modes

The thresholds are starting values for field tuning (decided by Amish, 2026-09-25, ZBX-DDR-001 item 8).

| Mode | When | Fans | Pump | Lamp |
| --- | --- | --- | --- | --- |
| Evaporative cooling | Outside wet-bulb depression 4 K or more and store above its 20 °C set point | On, speed by store temperature | On, duty cycled to keep the pad wet | Green |
| Night ventilation | Outside air at least 2 K cooler than the store, whatever its humidity | On, at reduced speed after the 2 h evening run | Off | Blue |
| Hold | Outside warmer than the store and too humid to cool | One fan at about 30 % speed, about 8 air changes an hour | Off | Amber |
| Guard | Store RH above 95 % for 60 min, sump float low, or battery low | Low | Off | Red, flashing |

The battery can carry full-speed night ventilation for only about 2.5 h beyond the evening run (ZBX-CAL-001 section 7), so night ventilation runs at reduced speed. The controller logs both sensor pairs and the mode every 10 min to a memory card, so a partner can compare seasons and sites. Firmware is out of scope at TRL 3 beyond a labeled sketch of this logic.

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`. Dimensions come from `cad/src/model.py` and drawing ZBX-DWG-001.

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Double brick walls and floor | Two 115 mm fired-brick leaves around a 75 mm cavity, 305 mm total, outside 3,010 x 2,110 mm; brick floor on compacted sand; about 1,980 bricks | Fired brick, decided by Amish 2026-10-02 (ZBX-DEC-001) |
| 2 | Dry rice husk cavity fill | About 1.3 m³ of dry rice husk mixed with hydrated lime, on a damp-proof course, capped with mortar | Decided (ZBX-DDR-002 item 12); dry sand is the fallback |
| 3 | Insulated ceiling | Timber boards with about 50 mm of straw, rice husk or foam and a plastic vapor sheet | Keeps roof heat out |
| 4 | Shade roof on posts | Corrugated steel, 3.9 x 3.0 m, on four 90 mm posts in 500 x 500 x 600 mm concrete footings, 450 mm clear above the ceiling | Carries the solar panel; 500 mm footings kept as a minimum (ZBX-DDR-002 item 13) |
| 5 | Insulated door with seal | 0.8 x 1.8 m, timber frame, plywood skins, 50 mm insulation, rubber seal, inside release | Opens from inside without a key |
| 6 | Cellulose pad, frame, header and gutter | 150 mm pad, 0.6 x 0.5 m (0.3 m²), center 1.25 m above ground, with a drip header and return gutter | Decided (ZBX-DDR-002 item 11; was 100 mm) |
| 7 | Sump drum, pump and hoses | 60 L covered drum, 12 V submersible pump about 6 W at 2 m head, float switch, feed and return hoses | Drained and cleaned weekly |
| 8 | Exhaust fans (pair) | Two 250 mm 12 V DC axial fans with guards and gravity shutters, in a ceiling fan box at the door end, blowing up into the roof space (ZBX-DDR-003) | About 12 W and about 280 m³/h each in service |
| 9 | Controller and sensors | Low-cost microcontroller, two digital temperature and RH sensors (inside, outside in a six-plate shield), MOSFET drivers, memory card, mode lamp on top of the box, clear-lid IP65 box | Generic parts |
| 10 | Solar panel | 150 W monocrystalline, about 1,480 x 670 mm, on the shade roof | Decided (item 2) |
| 11 | Power box | 20 A PWM charge controller, 12.8 V 12 Ah LiFePO4 battery with BMS, 15 A fuse, in a ventilated box | Battery decided (item 3); outside the store, shaded |
| 12 | Shelving racks | Two timber racks, 2.2 m long and 0.45 m deep, shelves at 0.30, 0.85 and 1.40 m above the floor | Termite-treated timber or steel angle |
| 13 | Produce crates | 24 ventilated crates, about 500 x 350 x 300 mm, 20 kg each | User supplied; not in the cost |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM. The racks are drawn out in front; the crates, ceiling, roof and panel are lifted.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section along the aisle, looking at one rack. The door and the ceiling fan box are at left, the pad at right, and the dry rice husk cavity shows as the pale band inside each end wall.*

## TRL 3 figures

All values come from ZBX-CAL-001 v0.3 (`python docs/04-calcs/sizing.py`). They are first-principles estimates, not measurements. The central case is quoted with the favorable to unfavorable range where it matters.

### Air, pad and store temperature

*Table 1. Design point, 35 °C and 30 % RH.*

| Quantity | Value | Basis |
| --- | --- | --- |
| Outside wet-bulb temperature | 21.5 °C | ASHRAE psychrometric relations |
| Airflow at the fan and pad operating point | 563 m³/h (331 cfm), 18 Pa; about 78 air changes an hour | Two fans on a straight-line curve against the 150 mm pad, shutters and guards |
| Pad face velocity and effectiveness | 0.52 m/s, about 88 % | NTU model calibrated to 75 % at 0.6 m/s for 100 mm, scaled to 150 mm |
| Supply air after the pad | 23.1 °C, 87 % RH | |
| Heat load | 442 W (376 to 558 W) | Walls, ceiling, floor, door, respiration, field heat, leaks |
| Exhaust air | 25.5 °C, 77 % RH | Supply plus 2.35 K |
| Mean store air | 24.3 °C, 81 % RH | |
| **Temperature drop below ambient** | **10.7 K (9.8 to 11.4 K)** | R2 (8 K) met in every case |

This matches field experience: D-Lab measured more than 8 °C of cooling from brick chambers in Mali's dry season. It also shows the limit. The store runs at about 24 °C, well above the 12.5 to 15 °C that tomatoes prefer, so ZeerBox slows spoilage rather than stopping it.

### Humidity

The store averages about 81 % RH while cooling (77 to 85 %), against 80 % in R3, relaxed from 85 % by ZBX-DDR-002. The supply air leaves the 150 mm pad at 87 % RH and loses about 4 to 5 percentage points of RH for every kelvin it warms in the store, so R3 is at risk in the unfavorable case. Reaching 85 % would need a pad about 185 mm deep or more. Covered or lined crates for leafy and water-sensitive produce hold humidity near the produce; they are an operating practice, not a kit item.

### Walls

The decided dry rice husk fill lets in about 84 W through the walls with no water. With the 150 mm pad, a wet sand cavity would let in about 163 W and use about 12 L of water a day, and dry sand (the fallback if no durable, pest-proof husk supply exists) about 192 W. The husk sits on a damp-proof course, is mixed with hydrated lime against insects and is capped with mortar, so it stays dry and closed to rodents.

### Water

| Quantity | Value | Requirement |
| --- | --- | --- |
| Evaporated at the pad | 32 L/day (29 to 35 L) | |
| Wall cavity | none (dry fill) | |
| Bleed, splash and cleaning | 4 L/day | |
| **Total** | **about 36 L/day** | R8 (70 L) met; the 60 L sump covers the 36 L of pad and bleed water |

### Energy

| Quantity | Value | Requirement |
| --- | --- | --- |
| Load while cooling | 31 W (fans 24 W, pump 6 W, controller 1 W) | |
| Daily energy | 372 Wh (fans 288, pump 60, controller 24) | |
| Panel yield, 150 W | 525 Wh/day at 5 peak sun hours and 30 % losses | R7 met, 41 % margin |
| Battery | 154 Wh, 123 Wh usable; 62 Wh needed after sunset | |
| Charge controller | 20 A PWM (1.25 x 9 A Isc) | 10 A was too small |

### Humid weather

| Outside air | Wet-bulb depression | Supply air | Mean store | Drop | Mode |
| --- | --- | --- | --- | --- | --- |
| 35 °C, 30 % RH (design point) | 13.5 K | 23.1 °C | 24.3 °C | 10.7 K | Evaporative cooling |
| 38 °C, 15 % RH | 18.8 K | 21.4 °C | 22.8 °C | 15.2 K | Evaporative cooling |
| 32 °C, 50 % RH | 8.3 K | 24.6 °C | 25.6 °C | 6.4 K | Evaporative cooling |
| 30 °C, 75 % RH | 3.7 K | 26.7 °C | 27.5 °C | 2.5 K | Hold by day, night ventilation |

In the rainy season ZeerBox does little more than a shaded, ventilated shed. The controller's job then is to avoid making things worse: no wet pad adding humidity to a damp room, and cool night air let in whenever it is available.

### Cost

| Group | Indicative cost | Requirement |
| --- | --- | --- |
| Cooling equipment kit (items 6 to 11, 14 and 18) | about $299 | R12: USD 1 under the USD 300 value-engineering target |
| Structure (items 1 to 5, 12, 15, 16 and 17), materials only, costed separately | about $574 | |
| Store total, crates excluded | about $873 | |
| Crates (item 13, user supplied) | about $96 if bought | Not in the total |

Labor for the mason and carpenter is not included.

## Key design choices

Items marked "decided" were decided by Amish on 2026-09-25 (go with recommendation, ZBX-DDR-001 and ZBX-DDR-002) or on 2026-10-02 (ZBX-DEC-001).

- **Forced air through a pad, not a passive chamber (decided).** A fan and pad give a larger, walk-in store with shelves at working height and a controlled airflow; a passive ZECC is cheaper and needs no power but holds far less and cannot respond to humidity.
- **Exhaust fans, pad on the opposite wall (decided).** Pulling air through the pad spreads it evenly over the pad face and keeps the fan motors out of the humid supply air.
- **Dry rice husk cavity fill (decided).** Replaces the wet sand cavity borrowed from the ZECC, which ZBX-CAL-001 found worth little. Decided by Amish, 2026-09-25: go with recommendation (ZBX-DDR-002 item 12), subject to a durable, pest-proof husk supply locally; dry sand is the fallback.
- **Size (decided).** 2.4 x 1.5 x 2.0 m inside for 24 crates, kept until the partner confirms the need.
- **Panel size (decided).** 150 W, with a 20 A charge controller.
- **Battery (decided).** A small LiFePO4 battery for evening ventilation and cloud.
- **Set point and thresholds (decided).** 20 °C set point, 4 K wet-bulb depression threshold and 95 % RH guard as starting values for field tuning.
- **Budget (decided).** `budget_usd: 300` covers the cooling equipment kit; the structure is costed separately. Since 2026-10-01 it is a hypothetical value-engineering target, not a limit.
- **Design for construction (accepted by Amish, 2026-10-02).** Footings, lintels, linings, a framed ceiling and roof, and the fans moved from the front wall to a ceiling fan box, so that every part can be built (ZBX-DDR-003). Decisions are recorded in the register ZBX-DEC-001.
- **Wall material (decided).** Fired brick, as modelled and calculated: the pad wall is kept wet and fired brick does not soften (decided by Amish, 2026-10-02, ZBX-DEC-001).
- **Pad depth and R3 (decided).** A 150 mm pad, R3 relaxed to 80 %, and covered or lined crates for sensitive produce (ZBX-DDR-002 item 11).
- **Roof footings (decided).** 500 x 500 x 600 mm footings as a minimum; the local design wind speed is confirmed with a builder at the chosen site (ZBX-DDR-002 item 13).

## Safety

> **Safety:** ZeerBox is a walk-in room that people enter, with a lithium iron phosphate battery, spinning fans, standing warm water, heavy masonry and a roof that can catch the wind. Treat each of these as a hazard at every stage.

- **Entrapment and air quality.** The door must open from inside at all times, with no outside lock that can be closed on a person inside. Produce respires and uses oxygen; with the fans off and door shut for a long time, open the door and let the store air out before entering.
- **Water-borne bacteria.** Warm recirculating water in pads and sumps can grow *Legionella* and other bacteria, and the fine droplets from a pad can carry them. Cover the sump, drain and clean it weekly, dry the pad out regularly, never use the sump water for drinking or washing produce, and replace a pad that smells or grows slime. Covered water also stops mosquitoes breeding.
- **Mold and spoilage.** A damp, poorly ventilated store can spread mold between crates. The guard mode, weekly cleaning and removal of rotten produce are part of operation.
- **Battery.** A 154 Wh LiFePO4 battery is far less prone to thermal runaway than other lithium chemistries but can still overheat or short. Use a battery with a BMS rated for at least 10 A of charge, fuse it at the terminal, keep it shaded and ventilated outside the store, and do not charge it below 0 °C or above 45 °C.
- **Electrical.** All wiring is 12 V DC and below the touch-safety threshold, but water and wiring meet at the pad and pump. Use IP65 connections, drip loops and a fused supply. Size the charge controller for 1.25 times the panel's short-circuit current.
- **Moving parts.** Fans need guards on both faces. Isolate power before cleaning a fan or the pump.
- **Structure.** Masonry walls (about 7 t of brick) and a roof that people stand under must be built by a competent mason. At a 30 m/s gust each roof post sees about 1.9 kN of uplift after the roof's own weight; set the posts in footings of at least 500 x 500 x 600 mm with an anchor bar through each post foot, tie every purlin to its beam, screw the sheets down, confirm the local design wind speed, and inspect for cracks each season.
- **Rice husk fill.** Dry husk is combustible. Keep the cavity capped with mortar, keep flames and hot work away from the walls during building, and keep the solar wiring in conduit where it passes the wall top.
- **Food safety.** Cooling slows spoilage; it does not make produce safe to eat. ZeerBox is not for meat, fish, milk or medicines.

## Open questions

- Confirm a durable, pest-proof rice husk supply near the chosen site, or fall back to dry sand (ZBX-DDR-002 item 12).
- Confirm the local design wind speed with a builder (ZBX-DDR-002 item 13).
- Confirm pad effectiveness and pressure drop, and the fan curve, from supplier data for the chosen parts.
- Review MIT D-Lab's forced-air evaporative chamber work in Kenya in detail and contact the team.
- Approach the first candidate partner, MIT D-Lab's evaporative cooling team, for a site in Mali's dry-season vegetable areas (decided by Amish, 2026-10-02, ZBX-DEC-001).
- The decisions and the items to confirm are kept in the design decisions register, ZBX-DEC-001 ([docs/06-design-decisions.md](06-design-decisions.md)).

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html). General arrangement: `cad/drawings/ZBX-DWG-001.pdf`.
