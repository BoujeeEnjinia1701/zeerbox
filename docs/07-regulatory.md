---
doc_id: ZBX-REG-001
title: ZeerBox regulatory and standards register
project: ZeerBox
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First register (kit 1.9.1 upgrade), stages P0 to P3, for the first candidate region (a dry-season vegetable area of Mali, ZBX-DEC-001)
---

# ZeerBox regulatory and standards register

ZeerBox is a walk-in room built by local trades with a 12 V solar kit inside it, used to keep vegetables, so the rules that matter fall into four groups: the building itself (local building practice and wind loads, G1 and G2), the low-voltage solar and battery kit (G3 to G8), the water and air in the store (G9 and G10), and food handling (G11). No product standard for evaporative produce stores was found, nothing here needs certification before TRL 4, and Mali's own building, electrical and food rules have not been researched and are all "to assess" with the partner. The agriculture focus area's shared register rows are in GrainGuard (GGD-REG-001, rows A1 to A3); they cover grain bins in the United States and do not apply here, so this register starts the rows for produce storage in West Africa. Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | Local building permission and building rules for small agricultural structures | Mali (first candidate region) | Whether a 3 x 2 m masonry store with a roof on posts needs a permit, and the rules it must follow | The structure (BOM lines 1 to 5, 12, 15 to 17); not researched | Partner with a local builder | To assess |
| G2 | EN 1991-1-4 (Eurocode 1, wind actions), used as practice; or the national wind map where one exists | International practice; national | Design wind speed and pressure coefficients for canopy roofs | Roof uplift is sized for a 30 m/s gust with a net pressure coefficient of 1.5 (ZBX-CAL-001 s10); the local design wind speed is still to confirm (ZBX-DEC-001 to confirm 6) | Design lead with a local builder | To assess (method followed, wind speed to confirm) |
| G3 | IEC 61140, protection against electric shock (extra-low voltage), and IEC 60364-4-41 | International | Shock protection; extra-low voltage below 120 V ripple-free DC | The whole kit runs at 12.8 V nominal (PR-009) | Electronics lead | Met by design (conformance not claimed) |
| G4 | IEC 60364-5-52, selection and erection of wiring systems (current-carrying capacity and temperature correction) | International | Cable sizing and protection | Used to check the load-circuit fuse against the derated 1.5 mm² cable (STM S16, ZBX-DEC-001 D1); values to confirm against the edition used | Electronics lead | Applies (method followed) |
| G5 | IEC 61215 and IEC 61730, PV module design qualification and safety | International | Module performance and safety qualification | Buy a 150 W module certified to both (BOM line 10) | Procurement | Applies (buy certified modules) |
| G6 | IEC 62509, battery charge controllers for photovoltaic systems | International | Performance and functioning of PV charge controllers | The 20 A PWM controller (BOM line 11) | Procurement | To assess (product stage) |
| G7 | UN Manual of Tests and Criteria, section 38.3 (lithium cells and batteries in transport) | International | Tests a lithium battery type must pass before it is shipped | The 12.8 V 12 Ah LiFePO4 battery: buy one with a UN 38.3 test summary | Procurement | Applies (buy certified batteries) |
| G8 | IEC 60529, degrees of protection provided by enclosures (IP code) | International | Dust and water ingress ratings | Controller box IP65 (bought rating) beside a wet pad; connections IP65 | Design lead | Met by design (bought ratings), to verify after drilling at TRL 4 |
| G9 | WHO, *Legionella and the prevention of legionellosis* (2007); AS/NZS 3666 (microbial control of air-handling and water systems, including evaporative coolers), cited as practice | International guidance; Australia and New Zealand | Risk of *Legionella* growth in warm recirculating water and its control | Covered sump, weekly drain and clean, pad dried regularly, sump water never used for drinking or washing produce (ZBX-PRC-001 Safety, STM S27) | Partner and users | Applies (guidance followed); AS/NZS 3666 to assess |
| G10 | Workplace exposure limits for carbon dioxide (for example 5,000 ppm, 8 h time-weighted average, in many national lists) | National | Air quality in an occupied room | Produce respiration in a closed store; at 1 air change an hour CO₂ stays near 2,300 ppm (STM S28); a sealed store reaches about 2.3 % in 12 h (STM S36, ZBX-DEC-001 D3) | Design lead | Met by design while powered; no-power case to Amish (D3) |
| G11 | Codex Alimentarius CXC 53-2003, code of hygienic practice for fresh fruits and vegetables | International (FAO and WHO) | Hygiene in production, packing, storage and transport of fresh produce | Clean crates and store, separate rotten produce, keep sump water off produce; ZeerBox slows spoilage and makes no food-safety claim | Partner and users | Applies (practice) |
| G12 | Restriction of hazardous substances and e-waste take-back (for example the EU RoHS Directive 2011/65/EU) | European Union; national | Hazardous substances in electronics; end of life of boards and the battery | Only if kits are sold in a market that has such rules | Electronics lead | Does not apply now |

Status: to assess, applies, does not apply, met by design, certification needed later.

Options B and C (ZBX-OPT-001) have no electrical kit, so G3 to G8 and G12 drop out; G1, G2, G9 (option B and C water in tanks and wet walls), G10 (both are slowly ventilated rooms with produce) and G11 apply as for option A.

## Sources

- World Health Organization. *Legionella and the Prevention of Legionellosis*. Geneva: WHO, 2007, https://www.who.int/publications/i/item/9241562978 (checked 2026-10-24).
- FAO and WHO, Codex Alimentarius. *Code of Hygienic Practice for Fresh Fruits and Vegetables* (CXC 53-2003), https://www.fao.org/fao-who-codexalimentarius/codex-texts/codes-of-practice/ (listing checked 2026-10-24).
- Rows G2 to G8, G10 and G12 and AS/NZS 3666 in G9 are listed from the standards' and regulations' own titles; their texts were not consulted for this register, except the two IEC 60364-5-52 table values used in ZBX-CAL-001 section 9, and each applicability is to be confirmed by the role named. Row G1 has not been researched.
