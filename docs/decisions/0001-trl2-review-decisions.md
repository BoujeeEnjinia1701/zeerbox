---
doc_id: ZBX-DDR-001
title: ZeerBox TRL 2 review decisions
project: ZeerBox
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Items 11 to 13 decided; item 6 superseded by item 12
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 8; items 11 to 13 accepted later the same day, see ZBX-DDR-002); items 9 and 10 remain proposed, awaiting Amish

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed ten items as "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." The same instruction approved cross-cutting SwapCell interface items, a pricing rule for shared SwapCell packs, and a rule that community designs pick co-design partners per area later.

This record lists what that instruction decides and what it leaves open because there was no recommendation to accept. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 section) and ZBX-PRC-001 v0.2. They are not repeated here.

## Decision

*Table 1. Decided items.*

| # | Item | Decision | Where it now lives |
| --- | --- | --- | --- |
| 1 | Budget | Decided by Amish, 2026-09-25: go with recommendation. Option (a): keep `budget_usd: 300` and redefine it as the cooling equipment kit (items 6 to 11 and 14). The structure is built from local materials and costed separately. R12 is redefined to match | `project.yaml` (budget unchanged), ZBX-REQ-001 v0.3 R12, `bom/bom-notes.md` |
| 2 | Solar panel size | Decided by Amish, 2026-09-25: go with recommendation. 150 W panel | `bom/bom.csv` line 10, `cad/src/model.py`, ZBX-CAL-001 section 7 |
| 3 | Battery | Decided by Amish, 2026-09-25: go with recommendation. Keep the 12.8 V 12 Ah LiFePO4 battery for evening ventilation | `bom/bom.csv` line 11 |
| 4 | Forced air through a pad | Decided by Amish, 2026-09-25: go with recommendation. Forced air, not a passive ZECC-style chamber | ZBX-PRC-001 v0.3 |
| 5 | Fan arrangement | Decided by Amish, 2026-09-25: go with recommendation. Exhaust fans beside the door, pad on the opposite wall | ZBX-PRC-001 v0.3, `cad/src/model.py` |
| 6 | Wall type | Decided by Amish, 2026-09-25: go with recommendation. Wet sand cavity walls, pending the TRL 3 heat balance. That heat balance (ZBX-CAL-001 section 4.1) shows only a small benefit. Superseded by item 12 (dry rice husk fill), decided in ZBX-DDR-002 | ZBX-PRC-001 v0.3, `cad/src/model.py` |
| 7 | Store size | Decided by Amish, 2026-09-25: go with recommendation. Keep 24 crates until a partner confirms the need | ZBX-REQ-001 R1, `cad/src/model.py` |
| 8 | Control thresholds | Decided by Amish, 2026-09-25: go with recommendation. 20 °C set point, 4 K wet-bulb depression and 95 % RH guard as starting values for field tuning | ZBX-PRC-001 v0.3, control modes |

The pitch and problem lines had no recommended rewording in the TRL 2 review and are unchanged.

Cross-cutting approvals from the same instruction, recorded here:

- **SwapCell interface v0.3.** Decided by Amish, 2026-09-25 (cross-cutting): the SwapCell interface adds a wake method for hosts without CAN, a charge-while-discharging mode and a latch vibration rating for vehicles. ZeerBox does not use SwapCell (its 31 W, 12 V load runs from a 154 Wh battery), so no v0.3 items apply.
- **Shared packs are priced once.** Decided by Amish, 2026-09-25 (cross-cutting). Not applicable: ZeerBox has no SwapCell pack.
- **Co-design partners per area later.** Decided by Amish, 2026-09-25 (cross-cutting): community designs pick co-design partners per area later. The partner for ZeerBox stays open (item 10).

### Items that remain open

*Table 2. Items open when this record was first issued. Items 11 to 13 are now decided by Amish, 2026-09-25: go with recommendation (ZBX-DDR-002). Items 9 and 10 remain proposed, awaiting Amish.*

| # | Item | Why it is open | Options and recommendation |
| --- | --- | --- | --- |
| 9 | Wall material | The TRL 2 review listed fired brick against mud brick or block with no recommendation | Fired brick (the working choice in the model and BOM), mud brick or concrete block. No recommendation stated |
| 10 | First partner, region and crop mix | No recommendation; the cross-cutting rule leaves partners to be picked per area later | For example a dry-season vegetable area in the Sahel, or a group already using D-Lab designs in Kenya |
| 11 | R3 not met, R2 at risk. Decided by Amish, 2026-09-25: go with recommendation (ZBX-DDR-002) | New at TRL 3: store RH is about 71 % against 85 %, and the unfavorable case gives 8.0 K against 8 K (ZBX-CAL-001 sections 4 and 5) | (a) 150 mm pad on the same fans: 10.5 K and 81 % RH, about $10 more (indicative); (b) relax R3 to 70 % and add produce-level measures such as lined or covered crates; (c) both. Recommendation: (c), a 150 mm pad and R3 at 80 % |
| 12 | Wet cavity against a dry insulating fill. Decided by Amish, 2026-09-25: go with recommendation (ZBX-DDR-002) | New at TRL 3: the wet cavity gives 0.15 K over dry sand for about 12 L of water a day, and is slightly worse than dry sand in the unfavorable case; dry rice husk gives 9.2 K with no water (ZBX-CAL-001 section 4.1) | (a) keep the wet cavity as decided; (b) dry rice husk or similar fill, kept dry and protected from termites and rodents; (c) dry sand. Recommendation: (b), subject to a durable, pest-proof fill being available locally |
| 13 | Roof footing size and design wind speed. Decided by Amish, 2026-09-25: go with recommendation (ZBX-DDR-002) | New at TRL 3: at a 30 m/s gust each post needs about 2.2 kN of hold-down; the model uses 500 x 500 x 600 mm footings (factor 1.6) | Confirm the local design wind speed with a builder. Recommendation: keep 500 mm footings as a minimum |

## Consequences

- R12 now covers the $300 cooling equipment kit; the kit costs $260 and the structure, about $360, is costed separately.
- The 150 W panel meets R7 with a 41 % margin, but it needs a 20 A charge controller and 2.5 mm² PV cable (ZBX-CAL-001 section 7). Both are in the BOM.
- R3 was not met and R2 at risk until items 11 and 12 were decided in ZBX-DDR-002; R2 is now met and R3 (relaxed to 80 %) is at risk.
- TRL 4 work (bench tests of the controller, a pad and fan test article, build procedures) is on hold by Amish's instruction.
