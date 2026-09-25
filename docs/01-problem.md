---
doc_id: ZBX-PRB-001
title: ZeerBox problem statement
project: ZeerBox
doc_type: Problem statement
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (users, context, constraints, out of scope, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the budget decision (ZBX-DDR-001 item 1), the co-design partner rule and the TRL 3 water figure
---

# ZeerBox problem statement

Smallholder farmers and traders in hot, dry regions lose a large share of their tomatoes, leafy greens and other perishables in the days after harvest because they have nowhere cool to keep them, and refrigerated cold rooms cost tens of thousands of dollars and need reliable power. Passive evaporative coolers are cheap and proven but small, hard to load, and weak whenever the air turns humid. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## The problem

Around 14 % of the world's food is lost between harvest and retail, and losses are higher for fruits and vegetables than for cereals at every stage of the chain ([FAO, *The State of Food and Agriculture 2019*](https://www.fao.org/interactive/state-of-food-agriculture/2019/en/)). In sub-Saharan Africa, on-farm losses of fruits and vegetables reported in that work range from 0 to 50 % ([summary of FAO SOFA 2019](https://www.globalagriculture.org/news/fao-14-of-the-worlds-food-is-lost-between-harvest-and-retail/)), and FAO's earlier estimate put total food loss in the region at about 37 % of production ([World Bank, *Africa Myths and Facts*](https://www.worldbank.org/en/programs/africa-myths-and-facts/publication/is-post-harvest-loss-significant-in-sub-saharan-africa)). Heat is the main driver for perishables: a tomato held at 30 to 35 °C respires and loses water several times faster than one held near its recommended 12.5 to 15 °C and 90 to 95 % relative humidity (RH) ([UC Davis Postharvest Center, tomato fact sheet](https://postharvest.ucdavis.edu/produce-facts-sheets/tomato)).

The result is that a farmer must sell on the day of harvest, often to the first trader who arrives, at whatever price is offered. Stored produce that would fetch a better price three or four days later spoils first.

Three gaps block the obvious fix:

1. **Refrigeration is out of reach.** A solar-powered walk-in cold room for smallholder agriculture in Malawi and Zimbabwe cost about $40,000 per unit for 10 t of capacity, with a 10 kWp array and 15 kWh of batteries, and some pilot rooms stood largely unused ([Efficiency for Access, lessons from Zimbabwe and Malawi](https://efficiencyforaccess.org/wp-content/uploads/Lessons-learned-from-implementing-solar-powered-walk-in-cold-rooms-for-smallholder-agriculture-in-Zimbabwe-and-Malawi.pdf)). Pay-per-crate solar cold rooms such as ColdHubs in Nigeria work where a business runs them, but they serve market hubs rather than individual farms ([ColdHubs, Wikipedia](https://en.wikipedia.org/wiki/ColdHubs)).
2. **Passive evaporative coolers are small and slow.** Clay pot-in-pot coolers and brick zero energy cool chambers (ZECCs) cost little and roughly double the shelf life of tomatoes in the dry season, but they hold tens of kilograms, sit at ground level where every crate must be lifted in and out, and depend on wind for air movement ([MIT D-Lab evaluation in Mali](https://news.mit.edu/2018/mit-d-lab-cite-evaluation-low-cost-evaporative-cooling-devices-mali-0620); [ZECC storage study, *e-planet* 18(2)](https://www.e-planet.co.in/images/Publication/vol-18-2/storage.pdf)).
3. **Evaporative cooling fails in humid weather, and nobody tells the user.** Evaporative chambers work best above about 25 °C and below about 40 % RH ([Evaporative cooling chambers, Wikipedia](https://en.wikipedia.org/wiki/Evaporative_cooling_chambers)). In the rainy season a wet pad adds humidity without much cooling, and a sealed, damp chamber can grow mold. Passive designs cannot sense this or change their behavior.

ZeerBox is a walk-in evaporative store, large enough for about 24 crates, that uses a small solar-powered fan to pull outside air through a wetted pad and a controller that reads temperature and humidity inside and out, so it cools hard when the air is dry, ventilates at night when the air is humid, and tells the user which mode it is in.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Smallholder vegetable grower | Hold one to five days of harvest so produce can be sold when the price is right, not on the day it is picked | 0.5 to 2 ha of tomatoes, peppers, okra, leafy greens; sells at a farm gate or weekly market |
| Farmer group or cooperative | Shared store near the collection point for several members' crates | Rota for loading, watering and cleaning; simple record of whose crates are where |
| Market trader | Keep stock fresh between market days | Stall or small depot near a market, several deliveries a week |
| Local builder (mason, carpenter) | Build the walls, roof and door from local materials with familiar methods | Brick or block walls, timber, corrugated sheet; no specialist cooling trades |
| Local electrician or phone-repair technician | Install and repair the fans, pump, solar and controller | 12 V solar home system skills; hand tools and a multimeter |

### Operating environment

- **Climate (design case):** hot, dry season in the Sahel and similar semi-arid regions, daytime highs of 32 to 40 °C and 15 to 35 % RH. The design point is 35 °C and 30 % RH.
- **Climate (off-design):** rainy season, 25 to 32 °C and 60 to 90 % RH, when evaporative cooling gives little benefit.
- **Water:** a borehole, well, tap or rainwater tank within carrying distance; water may be hard or silty.
- **Power:** no grid, or unreliable grid. About 5 peak sun hours per day in the dry season.
- **Produce:** mixed perishables in 20 kg plastic or wooden crates, loaded daily, often warm from the field.
- **Site:** open ground near the farm or market, dust, termites, livestock, occasional strong wind.
- **Supply chain:** bricks, sand, cement, timber and corrugated sheet are available locally; 12 V solar parts, DC fans and small pumps are sold in regional towns; cellulose cooling pads are sold for poultry houses and greenhouses but may need to come from a regional city.

## Constraints

- The $300 USD budget (`project.yaml`) covers the cooling equipment kit: pad, sump and pump, fans, controller, solar panel, power box and wiring. The walk-in structure is built from local materials and costed separately (decided by Amish, 2026-09-25, ZBX-DDR-001 item 1). At TRL 3 the kit costs about $260 and the structure about $360 (ZBX-CAL-001).
- Structure built by a local mason and carpenter from local materials, with no specialist refrigeration skills, refrigerant or mains power.
- Fans, pump and controller run from one small solar panel at 12 V, safe to touch and to work on.
- Water use modest enough to carry or pump by hand on the hottest day.
- No refrigerant, no compressor and no claim of cold-chain temperatures. ZeerBox slows spoilage; it does not replace a refrigerator.
- Every electrical and water part replaceable with a generic part from a regional town.

## Out of scope

- Refrigerated cold storage below about 15 °C (see ColdPod in this portfolio for active refrigeration).
- Storage of meat, fish, milk or vaccines, which need true cold chain.
- Drying, curing or processing of produce.
- Grain storage (see GrainGuard).
- Market linkage, pricing or the business model for a shared store, which a partner must design with users.

## Prior work

- **Pot-in-pot cooler (zeer).** Mohamed Bah Abba spread the clay pot-in-pot cooler in northern Nigeria in the 1990s and won a Rolex Award for Enterprise in 2001 ([Pot-in-pot refrigerator, Wikipedia](https://en.wikipedia.org/wiki/Pot-in-pot_refrigerator)). ZeerBox takes its name and its principle from the zeer.
- **Zero energy cool chamber (ZECC).** A double brick wall with a wet sand cavity, developed at the Indian Agricultural Research Institute from 1986. One study measured 4.4 to 5.0 K below ambient on monthly averages and 7.25 K on the best day, with tomato shelf life rising from 6 to 11 days and banana from 7 to 20 days ([*e-planet* 18(2)](https://www.e-planet.co.in/images/Publication/vol-18-2/storage.pdf)). ZeerBox reuses the wet-cavity wall.
- **MIT D-Lab evaluation in Mali.** Brick chambers and clay pot coolers achieved more than 8 °C of cooling in real use in the dry season, and brick chambers outperformed straw and sack designs ([MIT News, 2018](https://news.mit.edu/2018/mit-d-lab-cite-evaluation-low-cost-evaporative-cooling-devices-mali-0620)). D-Lab has since piloted forced-air evaporative chambers in Kenya, some solar powered ([MIT D-Lab, evaporative cooling research](https://d-lab.mit.edu/research/evaporative-cooling-vegetable-preservation)). This is the closest prior work to ZeerBox and should be studied before TRL 3.
- **Fan and pad cooling in poultry houses and greenhouses.** Cellulose pad walls with exhaust fans are standard practice and well characterized; once the pad is fully wetted, extra water flow adds little ([review of evaporative pad operation, *Renewable and Sustainable Energy Reviews*](https://www.sciencedirect.com/science/article/pii/S1364032121009072)). ZeerBox scales this down to one small pad and two 12 V fans.
- **Solar cold rooms.** ColdHubs (Nigeria) and the Zimbabwe and Malawi pilots show both the demand and the cost and utilization risks of refrigerated storage for smallholders (sources above).

## Open questions

- Which partner organization and which region first? A dry-season vegetable area in the Sahel (Mali, Niger, northern Nigeria, Burkina Faso) or a semi-arid area of East Africa (northern Kenya) fits the design point. Amish decided on 2026-09-25 that community designs pick co-design partners per area later; the choice for ZeerBox is still open (ZBX-DDR-001 item 10).
- Is the store for one farm or for a group? This drives size, cost and who waters and cleans it.
- How far is the water source, and is about 44 L on a hot day acceptable (ZBX-CAL-001)?
- Which crops dominate, and which must be kept apart (for example ethylene-producing tomatoes and bananas next to leafy greens)?
- Do users need the store to work in the rainy season, or only in the dry season when losses and prices are highest?

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO, university or an existing evaporative cooling program)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate climate, water, crop, load and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
