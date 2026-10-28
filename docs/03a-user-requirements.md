---
doc_id: ZBX-URS-001
title: ZeerBox user requirements
project: ZeerBox
doc_type: User requirements
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First issue (kit 1.9.1 upgrade), drawn from the users, operating environment and constraints in ZBX-PRB-001 v0.8
---

# ZeerBox user requirements

What smallholder growers, farmer groups, traders and the local builders and technicians who would build and mend ZeerBox need, written from their side. No user has been consulted yet: every row comes from ZBX-PRB-001 (users table, operating environment and constraints) and from the published field work it cites, and each is to be checked in co-design sessions with the first candidate partner (MIT D-Lab's evaporative cooling team, a dry-season vegetable area of Mali; ZBX-DEC-001). The product requirements that meet these needs are in ZBX-PRS-001 (`03-requirements.md`), and the links are in the generated traceability matrix ZBX-RTM-001 (`03b-traceability.md`). Method: STANDARDS section 22.

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Performance | Hold several days of harvest | I can keep one to five days of picking, about 20 crates, so I sell when the price is right and not on the day I pick | High | Smallholder vegetable grower; farmer group (PRB Table 1) |
| UR-002 | Usability | Load without heavy lifting | I can walk in and reach every crate without lifting a full crate above my shoulders or bending into a pit | Medium | Smallholder grower; market trader (PRB, gap 2: ground-level passive coolers) |
| UR-003 | Performance | Noticeably cooler on hot dry days | On a hot, dry afternoon the produce sits clearly cooler than the air outside | High | Smallholder grower (PRB, design climate and gap 1) |
| UR-004 | Performance | Produce does not wilt | Leafy greens and tomatoes do not dry out and shrivel while stored | High | Smallholder grower; market trader (PRB, produce conditions) |
| UR-005 | Usability | Know when it is not cooling | I can see at a glance whether the store is cooling, airing or idle, so I know when to keep the door shut and when the store is not helping | High | Smallholder grower; farmer group (PRB, gap 3) |
| UR-006 | Safety | No mold and safe air | The store does not grow mold or smell, and the air inside is safe to walk into | High | Farmer group; market trader (PRB, Safety) |
| UR-007 | Performance | Produce lasts longer | Tomatoes and peppers keep noticeably longer than in the shade outside | High | Smallholder grower (PRB, the problem) |
| UR-008 | Logistics | Works without the grid | It runs where there is no grid or an unreliable one | High | All users (PRB, operating environment: power) |
| UR-009 | Logistics | Water I can carry | The water it needs on the hottest day is an amount I can carry or pump by hand, and it holds a day's supply | Medium | Smallholder grower; farmer group (PRB, operating environment: water) |
| UR-010 | Safety | Safe to touch and work on | Nothing electrical can give a shock, the fans cannot catch a hand and nobody can be shut in | High | All users; local electrician (PRB, constraints) |
| UR-011 | Deployment and assembly | Built by local trades | A local mason and carpenter can build it from bricks, timber and sheet they already buy, with no refrigeration trade | High | Local builder (PRB Table 1 and constraints) |
| UR-012 | Maintenance | Mended from the regional town | A local electrician can swap a fan, pump, sensor or pad quickly with a generic part from the regional town | High | Local electrician or phone-repair technician (PRB Table 1) |
| UR-013 | Environment and durability | Lasts in heat, dust, termites and wind | The structure lasts many years, and the moving parts several seasons, in heat, dust, termites and strong wind | Medium | Farmer group; local builder (PRB, site) |
| UR-014 | Cost | Affordable to a group | A farmer group can afford the cooling equipment, and the building is priced in local materials | High | Farmer group or cooperative (PRB, constraints) |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.

Regulatory needs (food safety practice, battery and solar parts) are in the regulatory register ZBX-REG-001; they are not written as user requirements because no user stated them.
