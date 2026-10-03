"""ZeerBox product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of the walk-in evaporative store: fired-brick walls
with coursing and a rendered plinth, timber lintels, an insulated ceiling with a timber fascia, a
corrugated galvanized shade roof on purlins, rafters and steel posts with concrete footing collars, and a
150 W panel with its cells, frame and mounting frames. The cooling kit gets a cellulose pad with its
cross-fluted face in a timber frame, a PVC drip header and a galvanized return gutter; a 60 L
drum with rolling hoops, lid and label, and its feed and return hoses; two 250 mm fans in a ceiling box with
blades and gravity shutters; the IP65 controller with a clear lid over its
board, a lit green mode lamp and the outside sensor in a six-plate shield; and a
ventilated shaded power box with a plain door. The door has a seal, hinges and a
handle. Inside, the racks have slatted shelves and the crates carry produce. Context is a compact
patch of ground and the shared clay mannequin standing by the door.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, position and interface comes from PARAMS, derived() and build_parts() in
model.py (walls, cavity fill and rack geometry are reused directly). Axes as model.py: X along the
store with the door and fans at -X and the pad at +X, Y across it, Z up, ground at Z = 0.
Appearance-only differences from model.py are listed in docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / ".kit"))

from build123d import (Axis, Box, Compound, Cylinder, Face, Plane, Pos, Rot, Solid, Sphere, Vector,  # noqa: E402
                       Wire, extrude, fillet)
from model import PARAMS, derived, build_components, roof_frame, panel_frame  # noqa: E402

TITLE = "ZeerBox: solar-powered walk-in evaporative cooling store"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); store on a patch "
             "of ground with the wetted pad, drip header and sump drum on the near end, the 150 W panel "
             "on the shade roof and a person standing by the door at the far end for scale"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): panel, shade roof "
             "and posts, ceiling and rice husk fill lifted off the brick walls; pad, frame, header, "
             "gutter and sump at right; door, controller and power box at left; fans lifted clear above the ceiling; racks and crates "
             "pulled out in front"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 18, "az": -160,
     "note": "Detail from the door end, slightly to the front and above (about 18 deg elevation), cooling "
             "kit only: controller with its clear lid, lit green mode lamp and six-plate sensor shield, "
             "power box with a plain door in front, fans with gravity shutters in their ceiling box above; "
             "pad (inner face), drip header, gutter and sump drum at the far end"},
]

# Appearance-only sizes and placement (mm)
GROUND = (-2450.0, 2400.0, -1750.0, 1650.0, 80.0)   # x0, x1, y0, y1, thickness (top at Z = 0)
PERSON_AT = (-2000.0, -800.0)                       # beside the door at the -X end, clear of the post
PERSON_ROT = 30.0                                   # turned toward the hero camera
COURSE = 75.0                                       # brick course height (65 mm brick, 10 mm joint)

# Colours (restrained product palette; kit accent)
C_BRICK = "#A0573C"
C_PLINTH = "#9C9890"
C_FILL = "#CDB27A"
C_FASCIA = "#A87E55"
C_TIMBER = "#8C6A48"
C_RACK = "#B08457"
C_GALV = "#B7BDC4"
C_POST = "#9EA5AD"
C_CONC = "#BDB9B1"
C_ACCENT = "#0F766E"
C_ALU = "#C3C8CE"
C_PAD = "#C49A5E"
C_PVC = "#E4E4E0"
C_HOSE = "#23262B"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_SHUTTER = "#E5E7EB"
C_SHELL = "#E9EAEC"
C_SHELL2 = "#C9CDD3"
C_WINDOW = "#DCEBF5"
C_PCB = "#166534"
C_CHIP = "#111827"
C_LABEL = "#F4F4F2"
C_CELL = "#1B2A4A"
C_BACKSHEET = "#E6E8EB"
C_LED_G = "#22C55E"
C_LCD = "#5EEAD4"
C_CRATE = "#51677A"
C_TOMATO = "#B5412B"
C_PEPPER = "#4E7D2A"
C_ONION = "#B98A4B"
C_GROUND = "#CFC4A8"
C_CLAY = "#9CA3AF"


# ------------------------------------------------------------------------------------ helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _comp(shapes):
    return Compound(list(shapes))


def _edges_par(s, axis):
    return s.edges().filter_by(axis)


def _face_edges(s, axis, end):
    f = s.faces().sort_by(axis)
    return (f[-1] if end > 0 else f[0]).edges()


def _panel_pt(x, y, z, c, tilt):
    """World point of a point in the panel's local frame (Pos(*c) * Rot(-tilt,0,0))."""
    a = math.radians(-tilt)
    return (c[0] + x, c[1] + y * math.cos(a) - z * math.sin(a), c[2] + y * math.sin(a) + z * math.cos(a))


# ------------------------------------------------------------------------------------ structure
def _walls(P, D, C):
    """Model.py walls and floor with brick bed joints and a rendered plinth band."""
    ol, ow = D["out_l"], D["out_w"]
    walls = _comp(C["floor"][1] + C["walls"][1])
    ring = Box(ol + 20, ow + 20, 9) - Box(ol - 8, ow - 8, 11)
    cutters = [Pos(0, 0, COURSE * k) * ring for k in range(4, int(D["top"] // COURSE))]
    walls = walls - _comp(cutters)
    xf = -ol / 2
    dw = P["DOOR_W"] + 2 * P["LINING"]
    plinth = Pos(0, 0, 150) * (Box(ol + 16, ow + 16, 300) - Box(ol - 2, ow - 2, 302))
    plinth -= _box(xf, 0, P["FLOOR"] + 150, 60, dw, 300)
    top = _box(0, 0, 301, ol + 22, ow + 22, 6) - _box(0, 0, 301, ol - 2, ow - 2, 8)
    top -= _box(xf, 0, 301, 60, dw, 10)
    plinth += top
    return walls, plinth


def _roof(P, D, C):
    """Corrugated sheet and screws in model.py's roof envelope; framing, posts and footings from model.py."""
    L, W = P["ROOF_L"], P["ROOF_W"]
    loc = roof_frame(P)
    pitch_c, amp, t = 76.0, 8.0, 2.0
    n = int(L // pitch_c)
    x0 = -n * pitch_c / 2
    top, bot = [], []
    steps = 6
    for i in range(n * steps + 1):
        x = x0 + i * pitch_c / steps
        z = amp * math.cos(2 * math.pi * (x - x0) / pitch_c)
        top.append(Vector(x, 0, z + t / 2))
        bot.append(Vector(x, 0, z - t / 2))
    wire = Wire.make_polygon(top + bot[::-1], close=True)
    sheet = extrude(Face(wire), amount=W, dir=(0, 1, 0))
    sheet = loc * (Pos(0, -W / 2, 0) * sheet)
    frame = _comp(C["beams"][1] + C["purlins"][1])
    screws = []
    for y in P["PURLIN_Y"]:
        for i in range(0, n, 3):
            x = x0 + i * pitch_c
            s = _zcyl(x, y, amp + t / 2 + 1.5, 9, 3) + _zcyl(x, y, amp + t / 2 + 6, 5, 6)
            screws.append(loc * s)
    screws = _comp(screws)
    # posts above ground only (model.py posts run into their footings), and the footing tops
    above = _box(0, 0, 3000, 8000, 8000, 6000)
    posts = _comp([p & above for p in C["posts"][1]])
    fs = P["FOOTING"]
    collars = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = _box(sx * P["POST_X"], sy * P["POST_Y"], 15, fs, fs, 30)
            collars.append(_fillet_try(c, _face_edges(c, Axis.Z, 1), [12.0, 6.0]))
    return sheet, frame, screws, posts, _comp(collars)


def _panel(P, D, C):
    """150 W panel in model.py's position and tilt, with frame, cells and junction box; legs are model.py's mount."""
    L, W, T = P["PANEL_L"], P["PANEL_W"], P["PANEL_T"]
    loc = panel_frame(P)
    fr = Box(L, W, T)
    fr = _fillet_try(fr, _edges_par(fr, Axis.Z), [4.0, 2.0])
    fr -= Box(L - 44, W - 44, T + 2)
    lip = Pos(0, 0, T / 2 - 1.5) * (Box(L, W, 3) - Box(L - 56, W - 56, 4))
    frame = loc * (fr + lip)
    back = loc * Pos(0, 0, T / 2 - 6) * Box(L - 42, W - 42, 4)
    nx, ny, cs, g = 9, 4, 148.0, 4.0
    cells, bars = [], []
    for i in range(nx):
        for j in range(ny):
            x = (i - (nx - 1) / 2) * (cs + g)
            y = (j - (ny - 1) / 2) * (cs + g)
            cells.append(loc * Pos(x, y, T / 2 - 3.5) * Box(cs, cs, 1.0))
            for k in (-1, 1):
                bars.append(loc * Pos(x + k * cs / 4, y, T / 2 - 2.8) * Box(1.6, cs - 6, 0.4))
    jb = loc * Pos(0, W / 4, -T / 2 - 12) * Box(110, 80, 24)
    return frame, back, _comp(cells), _comp(bars), jb, _comp(C["mount"][1])


def _door(P, D):
    """Door leaf in its lining: outer face 8 mm behind the wall face, DOOR_T thick (model.py)."""
    xf = -D["out_l"] / 2
    xo = xf + 8.0
    dt = P["DOOR_T"]
    fl, dw, dh = P["FLOOR"], P["DOOR_W"], P["DOOR_H"]
    zc = fl + dh / 2
    leaf = _box(xo + dt / 2, 0, fl + 5 + (dh - 8) / 2, dt, dw - 6, dh - 8)
    leaf = _fillet_try(leaf, _face_edges(leaf, Axis.X, -1), [6.0, 4.0, 2.0])
    for dz in (-dh / 4, dh / 4):
        leaf -= _box(xo + 2, 0, zc + dz, 4, dw - 120, 6)
    seal = _box(xo + dt + 1, 0, fl + dh / 2, 2, dw, dh) - _box(xo + dt + 1, 0, fl + dh / 2 - 10, 4, dw - 40, dh - 20)
    hw = []
    for dz in (-dh / 2 + 200, 0, dh / 2 - 200):
        hw.append(_zcyl(xo - 2, -dw / 2 + 8, zc + dz, 9, 110) + _box(xo - 2, -dw / 2 + 50, zc + dz, 4, 70, 90))
    hx, hy, hz = xo - 25, dw / 2 - 90, fl + 1050
    hw.append(_box(xo - 3, hy, hz, 6, 50, 200))
    hw.append(_pipe([(xo - 2, hy, hz + 70), (hx, hy, hz + 70), (hx, hy, hz - 70), (xo - 2, hy, hz - 70)], 11))
    sign = _box(xo - 0.5, 0, fl + 1450, 1.0, 260, 150)
    sign_ink = _box(xo - 1.2, 0, fl + 1490, 0.6, 200, 24) + _box(xo - 1.2, 0, fl + 1440, 0.6, 160, 10) \
        + _box(xo - 1.2, 0, fl + 1415, 0.6, 180, 10)
    return leaf, seal, _comp(hw), sign, sign_ink


def _racks(P, C):
    """model.py racks (slats already spaced); steel wall brackets separate."""
    return _comp(C["racks"][1]), _comp(C["rack_brackets"][1])


def _crates(P):
    """Ventilated open crates with produce, at model.py's crate positions and envelope."""
    cl, cw, ch = P["CRATE_L"] - 30, P["CRATE_W"] - 10, P["CRATE_H"] - 10
    crate = Box(cl, cw, ch)
    crate = _fillet_try(crate, _edges_par(crate, Axis.Z), [12.0, 8.0])
    crate -= Pos(0, 0, 8) * Box(cl - 16, cw - 16, ch)
    for dx in (-150, -50, 50, 150):
        crate -= Pos(dx, 0, -10) * Box(60, cw + 10, 150)
    crate -= Pos(0, 0, ch / 2 - 40) * Box(cl + 10, 110, 34)
    fills = {}
    n, rd, fl = P["CRATES_PER_SHELF"], P["RACK_D"], P["FLOOR"]
    crates = []
    for s in (-1, 1):
        yc = s * (P["IN_W"] / 2 - rd / 2)
        for z in P["SHELVES"]:
            for k in range(n):
                x = -(n - 1) * P["CRATE_L"] / 2 + k * P["CRATE_L"]
                zc = fl + z + P["CRATE_H"] / 2
                crates.append((s, Pos(x, yc, zc) * crate))
                fills.setdefault((s, z), []).append(Pos(x, yc, zc - 30) * Box(cl - 18, cw - 18, ch - 80))
    return crates, fills


# ------------------------------------------------------------------------------------ cooling kit
def _pad(P, D, C):
    """Pad media with cross flutes; frame, bars, header and gutter from model.py."""
    xb = D["out_l"] / 2
    pt, pw, ph, pz = P["PAD_T"], P["PAD_W"], P["PAD_H"], P["PAD_Z"]
    pad_x = xb + pt / 2
    media = _box(pad_x, 0, pz, pt, pw, ph)
    cut = []
    sp = 40.0 / math.cos(math.radians(45))
    k = int((pw + ph) / sp) + 1
    for face_x, ang in ((pad_x + pt / 2, 45), (pad_x - pt / 2, -45)):
        for i in range(-k, k + 1):
            cut.append(Pos(face_x, i * sp, pz) * Rot(ang, 0, 0) * Box(10, 7, 1100))
    media = media - _comp(cut)
    wood = _comp(C["pad_lining"][1] + C["pad_battens"][1] + C["pad_frame"][1])
    bars = _comp(C["pad_bars"][1])
    hz = pz + ph / 2 + 16
    header = _comp(C["header"][1])
    for y in (-pw / 2 - 100, pw / 2 + 40):
        header += _ycyl(pad_x, y + (6 if y < 0 else -6), hz, 20, 12)
    gut = _comp(C["gutter"][1])
    brk = _comp(C["gutter_brackets"][1])
    return wood, bars, media, header, gut, brk


def _sump(P, D, C):
    dx, dy = P["SUMP_XY"]
    dr, dh = P["SUMP_D"] / 2, P["SUMP_H"]
    body = _zcyl(dx, dy, (dh - 30) / 2, dr, dh - 30)
    body = _fillet_try(body, _face_edges(body, Axis.Z, -1), [12.0, 6.0])
    hoops = _comp([_zcyl(dx, dy, z, dr + 6, 16) - _zcyl(dx, dy, z, dr - 2, 18) for z in (170, 400)])
    lid = _zcyl(dx, dy, dh - 15, dr + 5, 30)
    lid = _fillet_try(lid, _face_edges(lid, Axis.Z, 1), [6.0, 3.0])
    for i in range(24):
        a = 2 * math.pi * i / 24
        lid -= Pos(dx + (dr + 5) * math.cos(a), dy + (dr + 5) * math.sin(a), dh - 18) * Rot(0, 0, math.degrees(a)) * Box(6, 8, 22)
    fittings = (_zcyl(dx, dy, dh + 10, 22, 20) + _zcyl(dx, dy - 50, dh + 6, 20, 12) + _zcyl(dx, dy + 50, dh + 6, 22, 12)
                + _zcyl(dx + 100, dy, dh + 8, 14, 16))
    view = math.radians(-40)
    lab = _zcyl(dx, dy, 290, dr + 0.8, 150) - _zcyl(dx, dy, 290, dr - 2, 152)
    lab &= Pos(dx + dr * math.cos(view), dy + dr * math.sin(view), 290) * Rot(0, 0, -40) * Box(dr, 2 * dr * 0.8, 200)
    feed, ret = C["hoses"][1]
    return body, hoops, lid, fittings, lab, feed, ret


def _fans(P, D, C):
    """Two 250 mm fans in the ceiling fan box, axes vertical, exhausting up through gravity shutters."""
    top = D["top"]
    z0 = top + P["JOIST"][1] + P["DECK_T"] + P["FANBOX_UP"] + P["PLY"]
    fx, fr = P["FAN_X"], P["FAN_D"] / 2
    housing, blades, hubs, shframe, louvers = [], [], [], [], []
    for s in (-1, 1):
        y = s * P["FAN_Y"]
        h = _box(fx, y, z0 + 45, 274, 274, 90) - _zcyl(fx, y, z0 + 45, fr - 3, 92)
        h = _fillet_try(h, _edges_par(h, Axis.Z), [14.0, 8.0])
        housing.append(h)
        hubs.append(_zcyl(fx, y, z0 + 45, 45, 80) + (Pos(fx, y, z0 + 85) * Sphere(45) & _box(fx, y, z0 + 100, 100, 100, 30)))
        for k in range(5):
            blades.append(Pos(fx, y, z0 + 50) * Rot(0, 0, k * 72) * Pos(82, 0, 0) * Rot(32, 0, 0) * Box(70, 52, 3))
        f = _box(fx, y, z0 + 105, 280, 280, 30) - _box(fx, y, z0 + 105, 250, 250, 32)
        f = _fillet_try(f, _edges_par(f, Axis.Z), [8.0, 4.0])
        shframe.append(f)
        for i in range(5):
            yy = y - 100 + 50 * i
            louvers.append(Pos(fx, yy, z0 + 100) * Rot(14, 0, 0) * Box(246, 48, 2))
    fanbox = _comp(C["fan_box"][1])
    return _comp(housing), _comp(blades), _comp(hubs), _comp(shframe), _comp(louvers), fanbox


def _controller(P, D):
    xf = -D["out_l"] / 2
    cd, cw, ch = P["CTRL"]
    cy, cz = P["CTRL_YZ"]
    cx = xf - cd / 2
    outer = _box(cx, cy, cz, cd, cw, ch)
    outer = _fillet_try(outer, _edges_par(outer, Axis.X), [10.0, 6.0])
    outer = _fillet_try(outer, _face_edges(outer, Axis.X, -1), [3.0, 1.5])
    xs = xf - cd + 20                                       # lid parting plane
    body = outer & _box((xs + xf) / 2 + 0.5, cy, cz, xf - xs - 1, cw + 20, ch + 20)
    body -= _box(xs + 20, cy, cz, 50, cw - 12, ch - 12)
    # hole for the mode lamp through the top wall (model.py LAMP)
    lh, lfl, lft, ldome, ldh, ldy = P["LAMP"]
    lx, ly, ltop = xf - cd / 2, cy + ldy, cz + ch / 2
    body -= _zcyl(lx, ly, ltop - 3, lh / 2, 14)
    lid = outer & _box((xf - cd + xs) / 2 - 0.5, cy, cz, xs - (xf - cd) - 1, cw + 20, ch + 20)
    # clear lid: a thin frame around a large clear window
    lid -= _box(xf - cd + 10, cy, cz, 30, cw - 50, ch - 50)
    lid -= _box(xs - 4, cy, cz, 12, cw - 12, ch - 12)
    pane = _box(xf - cd + 4, cy, cz, 2.0, cw - 40, ch - 40)
    pcb = _box(xf - 8, cy, cz, 3, 180, 220)
    chips = (_box(xf - 16, cy - 30, cz + 40, 12, 50, 26) + _box(xf - 13, cy + 45, cz + 30, 6, 22, 22)
             + _box(xf - 14, cy + 40, cz - 20, 8, 40, 16) + _box(xf - 14, cy - 40, cz - 30, 8, 24, 30))
    term = _box(xf - 16, cy, cz - 80, 14, 150, 18)
    for k in range(8):
        term -= _box(xf - 23.5, cy - 63 + 18 * k, cz - 76, 2, 7, 6)
    card = _box(xf - 12, cy + 60, cz + 70, 4, 26, 30)
    screws = _comp([_xcyl(xf - cd - 0.6, cy + sy * (cw / 2 - 12), cz + sz * (ch / 2 - 12), 3.4, 1.2) for sy in (-1, 1) for sz in (-1, 1)])
    plate = _box(xf - cd - 0.4, cy, cz + 97, 0.6, 120, 14)
    glands = []
    for dy in (-50, 0, 50):
        g = _zcyl(cx + 5, cy + dy, cz - ch / 2 - 3, 11, 6) + _zcyl(cx + 5, cy + dy, cz - ch / 2 - 11, 8, 10)
        glands.append(g + _zcyl(cx + 5, cy + dy, cz - ch / 2 - 45, 4, 60))
    # mode lamp: flange on the box top, body through the hole, dome (lit green for evaporative cooling mode)
    lamp_base = _zcyl(lx, ly, ltop + lft / 2, lfl / 2, lft) + _zcyl(lx, ly, ltop - 3, lh / 2 - 0.5, 6)
    dome_cyl = ldh - ldome / 2
    lamp = _zcyl(lx, ly, ltop + lft + dome_cyl / 2, ldome / 2, dome_cyl) + Pos(lx, ly, ltop + lft + dome_cyl) * Sphere(ldome / 2)
    # outside sensor: six stacked plates on a stud, on a strip arm screwed to the wall (model.py SHIELD)
    sd, sn, st_, sp_, sz0, sr_, sdx, sy0 = P["SHIELD"]
    scx = xf - sdx
    zt = sz0 + sp_ * (sn - 1) + st_
    sh = _comp([_zcyl(scx, sy0, sz0 + sp_ * k + st_ / 2, sd / 2, st_) for k in range(sn)])
    stud = _zcyl(scx, sy0, (sz0 + zt) / 2, sr_, zt - sz0)
    probe = _zcyl(scx, sy0, sz0 + 2.5 * sp_, 6, 8)
    arm = _box((scx + xf) / 2, sy0, 1350, sdx, 20, 10) + _box(xf - 1.5, sy0, 1350, 3, 36, 36)
    return (body, lid, pane, pcb, chips, term, card, screws, plate, _comp(glands), lamp_base, lamp, sh, stud, probe, arm)


def _powerbox(P, D):
    xf = -D["out_l"] / 2
    cx, cy, cz = xf - 50, -860.0, 1150.0                    # model.py power box: 100 x 220 x 300
    outer = _box(cx, cy, cz, 100, 220, 300)
    outer = _fillet_try(outer, _edges_par(outer, Axis.X), [8.0, 5.0])
    xs = xf - 85
    body = outer & _box((xs + xf) / 2 + 0.5, cy, cz, xf - xs - 1, 240, 320)
    body -= _box(xs + 30, cy, cz, 72, 206, 286)
    for sgn in (-1, 1):
        for k in range(5):
            body -= _box(cx + 8, cy + sgn * 110, cz - 90 + 30 * k, 50, 20, 7)
    hood = _box(cx - 5, cy, cz + 157, 116, 236, 10)
    hood = _fillet_try(hood, _edges_par(hood, Axis.Y), [3.0, 1.5])
    door = outer & _box((xf - 100 + xs) / 2 - 0.5, cy, cz, xs - (xf - 100) - 1, 240, 320)     # plain door, no window
    door -= _box(xs - 4, cy, cz, 12, 206, 286)
    ctrl = _box(xf - 30, cy, cz + 70, 50, 130, 80)
    ctrl = _fillet_try(ctrl, _edges_par(ctrl, Axis.X), [4.0, 2.0])
    batt = _box(xf - 35, cy, cz - 60, 70, 180, 110)
    batt = _fillet_try(batt, batt.edges(), [3.0, 1.5])
    hinges = _comp([_zcyl(xf - 101, cy - 108, cz + dz, 5, 50) for dz in (-90, 90)])
    hasp = _box(xf - 102, cy + 100, cz, 4, 16, 40) + _xcyl(xf - 106, cy + 100, cz, 5, 8)
    label = _box(xf - 100.4, cy, cz - 60, 0.6, 120, 50)
    ink = _box(xf - 100.8, cy, cz - 45, 0.4, 90, 10) + _box(xf - 100.8, cy, cz - 68, 0.4, 100, 5) \
        + _box(xf - 100.8, cy, cz - 80, 0.4, 70, 5)
    return body, hood, door, ctrl, batt, hinges, hasp, label, ink


def _conduit(P, D):
    """Cable run from the power box over the door and down to the controller, and over the ceiling to the fan box."""
    xf = -D["out_l"] / 2
    x = xf - 30
    zc = D["ceil_top"] + 40
    run = _pipe([(x, -860.0, 1300.0), (x, -860.0, 2060.0), (x, 935.0, 2060.0), (x, 935.0, 1275.0)], 12)
    run += _pipe([(x, -860.0, 2060.0), (x, -860.0, zc), (P["FAN_X"], -860.0, zc), (P["FAN_X"], -P["FANBOX"][1] / 2 - 5, zc)], 12)
    clips = []
    for (y, z) in [(-860, 1700), (-400, 2060), (400, 2060), (935, 1700)]:
        clips.append(_box(x + 8, y, z, 46, 20, 30) if z == 2060 else _box(x + 8, y, z, 46, 30, 20))
    return run, _comp(clips)


def _ground():
    x0, x1, y0, y1, t = GROUND
    g = _box((x0 + x1) / 2, (y0 + y1) / 2, -t / 2, x1 - x0, y1 - y0, t)
    return _fillet_try(g, _face_edges(g, Axis.Z, 1), [30.0, 12.0])


# ------------------------------------------------------------------------------------ assembly
def product_parts(P=PARAMS):
    D = derived(P)
    C = build_components(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ---- structure (BOM 1 to 5, 15 to 18)
    walls, plinth = _walls(P, D, C)
    add("Double brick walls and floor", walls, C_BRICK, "paper", 1, "shell", (0, 0, 0))
    add("Rendered plinth band", plinth, C_PLINTH, "paper", 1, "shell", (0, 0, 0))
    add("Hardwood lintels", _comp(C["lintels"][1]), C_TIMBER, "wood", 1, "shell", (0, 0, 0))
    add("Dry rice husk cavity fill", _comp(C["fill"][1]), C_FILL, "fabric", 2, "shell", (0, 0, 900))
    ceil = _comp(C["joists"][1] + C["insulation"][1] + C["deck"][1])
    add("Insulated ceiling, timber joists and boards", ceil, C_FASCIA, "wood", 3, "shell", (0, 0, 1900))
    sheet, frame, screws, posts, collars = _roof(P, D, C)
    ER = (0, 0, 2700)
    add("Corrugated galvanized roof sheet", sheet, C_GALV, "metal", 4, "shell", ER)
    add("Roof beams and purlins, timber", frame, C_TIMBER, "wood", 17, "shell", ER)
    add("Roof screws with washers", screws, C_POST, "metal", 4, "shell", ER)
    add("Roof posts, galvanized steel", posts, C_POST, "metal", 4, "shell", ER)
    add("Post footing collars, concrete", collars, C_CONC, "paper", 4, "shell", ER)
    pf, pback, cells, bars, jb, mount = _panel(P, D, C)
    EP = (0, 0, 3500)
    add("Solar panel frame, aluminum", pf, C_ALU, "metal", 10, "shell", EP)
    add("Solar panel backsheet", pback, C_BACKSHEET, "plastic", 10, "shell", EP)
    add("Solar cells", cells, C_CELL, "screen", 10, "shell", EP)
    add("Solar cell busbars", bars, C_ALU, "metal", 10, "shell", EP)
    add("Panel junction box", jb, C_BLACK, "plastic", 10, "shell", EP)
    add("Panel mounting frames, aluminum", mount, C_ALU, "metal", 18, "shell", (0, 0, 3100))
    leaf, seal, hw, sign, ink = _door(P, D)
    ED = (-2500, 0, 0)
    add("Insulated door leaf", leaf, C_ACCENT, "painted", 5, "shell", ED)
    add("Door rubber seal", seal, C_BLACK, "rubber", 5, "shell", (-2150, 0, 0))
    add("Door hinges and handle", hw, C_POST, "metal", 5, "shell", ED)
    add("Door sign", sign, C_LABEL, "paper", 5, "shell", ED)
    add("Door sign print", ink, C_DARK, "paper", 5, "shell", ED)
    add("Door lining and stop beads, timber", _comp(C["door_lining"][1] + C["door_stops"][1]), C_TIMBER, "wood", 16,
        "shell", (-1800, 0, 0))

    # ---- racks and crates (BOM 12, 13); pulled out in front for the exploded view
    ERa, ERb = (-1250, -2600, 0), (1250, -3650, 0)
    crates, fills = _crates(P)
    for s, e, tag in ((-1, ERa, "near"), (1, ERb, "far")):
        add(f"Produce crates, {tag} rack", _comp([c for ss, c in crates if ss == s]), C_CRATE, "plastic", 13,
            "accessory", e)
        for z, col, what in zip(P["SHELVES"], (C_ONION, C_PEPPER, C_TOMATO), ("onions", "peppers", "tomatoes")):
            add(f"Produce, {what}, {tag} rack", _comp(fills[(s, z)]), col, "plastic", 13, "accessory", e)
    racks, brackets = _racks(P, C)
    for s, e, tag in ((-1, ERa, "near"), (1, ERb, "far")):
        box = _box(0, s * P["IN_W"] / 4, 1000, P["IN_L"] + 400, P["IN_W"] / 2, 2000)
        add(f"Shelving rack, slatted timber, {tag}", racks & box, C_RACK, "wood", 12, "shell", e)
        add(f"Rack wall brackets, steel, {tag}", brackets & box, C_POST, "metal", 12, "shell", e)

    # ---- cooling kit (BOM 6 to 9, 11, 14, 16)
    wood6, bars6, media, header, gut, gbrk = _pad(P, D, C)
    add("Pad lining, battens and frame, timber", wood6, C_TIMBER, "wood", 6, "internal", (700, 0, 0))
    add("Pad support and retaining bars", bars6, C_GALV, "metal", 6, "internal", (760, 0, 0))
    add("Cellulose evaporative pad, 150 mm", media, C_PAD, "paper", 6, "internal", (1050, 0, 0))
    add("Drip header, PVC", header, C_PVC, "plastic", 6, "internal", (1050, 0, 300))
    add("Return gutter, galvanized", gut, C_GALV, "metal", 6, "internal", (1050, 0, -250))
    add("Gutter brackets, galvanized", gbrk, C_GALV, "metal", 6, "internal", (1050, 0, -250))
    body, hoops, lid, fit, lab, feed, ret = _sump(P, D, C)
    ES = (1700, -300, 0)
    add("Sump drum, 60 L", body, C_ACCENT, "plastic", 7, "internal", ES)
    add("Sump drum hoops", hoops, C_ACCENT, "plastic", 7, "internal", ES)
    add("Sump drum lid", lid, C_DARK, "plastic", 7, "internal", (1700, -300, 250))
    add("Pump and hose fittings", fit, C_BLACK, "plastic", 7, "internal", (1700, -300, 250))
    add("Sump drum label", lab, C_LABEL, "paper", 7, "internal", ES)
    add("Feed hose to header", feed, C_HOSE, "rubber", 7, "internal", (1350, -150, 150))
    add("Return hose from gutter", ret, C_HOSE, "rubber", 7, "internal", (1350, -150, -120))
    housing, blades, hubs, shf, louv, fanbox = _fans(P, D, C)
    add("Fan box, plywood", fanbox, C_FASCIA, "wood", 16, "internal", (0, 0, 1900))
    EF = (0, 0, 2200)
    add("Fan housings", housing, C_DARK, "plastic", 8, "internal", EF)
    add("Fan blades", blades, C_BLACK, "plastic", 8, "internal", EF)
    add("Fan motor hubs", hubs, C_BLACK, "plastic", 8, "internal", EF)
    add("Gravity shutter frames", shf, C_SHUTTER, "plastic", 8, "internal", (0, 0, 2600))
    add("Gravity shutter louvers", louv, C_SHUTTER, "plastic", 8, "internal", (0, 0, 2600))
    (cbody, clid, cpane, pcb, chips, term, card, cscr, plate, glands,
     lbase, lamp, shield, stud, probe, arm) = _controller(P, D)
    EC, ECL = (-700, 300, -150), (-900, 300, -150)
    add("Controller enclosure, IP65", cbody, C_SHELL, "plastic", 9, "internal", EC)
    add("Controller clear lid frame", clid, C_SHELL2, "plastic", 9, "internal", ECL)
    add("Controller clear lid, polycarbonate", cpane, C_WINDOW, "clear", 9, "internal", ECL)
    add("Controller lid screws", cscr, C_POST, "metal", 9, "internal", ECL)
    add("Controller name plate", plate, C_ACCENT, "painted", 9, "internal", ECL)
    add("Controller board", pcb, C_PCB, "plastic", 9, "internal", EC)
    add("Controller board components", chips, C_CHIP, "plastic", 9, "internal", EC)
    add("Fan and pump driver terminals", term, "#2E7D5B", "plastic", 9, "internal", EC)
    add("Memory card logger", card, C_POST, "metal", 9, "internal", EC)
    add("Controller cable glands and cables", glands, C_DARK, "rubber", 9, "internal", EC)
    add("Mode lamp flange and body", lbase, C_DARK, "plastic", 9, "internal", EC)
    add("Mode lamp dome, green (lit)", lamp, C_LED_G, "emissive", 9, "internal", EC)
    add("Sensor shield, six stacked plates", shield, "#F2F2EF", "plastic", 9, "internal", (-700, 300, 150))
    add("Sensor shield stud", stud, C_POST, "metal", 9, "internal", (-700, 300, 150))
    add("Outside RH/T sensor probe", probe, C_DARK, "plastic", 9, "internal", (-700, 300, 150))
    add("Sensor strip arm", arm, C_POST, "metal", 9, "internal", (-700, 300, 150))
    (pbody, hood, pdoor, pctrl, batt, hinges, hasp, plab, pink) = _powerbox(P, D)
    EB, EBD = (-700, -300, -150), (-900, -300, -150)
    add("Power box, ventilated steel", pbody, C_SHELL2, "painted", 11, "internal", EB)
    add("Power box rain hood", hood, C_SHELL2, "painted", 11, "internal", (-700, -300, 0))
    add("Power box door, plain", pdoor, C_SHELL2, "painted", 11, "internal", EBD)
    add("Power box hinges and hasp", _comp([hinges, hasp]), C_POST, "metal", 11, "internal", EBD)
    add("Power box label", plab, C_LABEL, "paper", 11, "internal", EBD)
    add("Power box label print", pink, C_DARK, "paper", 11, "internal", EBD)
    add("PWM charge controller", pctrl, C_DARK, "plastic", 11, "internal", EB)
    add("LiFePO4 battery, 12.8 V", batt, "#1F4E79", "plastic", 11, "internal", EB)
    run, clips = _conduit(P, D)
    add("Cable conduit, PVC", run, C_PVC, "plastic", 14, "shell", (-650, 0, 0))
    add("Conduit clips", clips, C_POST, "metal", 14, "shell", (-650, 0, 0))

    # ---- context: compact ground patch and the shared clay mannequin by the door
    add("Ground patch, compacted earth", _ground(), C_GROUND, "paper", None, "context", (0, 0, 0))
    from context_parts import mannequin
    person = Pos(PERSON_AT[0], PERSON_AT[1], 0) * Rot(0, 0, PERSON_ROT) * mannequin(1750, "stand")
    add("Person, 1.75 m (scale)", person, C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:45s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1e6:10.3f} L")
