---
doc_id: ZBX-RSK-001
title: ZeerBox risk register and hazard analysis
project: ZeerBox
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First issue (kit 1.9.1 upgrade) with project risks, preliminary hazard analysis and a first-pass design FMEA of option A
---

# ZeerBox risk register and hazard analysis

The largest project risk is that the store is designed before anyone who would use it has been asked: size, ownership, crops and season are all proposals. The largest hazards are people inside a closed room (entrapment and air quality, the latter worst when the battery is flat, ZBX-DEC-001 D3), warm recirculating water (*Legionella*), and a roof on posts in a strong wind; the highest design FMEA risks are the pad drying or scaling so that the store stops cooling without the user noticing, and a flat battery leaving the room unventilated. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be found) to 5 (unlikely to be found).

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Requirements do not match users' needs | No co-design session yet; targets set from literature (ZBX-URS-001) | Wrong size, cost or season; a store that sits unused, as some solar cold rooms did (ZBX-PRB-001) | 4 | 5 | Project lead | Approach the first candidate partner (ZBX-DEC-001) before any TRL 4 work; revise URS and PRS from sessions |
| P2 | Fan and pad curves differ from the assumed ones | Airflow and effectiveness rest on assumed curves (STM S3, S5) | Less airflow or effectiveness, warmer and drier store | 3 | 3 | Design lead | Get supplier charts (ZBX-DEC-001 to confirm 2); rerun CAL; a 185 mm pad or a third fan are the levers |
| P3 | Humidity below target in the unfavorable case | The air warms 2 to 3 K across the store and loses RH (PR-003 at risk) | Leafy produce wilts | 3 | 3 | Design lead | Covered or lined crates (decided); measure at TRL 4 |
| P4 | No dry, pest-proof rice husk near the site | Local supply unknown | Fall back to dry sand, about 0.3 K warmer and about 1.8 t heavier | 3 | 2 | Partner | Confirm supply (to confirm 5) |
| P5 | Cellulose pads not sold in the region | Pads come from poultry or greenhouse suppliers, perhaps only in a capital city | Delay or higher cost; replacements every few years | 3 | 3 | Procurement | Survey suppliers with the partner (PR-010); price in MKT |
| P6 | Kit cost rises past the value-engineering target | Prices are indicative, not quoted; kit already at USD 300 | Over target | 3 | 2 | Project lead | Quotes at TRL 4; savings listed in ZBX-DEC-001 (steel angle frames, about USD 8) |
| P7 | The store is used in the rainy season and disappoints | Evaporative cooling gives 2 to 3 K at 75 % RH | Users lose trust | 3 | 3 | Partner | Lamp shows the mode; set expectations in training; ask whether rainy-season use matters (ZBX-PRB-001) |
| P8 | Recommended concept is not chosen | Options within 10 % (ZBX-OPT-001); concept choice is Amish's | Redesign to option B or C | 2 | 4 | Amish | Decision requested in ZBX-DDR-004 |

## Preliminary hazard analysis

Table 2. Hazards (option A).

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Entrapment in the store | Door closed on a person inside | Heat stress, fear, injury | 4 | 2 | Inside release latch, no outside lock (PR-009); door opens outward | Low |
| H2 | Poor air in a closed store | Produce respiration; fans off when the battery is flat for more than about 40 h, or hold-mode flow stalled by wind on the pad wall (independent review); door shut | About 2.3 % CO₂ in 12 h sealed (STM S36), dizziness | 3 | 2 | Hold mode keeps about 8 air changes an hour while powered (STM S28); safety note to air the store before entering; passive vent proposed (ZBX-DEC-001 D3) | Medium until D3 is decided |
| H3 | *Legionella* and other bacteria in the sump and pad | Warm recirculating water, sediment, biofilm; droplets from the pad | Respiratory infection | 4 | 2 | Covered, shaded sump; daily bleed and daily pad dry-out; fans run 10 min before entry (D5); weekly drain and clean; weekly shock chlorination proposed (D8); water never used for drinking or washing produce (WHO 2007, ZBX-REG-001 G9) | Medium, depends on routine |
| H4 | Mold on produce and walls | Damp store, rotten produce left in | Spoiled produce; spores | 2 | 3 | Guard mode stops the pump at 95 % RH for 60 min (PR-005); weekly cleaning | Low |
| H5 | Roof lifted by wind | Gust above the 30 m/s design case (the footing factor falls below 1.5 above about 32 m/s); edge-zone pressures; ties not rated | Falling sheets and timber | 5 | 2 | Footings 1.8 times the uplift; ties rated 2 kN; sheets screwed to every purlin; confirm the local design wind speed before building (to confirm 6, ZBX-DEC-001 D7) | Medium until the wind speed is confirmed |
| H6 | Masonry collapse | Poor workmanship; cracks; soft soil | Crushing | 5 | 1 | Strip footing, competent mason, seasonal inspection; bearing 16 kPa on firm soil | Low |
| H7 | Battery fire or burn | Short circuit, charging out of the 0 to 45 °C range, damaged cell | Fire, burns | 4 | 1 | LiFePO4 with BMS; DC-rated 15 A battery fuse on 2.5 mm² leads and 5 A load fuse (ZBX-DEC-001 D1, D5); shaded, ventilated box; location inside the store proposed (D6) | Low |
| H8 | Cable overheating | Load-circuit fault protected only by the 15 A battery fuse (found by STM S16) | Fire in the roof space | 4 | 2 | Fixed: 5 A load fuse within the 13.8 A capacity of the 1.5 mm² cable (D1) | Low |
| H9 | Fan blade contact | Hand in the fan during cleaning | Cuts | 2 | 2 | Guards on both faces; isolate power before cleaning | Low |
| H10 | Rice husk fire | Hot work near the walls; damaged conduit | Smouldering fire in the cavity | 4 | 1 | Cavity capped with mortar; no hot work near the walls; solar wiring in conduit at the wall top | Low |
| H11 | Food safety misunderstanding | Users treat the store as a cold room | Illness from meat, fish or milk stored warm | 4 | 2 | Clear labelling and training: not for meat, fish, milk or medicines (ZBX-PRC-001); Codex practice (REG G11) | Medium |

## Design FMEA (first pass, P3)

Table 3. Failure modes of option A. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Cellulose pad (line 6) | Wet the incoming air | Dry patches or scale on the pad | Warmer, drier store; user may not notice | Pump flow too low, blocked header holes, hard water | 4 | 3 | 4 | 48 | Bleed sized for 4 cycles of concentration (D5); log supply-air RH and alarm on a high supply temperature at TRL 4; clean header holes in weekly routine |
| F2 | Pump and float switch (line 7) | Lift water to the header | Pump runs dry or stops | Pad dries; pump burns out | Sump not refilled; float stuck | 3 | 3 | 3 | 27 | Float switch interlock (guard mode); sump level visible; weekly check |
| F3 | Exhaust fans (line 8) | Move about 560 m³/h | Fan stops or slows | No cooling; rising CO₂ | Dust in bearings; connector corrosion | 4 | 2 | 3 | 24 | Controller checks fan current; spare fan; guards cleaned |
| F4 | Inside and outside sensors (line 9) | Pick the mode | Sensor drift or failure | Wrong mode (wet pad in humid weather or no cooling) | Dust, condensation, radiation on the outside sensor | 3 | 3 | 3 | 27 | Six-plate shield; plausibility check between sensors; replace yearly |
| F5 | Battery and charge controller (line 11) | Store energy for the evening and cloud | Battery flat or BMS cut-off | Fans stop; sealed room (H2) | Long cloud, harmattan haze, ageing, BMS stopping charge above 45 °C | 4 | 3 | 3 | 36 | Low-battery guard mode; passive vent proposed (D3); battery inside the store proposed (D6) |
| F6 | Load fuse (line 11) | Protect the load cable | Wrong fuse fitted (15 A in place of 5 A) | Cable overheats on a fault | Generic fuses look alike | 4 | 2 | 4 | 32 | Label the holder "5 A"; fuse rating in the build plan wiring step |
| F7 | Door seal and latch (line 5) | Keep warm air out; open from inside | Seal worn; latch jams | More heat load; entrapment risk | Wear, dust, warping | 4 | 2 | 2 | 16 | Inside release with no lock; seasonal check |
| F8 | Rice husk fill (line 2) | Insulate the walls | Fill gets wet or eaten | Higher wall gain; pests | Leaking capping course; rodents | 2 | 2 | 4 | 16 | Damp-proof course, lime, mortar cap, mesh at openings |
| F9 | Hurricane ties and roof screws (lines 4, 17) | Hold the roof down | Tie or screw pulls out | Roof damage in a storm | Undersized or missing ties; rotten timber | 5 | 2 | 3 | 30 | Ties rated 2 kN (to confirm 4); count every tie at handover |
| F10 | Gutter and return hose (line 6) | Return pad water to the sump | Gutter overflows or hose blocks | Water on the floor and wall; sump empties | Debris, algae | 2 | 3 | 2 | 12 | Weekly clean; mesh at the outlet |

The pad drying or scaling unnoticed (F1, RPN 48), a flat battery leaving the room unventilated (F5, RPN 36) and a wrong fuse (F6, RPN 32) are the top design risks; they are addressed by the bleed (D5), the decisions proposed in D3 and D6, the build plan and logging at TRL 4.
