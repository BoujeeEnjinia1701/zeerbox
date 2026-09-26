# BOM notes

All prices are indicative 2026 USD for parts bought in a regional town in sub-Saharan Africa. They are checked for arithmetic and against the TRL 3 sizing (ZBX-CAL-001) but not yet quoted by suppliers.

- Line numbers match the callouts in `media/exploded.png`. Line 14 (wiring and plumbing) has no callout.
- **Budget.** Decided by Amish, 2026-09-25 (ZBX-DDR-001 item 1): `budget_usd: 300` covers the cooling equipment kit. The structure is built from local materials and costed separately.
- **Cooling equipment kit** (items 6 to 11 and 14): **$270**, 90 % of the $300 budget. It rose by $27 from TRL 2 for the decided 150 W panel (+$20), a 20 A charge controller in place of 10 A (+$4) and 2.5 mm² PV cable (+$3), then by $10 for the 150 mm pad (decided by Amish, 2026-09-25, ZBX-DDR-002 item 11).
- **Structure** (items 1 to 5 and 12), costed separately: **$355** in materials. It rose by $20 for 500 x 500 x 600 mm roof post footings, then fell by $5 when the wet sand cavity and wetting pipe gave way to dry rice husk with lime, mesh and a damp-proof course (ZBX-DDR-002 item 12). Mason's and carpenter's labor is not included.
- **Store total, crates excluded:** $625.
- **Crates** (item 13): $96 if bought; not included, since users normally own them.
- `python docs/04-calcs/sizing.py` reads this BOM and prints the group totals.
