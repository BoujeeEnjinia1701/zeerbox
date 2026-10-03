---
doc_id: ZBX-DDR-002
title: ZeerBox recommendations accepted
project: ZeerBox
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of all open recommendations (TRL 3 items 11 to 13) and the items that remain open
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Items 9 and 10 recorded as decided by Amish on 2026-10-02
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items 11, 12 and 13); items 9 and 10 decided by Amish on 2026-10-02 (ZBX-DEC-001)

## Context

After the TRL 3 session, `docs/REVIEW.md` and ZBX-DDR-001 listed five items as "Proposed, awaiting Amish". Three of them (11, 12 and 13) carried a recommendation; two (9 and 10) did not. On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." This record lists what that instruction decides, what changed in the repo because of it, and what stays open. TRL 4 remains on hold by Amish's instruction, and the repo stays at TRL 3.

## Options considered

The options for each item are in ZBX-DDR-001, Table 2, and in ZBX-CAL-001 v0.1, sections 4, 5 and 10. They are not repeated here.

## Decision

*Table 1. Newly decided items. Figures are central estimates from ZBX-CAL-001 at the 35 °C, 30 % RH design point.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 11 | R3 not met, R2 at risk | Decided by Amish, 2026-09-25: go with recommendation. Option (c): a 150 mm pad on the same fans, R3 relaxed from 85 % to 80 %, and produce-level measures (covered or lined crates for leafy and water-sensitive produce) | `PAD_T` 100 to 150 mm in `cad/src/model.py`; BOM line 6 $30 to $40; R3 target 85 to 80 % in ZBX-REQ-001 v0.4 and `sizing.py`; store RH 71 to 81 % (R3 not met to at risk); airflow 584 to 563 m³/h; ZBX-PRC-001 v0.4 |
| 12 | Wet cavity against a dry insulating fill | Decided by Amish, 2026-09-25: go with recommendation. Option (b): dry rice husk fill, kept dry and protected from termites and rodents, subject to a durable, pest-proof supply locally; dry sand is the fallback. This supersedes ZBX-DDR-001 item 6 (wet sand cavity) | `FILL` parameter set to rice husk in `cad/src/model.py`; BOM line 2 now lime-treated husk on a damp-proof course with a mortar cap and mesh ($20 to $15, wetting pipe removed); cavity water 12 to 0 L/day; total water 44 to 36 L/day; fill mass 2.4 to 0.15 t |
| 13 | Roof footing size and design wind speed | Decided by Amish, 2026-09-25: go with recommendation. Keep 500 x 500 x 600 mm footings as a minimum; confirm the local design wind speed with a builder at the chosen site | No geometry change. Recorded in ZBX-CAL-001 v0.2 section 10, ZBX-PRC-001 v0.4 and ZBX-REQ-001 v0.4 R11. Confirming the wind speed needs a site and a builder, so it waits for the partner (item 10) |

Combined effect of items 11 and 12 (ZBX-CAL-001 v0.2):

*Table 2. Before and after.*

| Quantity | Before (CAL-001 v0.1) | After (CAL-001 v0.2) |
| --- | --- | --- |
| Pad effectiveness | 75.7 % | 88.2 % |
| Supply air | 24.8 °C, 75 % RH | 23.1 °C, 87 % RH |
| Mean store air | 25.9 °C, 71 % RH | 24.3 °C, 81 % RH |
| Drop below ambient (R2, 8 K) | 9.1 K (8.0 to 10.0 K), at risk | 10.7 K (9.8 to 11.4 K), met |
| Store RH (R3) | 71 % against 85 %, not met | 81 % (77 to 85 %) against 80 %, at risk |
| Heat load | 418 W | 442 W |
| Water per design day (R8) | 44 L | 36 L |
| Cooling equipment kit (R12, $300) | $260 | $270 |
| Structure, costed separately | $360 | $355 |
| Store total, crates excluded | $620 | $625 |

`budget_usd` stays at $300 for the cooling equipment kit (ZBX-DDR-001 item 1); no budget change was recommended. The pitch and problem lines had no recommended rewording and are unchanged. Drawing ZBX-DWG-001 is reissued at Rev P2; the STEP and STL files, the concept media and `docs/04-calcs/results.csv` are regenerated from the model.

No item needs another repo to change, and no item was TRL 4 work that had to be put on hold.

### Items left open on 2026-09-25 (decided 2026-10-02)

*Table 3. No recommendation was made on 2026-09-25; both items were decided by Amish on 2026-10-02 (ZBX-DEC-001).*

| # | Item | Status |
| --- | --- | --- |
| 9 | Wall material: fired brick, mud brick or concrete block | Decided 2026-10-02: fired brick, the working choice in the model and BOM |
| 10 | First co-design partner, region and crop mix | Decided 2026-10-02: MIT D-Lab's evaporative cooling team as the first candidate to approach, Mali as the first candidate region, tomatoes, peppers and okra with leafy greens on a separate rack |

## Consequences

- R2 is now met in every case. R3, relaxed to 80 %, is at risk: 77 % in the unfavorable case. No requirement is not met; R6, R10 and R11 still need field data or a partner.
- The dry husk fill must stay dry and pest-free. If no durable husk supply exists at the chosen site, dry sand costs about 0.3 K of cooling and adds about 1.9 t of wall mass.
- Dry husk is combustible; ZBX-PRC-001 v0.4 adds a safety note on capping the cavity and keeping hot work away from it.
- TRL 4 work (a pad and fan test article, a controller bench test, crate liner trials, a site wind survey) is on hold by Amish's instruction.
