---
doc_id: ZBX-PLN-001
title: ZeerBox project plan
project: ZeerBox
doc_type: Project plan
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First plan (kit 1.9.1 upgrade) at stage P3 with the reference list of every source cited in the repo
---

# ZeerBox project plan

ZeerBox is at stage P3 (design outputs, TRL 3): the constructable design is modelled at detail level D3, drawn, priced and planned, with the pipeline documents in place. The next gate is P4 (verification, TRL 4), which is on hold while the portfolio is capped at P3; before it, Amish is asked to choose the concept (ZBX-DDR-004, all three options within 10 %) and to decide the no-power vent (ZBX-DEC-001 D3). Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Problem and users | Project lead | PRB with users-and-needs and stakeholder tables; URS | Done on paper (ZBX-PRB-001 v0.8, ZBX-URS-001); not validated with users |
| STEM check | Design lead | ZBX-STM-001 with `stem_check.py` | Open: six option A rows need supplier or field data, or Amish's decision (D6) |
| Concept options | Design lead | ZBX-OPT-001, ZBX-DDR-004, models of options A, B and C at D3 | Done; choice awaiting Amish |
| Requirements and traceability | Design lead | ZBX-PRS-001, ZBX-RTM-001 | Done; PR-003 at risk |
| Calculations | Design lead | ZBX-CAL-001 v0.4 | Done (load fuse corrected, D1) |
| Model, drawings, BOM | Design lead | `cad/src/model.py` (D3, `cad/fidelity.json`), ZBX-DWG-001 and build plan sheets, `bom/bom.csv` | Done |
| Build plan | Design lead | ZBX-BLD-001 | Done (TRL 3 paper plan) |
| Regulatory, feasibility, risk, market | Project lead | ZBX-REG-001, ZBX-FEA-001, ZBX-RSK-001 (with design FMEA), ZBX-MKT-001 | First issue; Mali rules to assess |
| Partner and co-design | Project lead | Approach MIT D-Lab's evaporative cooling team; co-design sessions in a dry-season vegetable area of Mali | Not started (decided as first candidate, ZBX-DEC-001) |
| Product renders | Coordinator | Cycles renders and storefront images from `cad/src/product_model.py` | Views defined; rendering on Amish's Mac |

## Resources needed

Table 2. Resources (estimates; no cost committed).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Partner field coordinator (co-design) | Two co-design sessions with growers and a farmer group; revised URS and PRS | 10 days | To assess with the partner |
| Local mason and carpenter (P4, on hold) | One prototype store from ZBX-BLD-001 | About 15 days | Labor to assess; materials about 574 (structure) |
| Local electrician (P4, on hold) | Kit installation and wiring | 2 days | Labor to assess; kit about 300 |
| Supplier data | Fan curve, pad effectiveness and pressure drop, pad price in the region | 2 days of enquiries | None |
| Logging through one dry season (P4 and P5, on hold) | Store and supply temperature and RH, airflow, water and energy against PR-002 to PR-008 | One season | Within the kit (the controller logs) |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB with users and stakeholders, STM, OPT, REG, FEA, PLN | Met (2026-10-24) |
| P1 Definition | URS, PRS draft, RSK with hazard analysis, MKT, REG complete | Met on paper (2026-10-24); REG has rows to assess |
| P2 Design inputs | PRS with targets, tolerance and verification; CAL; RTM; concept selection DDR; STEM check closed; feasibility closed | Met except the STEM check, which stays open on five data-dependent rows (allowed at TRL 3 for a repo upgraded to kit 1.8, STANDARDS section 20) |
| P3 Design outputs | Model, STEP, drawings, priced BOM, build plan, DEC, design FMEA, traceability | Met (2026-10-24) |
| P4 Verification | Test plans and reports, verification report, reliability plan | On hold (portfolio cap P3) |
| P5 Validation | Field trial with a partner, validation and human factors reports | On hold |
| P6 Commercialization | Launch plan, instructions for use, training; a named deployment partner | On hold |

## Next steps and decision requested

1. **Decision for Amish: concept choice** (ZBX-DDR-004). Options A (190), B (173) and C (173 of 235) are all within 10 %, so all three go to Amish without a pick. Option A is the current design and stays unless he decides otherwise.
2. **Decision for Amish: no-power ventilation** (ZBX-DEC-001 D3). Recommended: a meshed passive vent through the ceiling with option C's turbine head, so the store keeps a minimum air change when the battery is flat.
3. Ask the fan and pad suppliers for their curves (ZBX-DEC-001 to confirm 2) and rerun ZBX-CAL-001.
4. Approach the first candidate partner and plan co-design sessions before any TRL 4 work.
5. Ready for TRL 4 on paper once 1 and 2 are decided; TRL 4 itself waits for the portfolio cap to lift.

## References

Every source cited in this repo's documents, Chicago style.

- ASHRAE. *ASHRAE Handbook: Fundamentals*. Atlanta: ASHRAE, 2017.
- Cigarruista Solis, Luis, Miguel Chen Austin, Euclides Deago, Guillermo Lopez and Nacari Marin-Calvo. "Rice Husk-Based Insulators: Manufacturing Process and Thermal Potential Assessment." *Materials* 17 (2024). https://pmc.ncbi.nlm.nih.gov/articles/PMC11173955. Accessed October 24, 2026.
- ColdHubs. https://coldhubs.com/. Cited in ZBX-PRB-001.
- Efficiency for Access. *Lessons Learned from Implementing Solar-Powered Walk-In Cold Rooms for Smallholder Agriculture in Zimbabwe and Malawi*. https://efficiencyforaccess.org/wp-content/uploads/Lessons-learned-from-implementing-solar-powered-walk-in-cold-rooms-for-smallholder-agriculture-in-Zimbabwe-and-Malawi.pdf. Cited in ZBX-PRB-001.
- Engineering for Change. "Evaporative Cooling Chambers." https://www.engineeringforchange.org/solutions/product/evaporative-cooling-chambers/. Accessed October 24, 2026.
- *e-planet*. "Storage Study of Zero Energy Cool Chamber." *e-planet* 18, no. 2. https://www.e-planet.co.in/images/Publication/vol-18-2/storage.pdf. Cited in ZBX-PRB-001.
- FAO. *The State of Food and Agriculture 2019*. Rome: FAO, 2019. https://www.fao.org/interactive/state-of-food-agriculture/2019/en/.
- FAO and WHO, Codex Alimentarius. *Code of Hygienic Practice for Fresh Fruits and Vegetables*, CXC 53-2003. https://www.fao.org/fao-who-codexalimentarius/codex-texts/codes-of-practice/. Accessed October 24, 2026.
- Fans Online. "Bradford Windmaster, Natural Roof Ventilator, 300 mm." https://fansonline.com.au/product/csr-windmaster-whirlybird-deep-ocean-finish. Accessed October 24, 2026.
- Global Agriculture. "FAO: 14 % of the World's Food Is Lost Between Harvest and Retail." https://www.globalagriculture.org/news/fao-14-of-the-worlds-food-is-lost-between-harvest-and-retail/. Cited in ZBX-PRB-001.
- Howdy Brewer. "CoolBot Walk-In Cooler Controller." https://howdybrewer.com/products/coolbot-cooler-controller. Accessed October 24, 2026.
- IEC 60364-5-52:2009. *Low-Voltage Electrical Installations, Part 5-52: Selection and Erection of Electrical Equipment, Wiring Systems*. Geneva: IEC.
- IFPRI. "ColdHubs: Addressing a Crucial Problem of Food Loss in Nigeria with Solar-Powered Refrigeration." https://www.ifpri.org/blog/coldhubs-addressing-crucial-problem-food-loss-nigeria-solar-powered-refrigeration/. Cited in ZBX-PRB-001.
- IndiaMART. "Cellulose Pad." https://m.indiamart.com/impcat/cellulose-pad.html. Accessed October 24, 2026.
- Kader, Adel A., ed. *Postharvest Technology of Horticultural Crops*. 3rd ed. Oakland: University of California Agriculture and Natural Resources, Publication 3311, 2002.
- MIT D-Lab. "Evaporative Cooling for Vegetable Preservation." https://d-lab.mit.edu/research/evaporative-cooling-vegetable-preservation. Cited in ZBX-PRB-001.
- MIT D-Lab. "Room-Sized Cooling Chambers." https://d-lab.mit.edu/research/evaporative-cooling-vegetable-preservation/room-sized-cooling-chambers. Accessed October 24, 2026.
- MIT News. "MIT D-Lab and CITE Release Evaluation of Low-Cost Evaporative Cooling Devices in Mali." 2018. https://news.mit.edu/2018/mit-d-lab-cite-evaluation-low-cost-evaporative-cooling-devices-mali-0620.
- Munters. "CELdek." https://piec.com/celdek/. Cited in ZBX-PRS-001.
- Review of evaporative pad operation. *Renewable and Sustainable Energy Reviews*. https://www.sciencedirect.com/science/article/pii/S1364032121009072. Cited in ZBX-PRB-001.
- Stull, Roland. "Wet-Bulb Temperature from Relative Humidity and Air Temperature." *Journal of Applied Meteorology and Climatology* 50 (2011): 2267 to 2269.
- TechXLab. "Cold Rooms by ColdHubs." https://techxlab.org/solutions/cold-rooms-by-coldhubs/. Accessed October 24, 2026.
- *TIME*. "Best Inventions of 2001: The Pot-in-Pot Cooler." https://content.time.com/time/specials/packages/article/0,28804,1936165_1936254_1936632,00.html. Cited in ZBX-PRB-001.
- UC Davis Postharvest Center. "Tomato." https://postharvest.ucdavis.edu/produce-facts-sheets/tomato. Cited in ZBX-PRB-001.
- Verploegen, Eric, Ousmane Sanogo and Takemore Chagomoka. *Evaluation of Low-Cost Evaporative Cooling Technologies for Improved Vegetable Storage in Mali*. MIT D-Lab, GHTC paper. https://d-lab.mit.edu/sites/default/files/inline-files/GHTC%20-%20Evaluation%20of%20Low-Cost%20Evaporative%20Cooling%20Technologies%20for%20Improved%20Vegetable%20Storage%20in%20Mali.pdf.
- Verploegen, Eric, Ousmane Sanogo and Takemore Chagomoka. *Evaporative Cooling Technologies for Improved Vegetable Storage in Mali, Evaluation Report*. MIT D-Lab, June 2018. https://d-lab.mit.edu/sites/default/files/inline-files/Evaporative%20Cooling%20Technologies%20for%20Improved%20Vegetable%20Storage%20in%20Mali%20-%20Evaluation%20Report_0.pdf. Accessed October 24, 2026.
- Wayua, Francis O., Michael W. Okoth and John Wangoh. "Design and Performance Assessment of a Low Cost Evaporative Cooler for Storage of Camel Milk in Arid Pastoral Areas of Kenya." De Gruyter, 2012. https://www.degruyterbrill.com/document/doi/10.1515/1556-3758.2323/pdf. Accessed October 24, 2026.
- World Bank. "Is Post-Harvest Loss Significant in Sub-Saharan Africa?" *Africa Myths and Facts*. https://www.worldbank.org/en/programs/africa-myths-and-facts/publication/is-post-harvest-loss-significant-in-sub-saharan-africa.
- World Health Organization. *Legionella and the Prevention of Legionellosis*. Geneva: WHO, 2007. https://www.who.int/publications/i/item/9241562978. Accessed October 24, 2026.
