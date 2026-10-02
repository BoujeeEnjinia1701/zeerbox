"""ZeerBox prototype build plan pictures (ZBX-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|wiring|setout ...]
With no argument it draws everything. A sheet, joint or step can be drawn alone by number:
    python cad/src/build_plan_media.py sheets 103      steps 7      joints 4
Every picture is drawn from cad/src/model.py (build_components), so the pictures and the model
never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    docs/05-build-plan/setout.png          setting-out plan: footings, posts, walls and openings
    cad/drawings/ZBX-DWG-101 to 118        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level 12 V wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, shape_of, roof_frame, panel_frame, _bx  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
D = derived(P)
C = build_components(P)
XF, XB, TOP = -D["out_l"] / 2, D["out_l"] / 2, D["top"]

COL = {"strip_footing": "#A8A29E", "post_footings": "#A8A29E", "posts": "#64748B", "walls": "#B45F3C", "fill": "#D8B26E",
       "lintels": "#7C2D12", "floor": "#C08457", "door_lining": "#92400E", "door_stops": "#D97706", "door": "#A16207",
       "door_hinges": "#111827", "joists": "#CA8A04", "insulation": "#FDE68A", "deck": "#E7D3A8", "fan_box": "#78350F",
       "fans": "#111827", "beams": "#475569", "purlins": "#94A3B8", "sheet": "#CBD5E1", "mount": "#0E7490", "panel": "#1E3A8A",
       "pad_lining": "#92400E", "pad_battens": "#A16207", "pad_frame": "#CA8A04", "pad_bars": "#374151", "pad": "#0F766E",
       "header": "#E5E7EB", "gutter": "#6B7280", "gutter_brackets": "#1F2937", "sump": "#2563EB", "hoses": "#1D4ED8",
       "controller": "#7C3AED", "sensor": "#E5E7EB", "power_box": "#16A34A", "racks": "#B45309", "rack_brackets": "#111827",
       "crates": "#65A30D"}


def sh(*keys):
    return shape_of([s for k in keys for s in C[k][1]])


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def comp(key, name=None, explode=(0, 0, 0), color=None):
    return part(name or C[key][0], sh(key), color or COL[key], explode)


def win(shape, x0, x1, y0, y1, z0, z1):
    """The part of a shape inside a box (for close-ups and partial walls)."""
    return shape & _bx(x0, x1, y0, y1, z0, z1)


def pieces_in(key, x0, x1, y0, y1, z0, z1):
    out = []
    for s in C[key][1]:
        b = s.bounding_box()
        if b.max.X > x0 and b.min.X < x1 and b.max.Y > y0 and b.min.Y < y1 and b.max.Z > z0 and b.min.Z < z1:
            try:
                q = win(s, x0, x1, y0, y1, z0, z1)
                if q.volume > 1:
                    out.append(q)
            except Exception:
                pass
    return shape_of(out) if out else None


def jp(key, name, box, color=None):
    s = pieces_in(key, *box)
    return part(name, s, color or COL[key]) if s is not None else None


# ----------------------------------------------------------------- the build order
LINT_Z = P["FLOOR"] + D["door_open"][1]          # top of the door opening, where the door lintels sit
BIG = (-5000, 5000, -5000, 5000)


def walls_below(z):
    return win(sh("walls"), *BIG, -10, z)


def walls_above(z):
    return win(sh("walls"), *BIG, z, 5000)


def fill_below(z):
    return win(sh("fill"), *BIG, -10, z)


def fill_above(z):
    return win(sh("fill"), *BIG, z, 5000)


ORDER = [   # key, with its explode offset for the overview
    ("strip_footing", (0, 0, -1300)),
    ("post_footings", (0, 0, -1300)),
    ("posts", (0, -700, -300)),
    ("walls", (0, 0, 0)),
    ("fill", (0, 3300, 0)),
    ("lintels", (0, 0, 700)),
    ("floor", (0, 0, 0)),
    ("door_lining", (-1900, 0, 0)),
    ("door_stops", (-2600, 0, 0)),
    ("door", (-3300, 0, 0)),
    ("joists", (0, 0, 1300)),
    ("insulation", (0, 0, 1750)),
    ("fan_box", (-1500, 0, 2300)),
    ("deck", (0, 0, 2250)),
    ("fans", (-1500, 0, 2700)),
    ("beams", (0, 3300, 2300)),
    ("purlins", (0, 3300, 2900)),
    ("sheet", (3000, 3300, 3900)),
    ("mount", (3000, 3300, 4400)),
    ("panel", (3000, 3300, 4800)),
    ("pad_lining", (900, 0, 0)),
    ("pad_frame", (1600, 0, 0)),
    ("pad", (2300, 0, 0)),
    ("header", (2300, 0, 700)),
    ("gutter", (1900, 0, -700)),
    ("sump", (2900, -900, 0)),
    ("power_box", (-2600, -1600, 0)),
    ("racks", (0, -3000, 0)),
]
NAMES = {"posts": "Roof posts", "post_footings": "Post footings", "walls": "Double brick walls", "fill": "Rice husk fill",
         "lintels": "Lintels (4)", "door_lining": "Door lining", "door_stops": "Stop beads and seal", "door": "Door and hinges",
         "joists": "Ceiling joists (9)", "insulation": "Ceiling insulation", "fan_box": "Fan box", "deck": "Ceiling boards",
         "fans": "Fans and shutters (2)", "beams": "Roof beams (2)", "purlins": "Purlins (5)", "sheet": "Roof sheets",
         "mount": "Panel frames (2)", "panel": "Solar panel", "pad_lining": "Pad opening lining",
         "pad_frame": "Pad frame, battens, bars", "pad": "Cellulose pad", "header": "Drip header",
         "gutter": "Gutter and brackets", "sump": "Sump drum and hoses", "power_box": "Power box, controller, sensor",
         "racks": "Racks (2) and brackets", "strip_footing": "Wall strip footing", "floor": "Brick floor"}
GROUP = {"door": ("door", "door_hinges"), "pad_frame": ("pad_frame", "pad_battens", "pad_bars"), "gutter": ("gutter", "gutter_brackets"),
         "sump": ("sump", "hoses"), "power_box": ("power_box", "controller", "sensor"), "racks": ("racks", "rack_brackets")}


def overview():
    parts = [part(NAMES[k], sh(*GROUP.get(k, (k,))), COL[k], off) for k, off in ORDER]
    return bv.overview(parts, OUT / "overview.png", "ZeerBox prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the pad end and the right side, above. Crates are user supplied and not shown",
                       elev=20, azim=-40, size=(12, 10), dpi=150, key=True)


# ----------------------------------------------------------------- setting-out plan
def setout():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    ol, ow, w = D["out_l"], D["out_w"], D["wall"]
    fw = P["FOOT_W"]
    ov = (fw - w) / 2
    fig = plt.figure(figsize=(12, 8.6), dpi=150)
    ax = fig.add_axes([0.04, 0.07, 0.92, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    # strip footing
    ax.add_patch(Rectangle((-ol / 2 - ov, -ow / 2 - ov), ol + 2 * ov, ow + 2 * ov, fc="#E7E5E4", ec=MUT, lw=0.8, ls="--"))
    ax.add_patch(Rectangle((-ol / 2 + w + ov, -ow / 2 + w + ov), ol - 2 * w - 2 * ov, ow - 2 * w - 2 * ov, fc="white", ec=MUT, lw=0.8, ls="--"))
    # leaves and cavity
    for x0, y0, L, W, fc in ((-ol / 2, -ow / 2, ol, ow, "#C2410C"), (-ol / 2 + P["LEAF"], -ow / 2 + P["LEAF"], ol - 2 * P["LEAF"], ow - 2 * P["LEAF"], "#F5DEB3"),
                             (-P["IN_L"] / 2 - P["LEAF"], -P["IN_W"] / 2 - P["LEAF"], P["IN_L"] + 2 * P["LEAF"], P["IN_W"] + 2 * P["LEAF"], "#C2410C"),
                             (-P["IN_L"] / 2, -P["IN_W"] / 2, P["IN_L"], P["IN_W"], "white")):
        ax.add_patch(Rectangle((x0, y0), L, W, fc=fc, ec=INK, lw=0.6))
    # openings
    dw = D["door_open"][0]
    ax.add_patch(Rectangle((-ol / 2 - 5, -dw / 2), w + 10, dw, fc="white", ec=INK, lw=0.8))
    pw = D["pad_open"][0]
    ax.add_patch(Rectangle((ol / 2 - w - 5, -pw / 2), w + 10, pw, fc="white", ec=INK, lw=0.8))
    ax.text(-ol / 2 + w + 60, 0, "door opening\n840 wide", ha="left", va="center", fontsize=8, color=INK)
    ax.text(ol / 2 - w - 60, 0, "pad opening\n640 wide", ha="right", va="center", fontsize=8, color=INK)
    # posts and footings
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * P["POST_X"], sy * P["POST_Y"]
            ax.add_patch(Rectangle((x - 250, y - 250), 500, 500, fc="#E7E5E4", ec=MUT, lw=0.8, ls="--"))
            ax.add_patch(plt.Circle((x, y), 45, fc="#64748B", ec=INK, lw=0.6))
    ax.axhline(0, color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3))); ax.axvline(0, color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))

    def dim(x0, y0, x1, y1, text, off, vertical=False):
        if vertical:
            ax.annotate("", xy=(x0 + off, y0), xytext=(x0 + off, y1), arrowprops=dict(arrowstyle="<->", color=AC, lw=0.7))
            ax.text(x0 + off - 25, (y0 + y1) / 2, text, rotation=90, ha="right", va="center", fontsize=8, color=AC,
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none"))
        else:
            ax.annotate("", xy=(x0, y0 + off), xytext=(x1, y0 + off), arrowprops=dict(arrowstyle="<->", color=AC, lw=0.7))
            ax.text((x0 + x1) / 2, y0 + off + 25, text, ha="center", va="bottom", fontsize=8, color=AC,
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none"))
    dim(-P["POST_X"], P["POST_Y"], P["POST_X"], P["POST_Y"], "3,700 between post centres", 330)
    dim(-ol / 2, ow / 2, ol / 2, ow / 2, "3,010 outside the walls", 120)
    dim(-P["IN_L"] / 2, -P["IN_W"] / 2, P["IN_L"] / 2, -P["IN_W"] / 2, "2,400 inside", 120)
    dim(-ol / 2 - ov, -ow / 2, ol / 2 + ov, -ow / 2, "3,155 outside the footing", -330)
    dim(P["POST_X"], -P["POST_Y"], P["POST_X"], P["POST_Y"], "2,800 between post centres", 380, vertical=True)
    dim(ol / 2, -ow / 2, ol / 2, ow / 2, "2,110 outside", 140, vertical=True)
    dim(-P["IN_L"] / 2, -P["IN_W"] / 2, -P["IN_L"] / 2, P["IN_W"] / 2, "1,500 inside", 900, vertical=True)
    ax.text(-ol / 2 + 40, -ow / 2 + 40, "", fontsize=7)
    ax.set_xlim(-2500, 2500); ax.set_ylim(-1950, 1950)
    fig.text(0.03, 0.975, "Setting-out plan: footings, posts and walls", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.94, "Seen from above, door end at left, pad end at right. Sizes in mm, from the model. Dashed: concrete footings below ground.\n"
             "Walls: two 115 mm brick leaves (red) around a 75 mm cavity (pale). Strip footing 450 wide, centred under the 305 mm wall.",
             fontsize=8.5, color=MUT, va="top")
    fig.text(0.97, 0.10, "Check the diagonals: walls 3,682 corner to corner\n(outside), posts 4,640 centre to centre", ha="right", fontsize=8, color=INK)
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/zeerbox", fontsize=7, color=AC, ha="right", family="monospace")
    out = OUT / "setout.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


# ----------------------------------------------------------------- making sketches
def _flat_roof(shape):
    """A roof-frame part laid square to the axes."""
    return roof_frame(P).inverse() * shape


def _flat_panel(shape):
    return panel_frame(P).inverse() * shape


def sheets(only=None):
    import build123d as b
    out = []
    base = dict(project="ZeerBox", date=DATE)
    ghost_store = [comp("walls"), comp("floor")]

    def S(no, *a, **k):
        if only and no not in only:
            return
        out.append(bv.component_sheet(*a, dwg_no=f"ZBX-DWG-{no}", **k, **base))

    S(101, comp("strip_footing"), [comp("walls"), comp("post_footings")],
      title="ZeerBox wall strip footing: making sketch", material="Concrete about 1 cement : 3 sand : 6 stone, about 1.0 m3",
      inset_view=(30, -50),
      notes=["A ring of concrete 450 mm wide and 250 mm deep, top at ground level,",
             "  centred under the 305 mm wall. Outside 3,155 x 2,255 mm,",
             "  inside 2,255 x 1,355 mm. The setting-out plan gives every line.",
             "Peg out the outside corners; check both diagonals are equal.",
             "Dig the trench 450 wide and 250 deep; go deeper to firm ground if",
             "  the bottom is soft, and fill back with concrete, not soil.",
             "Pour, rod out air, strike the top level all round within 5 mm.",
             "Keep it damp under a sheet for 7 days before laying bricks.",
             "Lay a plastic damp-proof strip 305 mm wide on top, under both",
             "  leaves and the cavity, lapped 150 mm at the joins.",
             "Check: level within 5 mm all round; diagonals within 10 mm."])

    post = C["posts"][1][0]
    S(102, part("Roof post", post, COL["posts"]), [comp("post_footings"), comp("beams"), comp("walls")],
      title="ZeerBox roof post and footing (make 4): making sketch",
      material="Galvanized steel pipe 89 mm outside, 3 mm wall; 6 mm steel plate; 12 mm bar",
      inset_view=(20, -130),
      notes=["Pipe lengths: 2,703 mm for the two posts on the right (low) side,",
             "  2,899 mm for the two on the left (high) side. Square cuts.",
             "Cap plate 150 x 150 x 6 mm, two 11 mm holes 80 mm apart on the",
             "  beam line. Weld it to the pipe top tilted 4 degrees, sloping",
             "  down toward the right side, square to the beam.",
             "Drill 13 mm through the pipe 50 mm above its foot; push a 200 mm",
             "  length of 12 mm bar through and weld both sides (holds against uplift).",
             "Paint the welds with zinc-rich paint.",
             "Footing: hole 500 x 500 x 600 mm deep, centred 1,850 mm along and",
             "  1,400 mm across from the store centre (setting-out plan).",
             "Stand the post 450 mm into the hole, plumb, plate tops on a string",
             "  line: 2,253 mm above ground (right), 2,449 mm (left). Brace, pour.",
             "Check: plumb both ways; plate tops within 5 mm of the line."])

    S(103, comp("walls"), [comp("strip_footing"), comp("lintels"), comp("door_lining")],
      title="ZeerBox double brick walls: making sketch", material="Fired brick, cement-sand mortar 1:5, galvanized wall ties",
      inset_view=(25, -50),
      notes=["Two 115 mm leaves with a 75 mm cavity: 305 mm wall. Outside",
             "  3,010 x 2,110 mm; inside 2,400 x 1,500 mm. 2,100 mm high.",
             "Lay both leaves on the damp-proof strip together, a few courses",
             "  at a time. Wall ties across the cavity every 900 mm along and",
             "  every 450 mm up, staggered; keep the cavity clear of mortar.",
             "Door opening (door end, centred): 840 wide, from 100 to 1,920 mm",
             "  above ground. Bricks under it (to 100 mm) are the door sill.",
             "Pad opening (pad end, centred): 640 wide x 540 high, from 980",
             "  to 1,520 mm above ground.",
             "Lintels at 1,920 mm (door) and 1,520 mm (pad): see ZBX-DWG-104.",
             "Fill the cavity as the walls rise (ZBX-BLD-001 step 3).",
             "Capping course: the top 75 mm (2,025 to 2,100) bridges both leaves",
             "  and the cavity in one course, in mortar, closing the fill in.",
             "Check: plumb, level top within 10 mm, openings square."])

    lin = C["lintels"][1][0]
    S(104, part("Door lintel", lin, COL["lintels"]), [comp("walls"), comp("door_lining")],
      title="ZeerBox lintels (make 4): making sketch", material="Termite-treated hardwood 115 x 100 mm",
      view_shape=b.Pos(-lin.bounding_box().center().X, 0, -lin.bounding_box().min.Z) * lin, inset_view=(20, -130),
      notes=["Door lintels: two pieces 1,140 mm long, one over each leaf.",
             "Pad lintels: two pieces 940 mm long, one over each leaf.",
             "Section 115 wide (the leaf width) by 100 mm deep. Saw square,",
             "  treat the cut ends again.",
             "Each lintel bears 150 mm on the brick at both ends of the",
             "  opening, bedded in mortar, level, flush with both leaf faces.",
             "Door lintels: underside 1,920 mm above ground. Pad lintels:",
             "  underside 1,520 mm.",
             "Leave the cavity open between the two lintels of a pair; the",
             "  fill above runs down between them onto the lining head.",
             "Check: level, 150 mm bearing both ends, no rot or splits."])

    S(105, comp("floor"), [comp("walls")],
      title="ZeerBox brick floor: making sketch", material="Fired brick laid flat on a 25 mm sand bed",
      inset_view=(70, -40),
      notes=["Fills the room inside the inner leaf: 2,400 x 1,500 mm.",
             "Level the ground inside the walls and compact it hard. Lay a",
             "  25 mm sand bed, screeded level.",
             "Lay 75 mm bricks flat, close-jointed, in a stretcher bond; top",
             "  100 mm above ground, level with the door sill.",
             "Brush dry sand into the joints and wet it down.",
             "Check: level within 5 mm; no rocking brick."])

    S(106, part("Door lining and stop beads", sh("door_lining", "door_stops"), COL["door_lining"]), [comp("walls"), comp("lintels")],
      title="ZeerBox door lining and stop beads: making sketch", material="Treated board 20 x 305 mm; bead 20 x 40 mm; rubber seal",
      view_shape=b.Pos(-XF, 0, -P["FLOOR"]) * sh("door_lining", "door_stops"), inset_view=(20, -130),
      notes=["Jambs: two boards 20 x 305 mm, 1,820 mm long.",
             "Head: one board 20 x 305 mm, 800 mm long, between the jambs.",
             "The lining covers the whole reveal and closes the cavity.",
             "Fix each jamb with five screws in frame plugs into the inner and",
             "  outer leaves; pack behind with timber wedges until plumb.",
             "Clear opening inside the lining: 800 x 1,800 mm from the floor.",
             "Stop beads 20 x 40 mm on both jambs and the head, 84 mm in from",
             "  the outside face; a rubber seal along the outer face of the bead.",
             "Check: lining plumb and square (diagonals within 3 mm)."])

    dr = sh("door", "door_hinges")
    S(107, part("Door", dr, COL["door"]), [comp("door_lining"), comp("door_stops"), comp("walls")],
      title="ZeerBox door: making sketch", material="Timber frame 50 x 50 mm, 12 mm exterior plywood skins, 50 mm insulation",
      view_shape=b.Pos(-XF, 0, -P["FLOOR"]) * sh("door"), inset_view=(20, -130),
      notes=["Leaf 794 wide x 1,792 high x 74 mm thick (0.8 x 1.8 m nominal).",
             "Frame of 50 x 50 mm timber on edge: stiles, top, bottom and a",
             "  middle rail. Fill between with 50 mm foam board.",
             "Glue and screw a 12 mm plywood skin to each face.",
             "Three 100 mm butt hinges on the right edge (seen from outside):",
             "  250, 900 and 1,550 mm above the floor. The door opens outward.",
             "Inside: a latch that opens by pushing a lever, never a key.",
             "Outside: a pull handle only. No outside lock or bolt.",
             "Gaps: 3 mm each side, 3 mm at the head, 5 mm at the sill.",
             "Check: closes on the seal all round; opens from inside by one push."])

    j = C["joists"][1][2]
    S(108, part("Ceiling joist", j, COL["joists"]), [comp("walls"), comp("fan_box"), part("Other joists", shape_of([q for i, q in enumerate(C["joists"][1]) if i != 2]), "#D1D5DB")],
      title="ZeerBox ceiling joist (make 9): making sketch", material="Sawn timber 50 x 100 mm on edge; cleats 25 x 25 mm",
      view_shape=b.Pos(-j.bounding_box().center().X, 0, -TOP) * j, inset_view=(30, -40),
      notes=["Cut nine 2,110 mm lengths (the full wall width). Treat them.",
             "Nail a 25 x 25 mm cleat along each side at the bottom edge, full",
             "  length; the two end joists get one cleat, on the inner side.",
             "On the two joists either side of the fan box, stop the cleat",
             "  320 mm each side of the joist's mid-point (shown here).",
             "Joist centres along the store, from its centre: 0, 410, 820,",
             "  1,180 and 1,480 mm each way. The fan box goes between the",
             "  joists at 820 and 1,180 mm toward the door: 310 mm clear.",
             "Each joist bears on the full wall top; one galvanized strap",
             "  per end, built into the brickwork, nailed to the joist.",
             "Check: tops in line within 5 mm; the fan bay is 310 mm clear."])

    S(109, part("Ceiling insulation and boards", sh("insulation", "deck"), COL["deck"]), [comp("joists"), comp("walls"), comp("fan_box")],
      title="ZeerBox ceiling insulation and boards: making sketch",
      material="50 mm straw board or foam board; plastic vapor sheet; 20 mm boards",
      view_shape=b.Pos(0, 0, -TOP) * sh("insulation", "deck"), inset_view=(35, -40),
      notes=["Vapor sheet first: lay it over the cleats in each bay, lapped",
             "  100 mm up the joist sides.",
             "Insulation: cut boards to fill each bay between joists, 2,110 mm",
             "  long, resting on the cleats. Bays are 250 mm (ends), 310 mm (the",
             "  fan bay, insulated outside the fan box only) and 360 mm.",
             "Boards: 20 mm boards laid across the joists along the store,",
             "  3,010 x 2,110 mm in all, nailed to every joist.",
             "Leave a 310 x 640 mm hole over the fan bay, 640 mm along the bay,",
             "  centred across the store (the fan box comes up through it).",
             "The boards are for occasional maintenance access only.",
             "Check: no gaps between insulation boards; the fan hole is clear."])

    S(110, comp("fan_box"), [comp("joists"), comp("walls")],
      title="ZeerBox fan box: making sketch", material="18 mm exterior plywood, screws and wood glue",
      view_shape=b.Pos(-P["FAN_X"], 0, -TOP) * sh("fan_box"), inset_view=(45, -60),
      notes=["A plywood tube 310 x 640 mm outside, 150 mm deep, with a top plate.",
             "Long sides: two 640 x 150 mm. Short sides: two 274 x 150 mm,",
             "  glued and screwed between the long sides.",
             "Top plate 310 x 640 mm. Cut two 250 mm round holes, centred",
             "  across the 310 mm width and 160 mm each side of the middle.",
             "Glue and screw the plate on top of the tube.",
             "Fit: the tube drops into the fan bay from above, its bottom edge",
             "  flush with the joist undersides (the room ceiling). Four screws",
             "  through each long side into the joist beside it.",
             "The plate stands 30 mm above the ceiling boards.",
             "Check: square; plate flat; seal the joints with sealant."])

    bm = C["beams"][1][0]
    S(111, part("Roof beam", bm, COL["beams"]), [comp("posts"), comp("purlins"), comp("walls")],
      title="ZeerBox roof beam (make 2): making sketch", material="Sawn timber 75 x 150 mm, treated",
      view_shape=b.Pos(P["POST_X"], 0, 0) * _flat_roof(bm), inset_view=(20, -130),
      notes=["Cut two 2,940 mm lengths of 75 x 150 mm; treat the ends.",
             "Each lies on edge across the store on one pair of post cap plates,",
             "  sloping 4 degrees down toward the right side.",
             "It overhangs 70 mm past each post centre.",
             "Fix: two M10 x 100 mm coach screws up through each cap plate.",
             "Mark the five purlin positions on the top edge: 700 mm apart",
             "  along the slope, the outer two 1,400 mm from the middle.",
             "Check: both beams parallel, 3,700 mm apart centre to centre,",
             "  diagonals across the four post tops within 10 mm."])

    pu = C["purlins"][1][2]
    S(112, part("Purlin", pu, COL["purlins"]), [comp("beams"), comp("posts"), comp("walls"), part("Other purlins", shape_of([q for i, q in enumerate(C["purlins"][1]) if i != 2]), "#D1D5DB")],
      title="ZeerBox purlin (make 5): making sketch", material="Sawn timber 50 x 150 mm, treated; hurricane ties",
      view_shape=_flat_roof(pu), inset_view=(25, -40),
      notes=["Cut five 3,800 mm lengths of 50 x 150 mm; treat the ends.",
             "Each lies on edge across both beams along the store, at the marks",
             "  700 mm apart, ends 12 mm past the beams' outer faces.",
             "Fix each crossing with a galvanized hurricane tie rated 2 kN or",
             "  more, nailed with the tie maker's nails (the wind lifts about",
             "  1.1 kN at each crossing, ZBX-CAL-001 section 10).",
             "A 100 mm deep purlin is not strong enough for this span.",
             "Check: tops in one plane within 5 mm (string line across)."])

    mt = C["mount"][1]
    one = shape_of([mt[4], mt[5], mt[6], mt[7]])
    S(113, part("Panel mounting frame", one, COL["mount"]), [comp("panel"), part("Roof sheet (part)", win(sh("sheet"), -900, 900, -900, 200, 2000, 3200), "#D1D5DB")],
      title="ZeerBox panel mounting frame (make 2, a left and a right): making sketch",
      material="Aluminium angle 40 x 40 x 4 mm; flat bar 40 x 4 mm; M8 stainless bolts",
      view_shape=b.Pos(-P["MOUNT_X"], 0, -D["roof_z"]) * one, inset_view=(12, -20),
      notes=["Base rail: angle 820 mm long, laid on the sheet down the slope,",
             "  560 mm each side of the store's centre line, across the two",
             "  purlins 700 and 0 mm from the roof's middle (60 mm past each).",
             "  Screw through the angle and a sheet crest into each purlin.",
             "Top rail: angle 670 mm long under the panel's side edge; bolt",
             "  the panel frame to it through the frame's own holes.",
             "Legs: flat bar 40 x 4 mm, 339 mm (high side) and 136 mm (low",
             "  side), 25 mm in from the top rail ends. Each leg bolts to the",
             "  upright flanges of both rails with one M8 bolt top and bottom.",
             "Drill the leg holes on assembly so the panel sits at 15 degrees.",
             "The two frames are mirror images.",
             "Check: panel at 15 degrees within 1; all bolts tight."])

    S(114, comp("pad_lining"), [comp("walls"), comp("lintels")],
      title="ZeerBox pad opening lining: making sketch", material="Treated board 20 x 305 mm",
      view_shape=b.Pos(-XB, 0, -P["PAD_Z"]) * sh("pad_lining"), inset_view=(15, -15),
      notes=["Sides: two boards 20 x 305 mm, 540 mm long.",
             "Head and sill: two boards 20 x 305 mm, 600 mm long, between the sides.",
             "The lining covers the whole reveal and closes the cavity.",
             "Screw into frame plugs, three per board; outer edges flush with",
             "  the outside wall face.",
             "Clear opening: 600 x 500 mm, 1,000 to 1,500 mm above ground,",
             "  exactly the pad's face, so no air goes round the pad.",
             "Seal the lining to the brick with a bead of sealant outside.",
             "Check: square; clear size 600 x 500 within 3 mm."])

    pf = sh("pad_frame", "pad_battens", "pad_bars")
    S(115, part("Pad frame", pf, COL["pad_frame"]), [comp("walls"), comp("pad"), comp("gutter"), comp("header")],
      title="ZeerBox pad frame: making sketch", material="Treated board 25 mm; batten 25 x 50 mm; galvanized flat bar 30 x 3 mm",
      view_shape=b.Pos(-XB, 0, -P["PAD_Z"]) * pf, inset_view=(20, -40),
      notes=["Battens: two 25 x 50 mm, 585 mm long, plugged to the wall 325 mm",
             "  each side of centre, from 1,000 to 1,585 mm above ground.",
             "Sides: two boards 25 x 160 mm, 585 mm long, screwed to the",
             "  battens' inner faces; 600 mm apart inside. In each, drill a",
             "  34 mm hole 75 mm from the wall and 516 mm up from the bottom",
             "  for the drip header.",
             "Top: one board 25 x 160 mm, 600 mm long, between the sides at the top.",
             "Bottom bars: two 30 x 3 mm, 650 mm long, under the sides at 35 and",
             "  115 mm from the wall. The pad stands on them.",
             "Front bars: two 30 x 3 mm, 650 mm long, across the sides' front",
             "  edges, 150 and 350 mm up. They keep the pad in.",
             "Check: inside 600 wide, 160 deep; bars level."])

    S(116, comp("header"), [comp("pad"), comp("pad_frame"), comp("hoses")],
      title="ZeerBox drip header: making sketch", material="PVC pipe 32 mm, end cap, solvent cement",
      view_shape=b.Pos(-XB, 0, -P["PAD_Z"]) * sh("header"), inset_view=(25, -40),
      notes=["Cut 740 mm of 32 mm PVC pipe. Cement a cap on the left end.",
             "Drill a row of 3 mm holes every 75 mm along one side, starting",
             "  40 mm in from each side board position; deburr inside.",
             "Fit: slide it through both side boards so it lies on top of the",
             "  pad, holes facing down, and the open end sticks out 75 mm on",
             "  the right side for the feed hose.",
             "Check: water from a hose runs out of every hole evenly."])

    gt = sh("gutter", "gutter_brackets")
    S(117, part("Gutter and brackets", gt, COL["gutter"]), [comp("walls"), comp("pad"), comp("pad_frame"), comp("hoses")],
      title="ZeerBox return gutter and brackets: making sketch", material="Galvanized sheet 0.5 mm; galvanized strip 40 x 3 mm",
      view_shape=b.Pos(-XB, 0, -P["PAD_Z"]) * gt, inset_view=(15, -40),
      notes=["Gutter: a channel 170 wide x 60 deep x 780 mm long, bent from",
             "  sheet, both ends folded up and sealed.",
             "Outlet: a 32 mm hole in the bottom 40 mm from the right end,",
             "  95 mm out from the wall; fit a 32 mm tank connector.",
             "Brackets: two 40 x 3 mm strips bent to an L, 80 mm up the wall",
             "  and 180 mm out, 250 mm each side of centre; two plugs each.",
             "Fit: the gutter sits on the brackets with its top 20 mm below",
             "  the pad, 10 mm off the wall, reaching 120 mm past the pad on the",
             "  right and 60 mm on the left. Fall toward the outlet.",
             "Check: pour water in; it all leaves by the outlet."])

    rk = shape_of([s for s in C["racks"][1] if s.bounding_box().center().Y < 0])
    S(118, part("Shelving rack", rk, COL["racks"]), [comp("floor"), comp("rack_brackets"), part("Other rack", shape_of([s for s in C["racks"][1] if s.bounding_box().center().Y > 0]), "#D1D5DB")],
      title="ZeerBox shelving rack (make 2): making sketch", material="Termite-treated timber: posts 50 x 50, rails 50 x 75, slats 95 x 25 mm",
      view_shape=b.Pos(0, P["IN_W"] / 2 - P["RACK_D"] / 2, -P["FLOOR"]) * rk, inset_view=(25, -130),
      notes=["Posts: six 50 x 50 mm, 1,750 mm long, in two rows of three",
             "  (front and back) at both ends and the middle; rows 450 mm",
             "  apart outside, 350 mm inside.",
             "Rails: six 50 x 75 mm, 2,200 mm long, screwed to the inside faces",
             "  of the posts, two per shelf; tops 25 mm below each shelf top.",
             "Slats: 15 per shelf, 95 x 25 mm, 350 mm long, across the rails,",
             "  about 54 mm gaps for air; two screws each end.",
             "Shelf tops 300, 850 and 1,400 mm above the floor.",
             "Fit: stand the rack against a long wall, 100 mm from each end",
             "  wall; two steel angle brackets fix the end posts' tops to the wall.",
             "Check: square, no rocking; each shelf carries 160 kg (8 crates)."])
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    out = []

    def J(n, parts, title, sub, **kw):
        if only and n not in only:
            return
        parts = [q for q in parts if q is not None]
        out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))

    # 1 wall on its footing, cut across the right long wall near the door end
    bx = (-700, -500, -1400, -700, -260, 420)
    J(1, [jp("strip_footing", "Strip footing (top at ground)", bx), jp("walls", "Outer and inner brick leaves", bx),
          jp("fill", "Rice husk fill on the damp-proof strip", bx), jp("floor", "Brick floor on sand", bx)],
      "wall on the strip footing (right long wall, cut across)", "Both leaves and the fill sit on the damp-proof strip over the footing; the floor is laid against the inner leaf",
      elev=12, azim=-150, size=(8, 6))
    # 2 door lintels and lining head, cut at the door centre line
    bx = (XF - 5, XF + D["wall"] + 5, -700, 0, 1700, 2110)
    J(2, [jp("walls", "Brick", bx), jp("lintels", "Lintel over each leaf", bx, "#EAB308"), jp("fill", "Fill", bx),
          jp("door_lining", "Lining head", bx), jp("door_stops", "Stop bead", bx), jp("door", "Door", bx)],
      "door lintels over the opening (cut on the door's centre line)", "One lintel over each leaf, 150 mm bearing on the brick; the capping course closes the cavity above",
      elev=12, azim=100, size=(8, 6))
    # 3 jamb: lining, stop bead, seal, hinge; a plan section cut through the middle hinge
    z = P["FLOOR"] + 900
    bx = (XF - 5, XF + D["wall"] + 5, -520, -300, z - 80, z)
    J(3, [jp("walls", "Brick reveal", bx), jp("fill", "Fill", bx), jp("door_lining", "Jamb lining (closes the cavity)", bx, "#FCD34D"),
          jp("door_stops", "Stop bead with seal", bx, "#EA580C"), jp("door", "Door leaf, 74 mm", bx), jp("door_hinges", "Hinge", bx)],
      "door jamb at the middle hinge (plan section)", "Seen from above, outside at left. The leaf closes against the stop bead and opens outward on the hinge",
      elev=88, azim=-90, size=(8, 6))
    # 4 joist on the wall top with insulation and boards, cut across the right long wall
    bx = (-500, 100, -1080, -700, 1900, 2240)
    J(4, [jp("walls", "Wall top and capping course", bx), jp("joists", "Joist with cleats", bx), jp("insulation", "Insulation on the cleats", bx),
          jp("deck", "Ceiling boards", bx), jp("fill", "Fill", bx)],
      "ceiling joists on the wall top (right long wall)", "Joists bear on the whole wall top; insulation rests on the cleats; boards nailed on top",
      elev=20, azim=-140, size=(8, 6))
    # 5 fan box between joists, cut on the store's centre line
    bx = (P["FAN_X"] - 330, P["FAN_X"] + 330, 0, 420, 2050, 2420)
    J(5, [jp("joists", "Joists either side", bx), jp("fan_box", "Fan box (plywood)", bx), jp("deck", "Ceiling boards", bx),
          jp("insulation", "Insulation", bx), jp("fans", "Fan and gravity shutter", bx, "#475569")],
      "fan box between two joists (cut on the store's centre line)", "The box bottom is flush with the ceiling; the fan sits on the plate and blows up into the roof space",
      elev=6, azim=-95, size=(8, 6))
    # 6 post, cap plate, beam and purlin at the front right corner
    x, y = -P["POST_X"], -P["POST_Y"]
    bx = (x - 260, x + 260, y - 200, y + 260, 2050, 2620)
    J(6, [jp("posts", "Post and cap plate", bx), jp("beams", "Beam (two coach screws)", bx),
          jp("purlins", "Purlin (hurricane tie)", bx), jp("sheet", "Roof sheet", bx)],
      "post, beam and purlin (door end, right side)", "The cap plate is welded at the roof slope so the beam sits flat on it",
      elev=12, azim=-130, size=(8, 6))
    # 7 panel frame on the roof, right frame
    bx = (P["MOUNT_X"] - 120, P["MOUNT_X"] + 120, -800, 100, 2520, 3060)
    J(7, [jp("sheet", "Roof sheet", bx), jp("purlins", "Purlins under the sheet", bx), jp("mount", "Base rail, legs and top rail", bx),
          jp("panel", "Panel frame", bx)],
      "panel frame (right side)", "Base rail screwed through the sheet into two purlins; legs bolted to both rails; panel bolted to the top rail",
      elev=10, azim=-20, size=(8, 6))
    # 8 pad assembly, cut on the centre line, seen from the right
    bx = (XB - D["wall"] - 5, XB + 200, 0, 420, 860, 1720)
    J(8, [jp("walls", "Brick", bx), jp("lintels", "Pad lintels", bx, "#EAB308"), jp("pad_lining", "Opening lining (far side of the opening)", bx, "#FEF3C7"), jp("pad", "Pad", bx),
          jp("pad_frame", "Frame side and top", bx), jp("pad_battens", "Batten on the wall", bx), jp("pad_bars", "Support and retaining bars", bx),
          jp("header", "Drip header on the pad", bx), jp("gutter", "Gutter", bx), jp("gutter_brackets", "Bracket", bx)],
      "pad, frame, header and gutter (cut on the centre line)", "Seen from the right side. Air comes in through the pad and the lined opening (room at left); water runs down the pad into the gutter",
      elev=10, azim=-90, size=(8, 6.5))
    # 9 rack top at the wall: post, rail, slats, bracket, seen from the aisle
    bx = (880, 1199, -760, -280, 1300, 1860)
    J(9, [jp("walls", "Inner leaf face", (880, 1210, -770, -750, 1300, 1860)), jp("racks", "Posts, rails and slats", bx),
          jp("rack_brackets", "Wall bracket", bx), jp("crates", "Crate", bx, "#A3E635")],
      "rack end at the wall (pad end, right rack, top shelf)", "Seen from the aisle. Rails on the inside faces of the posts; slats across the rails; the bracket ties the end post to the wall",
      elev=22, azim=55, size=(8, 6))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    out = []

    def st(n, done, new, title, sub, **kw):
        if only and n not in only:
            return
        kw.setdefault("label_done", False)
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(key, e, name=None, shape=None):
        return part(name or C[key][0], shape if shape is not None else sh(*GROUP.get(key, (key,))), COL[key], e)

    def g(key, name=None, shape=None):
        return part(name or NAMES.get(key, C[key][0]), shape if shape is not None else sh(*GROUP.get(key, (key,))), COL[key])

    A = dict(elev=24, azim=-50)
    DOOR = dict(elev=20, azim=-135)
    st(1, [], [mv("strip_footing", (0, 0, 400))], "cast the wall strip footing",
       "Into a trench 450 mm wide and 250 mm deep; top level with the ground; damp-proof strip on top", **A)
    st(2, [g("strip_footing")], [mv("posts", (0, 0, 900)), mv("post_footings", (0, 0, 0))], "set the four roof posts in their footings",
       "Each post 450 mm into a 500 x 500 x 600 mm hole, plumb, cap plates on a string line; then concrete", **A)
    lo = P["PAD_Z"] + D["pad_open"][1] / 2          # top of the pad opening, 1,520 mm
    pad_l = shape_of(C["lintels"][1][2:])
    door_l = shape_of(C["lintels"][1][:2])
    st(3, [g("strip_footing"), g("post_footings"), g("posts")], [part("Walls, first lift", walls_below(lo), COL["walls"], (0, 0, 500)),
                                            part("Rice husk fill, poured as the walls rise", fill_below(lo), COL["fill"], (0, 0, 1100))],
       "lay both leaves and fill the cavity as they rise",
       "Wall ties every 900 along and 450 up; husk mixed with lime poured in every six courses. First lift to 1,520 mm", **A)
    done = [g("strip_footing"), g("post_footings"), g("posts"), part("Walls", walls_below(lo), COL["walls"]), part("Fill", fill_below(lo), COL["fill"])]
    st(4, done, [part("Pad lintels (2)", pad_l, COL["lintels"], (0, 0, 600))], "lintels over the pad opening",
       "One per leaf, 150 mm bearing each end, bedded level in mortar at 1,520 mm", **A)
    st(5, done + [part("Pad lintels", pad_l, COL["lintels"])],
       [part("Walls to the top and capping course", walls_above(lo), COL["walls"], (0, 0, 700)),
        part("Door lintels (2), laid at 1,920 mm", door_l, COL["lintels"], (0, 0, 1400)),
        part("Rest of the fill", fill_above(lo), COL["fill"], (0, 0, 1900))],
       "finish the walls, door lintels and capping course",
       "Door lintels at 1,920 mm; the capping course bridges both leaves and the cavity at 2,025 to 2,100 mm", **DOOR)
    walls = [g("strip_footing"), g("post_footings"), g("posts"), g("walls"), g("lintels")]
    st(6, walls, [mv("floor", (0, 0, 900))], "lay the brick floor", "Bricks flat on a 25 mm sand bed, top 100 mm above ground, level with the door sill", elev=60, azim=-50)
    walls.append(g("floor"))
    st(7, walls, [mv("door_lining", (-500, 0, 0)), mv("door_stops", (-900, 0, 0))], "line the door opening and fit the stop beads",
       "Jambs and head screwed into frame plugs, plumb; stop beads 84 mm in from the outside face", **DOOR)
    walls += [g("door_lining"), g("door_stops")]
    st(8, walls, [mv("door", (-700, 0, 0), "Door and hinges")], "hang the door",
       "Three hinges on the right edge; opens outward; inside push latch, no outside lock", **DOOR)
    walls.append(g("door"))
    st(9, walls, [mv("joists", (0, 0, 700))], "ceiling joists onto the wall tops",
       "Nine joists across the store; a strap at each end; the fan bay between the joists at 820 and 1,180 mm toward the door", **A)
    walls.append(g("joists"))
    st(10, walls, [mv("insulation", (0, 0, 600))], "vapor sheet and insulation into the bays",
       "Sheet over the cleats, then 50 mm boards cut to each bay, resting on the cleats", **A)
    walls.append(g("insulation"))
    st(11, walls, [mv("fan_box", (0, 0, 700))], "drop the fan box into the fan bay",
       "Bottom flush with the joist undersides; four screws through each long side into the joists", **A)
    walls.append(g("fan_box"))
    st(12, walls, [mv("deck", (0, 0, 600))], "nail the ceiling boards on", "20 mm boards across the joists, cut round the fan box", **A)
    walls.append(g("deck"))
    st(13, walls, [mv("fans", (0, 0, 500))], "fans and shutters onto the fan box",
       "Each fan over its hole, blowing up, four screws; guard under the hole; gravity shutter on top", **A)
    walls.append(g("fans"))
    st(14, walls, [mv("beams", (0, 0, 600))], "roof beams onto the post cap plates", "Two M10 coach screws up through each cap plate", **A)
    walls.append(g("beams"))
    st(15, walls, [mv("purlins", (0, 0, 500))], "purlins onto the beams", "Five purlins 700 mm apart along the slope; a hurricane tie at every crossing", **A)
    walls.append(g("purlins"))
    st(16, walls, [mv("sheet", (0, 0, 600))], "roof sheets onto the purlins",
       "Laid down the slope with side laps away from the wind; a sealing-washer screw on every second crest at each purlin", **A)
    walls.append(g("sheet"))
    st(17, walls, [mv("mount", (0, 0, 400), "Panel mounting frames (2)")], "panel frames onto the roof",
       "Base rails screwed through sheet crests into the purlins; legs and top rails bolted on", **A)
    walls.append(g("mount"))
    st(18, walls, [mv("panel", (0, 0, 400))], "solar panel onto its frames", "Bolted through the frame's own holes; check 15 degrees", **A)
    walls.append(g("panel"))
    PAD = dict(elev=15, azim=-30)
    pw_ = (1050, 2200, -1100, 1100, 0, 2200)          # the pad end of the store, for close-up steps
    pad_end = [part("Pad end wall", win(sh("walls"), *pw_), COL["walls"]), part("Lintels", win(sh("lintels"), *pw_), COL["lintels"]),
               part("Floor", win(sh("floor"), *pw_), COL["floor"])]
    walls_full = walls
    walls = list(pad_end)
    st(19, walls, [mv("pad_lining", (700, 0, 0))], "line the pad opening", "Four boards, flush with the outside face; clear opening 600 x 500 mm", **PAD)
    walls.append(g("pad_lining"))
    st(20, walls, [part("Battens and frame sides and top", sh("pad_battens", "pad_frame"), COL["pad_frame"], (500, 0, 0)),
                   part("Bottom support bars", shape_of(C["pad_bars"][1][:2]), COL["pad_bars"], (0, 0, -300))],
       "pad frame onto the wall", "Battens plugged to the wall; sides screwed to them; top between the sides; bottom bars under the sides", **PAD)
    walls.append(part("Pad frame", sh("pad_battens", "pad_frame", "pad_bars"), COL["pad_frame"]))
    st(21, walls, [mv("pad", (600, 0, 0)), part("Front retaining bars", shape_of(C["pad_bars"][1][2:]), COL["pad_bars"], (900, 0, 0))],
       "pad into its frame", "Pad in from the front onto the bottom bars, flutes sloping down toward the room; then the two front bars", **PAD)
    walls.append(g("pad"))
    st(22, walls, [mv("header", (0, -700, 0))], "drip header through the frame", "Slide in from the right side; holes down; open end out 75 mm on the right", **PAD)
    walls.append(g("header"))
    st(23, walls, [mv("gutter", (300, 0, -300), "Gutter and brackets")], "gutter under the pad", "Brackets plugged to the wall; gutter top 20 mm below the pad; fall to the outlet", **PAD)
    walls.append(g("gutter"))
    st(24, walls, [mv("sump", (500, -500, 0), "Sump drum and hoses")], "sump drum and hoses",
       "Drum on level ground at the right of the pad; feed hose from the pump to the header, return hose from the gutter outlet", **PAD)
    walls.append(g("sump"))
    walls = walls_full + walls[len(pad_end):]
    st(25, walls, [mv("power_box", (-400, 0, 0), "Power box (right of the door)"), part("Controller and outside sensor (left)", sh("controller", "sensor"), COL["controller"], (-400, 0, 0))],
       "power box, controller and sensor on the front wall", "Screwed into plugs at 1.0 to 1.3 m; wire as the wiring diagram", **DOOR)
    walls += [g("power_box", "Power box"), part("Controller", sh("controller", "sensor"), COL["controller"])]
    inside = [g("strip_footing"), g("walls"), g("floor"), g("door_lining")]
    st(26, inside, [part("Racks", sh("racks"), COL["racks"], (0, 0, 0)), part("Wall brackets", sh("rack_brackets"), COL["rack_brackets"], (0, 0, 0))],
       "racks in along the long walls (roof and ceiling hidden)", "Carried in through the door in parts and assembled inside; end posts bracketed to the wall",
       elev=72, azim=-60)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "ZeerBox prototype: block-level 12 V wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought parts wired at block level; no circuit board is laid out. Stranded copper; ferrules on every screw terminal; IP65 connectors outdoors.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/zeerbox", fontsize=7, color="#0F766E", ha="right", family="monospace")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    ax.add_patch(FancyBboxPatch((22, 30), 36, 30, boxstyle="round,pad=0.4", fc="#F0FDF4", ec="#16A34A", lw=1, ls="--"))
    ax.text(23.5, 58.8, "Power box (right of the door, shaded)", fontsize=8, color=MUT, va="top")
    ax.add_patch(FancyBboxPatch((64, 30), 22, 30, boxstyle="round,pad=0.4", fc="#F5F3FF", ec="#7C3AED", lw=1, ls="--"))
    ax.text(65.5, 58.8, "Controller box (left of the door)", fontsize=8, color=MUT, va="top")
    blk(3, 44, 14, 12, "Solar panel", "150 W, Vmp 18 V,\nIsc 9 A, on the roof", "#1E3A8A")
    blk(25, 44, 14, 11, "Charge controller", "20 A PWM,\n12.8 V LiFePO4 setting", "#16A34A")
    blk(25, 32, 14, 10, "Battery", "12.8 V 12 Ah LiFePO4\nwith BMS (10 A charge)", "#C2410C")
    blk(42, 32, 13, 10, "15 A fuse", "at the battery\nterminal", "#B91C1C")
    blk(67, 41, 16, 15, "Controller", "microcontroller, MOSFET\ndrivers, card logger,\nthree-colour mode lamp", "#7C3AED")
    blk(91, 50, 13, 9, "Fans (2)", "in the ceiling\nfan box, 12 W each", "#111827")
    blk(91, 38, 13, 9, "Pump", "in the sump drum,\n6 W, float switch", "#2563EB")
    blk(91, 26, 13, 9, "Inside sensor", "temperature and RH,\nmid-store, 1.5 m up", "#0F766E")
    blk(67, 16, 16, 9, "Outside sensor", "in its radiation\nshield on the wall", "#0F766E")
    wire([(10, 44), (10, 40), (21, 40), (21, 49), (25, 49)], RED); lab(4, 38, "PV cable 2.5 mm², down the door-end\nright post in conduit", RED)
    wire([(36, 44), (36, 43.2), (48.5, 43.2), (48.5, 42)], RED); lab(50, 43.2, "battery terminal, 2.5 mm²", RED)
    wire([(39, 37), (42, 37)], RED); lab(40.5, 39.6, "2.5 mm²", RED, "center")
    wire([(39, 47), (67, 47)], RED); lab(52, 45.2, "load output, 1.5 mm²", RED, "center")
    wire([(83, 54), (91, 54)], RED); lab(87, 56, "1.5 mm²", RED, "center")
    wire([(83, 44), (91, 43)], RED); lab(87, 45.6, "1.5 mm²", RED, "center")
    wire([(83, 42), (88, 42), (88, 30), (91, 30)], BLU, 1.2); lab(87.4, 27, "4-core 0.5 mm²", BLU, "right")
    wire([(75, 41), (75, 25)], BLU, 1.2); lab(75.6, 35, "4-core 0.5 mm²", BLU)
    ax.text(3, 21, "Cable routes", fontsize=8.5, fontweight="bold", color=INK)
    for i, t in enumerate(["Fans: 1.5 mm² twin from the controller box, up the wall in conduit, over the wall top under the",
                           "  ceiling boards to the fan box (keep the conduit sealed where it crosses the husk-filled wall top).",
                           "Pump: 1.5 mm² twin in conduit along the right long wall, 300 mm above ground, to the sump; drip loop at the drum.",
                           "Inside sensor: through the door lining head in a gland, to a sensor on the right rack's middle post."]):
        ax.text(3, 18 - i * 2.6, t, fontsize=7.4, color=INK)
    ax.text(3, 6.2, "Safety: battery fuse out until the wiring checks pass. Never charge the battery below 0 °C or above 45 °C. All circuits are 12 V DC.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(3, 3.8, "Red: power. Blue: signal. Wire sizes are for runs up to 6 m (ZBX-CAL-001 section 4).", fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "setout", "sheets", "joints", "steps", "wiring"]
    fns = {"overview": overview, "setout": setout, "sheets": sheets, "joints": joints, "steps": steps, "wiring": wiring}
    i = 0
    while i < len(args):
        w = args[i]; i += 1
        nums = []
        while i < len(args) and args[i].isdigit():
            nums.append(int(args[i])); i += 1
        r = fns[w](nums) if w in ("sheets", "joints", "steps") else fns[w]()
        print(w, "->", r)
