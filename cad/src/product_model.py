"""ZeerBox product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of the walk-in evaporative store: fired-brick walls
with coursing and a rendered plinth, timber lintels, an insulated ceiling with a timber fascia, a
corrugated galvanized shade roof on purlins, rafters and steel posts with concrete footing collars, and a
150 W panel with its cells, frame and mounting legs. The cooling kit gets a cellulose pad with its
cross-fluted face in an aluminum frame, a PVC drip header and a galvanized return gutter; a 60 L
drum with rolling hoops, lid and label, and its feed and return hoses; two 250 mm fans with
blades, finger guards and gravity shutters; the IP65 controller with a clear lid window over its
board, a lit green mode lamp and the outside sensor in a stacked-plate radiation shield; and a
ventilated power box with a window onto the charge controller. The door has a seal, hinges and a
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
from model import PARAMS, derived, build_parts  # noqa: E402

TITLE = "ZeerBox: solar-powered walk-in evaporative cooling store"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); store on a patch "
             "of ground with the wetted pad, drip header and sump drum on the near end, the 150 W panel "
             "on the shade roof and a person standing by the door at the far end for scale"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): panel, shade roof "
             "and posts, ceiling and rice husk fill lifted off the brick walls; pad, frame, header, "
             "gutter and sump at right; door, fans, controller and power box at left; racks and crates "
             "pulled out in front"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 18, "az": -160,
     "note": "Detail from the door end, slightly to the front and above (about 18 deg elevation), cooling "
             "kit only: controller with its lit green mode lamp and radiation shield, fans with gravity "
             "shutters and power box in front; pad (inner face), drip header, gutter and sump drum at the "
             "far end"},
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
def _walls(P, D, model_parts):
    """Model.py walls and floor with brick bed joints and a rendered plinth band."""
    ol, ow = D["out_l"], D["out_w"]
    walls = model_parts[1][1]
    ring = Box(ol + 20, ow + 20, 9) - Box(ol - 8, ow - 8, 11)
    cutters = [Pos(0, 0, COURSE * k) * ring for k in range(4, int(D["top"] // COURSE))]
    walls = walls - _comp(cutters)
    xf = -ol / 2
    plinth = Pos(0, 0, 150) * (Box(ol + 16, ow + 16, 300) - Box(ol - 2, ow - 2, 302))
    plinth -= _box(xf, 0, P["FLOOR"] + 150, 60, P["DOOR_W"], 300)
    top = _box(0, 0, 301, ol + 22, ow + 22, 6) - _box(0, 0, 301, ol - 2, ow - 2, 8)
    top -= _box(xf, 0, 301, 60, P["DOOR_W"], 10)
    plinth += top
    return walls, plinth


def _lintels(P, D):
    xf, xb = -D["out_l"] / 2, D["out_l"] / 2
    zp = P["PAD_Z"] + P["PAD_H"] / 2 + 120
    lp = _box(xb + 3, 0, zp, 6, P["PAD_W"] + 400, 120)
    zd = P["FLOOR"] + P["DOOR_H"] + 70
    ld = _box(xf - 3, 0, zd, 6, P["DOOR_W"] + 300, 120)
    return lp + ld


def _roof(P, D):
    """Corrugated sheet, purlins, rafters, screws, posts and footing collars, in model.py's roof envelope."""
    rz, pitch = D["roof_z"], P["ROOF_PITCH_DEG"]
    L, W = P["ROOF_L"], P["ROOF_W"]
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
    sheet = Pos(0, -W / 2, 0) * sheet
    loc = Pos(0, 0, rz) * Rot(pitch, 0, 0)
    sheet = loc * sheet

    # purlins along X under the sheet, rafters along Y on the post lines
    px, py = P["POST_X"], P["POST_Y"]
    purl_y = (-py, -py / 3, py / 3, py)
    frame = None
    for y in purl_y:
        b = loc * _box(0, y, -amp - t / 2 - 25, L - 100, 50, 50)
        frame = b if frame is None else frame + b
    for x in (-px, px):
        frame += loc * _box(x, 0, -amp - t / 2 - 50 - 37.5, 75, W - 60, 75)

    # roof screws on alternate crests along each purlin
    screws = []
    for y in purl_y:
        for i in range(0, n, 2):
            x = x0 + i * pitch_c
            s = _zcyl(x, y, amp + t / 2 + 1.5, 9, 3) + _zcyl(x, y, amp + t / 2 + 6, 5, 6)
            screws.append(loc * s)
    screws = _comp(screws)

    # posts (model.py positions and heights) with cap plates, and the visible tops of the footings
    rise = math.tan(math.radians(pitch))
    posts, collars = [], []
    fs = P["FOOTING"]
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * px, sy * py
            ztop = rz - 15 + y * rise - amp - t / 2 - 50 - 75 + 15
            posts.append(_zcyl(x, y, ztop / 2, P["POST_D"] / 2, ztop)
                         + _zcyl(x, y, ztop - 4, P["POST_D"] / 2 + 12, 8))
            c = _box(x, y, 15, fs, fs, 30)
            collars.append(_fillet_try(c, _face_edges(c, Axis.Z, 1), [12.0, 6.0]))
    return sheet, frame, screws, _comp(posts), _comp(collars)


def _panel(P, D):
    """150 W panel in model.py's position and tilt, with frame, cells, junction box and legs."""
    L, W, T = P["PANEL_L"], P["PANEL_W"], P["PANEL_T"]
    tilt = P["PANEL_TILT_DEG"]
    c = (0.0, -300.0, D["roof_z"] + 150)
    loc = Pos(*c) * Rot(-tilt, 0, 0)
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
    # four aluminum legs from the frame underside to the roof sheet
    rz, pitch = D["roof_z"], P["ROOF_PITCH_DEG"]
    rise = math.tan(math.radians(pitch))
    legs = []
    for lx in (-L / 2 + 180, L / 2 - 180):
        for ly in (-W / 2 + 60, W / 2 - 60):
            a = _panel_pt(lx, ly, -T / 2, c, tilt)
            zr = rz + a[1] * rise + 9.0
            legs.append(_box(a[0], a[1], (a[2] + zr) / 2, 30, 30, a[2] - zr + 10)
                        + _box(a[0], a[1], zr + 2, 60, 60, 4))
        a0 = _panel_pt(lx, -W / 2 + 60, -T / 2 - 12, c, tilt)
        a1 = _panel_pt(lx, W / 2 - 60, -T / 2 - 12, c, tilt)
        legs.append(_pipe([a0, a1], 12))
    return frame, back, _comp(cells), _comp(bars), jb, _comp(legs)


def _door(P, D):
    xf = -D["out_l"] / 2
    fl, dw, dh = P["FLOOR"], P["DOOR_W"], P["DOOR_H"]
    zc = fl + dh / 2
    leaf = _box(xf + 30, 0, zc, 50, dw - 10, dh - 10)
    leaf = _fillet_try(leaf, _face_edges(leaf, Axis.X, -1), [6.0, 4.0, 2.0])
    for dz in (-dh / 4, dh / 4):
        leaf -= _box(xf + 5, 0, zc + dz, 4, dw - 120, 6)
    seal = _box(xf + 40, 0, zc, 20, dw + 2, dh + 2) - _box(xf + 40, 0, zc, 24, dw - 10, dh - 10)
    hw = []
    for dz in (-dh / 2 + 200, 0, dh / 2 - 200):
        hw.append(_zcyl(xf - 2, -dw / 2 + 12, zc + dz, 9, 110) + _box(xf + 2, -dw / 2 + 50, zc + dz, 4, 70, 90))
    hx, hy, hz = xf - 25, dw / 2 - 90, fl + 1050
    hw.append(_box(xf + 3, hy, hz, 6, 50, 200))
    hw.append(_pipe([(xf + 2, hy, hz + 70), (hx, hy, hz + 70), (hx, hy, hz - 70), (xf + 2, hy, hz - 70)], 11))
    sign = _box(xf + 4, 0, fl + 1450, 1.0, 260, 150)
    sign_ink = _box(xf + 3.3, 0, fl + 1490, 0.6, 200, 24) + _box(xf + 3.3, 0, fl + 1440, 0.6, 160, 10) \
        + _box(xf + 3.3, 0, fl + 1415, 0.6, 180, 10)
    return leaf, seal, _comp(hw), sign, sign_ink


def _racks(P, model_parts):
    """model.py racks with slatted shelves (three gaps along each shelf)."""
    racks = model_parts[12][1]
    rd, rl, fl = P["RACK_D"], P["RACK_L"], P["FLOOR"]
    cut = []
    for s in (-1, 1):
        yc = s * (P["IN_W"] / 2 - rd / 2)
        for z in P["SHELVES"]:
            for dy in (-rd / 4, 0, rd / 4):
                cut.append(_box(0, yc + dy, fl + z - 12.5, rl - 2 * P["RACK_POST"] - 20, 14, 30))
    return racks - _comp(cut)


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
def _pad(P, D):
    xb = D["out_l"] / 2
    pt, pw, ph, pz = P["PAD_T"], P["PAD_W"], P["PAD_H"], P["PAD_Z"]
    pad_x = xb + pt / 2 + 10
    fo = _box(pad_x, 0, pz, pt + 20, pw + 100, ph + 100)
    fo = _fillet_try(fo, _edges_par(fo, Axis.X), [10.0, 6.0])
    fo = _fillet_try(fo, _face_edges(fo, Axis.X, 1), [3.0, 2.0])
    frame = fo - _box(pad_x, 0, pz, pt + 40, pw, ph)
    frame -= _box(pad_x + (pt + 20) / 2, 0, pz, 4, pw + 60, ph + 60) - _box(pad_x + (pt + 20) / 2, 0, pz, 6, pw + 56, ph + 56)
    screws = []
    for sy in (-1, 1):
        for sz in (-1, 1):
            screws.append(_xcyl(pad_x + (pt + 20) / 2 + 1, sy * (pw / 2 + 25), pz + sz * (ph / 2 + 25), 6, 3))
    media = _box(pad_x, 0, pz, pt, pw, ph)
    cut = []
    sp = 40.0 / math.cos(math.radians(45))
    k = int((pw + ph) / sp) + 1
    for face_x, ang in ((pad_x + pt / 2, 45), (pad_x - pt / 2, -45)):
        for i in range(-k, k + 1):
            cut.append(Pos(face_x, i * sp, pz) * Rot(ang, 0, 0) * Box(10, 7, 1100))
    media = media - _comp(cut)
    # drip header with end caps and a tee for the feed hose
    hz = pz + ph / 2 + 80
    header = _ycyl(pad_x, 0, hz, 16, pw + 160)
    for sy in (-1, 1):
        header += _ycyl(pad_x, sy * (pw / 2 + 80), hz, 20, 18)
    header += _ycyl(pad_x, -pw / 2 - 60, hz, 20, 44)
    # return gutter with an outlet
    gz = pz - ph / 2 - 80
    gut = _box(pad_x + 10, 0, gz, 150, pw + 160, 60)
    gut = _fillet_try(gut, _edges_par(gut, Axis.Y), [4.0, 2.0])
    gut -= _box(pad_x + 10, 0, gz + 15, 120, pw + 140, 60)
    gut += _zcyl(pad_x + 10, -pw / 2 - 60, gz - 40, 20, 30)
    return frame, _comp(screws), media, header, gut, pad_x, hz, gz


def _sump(P, D, pad_x, hz, gz):
    xb = D["out_l"] / 2
    dx, dy, dr, dh = xb + 450, -750.0, P["SUMP_D"] / 2, P["SUMP_H"]
    body = _zcyl(dx, dy, (dh - 30) / 2, dr, dh - 30)
    body = _fillet_try(body, _face_edges(body, Axis.Z, -1), [12.0, 6.0])
    hoops = _comp([_zcyl(dx, dy, z, dr + 6, 16) - _zcyl(dx, dy, z, dr - 2, 18) for z in (170, 400)])
    lid = _zcyl(dx, dy, dh - 15, dr + 5, 30)
    lid = _fillet_try(lid, _face_edges(lid, Axis.Z, 1), [6.0, 3.0])
    for i in range(24):
        a = 2 * math.pi * i / 24
        lid -= Pos(dx + (dr + 5) * math.cos(a), dy + (dr + 5) * math.sin(a), dh - 18) * Rot(0, 0, math.degrees(a)) * Box(6, 8, 22)
    fittings = _zcyl(dx, dy, dh + 10, 22, 20) + _zcyl(dx, dy + 60, dh + 8, 24, 16) + _zcyl(dx - 90, dy - 60, dh + 8, 14, 16)
    view = math.radians(-40)
    lab = _zcyl(dx, dy, 290, dr + 0.8, 150) - _zcyl(dx, dy, 290, dr - 2, 152)
    lab &= Pos(dx + dr * math.cos(view), dy + dr * math.sin(view), 290) * Rot(0, 0, -40) * Box(dr, 2 * dr * 0.8, 200)
    feed = _pipe([(dx, dy, dh + 20), (dx, dy, hz), (pad_x, -P["PAD_W"] / 2 - 60, hz)], 12)
    ret = _pipe([(pad_x + 10, -P["PAD_W"] / 2 - 60, gz - 55), (pad_x + 10, -P["PAD_W"] / 2 - 60, dh + 220),
                 (dx, dy + 60, dh + 220), (dx, dy + 60, dh + 16)], 16)
    return body, hoops, lid, fittings, lab, feed, ret


def _fans(P, D):
    xf = -D["out_l"] / 2
    fr = P["FAN_D"] / 2
    housing, blades, hubs, guards, shframe, louvers = [], [], [], [], [], []
    for s in (-1, 1):
        y, z = s * P["FAN_Y"], P["FAN_Z"]
        h = _xcyl(xf - 35, y, z, fr + 15, 90) - _xcyl(xf - 35, y, z, fr - 5, 100)
        h = _fillet_try(h, h.edges(), [3.0, 1.5])
        housing.append(h)
        hub = _xcyl(xf - 35, y, z, 45, 80) + (Pos(xf - 75, y, z) * Sphere(45) & _box(xf - 90, y, z, 30, 100, 100))
        hubs.append(hub)
        for k in range(5):
            b = Pos(xf - 50, y, z) * Rot(k * 72, 0, 0) * Pos(0, 0, 82) * Rot(0, 0, 32) * Box(3, 52, 70)
            blades.append(b)
        g = None
        for r in (60, 88, 116):
            ring = _xcyl(xf + 12, y, z, r + 2.5, 4) - _xcyl(xf + 12, y, z, r - 2.5, 6)
            g = ring if g is None else g + ring
        for a in (0, 90, 180, 270):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            g += _pipe([(xf + 12, y + 40 * ca, z + 40 * sa), (xf + 12, y + (fr + 5) * ca, z + (fr + 5) * sa)], 2.5)
        guards.append(g)
        sq = P["FAN_D"] + 40
        f = _box(xf - 85, y, z, 10, sq, sq) - _box(xf - 85, y, z, 12, sq - 40, sq - 40)
        f = _fillet_try(f, _edges_par(f, Axis.X), [6.0, 3.0])
        f += _box(xf - 85, y, z + sq / 2 + 12, 40, sq + 20, 8)
        shframe.append(f)
        for i in range(5):
            zz = z - (sq - 40) / 2 + (i + 0.5) * (sq - 40) / 5
            louvers.append(Pos(xf - 88, y, zz) * Rot(0, 25, 0) * Box(2, sq - 44, (sq - 40) / 5 + 4))
    return (_comp(housing), _comp(blades), _comp(hubs), _comp(guards), _comp(shframe), _comp(louvers))


def _controller(P, D):
    xf = -D["out_l"] / 2
    cx, cy, cz = xf - 40, 860.0, 1150.0
    outer = _box(cx, cy, cz, 80, 200, 250)
    outer = _fillet_try(outer, _edges_par(outer, Axis.X), [10.0, 6.0])
    outer = _fillet_try(outer, _face_edges(outer, Axis.X, -1), [3.0, 1.5])
    xs = xf - 60                                            # lid parting plane
    body = outer & _box((xs + xf) / 2 + 0.5, cy, cz, xf - xs - 1, 220, 270)
    body -= _box(xs + 20, cy, cz, 50, 188, 238)
    lid = outer & _box((xf - 80 + xs) / 2 - 0.5, cy, cz, xs - (xf - 80) - 1, 220, 270)
    wz = cz + 10
    lid -= _box(xf - 70, cy, wz, 30, 130, 130)
    lid -= _box(xs - 4, cy, cz, 12, 188, 238)
    pane = _box(xf - 76, cy, wz, 2.0, 140, 140)
    pcb = _box(xf - 8, cy, cz, 3, 180, 220)
    chips = (_box(xf - 16, cy - 30, cz + 40, 12, 50, 26) + _box(xf - 13, cy + 45, cz + 30, 6, 22, 22)
             + _box(xf - 14, cy + 40, cz - 20, 8, 40, 16) + _box(xf - 14, cy - 40, cz - 30, 8, 24, 30))
    term = _box(xf - 16, cy, cz - 80, 14, 150, 18)
    for k in range(8):
        term -= _box(xf - 23.5, cy - 63 + 18 * k, cz - 76, 2, 7, 6)
    card = _box(xf - 12, cy + 60, cz + 70, 4, 26, 30)
    screws = _comp([_xcyl(xf - 80.6, cy + sy * 88, cz + sz * 113, 3.4, 1.2) for sy in (-1, 1) for sz in (-1, 1)])
    plate = _box(xf - 80.4, cy, cz + 97, 0.6, 120, 14)
    glands = []
    for dy in (-50, 0, 50):
        g = _zcyl(cx + 5, cy + dy, cz - 125 - 3, 11, 6) + _zcyl(cx + 5, cy + dy, cz - 125 - 11, 8, 10)
        glands.append(g + _zcyl(cx + 5, cy + dy, cz - 125 - 45, 4, 60))
    # three-colour mode lamp on top of the box, lit green (evaporative cooling mode)
    lx, ly, ltop = xf - 45, 790.0, cz + 125
    lamp_base = _zcyl(lx, ly, ltop + 6, 20, 12)
    lamp = _zcyl(lx, ly, ltop + 17, 16, 10) + (Pos(lx, ly, ltop + 22) * Sphere(16) & _box(lx, ly, ltop + 32, 40, 40, 20))
    # outside RH/T sensor in a stacked-plate radiation shield (model.py envelope 40 x 40 x 60 mm)
    sx, sy_, sz = xf - 60, 860.0, 1350.0
    sh = _zcyl(sx, sy_, sz + 26, 23, 6)
    sh = _fillet_try(sh, _face_edges(sh, Axis.Z, 1), [2.0, 1.0])
    for k in range(4):
        z = sz - 24 + 12 * k
        sh += _zcyl(sx, sy_, z, 22, 3) - _zcyl(sx, sy_, z, 9, 4)
    for k in range(3):
        a = 2 * math.pi * k / 3
        sh += _zcyl(sx + 15 * math.cos(a), sy_ + 15 * math.sin(a), sz, 2.0, 58)
    probe = _zcyl(sx, sy_, sz - 6, 6, 26)
    arm = _pipe([(xf - 1, sy_, sz + 38), (sx, sy_, sz + 38), (sx, sy_, sz + 29)], 4.5) + _box(xf - 2.5, sy_, sz + 38, 5, 36, 36)
    return (body, lid, pane, pcb, chips, term, card, screws, plate, _comp(glands), lamp_base, lamp, sh, probe, arm)


def _powerbox(P, D):
    xf = -D["out_l"] / 2
    cx, cy, cz = xf - 50, -860.0, 1150.0
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
    door = outer & _box((xf - 100 + xs) / 2 - 0.5, cy, cz, xs - (xf - 100) - 1, 240, 320)
    door -= _box(xf - 95, cy, cz + 70, 30, 140, 90)
    door -= _box(xs - 4, cy, cz, 12, 206, 286)
    pane = _box(xf - 97, cy, cz + 70, 2.0, 150, 100)
    ctrl = _box(xf - 30, cy, cz + 70, 50, 130, 80)
    ctrl = _fillet_try(ctrl, _edges_par(ctrl, Axis.X), [4.0, 2.0])
    lcd = _box(xf - 55.5, cy + 20, cz + 78, 1.0, 60, 26)
    led = _xcyl(xf - 56, cy - 40, cz + 78, 3.5, 2.0)
    batt = _box(xf - 35, cy, cz - 60, 70, 180, 110)
    batt = _fillet_try(batt, batt.edges(), [3.0, 1.5])
    hinges = _comp([_zcyl(xf - 101, cy - 108, cz + dz, 5, 50) for dz in (-90, 90)])
    hasp = _box(xf - 102, cy + 100, cz, 4, 16, 40) + _xcyl(xf - 106, cy + 100, cz, 5, 8)
    label = _box(xf - 100.4, cy, cz - 60, 0.6, 120, 50)
    ink = _box(xf - 100.8, cy, cz - 45, 0.4, 90, 10) + _box(xf - 100.8, cy, cz - 68, 0.4, 100, 5) \
        + _box(xf - 100.8, cy, cz - 80, 0.4, 70, 5)
    return body, hood, door, pane, ctrl, lcd, led, batt, hinges, hasp, label, ink


def _conduit(P, D):
    xf = -D["out_l"] / 2
    x = xf - 30
    run = _pipe([(x, -860.0, 1300.0), (x, -860.0, 2060.0), (x, 935.0, 2060.0), (x, 935.0, 1275.0)], 12)
    run += _pipe([(x, -860.0, 2060.0), (x, -860.0, D["ceil_top"] - 2)], 12)
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
    M = build_parts(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ---- structure (BOM 1 to 5)
    walls, plinth = _walls(P, D, M)
    add("Double brick walls and floor", walls, C_BRICK, "paper", 1, "shell", (0, 0, 0))
    add("Rendered plinth band", plinth, C_PLINTH, "paper", 1, "shell", (0, 0, 0))
    add("Timber lintels", _lintels(P, D), C_TIMBER, "wood", 1, "shell", (0, 0, 0))
    add("Dry rice husk cavity fill", M[2][1], C_FILL, "fabric", 2, "shell", (0, 0, 900))
    ceil = M[3][1]
    ceil = _fillet_try(ceil, _face_edges(ceil, Axis.Z, 1), [8.0, 4.0])
    add("Insulated ceiling, timber fascia", ceil, C_FASCIA, "wood", 3, "shell", (0, 0, 1900))
    sheet, frame, screws, posts, collars = _roof(P, D)
    ER = (0, 0, 2700)
    add("Corrugated galvanized roof sheet", sheet, C_GALV, "metal", 4, "shell", ER)
    add("Roof purlins and rafters, timber", frame, C_TIMBER, "wood", 4, "shell", ER)
    add("Roof screws with washers", screws, C_POST, "metal", 4, "shell", ER)
    add("Roof posts, galvanized steel", posts, C_POST, "metal", 4, "shell", ER)
    add("Post footing collars, concrete", collars, C_CONC, "paper", 4, "shell", ER)
    pf, pback, cells, bars, jb, legs = _panel(P, D)
    EP = (0, 0, 3500)
    add("Solar panel frame, aluminum", pf, C_ALU, "metal", 10, "shell", EP)
    add("Solar panel backsheet", pback, C_BACKSHEET, "plastic", 10, "shell", EP)
    add("Solar cells", cells, C_CELL, "screen", 10, "shell", EP)
    add("Solar cell busbars", bars, C_ALU, "metal", 10, "shell", EP)
    add("Panel junction box", jb, C_BLACK, "plastic", 10, "shell", EP)
    add("Panel mounting legs, aluminum", legs, C_ALU, "metal", 10, "shell", EP)
    leaf, seal, hw, sign, ink = _door(P, D)
    ED = (-2500, 0, 0)
    add("Insulated door leaf", leaf, C_ACCENT, "painted", 5, "shell", ED)
    add("Door rubber seal", seal, C_BLACK, "rubber", 5, "shell", (-2150, 0, 0))
    add("Door hinges and handle", hw, C_POST, "metal", 5, "shell", ED)
    add("Door sign", sign, C_LABEL, "paper", 5, "shell", ED)
    add("Door sign print", ink, C_DARK, "paper", 5, "shell", ED)

    # ---- racks and crates (BOM 12, 13); pulled out in front for the exploded view
    ERa, ERb = (-1250, -2600, 0), (1250, -3650, 0)
    crates, fills = _crates(P)
    for s, e, tag in ((-1, ERa, "near"), (1, ERb, "far")):
        add(f"Produce crates, {tag} rack", _comp([c for ss, c in crates if ss == s]), C_CRATE, "plastic", 13,
            "accessory", e)
        for z, col, what in zip(P["SHELVES"], (C_ONION, C_PEPPER, C_TOMATO), ("onions", "peppers", "tomatoes")):
            add(f"Produce, {what}, {tag} rack", _comp(fills[(s, z)]), col, "plastic", 13, "accessory", e)
    # split the racks by side so each moves with its crates
    racks = _racks(P, M)
    for s, e, tag in ((-1, ERa, "near"), (1, ERb, "far")):
        half = racks & _box(0, s * P["IN_W"] / 4, 1000, P["IN_L"], P["IN_W"] / 2, 2000)
        add(f"Shelving rack, slatted timber, {tag}", half, C_RACK, "wood", 12, "shell", e)

    # ---- cooling kit (BOM 6 to 9, 11, 14)
    frame6, fscr, media, header, gut, pad_x, hz, gz = _pad(P, D)
    add("Pad frame, aluminum", frame6, C_ALU, "metal", 6, "internal", (700, 0, 0))
    add("Pad frame screws", fscr, C_POST, "metal", 6, "internal", (760, 0, 0))
    add("Cellulose evaporative pad, 150 mm", media, C_PAD, "paper", 6, "internal", (1050, 0, 0))
    add("Drip header, PVC", header, C_PVC, "plastic", 6, "internal", (1050, 0, 300))
    add("Return gutter, galvanized", gut, C_GALV, "metal", 6, "internal", (1050, 0, -250))
    body, hoops, lid, fit, lab, feed, ret = _sump(P, D, pad_x, hz, gz)
    ES = (1700, -300, 0)
    add("Sump drum, 60 L", body, C_ACCENT, "plastic", 7, "internal", ES)
    add("Sump drum hoops", hoops, C_ACCENT, "plastic", 7, "internal", ES)
    add("Sump drum lid", lid, C_DARK, "plastic", 7, "internal", (1700, -300, 250))
    add("Pump and hose fittings", fit, C_BLACK, "plastic", 7, "internal", (1700, -300, 250))
    add("Sump drum label", lab, C_LABEL, "paper", 7, "internal", ES)
    add("Feed hose to header", feed, C_HOSE, "rubber", 7, "internal", (1350, -150, 150))
    add("Return hose from gutter", ret, C_HOSE, "rubber", 7, "internal", (1350, -150, -120))
    housing, blades, hubs, guards, shf, louv = _fans(P, D)
    EF = (-700, 0, 0)
    add("Fan housings", housing, C_DARK, "plastic", 8, "internal", EF)
    add("Fan blades", blades, C_BLACK, "plastic", 8, "internal", EF)
    add("Fan motor hubs", hubs, C_BLACK, "plastic", 8, "internal", EF)
    add("Fan finger guards", guards, C_POST, "metal", 8, "internal", (-450, 0, 0))
    add("Gravity shutter frames", shf, C_SHUTTER, "plastic", 8, "internal", (-1000, 0, 0))
    add("Gravity shutter louvers", louv, C_SHUTTER, "plastic", 8, "internal", (-1000, 0, 0))
    (cbody, clid, cpane, pcb, chips, term, card, cscr, plate, glands,
     lbase, lamp, shield, probe, arm) = _controller(P, D)
    EC, ECL = (-700, 300, -150), (-900, 300, -150)
    add("Controller enclosure, IP65", cbody, C_SHELL, "plastic", 9, "internal", EC)
    add("Controller lid frame", clid, C_SHELL2, "plastic", 9, "internal", ECL)
    add("Controller window, clear polycarbonate", cpane, C_WINDOW, "clear", 9, "internal", ECL)
    add("Controller lid screws", cscr, C_POST, "metal", 9, "internal", ECL)
    add("Controller name plate", plate, C_ACCENT, "painted", 9, "internal", ECL)
    add("Controller board", pcb, C_PCB, "plastic", 9, "internal", EC)
    add("Controller board components", chips, C_CHIP, "plastic", 9, "internal", EC)
    add("Fan and pump driver terminals", term, "#2E7D5B", "plastic", 9, "internal", EC)
    add("Memory card logger", card, C_POST, "metal", 9, "internal", EC)
    add("Controller cable glands and cables", glands, C_DARK, "rubber", 9, "internal", EC)
    add("Mode lamp base", lbase, C_DARK, "plastic", 9, "internal", EC)
    add("Mode lamp, green (lit)", lamp, C_LED_G, "emissive", 9, "internal", EC)
    add("Radiation shield, outside sensor", shield, "#F2F2EF", "plastic", 9, "internal", (-700, 300, 150))
    add("Outside RH/T sensor probe", probe, C_DARK, "plastic", 9, "internal", (-700, 300, 150))
    add("Radiation shield bracket", arm, C_POST, "metal", 9, "internal", (-700, 300, 150))
    (pbody, hood, pdoor, ppane, pctrl, lcd, led, batt, hinges, hasp, plab, pink) = _powerbox(P, D)
    EB, EBD = (-700, -300, -150), (-900, -300, -150)
    add("Power box, ventilated steel", pbody, C_SHELL2, "painted", 11, "internal", EB)
    add("Power box rain hood", hood, C_SHELL2, "painted", 11, "internal", (-700, -300, 0))
    add("Power box door", pdoor, C_SHELL2, "painted", 11, "internal", EBD)
    add("Power box window, clear", ppane, C_WINDOW, "clear", 11, "internal", EBD)
    add("Power box hinges and hasp", _comp([hinges, hasp]), C_POST, "metal", 11, "internal", EBD)
    add("Power box label", plab, C_LABEL, "paper", 11, "internal", EBD)
    add("Power box label print", pink, C_DARK, "paper", 11, "internal", EBD)
    add("PWM charge controller", pctrl, C_DARK, "plastic", 11, "internal", EB)
    add("Charge controller display (lit)", lcd, C_LCD, "emissive", 11, "internal", EB)
    add("Charging indicator, green (lit)", led, C_LED_G, "emissive", 11, "internal", EB)
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
