---
doc_id: ZBX-BLD-001
title: ZeerBox prototype build plan
project: ZeerBox
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-02'
    author: Amish Chadha
    change: First build plan; design made constructable (ZBX-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: Controller box with its mode lamp and the plate shield for the outside sensor; power box with a plain door; pictures redrawn
---

# ZeerBox prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order. The crates are the users' own and are not shown.*

The prototype is one walk-in store, 2.4 x 1.5 x 2.0 m inside, on a patch of level, firm ground about 4.5 x 3.5 m. It has double brick walls around a dry rice husk cavity, a framed and insulated ceiling, a corrugated shade roof on four steel posts, a 150 mm wetted pad in the back wall, two 12 V fans in a ceiling fan box at the door end, a sump drum and pump, a 150 W solar panel on the roof, a controller and a power box beside the door, and two timber racks for 24 crates. Figure 1 shows the 28 components in the order they are made or fitted. Most are made on site: concrete is cast, bricks are laid, and timber, plywood, aluminium angle and galvanized sheet are sawn, drilled, bent and screwed. The pad, fans, pump, drum, panel, battery, charge controller and controller parts are bought and fitted. A local mason builds the footings and walls and a carpenter the timber work; the metal parts need a drill, a hacksaw and, for the post caps, a welder. The parts cost about $873 from the bill of materials, crates excluded.

> **Safety:** This is a building that people walk into and stand under. About 7 t of brickwork and a roof that the wind tries to lift must be built by a competent mason, and the roof must be screwed and tied down before the first windy day. The door must open from inside at all times, with no outside lock. The store holds a 154 Wh lithium iron phosphate battery, fans that can catch fingers and a drum of warm water that can grow *Legionella*: keep the battery fuse out until section 6 says otherwise, guard the fans on both faces, and keep the drum covered. Rice husk burns: no flames or hot work near the walls once the cavity is filled. Weld the post caps before the posts go in, away from the site.

## 2. What changed to make it buildable

The concept showed what the store does; some of its parts could not be built as drawn. Each change below keeps what the store does and its calculated cooling, and all of them are recorded in decision record ZBX-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Exhaust fans | Two round holes in the front wall beside the door | One plywood fan box in the ceiling at the door end, over the aisle; the fans blow up into the shaded roof space (Figures 16 and 17) | The wall holes left 50 mm of brick beside the door and the corners, too narrow to build or to carry a lintel |
| Shade roof | A sheet resting on four post tops | Two beams on welded post caps, five purlins, sheets screwed to the purlins (Figures 4 and 18 to 20) | A 3.9 x 3.0 m sheet cannot span between four posts; 150 mm deep purlins carry the wind uplift |
| Foundations | Walls on bare ground | A concrete strip footing 450 x 250 mm under both leaves (Figure 2) | The calculation already assumed it |
| Door and pad openings | Holes straight through the cavity wall | A hardwood lintel over each leaf, a board lining on every reveal, a door lining with stop beads and hinges, a 74 mm door (Figures 7, 8 and 10 to 12) | Something must carry the brick above, close the cavity at the reveal and hang the door |
| Ceiling | A solid slab | Joists, cleats, insulation and boards, the same 120 mm thick (Figures 13 to 15) | A slab of boards and straw needs a structure |
| Racks | Posts passing through the shelves | Rails on the inside faces of the posts, slats across them, wall brackets (Figures 28 and 29) | A shelf cannot occupy the same space as its post |
| Pad | A frame ring and a floating header | A board frame on wall battens with support and retaining bars, the header lying on the pad, a gutter on brackets (Figures 23 to 27) | Each part needs something to sit on and something to hold it |
| Solar panel | Floating 150 mm above the roof | Two aluminium frames screwed through the sheet into the purlins (Figures 21 and 22) | A fixing that reaches the structure |
| Sump drum | Half outside the roof edge | Fully under the roof | Shaded water stays cooler and cleaner |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" are as seen standing outside the door, looking at it; the door is at the front end and the pad at the back end. The roof slopes down to the right. Heights are above the finished ground at the walls. Site tolerance is 5 mm for masonry and 2 mm for joinery unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Wall strip footing

![Figure 2. Making sketch of the wall strip footing](../cad/drawings/ZBX-DWG-101.png)

*Figure 2. Wall strip footing making sketch (ZBX-DWG-101).*

![Figure 3. Setting-out plan](05-build-plan/setout.png)

*Figure 3. Setting-out plan: footings, posts, walls and openings.*

**What it is and what it is made from.** A rectangular ring of concrete that the two brick leaves stand on. About 1 m³ of concrete, about 1 part cement to 3 sand to 6 stone, with a plastic damp-proof strip on top.

**How to make it.**

1. Clear and level the site. Peg out the outside of the walls, 3,010 x 2,110 mm, from Figure 3; check that both diagonals are equal (3,682 mm).
2. Mark the trench 450 mm wide, centred on the wall line: 3,155 x 2,255 mm outside, 2,255 x 1,355 mm inside.
3. Dig 250 mm deep. Where the bottom is soft, dig to firm ground and fill back with concrete, not soil.
4. Pour, rod out the air, and strike the top level all round with the ground.
5. Keep it damp under a sheet for 7 days.
6. Lay a plastic damp-proof strip 305 mm wide on top, under both leaves and the cavity, lapped 150 mm at every join.

**How it fits the parts next to it.** Both brick leaves and the husk fill stand on the damp-proof strip, centred on the footing (Figure 5). The post footings sit 23 mm clear of its outside corners (Figure 3).

**Check before moving on.** Top level within 5 mm all round; diagonals within 10 mm.

### 3.2 Roof posts and their footings (make 4)

![Figure 4. Making sketch of the roof post](../cad/drawings/ZBX-DWG-102.png)

*Figure 4. Roof post making sketch (ZBX-DWG-102).*

**What it is and what it is made from.** A galvanized steel pipe, 89 mm outside and 3 mm wall, with a 150 x 150 x 6 mm steel cap plate welded on top and a 12 mm bar through its foot, cast 450 mm into a 500 x 500 x 600 mm concrete footing.

**How to make it.**

1. Cut two pipes 2,703 mm long for the right (low) side and two 2,899 mm long for the left (high) side, square.
2. Drill each cap plate with two 11 mm holes 80 mm apart on its centre line.
3. Weld the plate to the pipe top, tilted 4° so it slopes down toward the right side, with the holes running across the store.
4. Drill a 13 mm hole through each pipe 50 mm above its foot, push through a 200 mm length of 12 mm bar and weld both sides. This bar holds the post down against wind uplift.
5. Paint every weld with zinc-rich paint.
6. Dig the four holes 500 x 500 x 600 mm deep, centred 1,850 mm along and 1,400 mm across from the store's centre (Figure 3; 3,700 mm and 2,800 mm between centres, 4,640 mm on the diagonals).

**How it fits the parts next to it.** Each post stands 450 mm deep in its hole, plumb, with its cap plate top on a string line: 2,253 mm above ground on the right side and 2,449 mm on the left. The roof beams sit on the plates (Figure 19).

**Check before moving on.** Each post plumb both ways; plate tops within 5 mm of the string line.

### 3.3 Double brick walls and the rice husk fill

![Figure 5. Making sketch of the walls](../cad/drawings/ZBX-DWG-103.png)

*Figure 5. Double brick walls making sketch (ZBX-DWG-103).*

**What it is and what it is made from.** Two leaves of fired brick, each 115 mm thick, with a 75 mm cavity filled with dry rice husk: a 305 mm wall, 2,100 mm high. Outside 3,010 x 2,110 mm, inside 2,400 x 1,500 mm. Cement-sand mortar 1:5 and galvanized wire wall ties. The husk is mixed with hydrated lime against insects.

**How to make it.**

1. Lay both leaves together on the damp-proof strip, a few courses at a time.
2. Bed a wall tie across the cavity every 900 mm along and every 450 mm up, staggered. Keep mortar out of the cavity; a board lifted along it as you go catches droppings.
3. Leave the door opening in the front wall, centred: 840 mm wide, from 100 to 1,920 mm above ground. The bricks under it, up to 100 mm, are the door sill.
4. Leave the pad opening in the back wall, centred: 640 mm wide and 540 mm high, from 980 to 1,520 mm above ground.
5. Every six courses, pour husk and lime into the cavity and settle it by tapping the wall, not by ramming.
6. Stop at 1,520 mm for the pad lintels (section 3.4, step 4), then build on to 1,920 mm for the door lintels (step 5).
7. Finish with a capping course from 2,025 to 2,100 mm that bridges both leaves and the cavity in one course, closing the husk in.

**How it fits the parts next to it.**

![Figure 6. Joint 1: wall on the strip footing](05-build-plan/joint-01.png)

*Figure 6. Both leaves and the fill sit on the damp-proof strip over the footing; the floor is laid against the inner leaf.*

**Check before moving on.** Walls plumb; top level within 10 mm; openings square and to size; no mortar bridging the cavity.

### 3.4 Lintels (make 4)

![Figure 7. Making sketch of the lintels](../cad/drawings/ZBX-DWG-104.png)

*Figure 7. Lintels making sketch (ZBX-DWG-104).*

**What it is and what it is made from.** One beam over each leaf at each opening. Termite-treated hardwood, 115 mm wide (the leaf width) and 100 mm deep.

**How to make it.**

1. Cut two lengths of 1,140 mm for the door and two of 940 mm for the pad.
2. Treat the cut ends again.

**How it fits the parts next to it.**

![Figure 8. Joint 2: door lintels](05-build-plan/joint-02.png)

*Figure 8. One lintel over each leaf, flush with both leaf faces; the cavity stays open between them and the capping course closes it above.*

Each lintel bears 150 mm on the brick at both ends, bedded level in mortar: undersides at 1,520 mm for the pad and 1,920 mm for the door. The husk above an opening runs down between the two lintels onto the lining head.

**Check before moving on.** Level; 150 mm of bearing at both ends; no rot or splits.

### 3.5 Brick floor

![Figure 9. Making sketch of the floor](../cad/drawings/ZBX-DWG-105.png)

*Figure 9. Brick floor making sketch (ZBX-DWG-105).*

**What it is and what it is made from.** The floor of the room, 2,400 x 1,500 mm, of fired bricks laid flat on a 25 mm sand bed.

**How to make it.**

1. Level and compact the ground inside the walls.
2. Screed a 25 mm sand bed level.
3. Lay the bricks flat and close-jointed in a stretcher bond, top 100 mm above ground, level with the door sill.
4. Brush dry sand into the joints and wet it down.

**How it fits the parts next to it.** The floor fills the room against the inner leaf on all four sides; the racks stand on it.

**Check before moving on.** Level within 5 mm; no brick rocks.

### 3.6 Door lining and stop beads

![Figure 10. Making sketch of the door lining](../cad/drawings/ZBX-DWG-106.png)

*Figure 10. Door lining and stop beads making sketch (ZBX-DWG-106).*

**What it is and what it is made from.** Three treated boards, 20 x 305 mm, that line the door opening and close the cavity, with 20 x 40 mm stop beads and a rubber seal.

**How to make it.**

1. Cut two jambs 1,820 mm long and a head 800 mm long.
2. Cut stop beads to fit both jambs and the head.

**How it fits the parts next to it.**

![Figure 11. Joint 3: the door jamb](05-build-plan/joint-03.png)

*Figure 11. Plan section through the middle hinge: lining, stop bead with seal, door leaf and hinge.*

The jambs stand on the sill and the head sits between them, under the lintels. Fix each jamb with five screws in frame plugs into both leaves, packing behind with timber wedges until plumb. The clear opening inside the lining is 800 x 1,800 mm. The stop beads are screwed to the lining 84 mm in from the outside face, with the seal on their outer face.

**Check before moving on.** Lining plumb and square, diagonals within 3 mm.

### 3.7 Door

![Figure 12. Making sketch of the door](../cad/drawings/ZBX-DWG-107.png)

*Figure 12. Door making sketch (ZBX-DWG-107).*

**What it is and what it is made from.** An insulated leaf 794 x 1,792 x 74 mm: a frame of 50 x 50 mm timber, 50 mm foam board between, a 12 mm exterior plywood skin on each face.

**How to make it.**

1. Make the frame: two stiles, a top, a bottom and a middle rail, glued and screwed.
2. Cut and fit the foam between the frame members.
3. Glue and screw a plywood skin to each face.
4. Fit three 100 mm butt hinges on the right edge, 250, 900 and 1,550 mm above the floor.
5. Fit a latch that opens from inside by pushing a lever, and a pull handle outside. Fit no outside lock or bolt.

**How it fits the parts next to it.** The leaf hangs in the lining, hinged on the right, and closes against the stop beads from outside; it opens outward (Figure 11). Gaps are 3 mm at the sides and head and 5 mm at the sill.

**Check before moving on.** The door closes on the seal all round and opens from inside with one push.

### 3.8 Ceiling joists (make 9)

![Figure 13. Making sketch of the ceiling joist](../cad/drawings/ZBX-DWG-108.png)

*Figure 13. Ceiling joist making sketch (ZBX-DWG-108).*

**What it is and what it is made from.** Sawn, treated timber 50 x 100 mm on edge, 2,110 mm long, with a 25 x 25 mm cleat along each side at the bottom edge.

**How to make it.**

1. Cut nine joists 2,110 mm long and treat them.
2. Nail a cleat along each side at the bottom edge, full length. The two end joists get one cleat, on the inner side.
3. On the two joists either side of the fan box, stop the cleat on the fan side 320 mm each side of the joist's mid-point.

**How it fits the parts next to it.**

![Figure 14. Joint 4: joists on the wall top](05-build-plan/joint-04.png)

*Figure 14. Joists bear on the whole wall top; insulation rests on the cleats; boards are nailed on top.*

The joists lie across the store on the wall tops, their centres 0, 410, 820, 1,180 and 1,480 mm each way from the store's centre. The fan bay is between the joists at 820 and 1,180 mm toward the door: 310 mm clear. One galvanized strap per joist end, built into the brickwork, is nailed to the joist.

**Check before moving on.** Tops in line within 5 mm; the fan bay is 310 mm clear.

### 3.9 Ceiling insulation and boards

![Figure 15. Making sketch of the insulation and boards](../cad/drawings/ZBX-DWG-109.png)

*Figure 15. Ceiling insulation and boards making sketch (ZBX-DWG-109).*

**What it is and what it is made from.** A plastic vapor sheet, 50 mm straw board or foam board and 20 mm boards.

**How to make it.**

1. Cut the insulation to fill each bay between joists, 2,110 mm long: bays are 250 mm at the ends, 310 mm in the fan bay and 360 mm elsewhere.
2. Cut the boards to cover 3,010 x 2,110 mm, leaving a 310 x 640 mm hole over the fan bay, centred across the store.

**How it fits the parts next to it.** The vapor sheet lies over the cleats in each bay, lapped 100 mm up the joist sides; the insulation rests on it; the boards are nailed to every joist (Figure 14). In the fan bay the insulation fills only the length outside the fan box. The boards are for occasional maintenance access only.

**Check before moving on.** No gaps between insulation boards; the fan hole is clear.

### 3.10 Fan box

![Figure 16. Making sketch of the fan box](../cad/drawings/ZBX-DWG-110.png)

*Figure 16. Fan box making sketch (ZBX-DWG-110).*

**What it is and what it is made from.** A tube of 18 mm exterior plywood, 310 x 640 mm outside and 150 mm deep, with a top plate that carries the two fans.

**How to make it.**

1. Cut two long sides 640 x 150 mm and two short sides 274 x 150 mm. Glue and screw the short sides between the long sides.
2. Cut the top plate 310 x 640 mm. Cut two 250 mm holes, centred across its width and 160 mm each side of its middle.
3. Glue and screw the plate on top of the tube. Seal the joints.

**How it fits the parts next to it.**

![Figure 17. Joint 5: fan box between two joists](05-build-plan/joint-05.png)

*Figure 17. The box bottom is flush with the ceiling; the fans sit on the plate and blow up into the roof space.*

The tube drops into the fan bay from above, its bottom edge flush with the joist undersides, and is held by four screws through each long side into the joist beside it. The plate stands 30 mm above the ceiling boards. The fan shutters stay at least 100 mm below the roof framing.

**Check before moving on.** Square; plate flat; the fan frames fit over the holes.

### 3.11 Roof beams (make 2)

![Figure 18. Making sketch of the roof beam](../cad/drawings/ZBX-DWG-111.png)

*Figure 18. Roof beam making sketch (ZBX-DWG-111).*

**What it is and what it is made from.** Sawn, treated timber 75 x 150 mm, 2,940 mm long.

**How to make it.**

1. Cut two lengths and treat the ends.
2. Mark the five purlin positions on the top edge: 700 mm apart along the beam, the outer two 1,400 mm from its middle.

**How it fits the parts next to it.**

![Figure 19. Joint 6: post, beam and purlin](05-build-plan/joint-06.png)

*Figure 19. The cap plate is welded at the roof slope, so the beam sits flat on it.*

Each beam lies on edge across the store on one pair of cap plates, sloping 4° down to the right and overhanging 70 mm past each post centre. Two M10 x 100 mm coach screws go up through each cap plate into the beam.

**Check before moving on.** Beams parallel and 3,700 mm apart centre to centre; diagonals across the four post tops within 10 mm.

### 3.12 Purlins (make 5)

![Figure 20. Making sketch of the purlin](../cad/drawings/ZBX-DWG-112.png)

*Figure 20. Purlin making sketch (ZBX-DWG-112).*

**What it is and what it is made from.** Sawn, treated timber 50 x 150 mm, 3,800 mm long, and ten galvanized hurricane ties rated 2 kN or more.

**How to make it.** Cut five lengths and treat the ends. A 100 mm deep purlin is not strong enough for this span.

**How it fits the parts next to it.** Each purlin lies on edge across both beams, along the store, at the marks 700 mm apart, its ends 12 mm past the beams' outer faces. A hurricane tie at every crossing, nailed with the tie maker's nails, holds it down; the wind lifts about 1.1 kN at each crossing (Figure 19). The roof sheets are screwed to the purlins.

**Check before moving on.** Purlin tops in one plane within 5 mm, checked with a string line.

### 3.13 Panel mounting frames (make 2, a left and a right)

![Figure 21. Making sketch of the panel mounting frame](../cad/drawings/ZBX-DWG-113.png)

*Figure 21. Panel mounting frame making sketch (ZBX-DWG-113).*

**What it is and what it is made from.** Per frame: an aluminium angle 40 x 40 x 4 mm base rail 820 mm long, a top rail of the same angle 670 mm long, and two legs of 40 x 4 mm aluminium flat bar, 339 mm and 136 mm long; M8 stainless bolts.

**How to make it.**

1. Cut the rails and legs; deburr.
2. Drill the base rail for two roofing screws at each purlin crossing, 700 mm apart.
3. Drill the top rail to match the panel frame's mounting holes.
4. Drill one 9 mm hole at each end of each leg; drill the matching rail holes on assembly so the panel sits at 15°.
5. The two frames are mirror images.

**How it fits the parts next to it.**

![Figure 22. Joint 7: panel frame](05-build-plan/joint-07.png)

*Figure 22. Base rail screwed through the sheet into two purlins; legs bolted to both rails; panel bolted to the top rail.*

The base rails lie on the sheet down the slope, 560 mm each side of the store's centre line, across the purlins at 700 mm and 0 mm from the roof's middle, 60 mm past each. Each leg stands 25 mm in from a top rail end and bolts to the upright flanges of both rails.

**Check before moving on.** Panel at 15° within 1°; all bolts tight.

### 3.14 Pad opening lining

![Figure 23. Making sketch of the pad opening lining](../cad/drawings/ZBX-DWG-114.png)

*Figure 23. Pad opening lining making sketch (ZBX-DWG-114).*

**What it is and what it is made from.** Four treated boards, 20 x 305 mm, that line the pad opening and close the cavity.

**How to make it.** Cut two sides 540 mm long and a head and a sill 600 mm long.

**How it fits the parts next to it.** The head and sill fit between the sides; the outer edges are flush with the outside wall face; three screws in frame plugs per board. The clear opening is 600 x 500 mm, from 1,000 to 1,500 mm above ground: exactly the pad's face, so no air goes round the pad. A bead of sealant seals the lining to the brick outside.

**Check before moving on.** Square; clear size 600 x 500 mm within 3 mm.

### 3.15 Pad frame

![Figure 24. Making sketch of the pad frame](../cad/drawings/ZBX-DWG-115.png)

*Figure 24. Pad frame making sketch (ZBX-DWG-115).*

**What it is and what it is made from.** Two 25 x 50 mm wall battens; two side boards and a top board of 25 mm treated board, 160 mm deep; four galvanized flat bars 30 x 3 mm, 650 mm long.

**How to make it.**

1. Cut the battens and sides 585 mm long and the top 600 mm long.
2. In each side, drill a 34 mm hole 75 mm from the back edge and 516 mm up from the bottom, for the drip header.
3. Cut the four bars and drill them for two screws at each end.

**How it fits the parts next to it.**

![Figure 25. Joint 8: pad, frame, header and gutter](05-build-plan/joint-08.png)

*Figure 25. Section on the centre line, seen from the right: the lined opening, the pad on its bars inside the frame, the header on the pad, the gutter below.*

The battens are plugged to the wall 325 mm each side of centre, from 1,000 to 1,585 mm above ground. The sides are screwed to the battens' inner faces, 600 mm apart inside, and the top fits between them. The two bottom bars run under the sides, 35 and 115 mm from the wall; the pad stands on them. The two front bars cross the sides' front edges 150 and 350 mm up and keep the pad in.

**Check before moving on.** Inside 600 mm wide and 160 mm deep; bottom bars level.

### 3.16 Drip header

![Figure 26. Making sketch of the drip header](../cad/drawings/ZBX-DWG-116.png)

*Figure 26. Drip header making sketch (ZBX-DWG-116).*

**What it is and what it is made from.** 740 mm of 32 mm PVC pipe with an end cap.

**How to make it.**

1. Cut the pipe and cement a cap on the left end.
2. Drill a row of 3 mm holes every 75 mm along one side, between the frame sides; deburr inside.

**How it fits the parts next to it.** It slides through both side boards and lies on top of the pad, holes facing down, with its open end 75 mm out on the right for the feed hose (Figure 25).

**Check before moving on.** Water from a hose runs out of every hole evenly.

### 3.17 Return gutter and brackets

![Figure 27. Making sketch of the gutter](../cad/drawings/ZBX-DWG-117.png)

*Figure 27. Return gutter and brackets making sketch (ZBX-DWG-117).*

**What it is and what it is made from.** A channel bent from 0.5 mm galvanized sheet, 170 mm wide, 60 mm deep and 780 mm long, with a 32 mm tank connector outlet; two brackets of 40 x 3 mm galvanized strip.

**How to make it.**

1. Bend the channel; fold both ends up and seal them.
2. Cut a 32 mm hole in the bottom 40 mm from the right end and 95 mm out from the wall; fit the tank connector.
3. Bend each bracket to an L, 80 mm up the wall and 180 mm out; drill for two plugs.

**How it fits the parts next to it.** The brackets are plugged to the wall 250 mm each side of centre. The gutter sits on them 10 mm off the wall with its top 20 mm below the pad, reaching 120 mm past the pad on the right and 60 mm on the left, with a slight fall to the outlet (Figure 25).

**Check before moving on.** Pour water in: it all leaves by the outlet.

### 3.18 Shelving racks (make 2)

![Figure 28. Making sketch of the rack](../cad/drawings/ZBX-DWG-118.png)

*Figure 28. Shelving rack making sketch (ZBX-DWG-118).*

**What it is and what it is made from.** Termite-treated timber: six 50 x 50 mm posts, six 50 x 75 mm rails, 45 slats 95 x 25 mm; two 40 x 40 x 3 mm steel angle brackets.

**How to make it.**

1. Cut the posts 1,750 mm, the rails 2,200 mm and the slats 350 mm long.
2. Stand the posts in two rows of three, at both ends and the middle; the rows are 450 mm apart outside and 350 mm inside.
3. Screw two rails to the inside faces of the posts at each shelf, their tops 25 mm below the shelf top.
4. Screw 15 slats across the rails at each shelf, two screws each end, with about 54 mm gaps for air. Shelf tops are 300, 850 and 1,400 mm above the floor.

**How it fits the parts next to it.**

![Figure 29. Joint 9: rack end at the wall](05-build-plan/joint-09.png)

*Figure 29. Seen from the aisle: rails on the inside faces of the posts, slats across the rails, a bracket tying the end post to the wall.*

Each rack stands on the floor against a long wall, 100 mm from each end wall, leaving a 600 mm aisle. A steel angle bracket ties the top of each end post to the wall.

**Check before moving on.** Square, no rocking; each shelf carries 160 kg, eight full crates.

### 3.19 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Cellulose pad (line 6).** 150 mm cross-fluted evaporative cooling pad, 600 x 500 mm, flutes at the standard 45° and 15° angles.
- **Exhaust fans (line 8).** Two 250 mm 12 V DC axial fans, about 12 W and about 400 m³/h free air, with a square frame no wider than 290 mm, finger guards on both faces and gravity shutters.
- **Sump drum, pump and hoses (line 7).** A 60 L plastic drum with a tight lid; a 12 V submersible pump of about 6 W giving 3.6 L/min at 2 m head; a float switch; 25 mm feed hose and 32 mm return hose with clips. Drill the lid for the two hoses and a cable gland.
- **Solar panel (line 10).** 150 W monocrystalline, about 1,480 x 670 x 35 mm, Vmp about 18 V, Isc about 9 A, with mounting holes in the back flange of its frame.
- **Power box (line 11).** A 20 A PWM charge controller for 12.8 V lithium iron phosphate, a 12.8 V 12 Ah LiFePO4 battery with a BMS rated for 10 A charge or more, a 15 A fuse at the battery terminal, and a ventilated, shaded steel box with a plain door (no window), about 100 x 220 x 300 mm.
- **Controller and sensors (line 9).** A low-cost microcontroller board, two digital temperature and humidity sensors (one in a radiation shield on a strip arm), MOSFET drivers for the fans and pump, a memory card logger, a three-colour mode lamp with a 22 mm body and a clear-lid IP65 box about 80 x 200 x 250 mm. The outside sensor sits in a shield of six round plates, 46 mm across, stacked 10 mm apart on a stud that is fixed to a short strip arm.
- **Wiring and plumbing (line 14).** 2.5 mm² twin PV cable, 1.5 mm² twin load cable, 4-core 0.5 mm² sensor cable, conduit, IP65 connectors, glands, hose clips and fixings.
- **Fixings.** Frame plugs and screws, galvanized joist straps, ten hurricane ties, eight M10 x 100 mm coach screws, sealing-washer roofing screws, M8 stainless bolts, three 100 mm butt hinges, an inside push latch and a pull handle.

#### 3.19.1 Wiring

![Figure 30. Block-level 12 V wiring](05-build-plan/wiring.png)

*Figure 30. Block-level wiring with wire sizes. No circuit board is laid out at this stage; bought parts are wired together.*

1. Panel to the charge controller's panel terminals: 2.5 mm² PV cable down the right front post in conduit.
2. Charge controller to the battery through the 15 A fuse at the battery terminal: 2.5 mm².
3. Charge controller load output to the controller box: 1.5 mm².
4. Controller to each fan: 1.5 mm² twin, up the wall in conduit and over the wall top under the ceiling boards to the fan box. Seal the conduit where it crosses the husk-filled wall top.
5. Controller to the pump: 1.5 mm² twin in conduit along the right long wall, 300 mm above ground, with a drip loop at the drum.
6. Inside sensor: 4-core 0.5 mm² through a gland in the door lining head, to a sensor on the right rack's middle post about 1.5 m up. Outside sensor: 4-core 0.5 mm² to its shield beside the controller.

**Check before moving on.** With the fuse out, every circuit continues end to end and none reads short to another; every cable is labelled.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: cast the wall strip footing

![Step 1](05-build-plan/step-01.png)

Dig and pour as section 3.1. **Hold point:** 7 days of curing before any brick is laid.

### Step 2: set the roof posts in their footings

![Step 2](05-build-plan/step-02.png)

Stand each post 450 mm into its hole, plumb and braced, cap plates on the string line, then fill with concrete. Leave the bracing on for 7 days.

### Step 3: lay the walls and fill the cavity as they rise

![Step 3](05-build-plan/step-03.png)

Both leaves together with wall ties; husk and lime poured in every six courses. Stop at 1,520 mm.

### Step 4: lintels over the pad opening

![Step 4](05-build-plan/step-04.png)

One per leaf, 150 mm bearing each end, bedded level in mortar.

### Step 5: finish the walls, door lintels and capping course

![Step 5](05-build-plan/step-05.png)

Build on to 1,920 mm, bed the door lintels, finish the walls and the fill, and lay the capping course from 2,025 to 2,100 mm. Fix the joist straps into the top course at the joist positions.

### Step 6: lay the brick floor

![Step 6](05-build-plan/step-06.png)

Sand bed and bricks as section 3.5.

### Step 7: line the door opening and fit the stop beads

![Step 7](05-build-plan/step-07.png)

Jambs, then head, into frame plugs, plumb; stop beads 84 mm in from the outside face.

### Step 8: hang the door

![Step 8](05-build-plan/step-08.png)

Three hinges on the right edge; the door opens outward. **Hold point:** the door opens from inside with one push before anyone works inside with it closed.

### Step 9: ceiling joists onto the wall tops

![Step 9](05-build-plan/step-09.png)

Nine joists across the store at their marks, each end nailed to its strap. The fan bay is between the joists at 820 and 1,180 mm toward the door.

### Step 10: vapor sheet and insulation into the bays

![Step 10](05-build-plan/step-10.png)

Sheet over the cleats, then insulation cut to each bay, resting on the cleats.

### Step 11: drop the fan box into the fan bay

![Step 11](05-build-plan/step-11.png)

Bottom flush with the joist undersides; four screws through each long side into the joists.

### Step 12: nail the ceiling boards on

![Step 12](05-build-plan/step-12.png)

Boards across the joists, cut round the fan box.

### Step 13: fans and shutters onto the fan box

![Step 13](05-build-plan/step-13.png)

Each fan over its hole, blowing upward, four screws; a guard under each hole; a gravity shutter on top of each fan.

### Step 14: roof beams onto the post cap plates

![Step 14](05-build-plan/step-14.png)

Two M10 coach screws up through each cap plate. Work from scaffold or a stable platform, never from the ceiling boards.

### Step 15: purlins onto the beams

![Step 15](05-build-plan/step-15.png)

Five purlins at the marks, 700 mm apart; a hurricane tie at every crossing.

### Step 16: roof sheets onto the purlins

![Step 16](05-build-plan/step-16.png)

Sheets laid down the slope with side laps facing away from the prevailing wind; a sealing-washer screw through every second crest at each purlin. **Hold point:** every sheet screwed down before work stops for the day.

### Step 17: panel frames onto the roof

![Step 17](05-build-plan/step-17.png)

Base rails screwed through sheet crests into the purlins; legs and top rails bolted on.

### Step 18: solar panel onto its frames

![Step 18](05-build-plan/step-18.png)

With a helper, lift the panel on and bolt it to the top rails through its frame holes. Check the tilt is 15° with an angle finder. Keep the panel leads apart and taped until step 25.

### Step 19: line the pad opening

![Step 19](05-build-plan/step-19.png)

Four boards into frame plugs, flush with the outside face; seal outside.

### Step 20: pad frame onto the wall

![Step 20](05-build-plan/step-20.png)

Battens plugged to the wall; sides screwed to them; top between the sides; bottom bars under the sides.

### Step 21: pad into its frame

![Step 21](05-build-plan/step-21.png)

Slide the pad in from the front onto the bottom bars, steeper flutes sloping down toward the room, then fit the two front bars.

### Step 22: drip header through the frame

![Step 22](05-build-plan/step-22.png)

Slide it in from the right through both side boards, holes facing down, open end 75 mm out on the right.

### Step 23: gutter under the pad

![Step 23](05-build-plan/step-23.png)

Brackets plugged to the wall; gutter on the brackets, its top 20 mm below the pad, falling to the outlet.

### Step 24: sump drum and hoses

![Step 24](05-build-plan/step-24.png)

Drum on level ground to the right of the pad, under the roof, lid on. Pump and float switch inside; feed hose from the pump to the header inlet; return hose from the gutter outlet to the lid.

### Step 25: power box, controller and sensor on the front wall

![Step 25](05-build-plan/step-25.png)

Power box to the right of the door and the controller to its left, 1.0 to 1.3 m above ground, each on four screws in plugs. Drill a 22 mm hole in the top of the controller box, 70 mm from its middle toward the door, push the mode lamp body through from outside and tighten its nut inside, so the flange sits flat on top of the box. Screw the strip arm of the outside sensor to the wall about 1.35 m above ground, 75 mm above the top of the box, with its plates clear of the lamp by at least 15 mm. Wire as section 3.19.1 with the battery fuse out. **Hold point:** safety stops S3 and S4 of section 6.

### Step 26: racks in along the long walls

![Step 26](05-build-plan/step-26.png)

Carry the rack parts in through the door and assemble each rack in place against a long wall, 100 mm from each end wall; bracket the end posts to the wall.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of ZBX-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Crate fit and reach | R1 | Load 24 empty crates; an adult reaches every crate from the aisle | 24 crates fit; no crate is lifted above 1.6 m |
| Door opens from inside | R9 | Close the door from inside; open it with one push, in the dark | Opens every time; no outside lock fitted |
| Pad wetting | R8 | Run the pump with the fans off for 10 minutes | The whole pad face is wet; no dry streaks; all water returns to the drum; no splash outside the gutter |
| Fan direction and shutters | R9 | Run the fans at full speed | Air leaves upward through both shutters; shutters close by themselves when the fans stop; guards fitted on both faces |
| Airflow | R2 | Vane anemometer over the pad face at nine points | About 0.5 m/s mean face velocity (about 560 m³/h, ZBX-CAL-001) |
| Cooling on a dry day | R2 | Log inside and outside temperature and humidity for a day with the store loaded | Store air 8 K or more below outside air at about 35 °C and 30 % RH |
| Store humidity | R3 | Same log | 80 % RH or more while cooling |
| Mode change | R4, R5 | Feed the controller a humid-air reading and a 95 % RH store reading from a test input | It switches to hold, and stops the pump after 60 minutes at 95 %; the lamp shows the mode |
| Charge controller and fuse | R7, R9 | Measure the charge voltage; check the fuse rating and the BMS charge limit on their labels | Charge voltage within the battery maker's limit; 15 A fuse at the terminal; BMS 10 A or more |
| Day's energy | R7 | Log battery voltage over a sunny design day | The battery ends the day fuller than it started |
| Water use | R8 | Mark the drum level morning and evening | 70 L a day or less (about 36 L expected) |
| Roof tie-down | R11 | Pull up on each purlin end by hand; look at every tie and screw | Nothing lifts; every tie, coach screw and sheet screw in place |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before digging.** The site has been checked for buried cables and pipes; the trench and holes are fenced or covered when left.
- **S2. Before work at height (steps 9 to 18).** Work from scaffold or a stable platform with a second person present; never stand on the ceiling boards or the roof sheets; no work in wind strong enough to lift a sheet.
- **S3. Before the battery fuse goes in.** All wiring done and labelled; with the fuse out, no circuit reads short; panel leads connected to the charge controller only after the battery, as the controller maker says; battery shaded and ventilated in its box.
- **S4. Before the battery is charged unattended.** One full day of attended charging: battery temperature checked hourly, never charged below 0 °C or above 45 °C.
- **S5. Before the fans are run.** Guards fitted on both faces of both fans; nobody's hands near the fan box.
- **S6. Before the pump is run.** Drum covered; the float switch stops the pump when the drum is low; every cable joint near water is IP65 with a drip loop.
- **S7. Before anyone works inside with the door closed.** The door opens from inside with one push; the store has been aired out if the fans were off.
- **S8. Before produce goes in (outside this plan).** The drum has been drained and cleaned and the weekly cleaning routine is agreed with the users; the store is not used for meat, fish, milk or medicines.

## 7. Tools, skills and workspace

**Tools.** Tape measure, builder's line and pegs, spirit level and water level, builder's square; spade, mattock and wheelbarrow; concrete mixing tools and a tamping rod; bricklaying trowel, jointer and line blocks; hand saw and circular saw; drill with masonry, wood and metal bits up to 13 mm and a 250 mm hole saw or jigsaw; screwdrivers and spanners to 17 mm; hacksaw and files; tin snips and a folding bar for 0.5 mm sheet; an arc welder (or a workshop that welds) for the cap plates; angle finder; multimeter; vane anemometer and a temperature and humidity logger for the first checks; scaffold or a stable platform.

**Skills.** A competent mason for the footings, walls, lintels and capping course; a carpenter for the linings, door, ceiling, fan box, roof framing, pad frame and racks; welding of the four cap plates and anchor bars; basic 12 V wiring with crimped ferrules. All circuits are 12 V DC; no mains wiring is part of this build.

**Workspace.** A level, firm, well-drained site about 4.5 x 3.5 m with room around it to work and store bricks; shade and water for curing concrete and mortar; a covered, dry place to keep the rice husk, timber and electrical parts until they are fitted.

**Personal protective equipment.** Gloves for brick, concrete and sheet; eye protection for cutting and drilling; a welding mask and gloves for the cap plates; hearing protection for the circular saw; a dust mask for handling lime and husk; hard hats while the roof is being built.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/ZBX-DWG-101` to `ZBX-DWG-118`.
- General arrangement: `cad/drawings/ZBX-DWG-001.pdf`, Rev P3.
- Calculations: `docs/04-calcs/01-sizing.md` (ZBX-CAL-001 v0.3) and `docs/04-calcs/sizing.py`; structure and roof framing in section 10 and Table 6a.
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (ZBX-DDR-003), with ZBX-DDR-001 and ZBX-DDR-002; open items in `docs/06-design-decisions.md` (ZBX-DEC-001).
- Requirements: `docs/03-requirements.md` (ZBX-REQ-001 v0.5).
