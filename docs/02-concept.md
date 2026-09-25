---
doc_id: ZBX-PRC-001
title: ZeerBox design precis
project: ZeerBox
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, control modes, first-order numbers, cost, safety, media)
---

# ZeerBox design precis

ZeerBox is a walk-in store, 2.4 x 1.5 x 2.0 m inside, with double brick walls around a wet sand cavity, a shade roof, a 100 mm cellulose pad in the back wall, and two 12 V exhaust fans beside the door that pull outside air through the pad and along the aisle between two shelving racks. A controller reads temperature and humidity inside and outside and chooses between evaporative cooling, night ventilation and hold, and a 100 W solar panel with a small LiFePO4 battery powers it all. First-order numbers suggest that on a 35 °C, 30 % RH day the store holds about 480 kg of produce at about 26 °C, roughly 9 K below the outside air, using about 55 L of water and about 350 Wh of solar energy. The complete store costs about $575 in parts, well over the $300 budget; the cooling equipment alone costs about $235.

![Hero render](../media/hero.png)

*Figure 1. ZeerBox massing model with the pad and sump on the back wall, solar panel on the shade roof and a 1.75 m person for scale. The door and fans are on the far end.*

## How it works

1. **Wet.** A 12 V pump in a 60 L sump drum lifts water to a perforated header on top of the pad. Water runs down through the cellulose pad and drains back to the sump through a gutter. A perforated pipe keeps the sand in the wall cavity damp, as in a zero energy cool chamber, so the walls sit near the outside wet-bulb temperature and let in less heat.
2. **Cool.** Two 250 mm fans in the front wall exhaust air from the store, which pulls outside air in through the wetted pad on the opposite wall. Evaporation cools the air from 35 °C toward its wet-bulb temperature of about 21.5 °C; with a pad effectiveness of about 75 %, it enters at about 25 °C and 74 % RH.
3. **Store.** Air sweeps along the 0.6 m aisle and across 24 crates on two three-level timber racks, picking up about 550 W of heat from the walls, the produce and the day's warm field produce, and leaves through the fans at about 27.5 °C.
4. **Decide.** A controller compares the inside and outside readings every minute and runs one of four modes (below). A three-color lamp by the door shows the mode, so users know when to keep the door shut and when the store is not cooling.
5. **Power.** A 100 W panel on the shade roof charges a 12.8 V, 12 Ah LiFePO4 battery through a PWM charge controller. The battery covers cloud and about 2 h of evening ventilation.

The shade roof sits about 450 mm above an insulated ceiling so that sun never falls on the storage room, and its overhang shades the walls for most of the day.

![Air and water path](../media/flow.png)

*Figure 2. Air and water path on the design day, 35 °C and 30 % RH. All values are estimates.*

### Control modes

| Mode | When (proposed thresholds) | Fans | Pump | Lamp |
| --- | --- | --- | --- | --- |
| Evaporative cooling | Outside wet-bulb depression 4 K or more and store above its set point (proposed 20 °C) | On, speed by store temperature | On, duty cycled to keep the pad wet | Green |
| Night ventilation | Outside air at least 2 K cooler than the store, whatever its humidity | On | Off | Blue |
| Hold | Outside warmer than the store and too humid to cool | Off, or one fan at low speed for one air change per hour | Off | Amber |
| Guard | Store RH above 95 % for 60 min, sump float low, or battery low | Low | Off | Red, flashing |

The controller logs both sensor pairs and the mode every 10 min to a memory card, so a partner can compare seasons and sites. Firmware is out of scope at TRL 2 and 3 beyond a labeled sketch of this logic.

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Double brick walls and floor | Two 115 mm fired-brick leaves around a 75 mm cavity, 305 mm total; brick floor on compacted sand | Mud brick or block possible; proposed, awaiting Amish |
| 2 | Wet sand cavity fill | River sand kept damp by a perforated pipe along the top of the cavity | ZECC practice; about 1.5 m³ of sand |
| 3 | Insulated ceiling | Timber boards with about 50 mm of straw, rice husk or foam and a plastic vapor sheet | Keeps roof heat out |
| 4 | Shade roof on posts | Corrugated steel on four timber or steel posts, about 3.9 x 3.0 m, 450 mm clear above the ceiling | Carries the solar panel |
| 5 | Insulated door with seal | Timber frame, plywood skins, 50 mm insulation, rubber seal, inside release | Opens from inside without a key |
| 6 | Cellulose pad, frame, header and gutter | 100 mm pad, 0.6 x 0.5 m (0.3 m²), in a frame on the back wall with a drip header and return gutter | Poultry-house or greenhouse pad |
| 7 | Sump drum, pump and hoses | 60 L covered drum, 12 V submersible pump, float switch, feed and return hoses | Drained and cleaned weekly |
| 8 | Exhaust fans (pair) | Two 250 mm 12 V DC axial fans with guards and gravity shutters | About 12 W each |
| 9 | Controller and sensors | Low-cost microcontroller, two digital temperature and RH sensors (inside, outside in a radiation shield), MOSFET drivers, memory card, mode lamp, IP65 box | Generic parts |
| 10 | Solar panel | 100 W monocrystalline, about 1,000 x 670 mm, on the shade roof | 150 W option, see R7 |
| 11 | Power box | PWM charge controller, 12.8 V 12 Ah LiFePO4 battery with BMS, 15 A fuse, in a ventilated box | Shaded, outside the store |
| 12 | Shelving racks | Two timber racks, three levels, 2.2 m long and 0.45 m deep | Termite-treated timber or steel angle |
| 13 | Produce crates | 24 ventilated crates, about 500 x 350 x 300 mm, 20 kg each | User supplied; not in the cost |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM. The racks are drawn out in front; the crates, ceiling, roof and panel are lifted.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section along the aisle, looking at one rack. The door and fans are at left, the pad at right, and the wet sand cavity shows as the pale band inside each end wall.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

### Air, pad and store temperature

Assumptions: outside air at 35 °C and 30 % RH, sea-level pressure; pad effectiveness 75 %; supply air warms by 2.6 K across the store.

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Outside wet-bulb temperature | about 21.5 °C | Psychrometric relation at 35 °C, 30 % RH |
| Supply air after the pad | about 24.9 °C, 74 % RH | 35 minus 0.75 x (35 minus 21.5) |
| Exhaust air | about 27.5 °C, about 63 % RH before produce moisture | Supply plus 2.6 K at constant moisture |
| Mean store air | about 26 °C, 65 to 75 % RH | Average of supply and exhaust; produce adds moisture |
| **Temperature drop below ambient** | **about 9 K** | R2 (8 K) met |
| Moisture added by the pad | about 4.2 g per kg of air | Sensible heat removed divided by latent heat |

This matches field experience: D-Lab measured more than 8 °C of cooling from brick chambers in Mali's dry season. It also shows the limit. The store runs at about 26 °C, well above the 12.5 to 15 °C that tomatoes prefer, so ZeerBox slows spoilage rather than stopping it.

### Heat balance and airflow

| Heat gain | Estimate | Basis |
| --- | --- | --- |
| Walls | about 250 W | 15.6 m² x U about 1.8 W/(m²·K) x 9 K, cavity taken as dry (conservative) |
| Ceiling | about 25 W | 3.6 m² x U about 0.8 W/(m²·K) x 9 K, shaded by the roof |
| Produce respiration | about 70 W | 480 kg x about 0.15 W/kg near 26 °C, from tomato respiration data |
| Field heat of new produce | about 80 W | 100 kg/day x 3.9 kJ/(kg·K) x 6 K, removed over 8 h |
| Door openings and leaks | about 50 W | Allowance |
| Margin | about 75 W | Allowance |
| **Total** | **about 550 W** | |

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Airflow needed | about 0.18 m³/s (about 650 m³/h, 380 cfm) | 550 W / (1.15 kg/m³ x 1,006 J/(kg·K) x 2.6 K) |
| Air changes | about 90 per hour | 650 m³/h over 7.2 m³ |
| Pad face velocity | about 0.6 m/s | 0.18 m³/s over 0.3 m² |
| Fan pressure | about 30 Pa | Pad about 10 Pa, inlet, grilles and shutters about 20 Pa |
| Fan electrical power | about 22 to 24 W for both fans | 5.5 W of air power at about 25 % fan efficiency |

A wetted cavity should cut the wall gain substantially, since the outer wall surfaces run near the wet-bulb temperature, but this is not counted until it is checked at TRL 3.

### Water

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Evaporated at the pad | about 31 L/day | 0.21 kg/s of air x 4.2 g/kg for 10 h | |
| Wall cavity watering | about 20 L/day | ZECC practice of watering one to three times a day; allowance | |
| Bleed, splash and cleaning | about 4 L/day | Allowance to limit mineral build-up in the pad | |
| **Total** | **about 55 L/day** | | R8 (70 L) met |

### Energy

Assumptions: fans about 24 W, pump about 6 W at full duty, controller and sensors about 1 W; 10 h of cooling and 2 h of evening ventilation on the design day; 5 peak sun hours; 30 % combined loss for panel heat, dust, PWM charging and wiring.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Load while cooling | about 31 W | 24 + 6 + 1 | |
| Daily energy | about 350 Wh | 31 W x 10 h plus 24 W x 2 h | |
| Panel yield, 100 W | about 350 Wh/day | 100 W x 5 h x 0.7 | **R7 at risk: no margin** |
| Panel yield, 150 W option | about 525 Wh/day | 150 W x 5 h x 0.7 | R7 met with 50 % margin |
| Battery | 154 Wh, about 120 Wh usable | 12.8 V x 12 Ah x 80 % | About 4 h at full load |

### Humid weather

| Outside air | Supply air | Mean store (estimate) | Drop | Mode |
| --- | --- | --- | --- | --- |
| 35 °C, 30 % RH (design point) | about 24.9 °C | about 26 °C | about 9 K | Evaporative cooling |
| 38 °C, 15 % RH | about 23.9 °C | about 25 °C | about 13 K | Evaporative cooling |
| 32 °C, 50 % RH | about 25.7 °C | about 27 °C | about 5 K | Evaporative cooling |
| 30 °C, 75 % RH | about 27.2 °C | about 28.5 °C | about 1.5 K | Hold by day, night ventilation |

In the rainy season ZeerBox does little more than a shaded, ventilated shed. The controller's job then is to avoid making things worse: no wet pad adding humidity to a damp room, and cool night air let in whenever it is available.

### Cost

| Group | Indicative cost | Requirement |
| --- | --- | --- |
| Structure (items 1 to 5 and 12), materials only | about $340 | |
| Cooling equipment kit (items 6 to 11 and 14) | about $235 | |
| **Total, crates excluded** | **about $575** | **R12 ($300) not met, about 90 % over** |
| Crates (item 13, user supplied) | about $95 if bought | Not in the total |

Labor for the mason and carpenter is not included.

## Key design choices

Every choice below is **Proposed, awaiting Amish**.

- **Forced air through a pad, not a passive chamber.** A fan and pad give a larger, walk-in store with shelves at working height and a controlled airflow; a passive ZECC is cheaper and needs no power but holds far less and cannot respond to humidity. Recommendation: forced air, as in the pitch.
- **Exhaust fans, pad on the opposite wall (negative pressure).** Pulling air through the pad spreads it evenly over the pad face and keeps the fan motors out of the humid supply air. Blowing air in through the pad is the alternative. Recommendation: exhaust.
- **Wet sand cavity walls.** Borrowed from the ZECC to cut wall heat gain. Costs more brick and about 20 L/day of water; a single insulated wall is the alternative. Recommendation: wet cavity, to be checked by calculation at TRL 3.
- **Size.** 2.4 x 1.5 x 2.0 m inside for 24 crates. A smaller store (for example 1.6 x 1.5 m and 12 crates) would cost about a third less; a larger one would serve a group. Recommendation: keep 24 crates until the partner confirms the need.
- **Panel size.** 100 W has no margin on the design day (R7). Recommendation: 150 W, about $20 more.
- **Battery.** A small LiFePO4 battery allows evening ventilation and rides through cloud. PV-direct operation with no battery saves about $50 but stops the fans at dusk. Recommendation: keep the battery.
- **Set point and thresholds.** A 20 °C store set point, 4 K wet-bulb depression threshold and 95 % RH guard are starting values for field tuning.
- **Budget.** The complete store is about $575 against $300. Options are in `docs/REVIEW.md`. The `project.yaml` budget is unchanged.

## Safety

> **Safety:** ZeerBox is a walk-in room that people enter, with a lithium iron phosphate battery, spinning fans, standing warm water, heavy masonry and a roof that can catch the wind. Treat each of these as a hazard at every stage.

- **Entrapment and air quality.** The door must open from inside at all times, with no outside lock that can be closed on a person inside. Produce respires and uses oxygen; with the fans off and door shut for a long time, open the door and let the store air out before entering.
- **Water-borne bacteria.** Warm recirculating water in pads and sumps can grow *Legionella* and other bacteria, and the fine droplets from a pad can carry them. Cover the sump, drain and clean it weekly, dry the pad out regularly, never use the sump water for drinking or washing produce, and replace a pad that smells or grows slime. Covered water also stops mosquitoes breeding.
- **Mold and spoilage.** A damp, poorly ventilated store can spread mold between crates. The guard mode, weekly cleaning and removal of rotten produce are part of operation.
- **Battery.** A 154 Wh LiFePO4 battery is far less prone to thermal runaway than other lithium chemistries but can still overheat or short. Use a battery with a BMS, fuse it at the terminal, keep it shaded and ventilated outside the store, and do not charge it below 0 °C or above 45 °C.
- **Electrical.** All wiring is 12 V DC and below the touch-safety threshold, but water and wiring meet at the pad and pump. Use IP65 connections, drip loops and a fused supply.
- **Moving parts.** Fans need guards on both faces. Isolate power before cleaning a fan or the pump.
- **Structure.** Masonry walls and a roof that people stand under must be built by a competent mason. Anchor the roof posts and sheets against uplift in storms, keep the wet cavity from undermining the footings, and inspect for cracks each season.
- **Food safety.** Cooling slows spoilage; it does not make produce safe to eat. ZeerBox is not for meat, fish, milk or medicines.

## Open questions for TRL 3

- Check the heat balance with a wet cavity, sun on the walls at low sun angles and realistic door opening, and size the fans and pad from that.
- Find a way to meet R3 (85 % RH), for example by wetting the inner leaf or cutting airflow at night, and check the effect on temperature.
- Confirm pad effectiveness and pressure drop for a 100 mm pad at about 0.6 m/s from supplier data.
- Decide panel size (R7) and whether the battery stays.
- Review MIT D-Lab's forced-air evaporative chamber work in Kenya in detail and contact the team.
- Close the cost gap or propose a budget change (R12).
- Choose the first partner, site and crop mix for co-design.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
