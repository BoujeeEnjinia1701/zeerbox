"""ZeerBox parametric model (build123d), TRL 3, constructable design (ZBX-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl, print key sizes
    python cad/src/model.py --check    run the constructability checks (overlaps, contacts, fixings)

Every component that is made, bought or fixed is modelled with the faces it sits on, so the
build plan pictures (cad/src/build_plan_media.py) and the checks below come from one source.
Coordinates in mm. X runs along the store (door at -X, pad at +X), Y across it, Z up, ground at
Z = 0. The storage room is centred on the origin in plan. Figures and checks are in ZBX-CAL-001
(python docs/04-calcs/sizing.py), which reads PARAMS and derived() from here.

PRELIMINARY, NOT FOR FABRICATION.
"""
import math
import sys
from pathlib import Path

# Top-level parameters (mm unless stated). Edit these, not the geometry below.
PARAMS = {
    # storage room, inside faces of the inner brick leaf
    "IN_L": 2400.0, "IN_W": 1500.0, "IN_H": 2000.0,
    "FLOOR": 100.0,            # brick floor on a sand bed over compacted ground; top of floor above ground
    "LEAF": 115.0,             # fired-brick leaf (wall material still open, ZBX-DDR-001 item 9)
    "CAV": 75.0,               # dry rice husk cavity fill (ZBX-DDR-002 item 12)
    "FILL": "rice husk",       # cavity fill: "rice husk" (decided), "dry sand" (fallback) or "wet sand" (TRL 3 v0.1)
    "CAP": 75.0,               # brick capping course over both leaves and the cavity at the wall top
    "FOOT_W": 450.0, "FOOT_T": 250.0,                   # concrete strip footing under the walls, top at ground
    # openings: door and pad sizes are the clear sizes inside the timber linings
    "DOOR_W": 800.0, "DOOR_H": 1800.0, "DOOR_T": 74.0,   # 50 mm insulation between 12 mm skins (ZBX-CAL-001 U value)
    "LINING": 20.0,            # treated board lining every reveal, closing the cavity
    "LINTEL_H": 100.0, "LINTEL_BEAR": 150.0,            # hardwood lintel per leaf over the door and pad openings
    "PAD_W": 600.0, "PAD_H": 500.0, "PAD_T": 150.0, "PAD_Z": 1250.0,  # 150 mm pad (ZBX-DDR-002 item 11); centre above ground
    # fans: two 250 mm fans in one plywood fan box in the ceiling, over the aisle at the door end (ZBX-DDR-003 C1)
    "FAN_D": 250.0, "FAN_X": -1000.0, "FAN_Y": 160.0,
    "FANBOX": (310.0, 640.0), "FANBOX_UP": 30.0, "PLY": 18.0,
    # ceiling: joists across the walls, insulation on cleats between them, boards on top
    "CEIL_T": 120.0,           # 100 mm joists + 20 mm boards
    "JOIST": (50.0, 100.0), "JOIST_X": (-1480.0, -1180.0, -820.0, -410.0, 0.0, 410.0, 820.0, 1180.0, 1480.0),
    "CLEAT": 25.0, "INS_T": 50.0, "DECK_T": 20.0,
    # shade roof
    "ROOF_CLEAR": 450.0,       # from the ceiling boards to the roof sheet
    "ROOF_L": 3900.0, "ROOF_W": 3000.0, "ROOF_PITCH_DEG": 4.0, "SHEET_T": 25.0,
    "POST_D": 90.0, "POST_X": 1850.0, "POST_Y": 1400.0, "POST_EMBED": 450.0, "CAP_PLATE": (150.0, 6.0),
    "FOOTING": 500.0, "FOOTING_DEPTH": 600.0,           # concrete post footing, square side and depth (CAL-001 section 7)
    "BEAM": (75.0, 150.0), "PURLIN": (50.0, 150.0), "PURLIN_Y": (-1400.0, -700.0, 0.0, 700.0, 1400.0),
    # racks and crates
    "RACK_L": 2200.0, "RACK_D": 450.0, "RACK_POST": 50.0, "RAIL": (50.0, 75.0), "SLAT": (95.0, 25.0), "SLATS": 15,
    "SHELVES": (300.0, 850.0, 1400.0),                 # shelf top heights above the floor
    "CRATE_L": 500.0, "CRATE_W": 350.0, "CRATE_H": 300.0, "CRATES_PER_SHELF": 4,
    # water
    "SUMP_D": 380.0, "SUMP_H": 600.0, "SUMP_XY": (1765.0, -750.0),   # about 68 L gross, 60 L working
    # solar (150 W panel, DDR-001 item 2) on two aluminium side frames
    "PANEL_L": 1480.0, "PANEL_W": 670.0, "PANEL_T": 35.0, "PANEL_TILT_DEG": 15.0,
    "PANEL_C": (0.0, -350.0, 250.0),                   # centre: x, y, height above the roof reference
    "MOUNT_X": 560.0, "ANGLE": (40.0, 4.0),
    # controller box on the front wall beside the door (clear-lid IP65 box): depth x width x height, centre y and z, wall
    "CTRL": (80.0, 200.0, 250.0), "CTRL_YZ": (860.0, 1150.0), "CTRL_WALL": 3.0,
    # three-color mode lamp on top of the box (ZBX-DEC-001, 2026-10-02): hole diameter, flange diameter and thickness,
    # dome diameter and height above the flange, offset of the lamp along the box toward the door (y)
    "LAMP": (22.0, 30.0, 3.0, 22.0, 20.0, -70.0),
    # outside sensor shield (ZBX-DEC-001, 2026-10-02): stacked round plates on a stud: plate diameter, number of plates,
    # plate thickness, plate pitch, height of the lowest plate, stud radius, centre distance from the wall, centre y
    "SHIELD": (46.0, 6, 2.0, 10.0, 1320.0, 3.0, 63.0, 860.0),
}

PROCESS = {   # how each component is made, for the constructability review (ZBX-DDR-003)
    "strip_footing": "cast concrete in a trench", "floor": "brick laid on a sand bed", "walls": "bricklaying",
    "fill": "poured dry husk with lime", "lintels": "sawn hardwood, built in", "door_lining": "sawn and screwed boards",
    "door_stops": "sawn bead, screwed", "door": "carpentry, plywood skins on a timber frame", "door_hinges": "bought butt hinges",
    "joists": "sawn timber with nailed cleats", "insulation": "cut board or bagged straw", "deck": "sawn boards nailed down",
    "fan_box": "plywood, cut and screwed", "fans": "bought", "post_footings": "cast concrete",
    "posts": "steel pipe with welded cap plate", "beams": "sawn timber", "purlins": "sawn timber",
    "sheet": "bought corrugated sheet, screwed", "mount": "aluminium angle and flat bar, cut and drilled",
    "panel": "bought", "pad_lining": "sawn boards, screwed", "pad_battens": "sawn timber, plugged to the wall",
    "pad_frame": "sawn boards, screwed", "pad_bars": "galvanised flat bar, drilled", "pad": "bought, cut to size",
    "header": "PVC pipe, drilled", "gutter": "bent galvanised sheet", "gutter_brackets": "bent galvanised strip",
    "sump": "bought drum, lid drilled", "hoses": "bought hose", "controller": "bought box, wired",
    "sensor": "bought plate shield on a bent strip arm", "mode_lamp": "bought lamp, fitted in a drilled hole", "power_box": "bought box, wired", "racks": "sawn timber, screwed",
    "rack_brackets": "bought steel angle", "crates": "user supplied",
}


def derived(p=PARAMS):
    """Key dimensions and quantities derived from the parameters (mm, m2, m3)."""
    wall = 2 * p["LEAF"] + p["CAV"]
    out_l, out_w = p["IN_L"] + 2 * wall, p["IN_W"] + 2 * wall
    top = p["FLOOR"] + p["IN_H"]
    ceil_top = top + p["CEIL_T"]
    roof_z = ceil_top + p["ROOF_CLEAR"]
    aisle = p["IN_W"] - 2 * p["RACK_D"]
    fan_area = 2 * math.pi * (p["FAN_D"] / 2) ** 2 / 1e6
    lin = p["LINING"]
    return {
        "wall": wall, "out_l": out_l, "out_w": out_w, "top": top, "ceil_top": ceil_top,
        "roof_z": roof_z, "aisle": aisle,
        "room_volume_m3": p["IN_L"] * p["IN_W"] * p["IN_H"] / 1e9,
        "pad_area_m2": p["PAD_W"] * p["PAD_H"] / 1e6,
        "fan_area_m2": fan_area,
        "door_area_m2": p["DOOR_W"] * p["DOOR_H"] / 1e6,
        "door_open": (p["DOOR_W"] + 2 * lin, p["DOOR_H"] + lin),          # brick opening, from the floor top
        "pad_open": (p["PAD_W"] + 2 * lin, p["PAD_H"] + 2 * lin),
        "door_open_m2": (p["DOOR_W"] + 2 * lin) * (p["DOOR_H"] + lin) / 1e6,
        "pad_open_m2": (p["PAD_W"] + 2 * lin) * (p["PAD_H"] + 2 * lin) / 1e6,
        "crates": 2 * len(p["SHELVES"]) * p["CRATES_PER_SHELF"],
        "top_shelf_m": max(p["SHELVES"]) / 1000,
        "roof_area_m2": p["ROOF_L"] * p["ROOF_W"] / 1e6,
    }


# ----------------------------------------------------------------------------- helpers
def _bx(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def _tube(a, b, r):
    from build123d import Plane, Solid, Vector
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _hose(pts, r):
    """A hose along a polyline, as one solid (tubes joined by spheres at the bends)."""
    from build123d import Pos, Sphere
    out = _tube(pts[0], pts[1], r)
    for a, b in zip(pts[1:-1], pts[2:]):
        out = out + Pos(*a) * Sphere(r) + _tube(a, b, r)
    return out


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def roof_frame(p=PARAMS):
    """Location of the roof sheet's mid-plane: origin over the store centre at roof_z, tilted by the pitch about X."""
    from build123d import Pos, Rot
    return Pos(0, 0, derived(p)["roof_z"]) * Rot(p["ROOF_PITCH_DEG"], 0, 0)


def roof_local_y(yw, zl, p=PARAMS):
    """Local y in the roof frame of the point with world y = yw and local z = zl."""
    t = math.radians(p["ROOF_PITCH_DEG"])
    return (yw + zl * math.sin(t)) / math.cos(t)


def roof_world_z(yw, zl, p=PARAMS):
    t = math.radians(p["ROOF_PITCH_DEG"])
    yl = roof_local_y(yw, zl, p)
    return derived(p)["roof_z"] + yl * math.sin(t) + zl * math.cos(t)


def panel_frame(p=PARAMS):
    from build123d import Pos, Rot
    cx, cy, dz = p["PANEL_C"]
    return Pos(cx, cy, derived(p)["roof_z"] + dz) * Rot(-p["PANEL_TILT_DEG"], 0, 0)


def panel_point(x, yl, zl, p=PARAMS):
    """World point of panel-local (x, yl, zl)."""
    cx, cy, dz = p["PANEL_C"]
    t = math.radians(-p["PANEL_TILT_DEG"])
    return (cx + x, cy + yl * math.cos(t) - zl * math.sin(t), derived(p)["roof_z"] + dz + yl * math.sin(t) + zl * math.cos(t))


# ----------------------------------------------------------------------------- components
def build_components(p=PARAMS):
    """Every component as {key: (name, [solids])}, in build order."""
    from build123d import Box, Cylinder, Pos, Rot
    d = derived(p)
    wall, out_l, out_w, top = d["wall"], d["out_l"], d["out_w"], d["top"]
    xf, xb = -out_l / 2, out_l / 2
    leaf, fl, cav, lin = p["LEAF"], p["FLOOR"], p["CAV"], p["LINING"]
    hl, hw = p["IN_L"] / 2, p["IN_W"] / 2
    C = {}

    # 15 concrete strip footing under both leaves, top at ground level
    fw, ft = p["FOOT_W"], p["FOOT_T"]
    ov = (fw - wall) / 2
    ring = _bx(-out_l / 2 - ov, out_l / 2 + ov, -out_w / 2 - ov, out_w / 2 + ov, -ft, 0) \
        - _bx(-out_l / 2 + wall + ov, out_l / 2 - wall - ov, -out_w / 2 + wall + ov, out_w / 2 - wall - ov, -ft - 1, 1)
    C["strip_footing"] = ("Wall strip footing", [ring])

    # openings through the wall (brick sizes) and the lintels over them
    dw, dh = d["door_open"]
    pw, ph = d["pad_open"]
    pz = p["PAD_Z"]
    door_cut = _bx(xf - 10, xf + wall + 10, -dw / 2, dw / 2, fl, fl + dh)
    pad_cut = _bx(xb - wall - 10, xb + 10, -pw / 2, pw / 2, pz - ph / 2, pz + ph / 2)
    lh, lb = p["LINTEL_H"], p["LINTEL_BEAR"]
    lintels = []
    for x0 in (xf, xf + leaf + cav):                  # door: outer leaf, inner leaf
        lintels.append(_bx(x0, x0 + leaf, -dw / 2 - lb, dw / 2 + lb, fl + dh, fl + dh + lh))
    for x1 in (xb, xb - leaf - cav):                  # pad: outer leaf, inner leaf
        lintels.append(_bx(x1 - leaf, x1, -pw / 2 - lb, pw / 2 + lb, pz + ph / 2, pz + ph / 2 + lh))

    # 1 floor and walls (two leaves with a brick capping course over the cavity)
    C["floor"] = ("Brick floor on a sand bed", [_bx(-hl, hl, -hw, hw, 0, fl)])
    outer = _bx(-out_l / 2, out_l / 2, -out_w / 2, out_w / 2, 0, top) - _bx(-out_l / 2 + leaf, out_l / 2 - leaf, -out_w / 2 + leaf, out_w / 2 - leaf, -1, top + 1)
    inner = _bx(-hl - leaf, hl + leaf, -hw - leaf, hw + leaf, 0, top) - _bx(-hl, hl, -hw, hw, -1, top + 1)
    cap = _bx(-out_l / 2 + leaf, out_l / 2 - leaf, -out_w / 2 + leaf, out_w / 2 - leaf, top - p["CAP"], top) - _bx(-hl - leaf, hl + leaf, -hw - leaf, hw + leaf, top - p["CAP"] - 1, top + 1)
    walls = outer + inner + cap - door_cut - pad_cut
    for l_ in lintels:
        walls = walls - l_
    C["walls"] = ("Double brick walls", [walls])

    # 2 dry rice husk fill, from the damp-proof course at ground level up to the capping course
    fill = (_bx(-out_l / 2 + leaf, out_l / 2 - leaf, -out_w / 2 + leaf, out_w / 2 - leaf, 0, top - p["CAP"])
            - _bx(-hl - leaf, hl + leaf, -hw - leaf, hw + leaf, -1, top) - door_cut - pad_cut)
    C["fill"] = ("Dry rice husk cavity fill", [fill])
    C["lintels"] = ("Lintels over the door and pad openings", lintels)

    # 16 door lining (jambs and head, full wall depth), stop beads, door leaf
    jy = p["DOOR_W"] / 2
    lining = [_bx(xf, xf + wall, s * jy, s * (jy + lin), fl, fl + dh) for s in (-1, 1)]
    lining.append(_bx(xf, xf + wall, -jy, jy, fl + p["DOOR_H"], fl + dh))
    C["door_lining"] = ("Door lining", lining)
    sx0 = xf + 8 + p["DOOR_T"] + 2
    sx1 = sx0 + 40
    stops = [_bx(sx0, sx1, s * (jy - 20), s * jy, fl, fl + p["DOOR_H"]) for s in (-1, 1)]
    stops.append(_bx(sx0, sx1, -(jy - 20), jy - 20, fl + p["DOOR_H"] - 20, fl + p["DOOR_H"]))
    C["door_stops"] = ("Door stop beads with seal", stops)
    hinges = [_bx(xf + 8, xf + 40, -jy, -jy + 3, z - 50, z + 50) for z in (fl + 250, fl + 900, fl + 1550)]
    C["door"] = ("Insulated door", [_bx(xf + 8, xf + 8 + p["DOOR_T"], -jy + 3, jy - 3, fl + 5, fl + p["DOOR_H"] - 3)])
    C["door_hinges"] = ("Door hinges (3)", hinges)

    # 3 ceiling: joists with cleats, insulation between, boards on top
    jw, jh = p["JOIST"]
    cl, it, dt = p["CLEAT"], p["INS_T"], p["DECK_T"]
    bx, by = p["FANBOX"]
    fx = p["FAN_X"]
    fb_cut = _bx(fx - bx / 2, fx + bx / 2, -by / 2, by / 2, top - 1, top + jh + dt + 1)
    joists, ins = [], []
    xs = sorted(p["JOIST_X"])
    for x in xs:
        j = _bx(x - jw / 2, x + jw / 2, -out_w / 2, out_w / 2, top, top + jh)
        for s in (-1, 1):
            if (s < 0 and x == xs[0]) or (s > 0 and x == xs[-1]):
                continue
            xc = x + s * jw / 2
            j = j + (_bx(min(xc, xc + s * cl), max(xc, xc + s * cl), -out_w / 2, out_w / 2, top, top + cl) - fb_cut)
        joists.append(j)
    for a, b in zip(xs[:-1], xs[1:]):
        ins.append(_bx(a + jw / 2, b - jw / 2, -out_w / 2, out_w / 2, top + cl, top + cl + it) - fb_cut)
    C["joists"] = ("Ceiling joists with cleats", joists)
    C["insulation"] = ("Ceiling insulation", ins)
    C["deck"] = ("Ceiling boards", [_bx(-out_l / 2, out_l / 2, -out_w / 2, out_w / 2, top + jh, top + jh + dt) - fb_cut])

    # 16 fan box: plywood tube between two joists, top plate with two fan holes
    ply, up = p["PLY"], p["FANBOX_UP"]
    zt = top + jh + dt + up
    box = _bx(fx - bx / 2, fx + bx / 2, -by / 2, by / 2, top, zt) - _bx(fx - bx / 2 + ply, fx + bx / 2 - ply, -by / 2 + ply, by / 2 - ply, top - 1, zt + 1)
    plate = _bx(fx - bx / 2, fx + bx / 2, -by / 2, by / 2, zt, zt + ply)
    fr = p["FAN_D"] / 2
    for s in (-1, 1):
        plate = plate - Pos(fx, s * p["FAN_Y"], zt + ply / 2) * Cylinder(fr, ply + 2)
    C["fan_box"] = ("Fan box", [box, plate])

    # 8 fans on the plate, gravity shutters on top
    fans = []
    for s in (-1, 1):
        y = s * p["FAN_Y"]
        z0 = zt + ply
        hous = _bx(fx - 137, fx + 137, y - 137, y + 137, z0, z0 + 90) - Pos(fx, y, z0 + 45) * Cylinder(fr - 3, 92)
        hub = Pos(fx, y, z0 + 45) * Cylinder(45, 80)
        shutter = _bx(fx - 140, fx + 140, y - 140, y + 140, z0 + 90, z0 + 120) - _bx(fx - 125, fx + 125, y - 125, y + 125, z0 + 89, z0 + 110)
        fans += [hous + hub, shutter]
    C["fans"] = ("Exhaust fans with shutters (pair)", fans)

    # 4 post footings and posts (steel pipe with a welded cap plate, square to the roof slope)
    R = roof_frame(p)
    sh_t = p["SHEET_T"]
    pu_w, pu_h = p["PURLIN"]
    be_w, be_h = p["BEAM"]
    z_pu = (-sh_t / 2 - pu_h, -sh_t / 2)
    z_be = (z_pu[0] - be_h, z_pu[0])
    cp, ct = p["CAP_PLATE"]
    fs, fd = p["FOOTING"], p["FOOTING_DEPTH"]
    px, py = p["POST_X"], p["POST_Y"]
    footings, posts = [], []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * px, sy * py
            footings.append(_bx(x - fs / 2, x + fs / 2, y - fs / 2, y + fs / 2, -fd, 0))
            yl = roof_local_y(y, z_be[0] - ct / 2, p)
            plate = R * Pos(x, yl, z_be[0] - ct / 2) * Box(cp, cp, ct)
            ztop = roof_world_z(y, z_be[0] - ct, p) - 4
            bar = Pos(x, y, -p["POST_EMBED"] + 50) * Rot(0, 90, 0) * Cylinder(6, 200)      # anchor bar through the pipe foot
            posts.append(plate + bar + Pos(x, y, (ztop - p["POST_EMBED"]) / 2) * Cylinder(p["POST_D"] / 2, ztop + p["POST_EMBED"]))
    C["post_footings"] = ("Post footings", footings)
    C["posts"] = ("Roof posts with cap plates", posts)

    # 17 roof framing: beams on the post lines, purlins on the beams
    L, W = p["ROOF_L"], p["ROOF_W"]
    beams = [R * _bx(sx * px - be_w / 2, sx * px + be_w / 2, -W / 2 + 30, W / 2 - 30, *z_be) for sx in (-1, 1)]
    purlins = [R * _bx(-L / 2 + 50, L / 2 - 50, y - pu_w / 2, y + pu_w / 2, *z_pu) for y in p["PURLIN_Y"]]
    C["beams"] = ("Roof beams", beams)
    C["purlins"] = ("Purlins", purlins)
    C["sheet"] = ("Corrugated roof sheets", [R * Box(L, W, sh_t)])

    # 18 panel mount: base rail on the sheet, two flat-bar legs, top rail under the panel (each side)
    a, t = p["ANGLE"]
    mx = p["MOUNT_X"]
    PW = p["PANEL_W"]
    PF = panel_frame(p)
    mount = []
    for s in (-1, 1):
        x0 = s * mx
        xo = (x0, x0 + s * a) if s > 0 else (x0 + s * a, x0)
        xv = (x0, x0 + s * t) if s > 0 else (x0 + s * t, x0)
        y0, y1 = p["PURLIN_Y"][1] - 60, p["PURLIN_Y"][2] + 60
        base = R * (_bx(*xo, y0, y1, sh_t / 2, sh_t / 2 + t) + _bx(*xv, y0, y1, sh_t / 2, sh_t / 2 + a))
        rail = PF * (_bx(*xo, -PW / 2, PW / 2, -p["PANEL_T"] / 2 - t, -p["PANEL_T"] / 2)
                     + _bx(*xv, -PW / 2, PW / 2, -p["PANEL_T"] / 2 - a, -p["PANEL_T"] / 2))
        mount += [base, rail]
        xl = (x0 - s * t, x0) if s > 0 else (x0, x0 - s * t)
        for yl in (-PW / 2 + 25, PW / 2 - 25):
            _, yw, zw = panel_point(x0, yl, -p["PANEL_T"] / 2, p)
            zb = roof_world_z(yw, sh_t / 2, p) + 2
            mount.append(_bx(*xl, yw - a / 2, yw + a / 2, zb, zw - 6))
    C["mount"] = ("Panel mounting frames", mount)
    C["panel"] = ("Solar panel, 150 W", [PF * Box(p["PANEL_L"], PW, p["PANEL_T"])])

    # 6 pad: reveal lining, wall battens, frame (sides, top), bottom and front bars, pad, header, gutter
    PWc, PHc, PT = p["PAD_W"], p["PAD_H"], p["PAD_T"]
    zb_, zt_ = pz - PHc / 2, pz + PHc / 2
    padl = [_bx(xb - wall, xb, s * PWc / 2, s * (PWc / 2 + lin), zb_ - lin, zt_ + lin) for s in (-1, 1)]
    padl += [_bx(xb - wall, xb, -PWc / 2, PWc / 2, zt_, zt_ + lin), _bx(xb - wall, xb, -PWc / 2, PWc / 2, zb_ - lin, zb_)]
    C["pad_lining"] = ("Pad opening lining", padl)
    fdp, bt = PT + 10, 25.0
    ftop = zt_ + 60 + bt
    C["pad_battens"] = ("Pad frame battens", [_bx(xb, xb + 50, s * (PWc / 2 + bt), s * (PWc / 2 + bt + 25), zb_, ftop) for s in (-1, 1)])
    hz, hr = zt_ + 16, 17.0
    hdr_cut = Pos(xb + PT / 2, 0, hz) * Rot(90, 0, 0) * Cylinder(hr, PWc + 200)
    sides = [_bx(xb, xb + fdp, s * PWc / 2, s * (PWc / 2 + bt), zb_, ftop) - hdr_cut for s in (-1, 1)]
    C["pad_frame"] = ("Pad frame", sides + [_bx(xb, xb + fdp, -PWc / 2, PWc / 2, ftop - bt, ftop)])
    bars = [_bx(xb + c - 15, xb + c + 15, -PWc / 2 - bt, PWc / 2 + bt, zb_ - 3, zb_) for c in (35, PT - 35)]
    bars += [_bx(xb + fdp, xb + fdp + 3, -PWc / 2 - bt, PWc / 2 + bt, z - 15, z + 15) for z in (pz - 100, pz + 100)]
    C["pad_bars"] = ("Pad support and retaining bars", bars)
    C["pad"] = ("Cellulose pad", [_bx(xb, xb + PT, -PWc / 2, PWc / 2, zb_, zt_)])
    h_y0, h_y1 = -PWc / 2 - 100, PWc / 2 + 40
    C["header"] = ("Drip header", [Pos(xb + PT / 2, (h_y0 + h_y1) / 2, hz) * Rot(90, 0, 0) * Cylinder(16, h_y1 - h_y0)])
    g = (xb + 10, xb + 180, -PWc / 2 - 120, PWc / 2 + 60, zb_ - 80, zb_ - 20)
    gut = _bx(*g) - _bx(g[0] + 2, g[1] - 2, g[2] + 2, g[3] - 2, g[4] + 2, g[5] + 1)
    spig = (xb + 95, g[2] + 40)
    gut = gut + Pos(spig[0], spig[1], g[4] - 20) * (Cylinder(16, 40) - Cylinder(13, 42))
    C["gutter"] = ("Return gutter", [gut])
    C["gutter_brackets"] = ("Gutter brackets", [_bx(xb, xb + 3, y - 20, y + 20, g[4] - 20, g[5]) + _bx(xb, g[1], y - 20, y + 20, g[4] - 3, g[4])
                                                for y in (-250.0, 250.0)])

    # 7 sump drum with lid, feed and return hoses
    sx_, sy_ = p["SUMP_XY"]
    dr, dh_ = p["SUMP_D"] / 2, p["SUMP_H"]
    C["sump"] = ("Sump drum with lid and pump", [Pos(sx_, sy_, dh_ / 2) * Cylinder(dr, dh_)])
    feed = [(sx_, sy_ - 50, dh_), (sx_, sy_ - 50, hz), (xb + PT / 2, h_y0 - 60, hz), (xb + PT / 2, h_y0, hz)]
    ret = [(spig[0], spig[1], g[4] - 40), (spig[0], spig[1], 700), (sx_, sy_ + 50, 700), (sx_, sy_ + 50, dh_)]
    hoses = [_hose(feed, 12), _hose(ret, 16)]
    C["hoses"] = ("Feed and return hoses", hoses)

    # 9 controller and outside sensor; 11 power box; on the front wall beside the door
    from build123d import Cylinder, Pos, Sphere
    cd_, cw_, ch_ = p["CTRL"]
    cy_, cz_ = p["CTRL_YZ"]
    cwall = p["CTRL_WALL"]
    z0c, z1c = cz_ - ch_ / 2, cz_ + ch_ / 2
    lh, lfl, lft, ldome, ldh, ldy = p["LAMP"]
    lx, ly = xf - cd_ / 2, cy_ + ldy
    ctrl = (_bx(xf - cd_, xf, cy_ - cw_ / 2, cy_ + cw_ / 2, z0c, z1c)
            - _bx(xf - cd_ + cwall, xf - cwall, cy_ - cw_ / 2 + cwall, cy_ + cw_ / 2 - cwall, z0c + cwall, z1c - cwall)
            - Pos(lx, ly, z1c - cwall / 2) * Cylinder(lh / 2, cwall + 2))
    C["controller"] = ("Controller box (clear lid, hole for the mode lamp)", [ctrl])
    lamp = (Pos(lx, ly, z1c + lft / 2) * Cylinder(lfl / 2, lft) + Pos(lx, ly, z1c - (cwall + 3) / 2) * Cylinder(lh / 2 - 0.5, cwall + 3 + 0.01)
            + Pos(lx, ly, z1c + lft + (ldh - ldome / 2) / 2) * Cylinder(ldome / 2, ldh - ldome / 2)
            + Pos(lx, ly, z1c + lft + ldh - ldome / 2) * Sphere(ldome / 2))
    C["mode_lamp"] = ("Three-color mode lamp", [lamp])
    sd, sn, st_, sp_, sz0, sr_, sdx, sy0 = p["SHIELD"]
    scx = xf - sdx
    zt = sz0 + sp_ * (sn - 1) + st_
    sens = _bx(scx, xf, sy0 - 10, sy0 + 10, 1345, 1355) + Pos(scx, sy0, (sz0 + zt) / 2) * Cylinder(sr_, zt - sz0)
    for k in range(sn):
        sens = sens + Pos(scx, sy0, sz0 + sp_ * k + st_ / 2) * Cylinder(sd / 2, st_)
    C["sensor"] = ("Outside sensor and plate shield", [sens])
    C["power_box"] = ("Power box", [_bx(xf - 100, xf, -970, -750, 1000, 1300)])

    # 12 racks: posts, rails on the inside faces of the posts, slats across the rails; wall brackets
    rl, rd, rp = p["RACK_L"], p["RACK_D"], p["RACK_POST"]
    rw, rh = p["RAIL"]
    sw, st = p["SLAT"]
    rack_h = max(p["SHELVES"]) + 350
    racks, brackets = [], []
    for s in (-1, 1):
        yc = s * (hw - rd / 2)
        yi = rd / 2 - rp                      # post inside face from the rack centre line
        pcs = []
        for x in (-rl / 2 + rp / 2, 0, rl / 2 - rp / 2):
            for sy in (-1, 1):
                pcs.append(_bx(x - rp / 2, x + rp / 2, yc + sy * yi, yc + sy * (yi + rp), fl, fl + rack_h))
        for z in p["SHELVES"]:
            zs = fl + z
            for sy in (-1, 1):
                pcs.append(_bx(-rl / 2, rl / 2, yc + sy * (yi - rw), yc + sy * yi, zs - st - rh, zs - st))
            pitch = (rl - 2 * rp - sw) / (p["SLATS"] - 1)
            for k in range(p["SLATS"]):
                x = -rl / 2 + rp + sw / 2 + k * pitch
                pcs.append(_bx(x - sw / 2, x + sw / 2, yc - yi, yc + yi, zs - st, zs))
        racks.append(pcs)
        yw_ = s * hw
        for x in (-rl / 2, rl / 2):           # the outer end faces of the two end posts
            brackets.append(_rack_bracket(x, 1 if x > 0 else -1, s * hw, s, fl + rack_h))
    C["racks"] = ("Shelving racks", [q for r in racks for q in r])
    C["rack_brackets"] = ("Rack wall brackets", brackets)

    # 13 crates
    n, cl_ = p["CRATES_PER_SHELF"], p["CRATE_L"]
    crates = []
    for s in (-1, 1):
        yc = s * (hw - rd / 2)
        for z in p["SHELVES"]:
            for k in range(n):
                x = -(n - 1) * cl_ / 2 + k * cl_
                crates.append(_bx(x - cl_ / 2 + 15, x + cl_ / 2 - 15, yc - p["CRATE_W"] / 2 + 5, yc + p["CRATE_W"] / 2 - 5, fl + z, fl + z + p["CRATE_H"] - 10))
    C["crates"] = ("Produce crates (user supplied)", crates)
    return C


def _rack_bracket(x, xo, yw, s, ztop):
    """Steel angle 40 x 40 x 3 at the top of an end post: one flange on the post's outer end face,
    one on the wall. x is the post's outer end face, xo the outward direction, yw the wall face."""
    x0, x1 = sorted((x, x + xo * 3))
    a0, a1 = sorted((x, x + xo * 40))
    y0, y1 = sorted((yw, yw - s * 40))
    w0, w1 = sorted((yw, yw - s * 3))
    return _bx(x0, x1, y0, y1, ztop - 60, ztop - 10) + _bx(a0, a1, w0, w1, ztop - 60, ztop - 10)


BOM_LINES = {   # bom line: (name, component keys)
    1: ("Double brick walls, floor and lintels", ("floor", "walls", "lintels")),
    2: ("Dry rice husk cavity fill", ("fill",)),
    3: ("Insulated ceiling", ("joists", "insulation", "deck")),
    4: ("Shade roof: sheets, posts and footings", ("post_footings", "posts", "sheet")),
    5: ("Insulated door", ("door", "door_hinges")),
    6: ("Cellulose pad, frame, header, gutter", ("pad_lining", "pad_battens", "pad_frame", "pad_bars", "pad", "header", "gutter", "gutter_brackets")),
    7: ("Sump drum, 12 V pump and hoses", ("sump", "hoses")),
    8: ("Exhaust fans, 12 V DC (pair)", ("fans",)),
    9: ("Controller and RH/T sensors", ("controller", "sensor", "mode_lamp")),
    10: ("Solar panel, 150 W", ("panel",)),
    11: ("Power box: charger, LiFePO4, fuse", ("power_box",)),
    12: ("Shelving racks", ("racks", "rack_brackets")),
    13: ("Produce crates (user supplied)", ("crates",)),
    15: ("Wall strip footing", ("strip_footing",)),
    16: ("Door lining, stops and fan box", ("door_lining", "door_stops", "fan_box")),
    17: ("Roof beams and purlins", ("beams", "purlins")),
    18: ("Panel mounting frames", ("mount",)),
}


def shape_of(pieces):
    from build123d import Compound
    return pieces[0] if len(pieces) == 1 else Compound(pieces)


def build_parts(p=PARAMS, components=None):
    """Return {bom_no: (name, shape)} for the modelled BOM lines (line 14, wiring and plumbing, is not modelled)."""
    C = components or build_components(p)
    return {k: (name, shape_of([s for key in keys for s in C[key][1]])) for k, (name, keys) in BOM_LINES.items()}


UNITS = {
    "zeerbox-structure": (1, 2, 3, 4, 5, 12, 15, 16, 17),     # built by the mason and carpenter
    "zeerbox-cooling-kit": (6, 7, 8, 9, 10, 11, 18),          # the equipment kit (value-engineering target, DDR-001 item 1)
}


def assembly(parts=None, include_crates=True):
    from build123d import Compound
    parts = parts or build_parts()
    return Compound([parts[k][1] for k in sorted(parts) if include_crates or k != 13])


# ----------------------------------------------------------------------------- checks
# pairs that are meant to share volume: a post cast into its footing
ALLOWED_OVERLAP = {("post_footings", "posts")}
# (a, b, what) pairs that must touch (gap 0.5 mm or less): every joint in the build plan
CONTACTS = [
    ("strip_footing", "walls", "walls stand on the strip footing"),
    ("walls", "floor", "floor laid against the inner leaf"),
    ("walls", "lintels", "lintels bed on the brick piers"),
    ("fill", "walls", "fill held between the leaves"),
    ("fill", "strip_footing", "fill sits on the damp-proof course over the footing"),
    ("door_lining", "walls", "door lining screwed to the reveal"),
    ("door_lining", "lintels", "door lining head under the lintels"),
    ("door_stops", "door_lining", "stop beads screwed to the lining"),
    ("door_hinges", "door_lining", "hinges screwed to the lining"),
    ("door_hinges", "door", "hinges screwed to the door edge"),
    ("joists", "walls", "joists bear on the wall top"),
    ("insulation", "joists", "insulation rests on the cleats"),
    ("deck", "joists", "boards nailed to the joists"),
    ("fan_box", "joists", "fan box screwed to two joists"),
    ("fans", "fan_box", "fans screwed to the fan box plate"),
    ("posts", "beams", "beams bolted to the post cap plates"),
    ("beams", "purlins", "purlins tied down to the beams"),
    ("purlins", "sheet", "sheets screwed to the purlins"),
    ("mount", "sheet", "base rails screwed through the sheet"),
    ("mount", "panel", "panel bolted to the top rails"),
    ("pad_lining", "walls", "pad lining screwed to the reveal"),
    ("pad_lining", "lintels", "pad lining head under the lintels"),
    ("pad_battens", "walls", "battens plugged to the wall"),
    ("pad_frame", "pad_battens", "frame sides screwed to the battens"),
    ("pad_bars", "pad_frame", "bars screwed to the frame sides"),
    ("pad", "pad_bars", "pad rests on the bottom bars"),
    ("header", "pad", "header lies on the pad"),
    ("gutter_brackets", "walls", "gutter brackets screwed to the wall"),
    ("gutter", "gutter_brackets", "gutter sits on its brackets"),
    ("hoses", "sump", "hoses through the drum lid"),
    ("hoses", "header", "feed hose on the header inlet"),
    ("hoses", "gutter", "return hose on the gutter outlet"),
    ("controller", "walls", "controller box screwed to the wall"),
    ("sensor", "walls", "sensor arm screwed to the wall"),
    ("mode_lamp", "controller", "lamp flange on the box top, its body through the hole"),
    ("power_box", "walls", "power box screwed to the wall"),
    ("racks", "floor", "racks stand on the floor"),
    ("rack_brackets", "racks", "brackets screwed to the end posts"),
    ("rack_brackets", "walls", "brackets screwed to the wall"),
    ("crates", "racks", "crates stand on the slats"),
]
# (a, b, minimum gap mm, what): parts that must stay apart
CLEARANCES = [
    ("fans", "purlins", 100.0, "fan shutters clear of the roof framing"),
    ("door", "door_lining", 2.0, "door leaf free in its lining"),
    ("crates", "fan_box", 200.0, "air path from the top crates to the fans"),
    ("racks", "door", 50.0, "racks clear of the door"),
    ("post_footings", "strip_footing", 15.0, "post footings apart from the wall footing"),
    ("sump", "posts", 300.0, "sump clear of the roof post"),
    ("pad", "gutter", 5.0, "pad drips into the gutter"),
    ("mode_lamp", "sensor", 15.0, "lamp clear of the sensor shield"),
    ("mode_lamp", "door_lining", 100.0, "lamp clear of the door lining"),
]


def check(p=PARAMS, verbose=True):
    """Constructability checks: no unintended overlaps, every joint touches, the clearances hold."""
    C = build_components(p)
    keys = list(C)
    fails, n = [], 0

    def bb_hit(a, b, pad=0.0):
        A, B = a.bounding_box(), b.bounding_box()
        return not (A.max.X + pad < B.min.X or B.max.X + pad < A.min.X or A.max.Y + pad < B.min.Y or B.max.Y + pad < A.min.Y
                    or A.max.Z + pad < B.min.Z or B.max.Z + pad < A.min.Z)
    # 1. overlaps between components, and between the pieces of one component
    for i, ka in enumerate(keys):
        for kb in keys[i + 1:]:
            if (ka, kb) in ALLOWED_OVERLAP or (kb, ka) in ALLOWED_OVERLAP:
                continue
            n += 1
            for sa in C[ka][1]:
                for sb in C[kb][1]:
                    if bb_hit(sa, sb):
                        v = (sa & sb).volume
                        if v > 1.0:
                            fails.append(f"overlap {ka} / {kb}: {v / 1000:.1f} cm3")
    for k in keys:
        ps = C[k][1]
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                n += 1
                if bb_hit(ps[i], ps[j]) and (ps[i] & ps[j]).volume > 1.0:
                    fails.append(f"overlap within {k}: pieces {i} and {j}")
    # 2. contacts
    for a, b, what in CONTACTS:
        n += 1
        dmin = min(sa.distance_to(sb) for sa in C[a][1] for sb in C[b][1] if bb_hit(sa, sb, 5.0)) if any(
            bb_hit(sa, sb, 5.0) for sa in C[a][1] for sb in C[b][1]) else 1e9
        if dmin > 0.5:
            fails.append(f"no contact {a} / {b} ({what}): gap {dmin:.1f} mm")
    # 3. every piece of a fixed component touches something else (nothing floats)
    for k in keys:
        if k in ("strip_footing", "post_footings", "floor"):
            continue
        others = [s for kk in keys if kk != k for s in C[kk][1]]
        for i, s in enumerate(C[k][1]):
            n += 1
            own = [q for j, q in enumerate(C[k][1]) if j != i]
            near = [q for q in others + own if bb_hit(s, q, 1.0)]
            if not near or min(s.distance_to(q) for q in near) > 0.5:
                fails.append(f"floating: {k} piece {i}")
    # 4. clearances
    for a, b, gmin, what in CLEARANCES:
        n += 1
        g = min(sa.distance_to(sb) for sa in C[a][1] for sb in C[b][1])
        if g < gmin:
            fails.append(f"clearance {a} / {b} ({what}): {g:.1f} mm, need {gmin:.0f}")
    if verbose:
        print(f"{n} constructability checks, {len(fails)} failed")
        for f in fails:
            print("  FAIL", f)
    return n, fails


if __name__ == "__main__":
    if "--check" in sys.argv:
        n, fails = check()
        sys.exit(1 if fails else 0)
    from build123d import Compound, export_step, export_stl
    parts = build_parts()
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    shapes = {"zeerbox-assembly": assembly(parts)}
    for name, keys in UNITS.items():
        shapes[name] = Compound([parts[k][1] for k in keys])
    for name, shp in shapes.items():
        export_step(shp, str(root / "step" / f"{name}.step"))
        export_stl(shp, str(root / "stl" / f"{name}.stl"), tolerance=2.0, angular_tolerance=0.5)
    bb = shapes["zeerbox-assembly"].bounding_box()
    print(f"assembly bounding box: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    for k, v in derived().items():
        print(f"  {k:16s} {v:10.3f}" if isinstance(v, float) else f"  {k:16s} {v}")
    for k in sorted(parts):
        print(f"  item {k:2d}  {parts[k][0]:40s} volume {parts[k][1].volume / 1e9:8.3f} m3")
    print("wrote cad/step/*.step and cad/stl/*.stl")
