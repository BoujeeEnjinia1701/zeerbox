# ZeerBox

**Area:** Agriculture · **Status:** Concept · **Prototype budget:** about $300 USD · **Difficulty:** 2 of 5

Walk-in evaporative cooling chamber with a solar fan that forces air through a wetted pad, and a controller that responds to humidity.

## Problem

Smallholders lose produce after harvest because they have no cold storage.

## Concept

Walk-in evaporative cooling chamber with a solar fan that forces air through a wetted pad, and a controller that responds to humidity.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Brick or panel walls
- Cellulose evaporative pads
- 12 V fans
- Small pump
- PV panel
- Humidity and temperature sensor

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
