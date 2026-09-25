# ZeerBox

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Agriculture · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** $300 USD for the cooling equipment kit · **Difficulty:** 2 of 5

Walk-in evaporative cooling chamber with a solar fan that forces air through a wetted pad, and a controller that responds to humidity.

![ZeerBox concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement ZBX-DWG-001 (PDF)](cad/drawings/ZBX-DWG-001.pdf) · [Sizing note ZBX-CAL-001](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Smallholders lose produce after harvest because they have no cold storage. Refrigerated cold rooms cost tens of thousands of dollars, and passive evaporative coolers are small and fail in humid weather. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## Concept

A walk-in store (2.4 x 1.5 x 2.0 m inside, 24 crates) with double brick walls around a wet sand cavity. Two 12 V fans pull outside air through a wetted cellulose pad, and a controller reads temperature and humidity inside and out to choose between evaporative cooling, night ventilation and hold. A 150 W solar panel with a small battery powers it. The TRL 3 calculation puts the store at about 25.9 °C on a 35 °C, 30 % RH day, 9.1 K below the outside air, using about 44 L of water. Store humidity is about 71 %, short of the 85 % target (estimates, [ZBX-CAL-001](docs/04-calcs/01-sizing.md)).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Double brick walls with a wet sand cavity, insulated ceiling and shade roof
- 100 mm cellulose evaporative pad with drip header and gutter
- Two 250 mm 12 V DC exhaust fans
- 60 L sump drum with a 12 V pump
- 150 W PV panel, 20 A PWM charge controller and small LiFePO4 battery
- Controller with inside and outside humidity and temperature sensors

The priced bill of materials is in [bom/bom.csv](bom/bom.csv). The $300 budget covers the cooling equipment kit, about $260; the structure is built from local materials and costed separately, about $360 (indicative).

## Safety

> A walk-in room: the door must open from inside. Warm recirculating water can grow *Legionella*, so cover, drain and clean the sump weekly. Contains a LiFePO4 battery; use a BMS, fuse it and keep it shaded. Guard the fans. Not for meat, fish, milk or medicines.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (ZBX-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `ZBX-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
