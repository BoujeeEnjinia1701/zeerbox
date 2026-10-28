---
doc_id: ZBX-DDR-004
title: ZeerBox concept selection
project: ZeerBox
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Concept selection for the kit 1.9.1 upgrade: options A, B and C within 10 %, all three to Amish without a pick (Proposed, awaiting Amish)"
---

# 0004: Concept selection

- **Date:** 2026-10-24
- **Status:** Proposed, awaiting Amish. No pick: the three options score within 10 % of each other (STANDARDS section 21).

## Context

ZeerBox was designed and taken to TRL 3 before kit 1.8, as a forced-air evaporative store (ZBX-DDR-001 to ZBX-DDR-003). Kit 1.8 asks for at least two concept options with different working principles, scored against the user requirements, with the existing design as option A (STANDARDS section 21); kit 1.9 asks for every option to be modelled to the repo's detail level, D3 at stage P3 (section 24; Amish, 2026-10-24: "Detail every option"). The options, their first-order numbers and the scoring are in ZBX-OPT-001; their STEM rows are in ZBX-STM-001.

## Options considered

| Option | Working principle | Score (of 235) | Meets PR-002 (8 K) | Meets PR-004 (mode shown) | Parts cost (USD, estimate) |
| --- | --- | --- | --- | --- | --- |
| A, forced-air pad store (existing) | Fans pull outside air through a wetted pad into an insulated store; a controller picks the mode from inside and outside temperature and humidity | 190 | Yes, 10.7 K | Yes | 874 |
| B, passive wet-wall chamber | Water in a sand-filled brick cavity evaporates from the outer leaf and cools the walls; stack ventilation; no power | 173 | No, about 3 K at full load | No (a dial only) | About 670 |
| C, charcoal-wall wind cooler | Wind and a turbine ventilator pull air through wet charcoal walls on a timber frame; no power | 173 | No, about 7 K in a light wind | No (a dial only) | About 520 |

Rejected before scoring: a solar-powered refrigerated room (CoolBot-type controller on an air conditioner, or a solar cold room), because the problem statement rules out refrigerant, compressors and cold-chain claims (ZBX-PRB-001, constraints and out of scope) and the pitch is evaporative; and indirect (two-stage) evaporative cooling, because it dries the air the produce needs and its plate heat exchanger is beyond a local workshop.

## Decision

Proposed, awaiting Amish. Options A, B and C are within 10 % of each other, so all three go to Amish without a pick. Until he decides, option A stays the design of record (`CHOSEN = "A"` in `cad/src/model.py`; `concept_chosen` left unset in `project.yaml`), as the current design and the only option that meets both of the pitch's promises (PR-002 and PR-004). Choosing B or C would change the pitch ("a solar fan ... and a controller that responds to humidity") and so is Amish's call in any case.

Whichever option is chosen, the runner-up's best idea is proposed as a graft: option B's passive low vent and stack, with option C's turbine head, as an always-open air path for when option A's battery is flat (ZBX-DEC-001 D3).

## Consequences

- If Amish keeps option A: nothing in the model, drawings, BOM or build plan changes; D3 is decided separately.
- If Amish chooses option B or C: the pitch, the PRS targets for cooling and mode indication, the CAL, drawings, BOM and build plan are redone for that option at TRL 3, from its D3 model in `cad/src/model.py`.
- Options B and C stay in the model at D3 for the record, with assembly STEP files in `cad/step/`.
