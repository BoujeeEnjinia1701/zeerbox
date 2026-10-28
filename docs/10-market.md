---
doc_id: ZBX-MKT-001
title: ZeerBox market and viability
project: ZeerBox
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First issue (kit 1.9.1 upgrade), with benchmarks checked on 2026-10-24
---

# ZeerBox market and viability

ZeerBox is for smallholder vegetable growers, farmer groups and traders in hot, dry regions who lose produce after harvest and cannot reach or pay for refrigerated storage; it sits between passive brick chambers (about USD 70 to 350, small, ground level, no humidity sense) and solar cold rooms (tens of thousands of dollars, or pay-per-crate where a business runs one). An open design matters because the structure is built from local materials by local trades and every electrical part is generic, so a partner can build and adapt it without buying from one maker. Prices and benchmarks are cited with the date they were checked; nothing here is a quote. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Farmer group or cooperative store | A group of growers sharing a store at a collection point; first candidate region a dry-season vegetable area of Mali (ZBX-DEC-001) | Brick evaporative cooling chamber, USD 70 to 350 for 500 to 5,000 L, USD 260 for the 2,500 L chamber tested, plus about USD 45 for its shade (MIT D-Lab, Mali evaluation, June 2018, Table 8, checked 2026-10-24) | 874 (kit 300 plus structure 574, materials only; labor and crates excluded; ZBX-CAL-001 s11) | About 7 m³ walk-in store for 24 crates at working height, 10.7 K below outside air on a design day against 4 to 7 K for a passive chamber, and a lamp that says whether it is cooling |
| Market trader's depot | Traders keeping stock between market days near a market | Pay-per-crate solar cold room: ColdHubs, about NGN 100 (about USD 0.25) per crate per day, 3 t (about 150 crates) per hub at about 5 °C, not sold as a product (TechXLab listing, checked 2026-10-24); earlier reported at about USD 0.50 per crate per day (ZBX-PRB-001) | 874, as above | Owned rather than rented and near the stall; does not reach cold-chain temperatures, so it suits tomatoes, peppers and okra held for days, not meat or milk |
| Individual farm store | A smallholder with 0.5 to 2 ha of vegetables | Clay pot coolers, USD 6 to 50 for 10 to 150 L (MIT D-Lab, Mali evaluation, 2018, Table 8); DIY cold room controller for a room air conditioner (CoolBot), USD 379 for the controller alone (Howdy Brewer listing, checked 2026-10-24), which still needs an insulated room, an air conditioner and mains power | 874, as above | Larger than a pot cooler and needs no mains power or compressor; likely too costly for one farm (an open question in ZBX-PRB-001: one farm or a group) |
| NGO and research programs | Extension services and university programs testing post-harvest storage | Forced-air evaporative chambers in shipping containers piloted by MIT D-Lab with partners in Kenya and India; described as using a quarter of the energy of refrigerated cold rooms at half the cost to build; no unit price published (MIT D-Lab, checked 2026-10-24) | 874, as above | An open, smaller, brick-built design with documented calculations, build plan and logging controller for comparing seasons and sites |

Parts benchmarks used in the BOM review:

| Part | Cited price | Source and date | BOM line and indicative price |
| --- | --- | --- | --- |
| 150 mm cellulose evaporative pad | INR 460 per square foot (one listing, 1,000 x 450 x 150 mm); others at INR 425 to 450 per square foot for 100 to 200 mm pads | IndiaMART cellulose pad listings, checked 2026-10-24 | Line 6, pad about USD 30 of USD 50; a West African price to assess |
| 300 mm turbine roof ventilator (option C) | AUD 199 retail | Fans Online, Bradford Windmaster 300 mm listing, checked 2026-10-24 | Option C only; a regional-market price to assess |
| 250 mm 12 V DC axial fan | No listing found for this size and voltage in the sources checked | To assess | Line 8, USD 15 each, indicative |

## Value and viability

- **Cost per crate-day.** At USD 874 for 24 crates, and assuming the store is full for 150 days a year over a 10-year structure life with the kit replaced once (about USD 300 more), the materials cost about USD 0.03 per crate per day before labor, water and maintenance. This is an illustration of scale, not a business case: utilization, labor and ownership are for the partner to work out with users (ZBX-PRB-001, out of scope).
- **What it does not do.** It holds about 24 °C on a 35 °C day, not 12.5 to 15 °C; it slows spoilage of tomatoes, peppers and okra and is not for meat, fish, milk or medicines. In the rainy season it is little more than a shaded, ventilated shed.
- **Options B and C** (ZBX-OPT-001) cost less (about USD 670 and USD 520, estimates) and need no power, but cool less on a full load (about 3 K and about 7 K in a light wind, first order) and neither tells the user whether it is cooling.

## Open route

Who would build it: a local mason and carpenter for the structure, and a local electrician or phone-repair technician for the 12 V kit, from the build plan ZBX-BLD-001 and the drawings. How it spreads: through a partner that already runs evaporative cooling programs (the first candidate is MIT D-Lab's evaporative cooling team), farmer groups and extension services, and open publication of the design under CERN-OHL-S-2.0 (hardware) and MIT (software), which requires that modified designs stay open. What keeps it open: generic parts in every line of the BOM, no proprietary controller, and the calculation, model and drawings in one public repository that a partner can rerun for a new site or crop.

## Sources

- Verploegen, E., O. Sanogo and T. Chagomoka. *Evaporative Cooling Technologies for Improved Vegetable Storage in Mali, Evaluation Report*. MIT D-Lab, June 2018, Table 8, https://d-lab.mit.edu/sites/default/files/inline-files/Evaporative%20Cooling%20Technologies%20for%20Improved%20Vegetable%20Storage%20in%20Mali%20-%20Evaluation%20Report_0.pdf (checked 2026-10-24).
- TechXLab. "Cold Rooms by ColdHubs." https://techxlab.org/solutions/cold-rooms-by-coldhubs/ (checked 2026-10-24).
- Howdy Brewer. "CoolBot Walk-In Cooler Controller." https://howdybrewer.com/products/coolbot-cooler-controller (checked 2026-10-24).
- MIT D-Lab. "Room-sized cooling chambers." https://d-lab.mit.edu/research/evaporative-cooling-vegetable-preservation/room-sized-cooling-chambers (checked 2026-10-24).
- IndiaMART. "Cellulose Pad." https://m.indiamart.com/impcat/cellulose-pad.html (checked 2026-10-24).
- Fans Online. "Bradford Windmaster, Natural Roof Ventilator, 300 mm." https://fansonline.com.au/product/csr-windmaster-whirlybird-deep-ocean-finish (checked 2026-10-24).
- Engineering for Change. "Evaporative Cooling Chambers." https://www.engineeringforchange.org/solutions/product/evaporative-cooling-chambers/ (checked 2026-10-24): open-source brick chamber, suggested retail price USD 100 depending on local materials.
