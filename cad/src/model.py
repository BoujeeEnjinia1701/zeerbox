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



# =============================================================================================================
# Kit 1.9 interface (STANDARDS section 24): every concept option at detail level D3
# =============================================================================================================
# The functions above (build_components, build_parts, assembly, check) are the constructable design of
# ZBX-DDR-003 and stay the source for the build plan pictures, the general arrangement and sizing.py. The
# functions below turn that geometry into individual parts with real stock, broken edges, holes and every
# fixing, and model options B and C (ZBX-OPT-001) to the same level. No design dimension changes here; the
# details added (pipe wall, sheet profile, fixings and their sizes) are listed in ZBX-DEC-001.

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[2] / ".kit")]

TITLE = "ZeerBox"
OPTIONS = {"A": "Forced-air pad store", "B": "Passive wet-wall chamber", "C": "Charcoal-wall wind cooler"}
PRINCIPLES = {
    "A": "Two solar 12 V fans pull outside air through a wetted cellulose pad and along the aisle of an insulated "
         "brick store; a controller reads temperature and humidity inside and out and picks the mode.",
    "B": "A walk-in zero energy cool chamber: water dripped into a sand-filled cavity between two brick leaves "
         "evaporates from the outer leaf and cools the walls; a low vent and a roof stack ventilate it, no power.",
    "C": "Wind pulls outside air through walls of wet lump charcoal held between two welded meshes on a timber "
         "frame; a roof turbine ventilator draws it out, and a header tank keeps the charcoal wet, no power.",
}
CHOSEN = "A"
OPTION_VIEWS = {k: {"el": 24, "az": -58, "scale": "person", "keep_context": True, "ground_z": 0} for k in OPTIONS}

# Pairs of part-name fragments allowed to share volume, each for a physical reason:
ALLOWED_CONTACTS = [
    ("Wood screw", "timber"), ("Wood screw", "plywood"),         # screws cut their own thread in timber
    ("Nail", "timber"), ("Nail", "plywood"),                      # nails are driven, no hole
    ("Coach screw", "timber"),                                    # coach screws in pilot holes
    ("Roofing screw", "timber"), ("Roofing screw", "Roof sheet"), # self-drilling roofing screws
    ("Frame fixing", "brick"), ("Frame fixing", "timber"),        # nylon plug fills its drilled hole; screw through the timber
    ("Wall tie", "brick"), ("Wall tie", "cavity fill"),           # ties bedded in the mortar joints across the cavity
    ("Coach screw", "concrete"),                                  # (none at present)
    ("Nail", "Hurricane tie"), ("Nail", "mesh"),                  # nailed through the tie's punched holes; mesh staples
    ("Door hinge", "timber"), ("Door hinge", "plywood"),          # hinge leaves let into the lining and door edge
    ("Weld", "steel"), ("Weld", "galvanised"),                    # weld metal fuses into both parts
    ("Lid screw", "box"),                                         # self-tapping screws into the box's moulded bosses
    ("Hose", "drum lid"), ("Hose", "gutter"), ("Hose", "header"), # hoses pushed onto spigots and through grommets
    ("Charcoal", "mesh"),                                         # lump charcoal packs round the mesh wires
    ("Cable gland", "box"),                                       # glands screwed into punched holes
]

EXPLODE = {   # bom line: exploded-view offset in mm (as the TRL 3 concept media)
    1: (0, 0, 0), 2: (0, 0, 900), 3: (0, 0, 3900), 4: (0, 0, 4900), 5: (-1300, -2600, 0), 6: (800, 0, 0),
    7: (1500, -500, 0), 8: (-1300, -2600, 1200), 9: (-1300, -5000, 200), 10: (0, 0, 5600), 11: (-1300, -1300, 2600),
    12: (600, -3300, 0), 13: (0, 0, 3100), 14: (0, 0, 0), 15: (0, 0, 0), 16: (-1300, -2600, 600), 17: (0, 0, 4500),
    18: (0, 0, 5350),
}


def _zp():
    import zbx_parts  # noqa: F401  (registers the repo materials)
    return zbx_parts


class _Parts(list):
    """Collects cad_parts.part() dicts for one option; bom numbers only on the chosen option."""

    def __init__(self, with_bom=True):
        super().__init__()
        self.with_bom = with_bom

    def add(self, name, shape, material, kind="made", bom=None, group="shell", explode=None):
        from cad_parts import part
        b = bom if self.with_bom else None
        ex = explode if explode is not None else (EXPLODE.get(bom, (0, 0, 0)) if bom else (0, 0, 0))
        self.append(part(name, shape, material, kind=kind, bom=b, group=group, explode=ex))


def _region_split(solid, regions):
    out = []
    for name, reg in regions:
        s = solid & reg
        if s.volume > 1.0:
            out.append((name, s))
    return out


# ------------------------------------------------------------------------------------------------ structure
def _footing_walls_fill(P, p, C, fill_name, fill_mat, bom_walls=1, bom_fill=2, bom_foot=15):
    """Strip footing, the two brick leaves split into eight wall panels and the capping course, the floor,
    the lintels and the wall ties; the cavity fill split into four sides."""
    z = _zp()
    d = derived(p)
    wall, out_l, out_w, top = d["wall"], d["out_l"], d["out_w"], d["top"]
    leaf, cav = p["LEAF"], p["CAV"]
    hl, hw = p["IN_L"] / 2, p["IN_W"] / 2
    ox, oy = out_l / 2, out_w / 2
    ix, iy = hl + leaf, hw + leaf                 # outer faces of the inner leaf
    P.add("Wall strip footing, concrete", C["strip_footing"][1][0], "concrete", bom=bom_foot)
    walls = C["walls"][1][0]
    regions = [
        ("Outer brick leaf, long wall, door side left", z.box(-ox, ox, -oy, -oy + leaf, -1, top + 1)),
        ("Outer brick leaf, long wall, right", z.box(-ox, ox, oy - leaf, oy, -1, top + 1)),
        ("Outer brick leaf, door end wall", z.box(-ox, -ox + leaf, -oy + leaf, oy - leaf, -1, top + 1)),
        ("Outer brick leaf, pad end wall", z.box(ox - leaf, ox, -oy + leaf, oy - leaf, -1, top + 1)),
        ("Inner brick leaf, long wall left", z.box(-ix, ix, -iy, -hw, -1, top + 1)),
        ("Inner brick leaf, long wall right", z.box(-ix, ix, hw, iy, -1, top + 1)),
        ("Inner brick leaf, door end wall", z.box(-ix, -hl, -hw, hw, -1, top + 1)),
        ("Inner brick leaf, pad end wall", z.box(hl, ix, -hw, hw, -1, top + 1)),
        ("Brick capping course over the cavity", z.box(-ox + leaf, ox - leaf, -oy + leaf, oy - leaf, top - p["CAP"], top + 1)
         - z.box(-ix, ix, -iy, iy, top - p["CAP"] - 1, top + 2)),
    ]
    for name, s in _region_split(walls, regions):
        P.add(name, z.eased(s, 4.0) if len(s.faces()) == 6 else s, "fired_brick", bom=bom_walls)
    P.add("Brick floor on a sand bed", z.eased(C["floor"][1][0], 3.0), "fired_brick", bom=bom_walls)
    for k, l_ in enumerate(C["lintels"][1]):
        P.add(f"Lintel {k + 1}, hardwood timber 115 x 100", z.eased(l_, 3.0), "hardwood", bom=bom_walls)
    fill = C["fill"][1][0]
    fregions = [("long side left", z.box(-ox + leaf, ox - leaf, -iy - cav, -iy, -1, top)),
                ("long side right", z.box(-ox + leaf, ox - leaf, iy, iy + cav, -1, top)),
                ("door end", z.box(-ix - cav, -ix, -iy, iy, -1, top)),
                ("pad end", z.box(ix, ix + cav, -iy, iy, -1, top))]
    for name, s in _region_split(fill, fregions):
        P.add(f"{fill_name}, cavity fill, {name}", z.eased(s, 2.0) if len(s.faces()) == 6 else s, fill_mat, bom=bom_fill)
    # wall ties: 150 mm into each leaf's mortar joint, across the cavity
    tl = cav + 2 * 50
    for zt in (450.0, 1050.0, 1650.0):
        for x in (-1000.0, -500.0, 0.0, 500.0, 1000.0):
            for s in (-1, 1):
                tie = Pos(x, s * (iy - 50), zt) * Rot(0, 0, 90 * s) * z.wall_tie(tl)
                P.add("Wall tie, galvanised wire", tie, "galvanised", kind="fastener", bom=bom_walls)
        for y in (-650.0, 650.0):
            for s in (-1, 1):
                tie = Pos(s * (ix - 50), y, zt) * Rot(0, 0, 0 if s > 0 else 180) * z.wall_tie(tl)
                P.add("Wall tie, galvanised wire", tie, "galvanised", kind="fastener", bom=bom_walls)


def _door(P, p, C, bom_door=5, bom_lining=16):
    """Door lining and stop beads, the insulated door built up from skins, frame and insulation, three butt
    hinges let into lining and door edge, every hinge screw, the inside release latch and the seal."""
    import cad_parts as cp
    z = _zp()
    d = derived(p)
    xf = -d["out_l"] / 2
    fl, lin = p["FLOOR"], p["LINING"]
    jy = p["DOOR_W"] / 2
    names = ("Door lining jamb left, treated timber", "Door lining jamb right, treated timber", "Door lining head, treated timber")
    for nm, s in zip(names, C["door_lining"][1]):
        P.add(nm, z.eased(s, 2.0), "timber", bom=bom_lining)
    for k, s in enumerate(C["door_stops"][1]):
        P.add(f"Door stop bead {k + 1}, timber 20 x 40", z.eased(s, 1.5), "timber", bom=bom_lining)
    # seal: EPDM strip on the stop beads' door face
    sx0 = xf + 8 + p["DOOR_T"] + 2
    seal = z.box(sx0 - 2, sx0, -(jy - 6), jy - 6, fl + 20, fl + p["DOOR_H"] - 8)
    seal = seal - z.box(sx0 - 3, sx0 + 1, -(jy - 18), jy - 18, fl + 32, fl + p["DOOR_H"] - 20)
    P.add("Door seal, EPDM strip on the stop beads", seal, "epdm", kind="bought", bom=bom_door)
    # door leaf: 12 mm plywood skins, 50 mm timber frame, 50 mm insulation board (U value of ZBX-CAL-001)
    x0, x1 = xf + 8, xf + 8 + p["DOOR_T"]
    y0, y1 = -jy + 3, jy - 3
    z0, z1 = fl + 5, fl + p["DOOR_H"] - 3
    P.add("Door outer skin, exterior plywood 12 mm", z.sawn(x0, x0 + 12, y0, y1, z0, z1, 1.5), "plywood", bom=bom_door)
    P.add("Door inner skin, exterior plywood 12 mm", z.sawn(x1 - 12, x1, y0, y1, z0, z1, 1.5), "plywood", bom=bom_door)
    fx0, fx1 = x0 + 12, x1 - 12
    P.add("Door stile, hinge side, timber 50 x 50", z.sawn(fx0, fx1, y0, y0 + 50, z0, z1, 1.0), "timber", bom=bom_door)
    P.add("Door stile, latch side, timber 50 x 50", z.sawn(fx0, fx1, y1 - 50, y1, z0, z1, 1.0), "timber", bom=bom_door)
    P.add("Door top rail, timber 50 x 50", z.sawn(fx0, fx1, y0 + 50, y1 - 50, z1 - 50, z1, 1.0), "timber", bom=bom_door)
    P.add("Door bottom rail, timber 50 x 50", z.sawn(fx0, fx1, y0 + 50, y1 - 50, z0, z0 + 50, 1.0), "timber", bom=bom_door)
    P.add("Door mid rail, timber 50 x 50", z.sawn(fx0, fx1, y0 + 50, y1 - 50, (z0 + z1) / 2 - 25, (z0 + z1) / 2 + 25, 1.0), "timber", bom=bom_door)
    zm = (z0 + z1) / 2
    for nm, za, zb in (("lower", z0 + 50, zm - 25), ("upper", zm + 25, z1 - 50)):
        P.add(f"Door insulation board, {nm}", z.eased(z.box(fx0, fx1, y0 + 50, y1 - 50, za, zb), 1.0), "insulated_white", bom=bom_door)
    # skin nails into the frame
    for xs, dirx in ((x0, 1), (x1, -1)):
        for zz in (z0 + 25, zm, z1 - 25):
            for yy in (y0 + 25, y1 - 25):
                P.add("Nail 2.8 x 50, skin to door frame timber", z.aim(z.nail(2.8, 50), (xs, yy, zz), (dirx, 0, 0)), "galvanised", kind="fastener", bom=bom_door)
    # hinges: knuckle in the 3 mm gap at the outer face, leaves let into the lining and the stile
    for zc in (fl + 250, fl + 900, fl + 1550):
        kn, pin = cp.butt_hinge(100, 32, 1.5, 5, open_deg=0)
        kn = kn - pin
        h = Pos(x0 + 4, -jy + 1.5, zc - 50) * kn
        P.add("Door hinge, 100 mm steel butt", h, "zinc_plated", kind="bought", bom=bom_door)
        P.add("Door hinge pin", Pos(x0 + 4, -jy + 1.5, zc - 50) * pin, "zinc_plated", kind="fastener", bom=bom_door)
        for zz in (zc - 30, zc + 30):
            for xx in (x0 + 18, x0 + 30):
                P.add("Wood screw 4 x 12, hinge to lining timber", z.aim(z.wood_screw(4, 12), (xx, -jy, zz), (0, -1, 0)), "zinc_plated", kind="fastener", bom=bom_door)
                P.add("Wood screw 4 x 30, hinge to door stile timber", z.aim(z.wood_screw(4, 30), (xx, -jy + 3.0, zz), (0, 1, 0)), "zinc_plated", kind="fastener", bom=bom_door)
    # inside release latch: lever handle on the inner face, keeper on the jamb; no outside lock
    zl = fl + 1000
    plate = z.eased(z.box(x1, x1 + 3, y1 - 70, y1 - 20, zl - 60, zl + 60), 0.8)
    lever = z.tube_between((x1 + 3 + 25, y1 - 45, zl), (x1 + 3 + 25, y1 - 160, zl), 16)
    boss = z.tube_between((x1 + 3, y1 - 45, zl), (x1 + 3 + 33, y1 - 45, zl), 20)
    lscr = [z.aim(z.pan_screw(4, 30), (x1 + 3, y1 - 45, zz), (-1, 0, 0)) for zz in (zl - 45, zl + 45)]
    latch = plate + boss + lever
    for sc in lscr:
        latch = latch - sc
    P.add("Inside release latch with lever, no outside lock", latch, "zinc_plated", kind="bought", bom=bom_door)
    for sc in lscr:
        P.add("Wood screw 4 x 30 pan head, latch to door stile timber", sc, "zinc_plated", kind="fastener", bom=bom_door)
    # lining screws into the brick reveal (frame fixings through the jambs)
    for s in (-1, 1):
        for zz in (fl + 300, fl + 900, fl + 1500):
            for xx in (xf + 60, xf + 245):
                P.add("Frame fixing 8 x 100, lining jamb timber to brick", z.aim(z.frame_fixing(8, 100), (xx, s * jy, zz), (0, s, 0)), "hdpe_natural", kind="fastener", bom=bom_lining)


def _ceiling(P, p, C, bom_ceiling=3, bom_box=16, fan_box=True):
    """Joists with their cleats as separate pieces, insulation bays, ceiling boards, nails and joist straps."""
    z = _zp()
    d = derived(p)
    top, out_w, out_l = d["top"], d["out_w"], d["out_l"]
    jw, jh = p["JOIST"]
    cl, it, dt = p["CLEAT"], p["INS_T"], p["DECK_T"]
    bx, by = p["FANBOX"]
    fx = p["FAN_X"]
    fb_cut = z.box(fx - bx / 2, fx + bx / 2, -by / 2, by / 2, top - 1, top + jh + dt + 1) if fan_box else None
    xs = sorted(p["JOIST_X"])
    for i, x in enumerate(xs):
        P.add(f"Ceiling joist {i + 1}, timber 50 x 100", z.sawn(x - jw / 2, x + jw / 2, -out_w / 2, out_w / 2, top, top + jh, 2.0), "timber", bom=bom_ceiling)
        for s in (-1, 1):
            if (s < 0 and i == 0) or (s > 0 and i == len(xs) - 1):
                continue
            xc = x + s * jw / 2
            pieces = [(-out_w / 2, out_w / 2)]
            if fan_box and abs(xc - fx) < bx / 2 + 1:
                pieces = [(-out_w / 2, -by / 2), (by / 2, out_w / 2)]
            for k, (ya, yb) in enumerate(pieces):
                c = z.sawn(min(xc, xc + s * cl), max(xc, xc + s * cl), ya, yb, top, top + cl, 1.0)
                P.add(f"Ceiling cleat, joist {i + 1} {'right' if s > 0 else 'left'} {k + 1}, timber 25 x 25", c, "timber", bom=bom_ceiling)
                for yy in [ya + 100 + j * (yb - ya - 200) / 3 for j in range(4)]:
                    P.add("Nail 2.8 x 50, cleat to joist timber", z.aim(z.nail(2.8, 50), (xc + s * cl, yy, top + cl / 2), (-s, 0, 0)), "galvanised", kind="fastener", bom=bom_ceiling)
    for a, b in zip(xs[:-1], xs[1:]):
        ins = z.box(a + jw / 2, b - jw / 2, -out_w / 2, out_w / 2, top + cl, top + cl + it)
        if fan_box:
            ins = ins - fb_cut
        P.add(f"Ceiling insulation bay {xs.index(a) + 1}, straw board 50 mm", z.eased(ins, 2.0), "straw_board", bom=bom_ceiling)
    nb = 14
    bw = out_w / nb
    for k in range(nb):
        y0 = -out_w / 2 + k * bw
        b = z.box(-out_l / 2, out_l / 2, y0, y0 + bw - 2, top + jh, top + jh + dt)
        if fan_box:
            b = b - fb_cut
        if b.volume < 1:
            continue
        P.add(f"Ceiling board {k + 1}, timber 20 mm", z.eased(b, 1.0), "timber", bom=bom_ceiling)
        for x in xs:
            if fan_box and abs(x - fx) < bx / 2 + jw and abs(y0 + bw / 2) < by / 2:
                continue
            P.add("Nail 2.8 x 60, board to joist timber", z.aim(z.nail(2.8, 60), (x, y0 + bw / 2, top + jh + dt), (0, 0, -1)), "galvanised", kind="fastener", bom=bom_ceiling)
    # joist straps: a galvanised strap on the outer wall face, one fixing in the brick and one screw in the joist end
    for x in xs:
        for s in (-1, 1):
            yf = s * out_w / 2
            st = z.strap(300, 30, 2.0, holes=2, d=6.0)            # along Z, thickness along +X, width along Y
            st = Pos(x, yf, top - 150) * Rot(0, 0, 90 * s) * st
            P.add("Joist strap, galvanised 30 x 2", st, "galvanised", kind="bought", bom=bom_ceiling)
            P.add("Frame fixing 6 x 60, joist strap to brick", z.aim(z.frame_fixing(6, 60), (x, yf + s * 2.0, top - 50), (0, -s, 0)), "hdpe_natural", kind="fastener", bom=bom_ceiling)
            P.add("Wood screw 5 x 50 pan head, joist strap to joist timber", z.aim(z.pan_screw(5, 50), (x, yf + s * 2.0, top + 50), (0, -s, 0)),
                  "zinc_plated", kind="fastener", bom=bom_ceiling)


def _fan_box(P, p, C, bom_box=16, bom_fans=8):
    """Fan box of four plywood sides and a top plate, its screws, two 250 mm fans with struts, blades, finger
    guards and gravity shutters, and the fan screws."""
    z = _zp()
    d = derived(p)
    top = d["top"]
    jh, dt = p["JOIST"][1], p["DECK_T"]
    bx, by = p["FANBOX"]
    fx, ply, up = p["FAN_X"], p["PLY"], p["FANBOX_UP"]
    zt = top + jh + dt + up
    sides = [("long side left", z.box(fx - bx / 2, fx + bx / 2, -by / 2, -by / 2 + ply, top, zt)),
             ("long side right", z.box(fx - bx / 2, fx + bx / 2, by / 2 - ply, by / 2, top, zt)),
             ("end door side", z.box(fx - bx / 2, fx - bx / 2 + ply, -by / 2 + ply, by / 2 - ply, top, zt)),
             ("end pad side", z.box(fx + bx / 2 - ply, fx + bx / 2, -by / 2 + ply, by / 2 - ply, top, zt))]
    for nm, s in sides:
        P.add(f"Fan box {nm}, exterior plywood 18 mm", z.eased(s, 1.0), "plywood", bom=bom_box)
    plate = C["fan_box"][1][1]
    P.add("Fan box top plate, exterior plywood 18 mm", z.eased(plate, 1.0), "plywood", bom=bom_box)
    for xx in (fx - bx / 2 + ply / 2, fx + bx / 2 - ply / 2):
        for yy in (-by / 2 + 60, 0.0, by / 2 - 60):
            P.add("Wood screw 4 x 40, top plate to fan box plywood", z.aim(z.wood_screw(4, 40), (xx, yy, zt + ply), (0, 0, -1)), "zinc_plated", kind="fastener", bom=bom_box)
    for s in (-1, 1):
        for zz in (top + 40, zt - 40):
            P.add("Wood screw 4 x 40, fan box corner plywood", z.aim(z.wood_screw(4, 40), (fx - bx / 2, s * (by / 2 - ply - 30), zz), (1, 0, 0)),
                  "zinc_plated", kind="fastener", bom=bom_box)
            P.add("Wood screw 4 x 40, fan box corner plywood", z.aim(z.wood_screw(4, 40), (fx + bx / 2, s * (by / 2 - ply - 30), zz), (-1, 0, 0)), "zinc_plated", kind="fastener", bom=bom_box)
    # fan box to the two joists either side (screws through the end pieces into the joists)
    for xj, dx in ((fx - bx / 2, -1), (fx + bx / 2, 1)):
        for yy in (-by / 2 + 60, by / 2 - 60):
            P.add("Wood screw 5 x 60, fan box to joist timber", z.aim(z.wood_screw(5, 60), (xj - dx * ply, yy, top + jh / 2), (dx, 0, 0)), "zinc_plated", kind="fastener", bom=bom_box)
    fr = p["FAN_D"] / 2
    z0 = zt + ply
    from build123d import Cylinder as Cyl
    for s in (-1, 1):
        y = s * p["FAN_Y"]
        frame = z.box(fx - 137, fx + 137, y - 137, y + 137, z0, z0 + 90) - Pos(fx, y, z0 + 45) * Cyl(fr - 3, 92)
        for cx in (-117, 117):
            for cy in (-117, 117):
                frame = frame - Pos(fx + cx, y + cy, z0 + 45) * Cyl(3, 92)
        hub = Pos(fx, y, z0 + 45) * Cyl(45, 80)
        rotor = hub
        for k in range(5):
            bl = Pos(fx, y, z0 + 45) * Rot(0, 0, 72 * k) * Pos(84, 0, 0) * Rot(25, 0, 0) * Box(76, 60, 3)
            rotor = rotor + bl
        struts = [Pos(fx, y, z0 + 82) * Rot(0, 0, 120 * k + 30) * Pos(84, 0, 0) * Box(80, 8, 6) for k in range(3)]
        body = frame + rotor
        for st_ in struts:
            body = body + st_
        P.add(f"Exhaust fan {'right' if s > 0 else 'left'}, 250 mm 12 V DC axial", body, "matte_black", kind="bought", bom=bom_fans)
        guard = None
        for r in (40, 75, 110):
            ring = Pos(fx, y, z0 + 92) * (Cyl(r + 1.5, 3) - Cyl(r - 1.5, 3))
            guard = ring if guard is None else guard + ring
        for k in range(4):
            guard = guard + Pos(fx, y, z0 + 92) * Rot(0, 0, 45 * k) * Box(2 * 111.5, 3, 3)
        P.add(f"Fan finger guard {'right' if s > 0 else 'left'}, steel wire", guard, "zinc_plated", kind="bought", bom=bom_fans)
        sh = C["fans"][1][1 if s < 0 else 3]
        sh = sh - Pos(fx, y, z0 + 92) * Cyl(113, 5)
        P.add(f"Gravity shutter {'right' if s > 0 else 'left'}, plastic", sh, "hdpe_natural", kind="bought", bom=bom_fans)
        for cx in (-117, 117):
            for cy in (-117, 117):
                P.add("Wood screw 5 x 120 pan head, fan to top plate plywood", z.aim(z.pan_screw(5, 112), (fx + cx, y + cy, z0 + 90), (0, 0, -1)), "zinc_plated", kind="fastener", bom=bom_fans)


def _roof(P, p, C, bom_roof=4, bom_frame=17, posts_only=False):
    """Post footings cast round the posts, galvanised pipe posts with welded cap plates and anchor bars, coach
    screws into the beams, beams and purlins, hurricane ties and their nails, box-profile sheets and screws."""
    import cad_parts as cp
    z = _zp()
    d = derived(p)
    R = roof_frame(p)
    sh_t = p["SHEET_T"]
    pu_w, pu_h = p["PURLIN"]
    be_w, be_h = p["BEAM"]
    z_pu = (-sh_t / 2 - pu_h, -sh_t / 2)
    z_be = (z_pu[0] - be_h, z_pu[0])
    cpl, ct = p["CAP_PLATE"]
    fs, fd = p["FOOTING"], p["FOOTING_DEPTH"]
    px, py = p["POST_X"], p["POST_Y"]
    t_pipe = 3.2
    from build123d import Cylinder as Cyl
    import math as _m
    tilt = _m.radians(p["ROOF_PITCH_DEG"])
    nrm = (0.0, -_m.sin(tilt), _m.cos(tilt))          # roof normal (up) in world
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * px, sy * py
            ztop = roof_world_z(y, z_be[0] - ct, p) - 4
            L = ztop + p["POST_EMBED"]
            pipe = Pos(x, y, -p["POST_EMBED"]) * cp.round_tube(p["POST_D"], t_pipe, L)
            bar_z = -p["POST_EMBED"] + 50
            hole = Pos(x, y, bar_z) * Rot(0, 90, 0) * Cyl(6.5, 200)
            pipe = pipe - hole
            bar = Pos(x - 100, y, bar_z) * Rot(0, 90, 0) * cp.round_bar(12, 200)
            foot = z.box(x - fs / 2, x + fs / 2, y - fs / 2, y + fs / 2, -fd, 0)
            foot = foot - Pos(x, y, -p["POST_EMBED"]) * Cyl(p["POST_D"] / 2, 2 * p["POST_EMBED"]) - bar
            nm = f"{'left' if sx < 0 else 'right'} {'front' if sy < 0 else 'back'}"
            P.add(f"Post footing {nm}, concrete 500 x 500 x 600", z.eased(foot, 5.0), "concrete", bom=bom_roof)
            P.add(f"Roof post {nm}, galvanised steel pipe 90 x 3.2", pipe, "galvanised", bom=bom_roof)
            P.add(f"Anchor bar {nm}, steel 12 mm", bar, "mild_steel", kind="bought", bom=bom_roof)
            yl = roof_local_y(y, z_be[0] - ct / 2, p)
            plate = R * Pos(x, yl, z_be[0] - ct) * cp.sheet(cpl, cpl, ct, holes=[(0, 58, 12), (0, -58, 12)])
            P.add(f"Post cap plate {nm}, galvanised steel 150 x 150 x 6", plate, "galvanised", bom=bom_roof)
            weld = Pos(x, y, ztop) * z.ring_weld(p["POST_D"] / 2, 6.0, -6.0, 5.0)
            P.add(f"Weld, post to cap plate {nm}, fillet 4 mm on galvanised steel", weld, "galvanised", kind="weld", bom=bom_roof)
            if posts_only:
                continue
            for yo in (58.0, -58.0):
                yl2 = roof_local_y(y, z_be[0] - ct, p) + yo
                pt = R * Pos(x, yl2, z_be[0] - ct)
                o = pt.position
                oh = (o.X - 2.0 * nrm[0], o.Y - 2.0 * nrm[1], o.Z - 2.0 * nrm[2])     # head under the 2 mm washer
                P.add("Coach screw M10 x 100, cap plate to beam timber", z.aim(cp.coach_screw(10, 100), oh, nrm),
                      "galvanised", kind="fastener", bom=bom_frame)
                P.add("Washer M10 under the coach screw head", z.aim(cp.washer(10), (o.X, o.Y, o.Z), nrm), "galvanised", kind="fastener", bom=bom_frame)
    if posts_only:
        return
    L_, W_ = p["ROOF_L"], p["ROOF_W"]
    for sx in (-1, 1):
        b = R * z.sawn(sx * px - be_w / 2, sx * px + be_w / 2, -W_ / 2 + 30, W_ / 2 - 30, *z_be, r=3.0)
        P.add(f"Roof beam {'left' if sx < 0 else 'right'}, timber 75 x 150", b, "timber", bom=bom_frame)
    for i, yp in enumerate(p["PURLIN_Y"]):
        b = R * z.sawn(-L_ / 2 + 50, L_ / 2 - 50, yp - pu_w / 2, yp + pu_w / 2, *z_pu, r=3.0)
        P.add(f"Purlin {i + 1}, timber 50 x 150", b, "timber", bom=bom_frame)
        for sx in (-1, 1):
            bxf = sx * px + sx * be_w / 2                 # outer face of the beam
            t, w = 1.5, 35.0
            yo = yp + pu_w / 2                            # purlin face the tie sits on
            if sx > 0:
                upper = z.box(bxf - w, bxf, yo, yo + t, z_pu[0], z_pu[0] + 100)
                lower = z.box(bxf, bxf + t, yo + t - w, yo + t, z_pu[0] - 100, z_pu[0] + 0.0)
            else:
                upper = z.box(bxf, bxf + w, yo, yo + t, z_pu[0], z_pu[0] + 100)
                lower = z.box(bxf - t, bxf, yo + t - w, yo + t, z_pu[0] - 100, z_pu[0])
            tie = R * (upper + lower)
            P.add("Hurricane tie, galvanised, rated 2 kN uplift", tie, "galvanised", kind="bought", bom=bom_frame)
            for k in range(3):
                xa = bxf - sx * (w / 2)
                pt = R * Pos(xa, yo + t, z_pu[0] + 25 + 25 * k)
                o = pt.position
                dvec = R * Pos(0, -1, 0)
                dv = (dvec.position.X - R.position.X, dvec.position.Y - R.position.Y, dvec.position.Z - R.position.Z)
                P.add("Nail 3.75 x 40, hurricane tie to purlin timber", z.aim(z.nail(3.75, 40), (o.X, o.Y, o.Z), dv), "galvanised", kind="fastener", bom=bom_frame)
                pt2 = R * Pos(bxf + sx * t, yo + t - w / 2, z_pu[0] - 25 - 25 * k)
                o2 = pt2.position
                dvx = R * Pos(-sx, 0, 0)
                dv2 = (dvx.position.X - R.position.X, dvx.position.Y - R.position.Y, dvx.position.Z - R.position.Z)
                P.add("Nail 3.75 x 40, hurricane tie to beam timber", z.aim(z.nail(3.75, 40), (o2.X, o2.Y, o2.Z), dv2), "galvanised", kind="fastener", bom=bom_frame)
    # box-profile sheets, four across the 3.9 m, each running down the slope; screws on the crests at each purlin
    nsh = 4
    sw = L_ / nsh
    depth = sh_t - 0.5
    for k in range(nsh):
        xc = -L_ / 2 + sw / 2 + k * sw
        sheet = R * Pos(xc, 0, 0.25) * z.corrugated(W_, sw - 1.0, t=0.5, pitch=190.0, depth=depth)
        P.add(f"Roof sheet {k + 1}, box-profile galvanised steel 0.5 mm", sheet, "galvanised", bom=bom_roof)
        crests = z.crest_x(sw - 1.0, 190.0)
        for yp in p["PURLIN_Y"]:
            for cx in (crests[1], crests[-2]):
                pt = R * Pos(xc + cx, yp, sh_t / 2)
                o = pt.position
                P.add("Roofing screw 6 x 100, sheet to purlin timber", z.aim(z.roofing_screw(6, 100), (o.X, o.Y, o.Z), (-nrm[0], -nrm[1], -nrm[2])),
                      "galvanised", kind="fastener", bom=bom_roof)


def _panel(P, p, C, bom_mount=18, bom_panel=10):
    """Panel mounting frames (angle rails and flat-bar legs, drilled, bolted), the 150 W panel as frame,
    laminate and junction box, the panel bolts and the base-rail roofing screws."""
    import cad_parts as cp
    z = _zp()
    from build123d import Cylinder as Cyl
    import math as _m
    R = roof_frame(p)
    PF = panel_frame(p)
    sh_t = p["SHEET_T"]
    a, t = p["ANGLE"]
    mx = p["MOUNT_X"]
    PW, PL, PT = p["PANEL_W"], p["PANEL_L"], p["PANEL_T"]
    tilt = _m.radians(p["ROOF_PITCH_DEG"])
    nrm = (0.0, -_m.sin(tilt), _m.cos(tilt))
    for s in (-1, 1):
        side = "left" if s < 0 else "right"
        x0 = s * mx
        xo = (x0, x0 + s * a) if s > 0 else (x0 + s * a, x0)
        xv = (x0, x0 + s * t) if s > 0 else (x0 + s * t, x0)
        y0, y1 = p["PURLIN_Y"][1] - 60, p["PURLIN_Y"][2] + 60
        base_l = _bx(*xo, y0, y1, sh_t / 2, sh_t / 2 + t) + _bx(*xv, y0, y1, sh_t / 2, sh_t / 2 + a)
        rail_l = (_bx(*xo, -PW / 2, PW / 2, -PT / 2 - t, -PT / 2) + _bx(*xv, -PW / 2, PW / 2, -PT / 2 - a, -PT / 2))
        xl = (x0 - s * t, x0) if s > 0 else (x0, x0 - s * t)
        legs, bolts_x = [], []
        for yl in (-PW / 2 + 25, PW / 2 - 25):
            _, yw, zw = panel_point(x0, yl, -PT / 2, p)
            zb = roof_world_z(yw, sh_t / 2, p) + 2
            legs.append((yw, zb, zw - 6))
        # holes for the leg bolts, in roof and panel local frames
        for yw, zb, ztop in legs:
            zlo, zhi = zb + 20, ztop - 20
            bolts_x.append((yw, zlo, "base"))
            bolts_x.append((yw, zhi, "rail"))
        base = R * base_l
        rail = PF * rail_l
        for yw, zz, which in bolts_x:
            h = Pos(x0, yw, zz) * Rot(0, 90, 0) * Cyl(4.5, 40)
            if which == "base":
                base = base - h
            else:
                rail = rail - h
        # base rail roofing-screw holes at the two purlins; panel bolt holes in the top rail
        xs_c = x0 + s * a / 2
        for yp in (p["PURLIN_Y"][1], p["PURLIN_Y"][2]):
            base = base - R * Pos(xs_c, yp, sh_t / 2) * Cyl(3.5, 3 * t)
        for yb in (-(PW / 2 - 15), PW / 2 - 15):
            rail = rail - PF * Pos(xs_c, yb, -PT / 2) * Cyl(4.5, 3 * t)
        P.add(f"Panel frame base rail {side}, aluminium angle 40 x 40 x 4", z.eased(base, 0.8), "aluminium", bom=bom_mount)
        P.add(f"Panel frame top rail {side}, aluminium angle 40 x 40 x 4", z.eased(rail, 0.8), "aluminium", bom=bom_mount)
        for k, (yw, zb, ztop) in enumerate(legs):
            leg = _bx(*xl, yw - a / 2, yw + a / 2, zb, ztop)
            for yy, zz, which in bolts_x:
                if abs(yy - yw) < 1:
                    leg = leg - Pos(x0, yy, zz) * Rot(0, 90, 0) * Cyl(4.5, 40)
            P.add(f"Panel frame leg {side} {k + 1}, aluminium flat bar 40 x 4", z.eased(leg, 0.8), "aluminium", bom=bom_mount)
        for yw, zz, which in bolts_x:
            jt = x0 + s * t                                   # outer face of the flange: joint top face
            from build123d import Location, Plane, Vector
            L = Location(Plane(origin=Vector(jt, yw, zz), x_dir=Vector(0, 1, 0), z_dir=Vector(s, 0, 0)))
            for nm, shp in cp.hex_bolt_set(8, 2 * t):
                P.add(f"{nm}, stainless, panel frame leg", L * shp, "stainless", kind="fastener", bom=bom_mount)
        for yp in (p["PURLIN_Y"][1], p["PURLIN_Y"][2]):
            o = (R * Pos(xs_c, yp, sh_t / 2 + t)).position
            P.add("Roofing screw 6 x 100, base rail through sheet to purlin timber", z.aim(z.roofing_screw(6, 100), (o.X, o.Y, o.Z), (-nrm[0], -nrm[1], -nrm[2])),
                  "galvanised", kind="fastener", bom=bom_mount)
        for yb in (-(PW / 2 - 15), PW / 2 - 15):
            from build123d import Location, Plane, Vector
            o = (PF * Pos(xs_c, yb, -PT / 2 - t)).position          # rail underside; the joint runs up through rail and flange
            nz = (PF * Pos(0, 0, 1)).position - PF.position
            L = Location(Plane(origin=o, x_dir=Vector(1, 0, 0), z_dir=Vector(-nz.X, -nz.Y, -nz.Z)))   # head below the rail
            for nm, shp in cp.hex_bolt_set(8, t + 3):
                P.add(f"{nm}, stainless, panel to top rail", L * Pos(0, 0, 0) * shp, "stainless", kind="fastener", bom=bom_panel)
    # panel: aluminium frame (thin walls, back flange with holes, top lip), laminate, junction box
    ring = _bx(-PL / 2, PL / 2, -PW / 2, PW / 2, -PT / 2, PT / 2) - _bx(-PL / 2 + 2, PL / 2 - 2, -PW / 2 + 2, PW / 2 - 2, -PT / 2 - 1, PT / 2 + 1)
    flange = _bx(-PL / 2 + 2, PL / 2 - 2, -PW / 2 + 2, PW / 2 - 2, -PT / 2, -PT / 2 + 3) - _bx(-PL / 2 + 30, PL / 2 - 30, -PW / 2 + 30, PW / 2 - 30, -PT / 2 - 1, -PT / 2 + 4)
    lip = _bx(-PL / 2 + 2, PL / 2 - 2, -PW / 2 + 2, PW / 2 - 2, PT / 2 - 2, PT / 2) - _bx(-PL / 2 + 12, PL / 2 - 12, -PW / 2 + 12, PW / 2 - 12, PT / 2 - 3, PT / 2 + 1)
    frame = ring + flange + lip
    for s in (-1, 1):
        for yb in (-(PW / 2 - 15), PW / 2 - 15):
            frame = frame - Pos(s * mx + s * a / 2, yb, -PT / 2 + 1.5) * Cyl(4.5, 6)
    P.add("Solar panel frame, aluminium", PF * frame, "aluminium", kind="bought", bom=bom_panel)
    lam = _bx(-PL / 2 + 2, PL / 2 - 2, -PW / 2 + 2, PW / 2 - 2, PT / 2 - 6, PT / 2 - 2)
    P.add("Solar panel laminate, glass on monocrystalline cells, 150 W", PF * z.eased(lam, 0.5), "glass", kind="bought", bom=bom_panel)
    jb = z.hollow_box(-60, 60, -50, 50, PT / 2 - 6 - 22, PT / 2 - 6, 2.0, None, 3.0)
    P.add("Solar panel junction box", PF * jb, "hdpe_black", kind="bought", bom=bom_panel)


def _pad(P, p, C, bom=6):
    """Pad opening lining, battens and their fixings, frame, bars and screws, the pad, the drilled drip
    header with end cap, the return gutter and its brackets."""
    import cad_parts as cp
    z = _zp()
    from build123d import Cylinder as Cyl
    d = derived(p)
    xb = d["out_l"] / 2
    PWc, PHc, PT = p["PAD_W"], p["PAD_H"], p["PAD_T"]
    pz = p["PAD_Z"]
    zb_, zt_ = pz - PHc / 2, pz + PHc / 2
    for k, s in enumerate(C["pad_lining"][1]):
        P.add(f"Pad opening lining {k + 1}, treated timber 20 mm", z.eased(s, 1.5), "timber", bom=bom)
    for k, s in enumerate(C["pad_battens"][1]):
        P.add(f"Pad frame batten {k + 1}, treated timber 25 x 50", z.eased(s, 1.5), "timber", bom=bom)
        bb = s.bounding_box()
        for zz in (zb_ + 60, zt_ + 40):
            P.add("Frame fixing 8 x 80, batten timber to brick", z.aim(z.frame_fixing(8, 80), ((bb.min.X + bb.max.X) / 2 + 25, (bb.min.Y + bb.max.Y) / 2, zz), (-1, 0, 0)),
                  "hdpe_natural", kind="fastener", bom=bom)
    for k, s in enumerate(C["pad_frame"][1]):
        P.add(f"Pad frame {'side' if k < 2 else 'top'} {k + 1}, treated timber 25 mm board", z.eased(s, 1.5), "timber", bom=bom)
    for k, s in enumerate(C["pad_frame"][1][:2]):
        bb = s.bounding_box()
        yc = (bb.min.Y + bb.max.Y) / 2
        sgn = 1 if yc > 0 else -1
        for zz in (zb_ + 120, zt_ - 40):
            P.add("Wood screw 5 x 45, frame side to batten timber", z.aim(z.wood_screw(5, 45), (xb + 60, yc + sgn * 12.5, zz), (0, sgn, 0)),
                  "zinc_plated", kind="fastener", bom=bom)
    for k, s in enumerate(C["pad_bars"][1]):
        bb = s.bounding_box()
        screws = []
        for yy in (bb.min.Y + 12.5, bb.max.Y - 12.5):
            if k < 2:
                screws.append(("Wood screw 4 x 30 pan head, support bar to frame timber",
                               z.aim(z.pan_screw(4, 30), ((bb.min.X + bb.max.X) / 2, yy, bb.min.Z), (0, 0, 1))))
            else:
                screws.append(("Wood screw 4 x 30 pan head, retaining bar to frame timber",
                               z.aim(z.pan_screw(4, 30), (bb.max.X, yy, (bb.min.Z + bb.max.Z) / 2), (-1, 0, 0))))
        bar = z.eased(s, 0.8)
        for _, sc in screws:
            bar = bar - sc
        P.add(f"Pad {'support' if k < 2 else 'retaining'} bar {k + 1}, galvanised steel flat 30 x 3", bar, "galvanised", bom=bom)
        for nm, sc in screws:
            P.add(nm, sc, "zinc_plated", kind="fastener", bom=bom)
    pad = C["pad"][1][0]
    for k in range(1, 6):                            # flute faces seen on the outside face
        yk = -PWc / 2 + k * PWc / 6
        pad = pad - Pos(xb + PT, yk, pz) * Box(6, 3, PHc + 2)
    P.add("Cellulose evaporative pad, 150 mm, 0.6 x 0.5 m", z.eased(pad, 2.0), "cellulose_pad", kind="bought", bom=bom)
    hz = zt_ + 16
    h_y0, h_y1 = -PWc / 2 - 100, PWc / 2 + 40
    hdr = Pos(xb + PT / 2, h_y0, hz) * Rot(-90, 0, 0) * cp.round_tube(32, 2.4, h_y1 - h_y0)
    for k in range(10):
        yk = -PWc / 2 + 30 + k * (PWc - 60) / 9
        hdr = hdr - Pos(xb + PT / 2, yk, hz - 14) * Cyl(1.5, 10)
    P.add("Drip header, PVC pipe 32 mm drilled 3 mm", hdr, "pvc", bom=bom)
    cap = Pos(xb + PT / 2, h_y1, hz) * Rot(-90, 0, 0) * (Cyl(18, 20).moved(Pos(0, 0, 10)) - Cyl(16, 12).moved(Pos(0, 0, 5)))
    P.add("Drip header end cap, PVC 32 mm", cap, "pvc", kind="bought", bom=bom)
    P.add("Return gutter, folded galvanised sheet 170 x 60", C["gutter"][1][0], "galvanised", bom=bom)
    for k, s in enumerate(C["gutter_brackets"][1]):
        bb = s.bounding_box()
        fx_ = z.aim(z.frame_fixing(6, 60), (xb + 3, (bb.min.Y + bb.max.Y) / 2, bb.max.Z - 15), (-1, 0, 0))
        P.add(f"Gutter bracket {k + 1}, galvanised strip", z.eased(s, 0.5) - fx_, "galvanised", bom=bom)
        P.add("Frame fixing 6 x 60, gutter bracket to brick", fx_, "hdpe_natural", kind="fastener", bom=bom)


def _sump(P, p, C, bom=7):
    z = _zp()
    from build123d import Cylinder as Cyl
    sx_, sy_ = p["SUMP_XY"]
    dr, dh_ = p["SUMP_D"] / 2, p["SUMP_H"]
    drum = Pos(sx_, sy_, (dh_ - 6) / 2) * Cyl(dr, dh_ - 6) - Pos(sx_, sy_, (dh_ - 6) / 2 + 4) * Cyl(dr - 4, dh_ - 6)
    P.add("Sump drum, 60 L HDPE", z.eased(drum, 1.0), "hdpe_natural", kind="bought", bom=bom)
    hoses = C["hoses"][1]
    lid = Pos(sx_, sy_, dh_ - 3) * Cyl(dr + 3, 6)
    lid = lid - hoses[0] - hoses[1]
    P.add("Sump drum lid, HDPE", z.eased(lid, 1.0), "hdpe_black", kind="bought", bom=bom)
    pump = Pos(sx_, sy_ - 50, 4 + 45) * Cyl(45, 90) + Pos(sx_, sy_ - 50, 4 + 90 + 15) * Cyl(10, 30)
    P.add("Pump, 12 V DC submersible, about 6 W", pump, "matte_black", kind="bought", bom=bom)
    flt = Pos(sx_ + 100, sy_ + 60, 4 + 60) * Cyl(15, 40) + Pos(sx_ + 100, sy_ + 60, 4 + 20) * Cyl(5, 40)
    P.add("Float switch on the sump floor weight", flt, "hdpe_black", kind="bought", bom=bom)
    P.add("Feed hose to the drip header, PVC 20 mm", hoses[0], "hdpe_black", kind="bought", bom=bom)
    P.add("Return hose from the gutter, PVC 32 mm", hoses[1], "hdpe_black", kind="bought", bom=bom)


def _controls(P, p, C, bom_ctrl=9, bom_power=11):
    """Clear-lid controller box with its PCBs on standoffs, glands and screws; the mode lamp; the six-plate
    outside sensor shield on its arm; the inside sensor; the ventilated power box with battery, charge
    controller and fuse holder."""
    z = _zp()
    from build123d import Cylinder as Cyl
    d = derived(p)
    xf = -d["out_l"] / 2
    hl = p["IN_L"] / 2
    cd_, cw_, ch_ = p["CTRL"]
    cy_, cz_ = p["CTRL_YZ"]
    cw = p["CTRL_WALL"]
    z0c, z1c = cz_ - ch_ / 2, cz_ + ch_ / 2
    lh, lfl, lft, ldome, ldh, ldy = p["LAMP"]
    lx, ly = xf - cd_ / 2, cy_ + ldy
    body = z.hollow_box(xf - cd_ + cw, xf, cy_ - cw_ / 2, cy_ + cw_ / 2, z0c, z1c, cw, "-x", 2.0)
    body = body - Pos(lx, ly, z1c - cw / 2) * Cyl(lh / 2, cw + 2)
    for yy in (cy_ - cw_ / 2 + 25, cy_ + cw_ / 2 - 25):
        for zz in (z0c + 25, z1c - 25):
            body = body - Pos(xf - cw / 2, yy, zz) * Rot(0, 90, 0) * Cyl(3.5, cw + 2)
    for yy in (cy_ - 40, cy_ + 40):
        body = body - Pos(xf - cd_ / 2, yy, z0c + cw / 2) * Cyl(8, cw + 2)
    P.add("Controller box, IP65 ABS 200 x 250 x 80", body, "hdpe_natural", kind="bought", bom=bom_ctrl)
    lid = z.box(xf - cd_, xf - cd_ + cw, cy_ - cw_ / 2, cy_ + cw_ / 2, z0c, z1c)
    for yy in (cy_ - cw_ / 2 + 8, cy_ + cw_ / 2 - 8):
        for zz in (z0c + 8, z1c - 8):
            lid = lid - Pos(xf - cd_ + cw / 2, yy, zz) * Rot(0, 90, 0) * Cyl(2.2, cw + 2)
    P.add("Controller box clear lid, polycarbonate", z.eased(lid, 0.8), "polycarbonate", kind="bought", bom=bom_ctrl)
    for yy in (cy_ - cw_ / 2 + 8, cy_ + cw_ / 2 - 8):
        for zz in (z0c + 8, z1c - 8):
            P.add("Lid screw 4 x 16 into the box boss", z.aim(z.pan_screw(4, 16), (xf - cd_, yy, zz), (1, 0, 0)), "stainless", kind="fastener", bom=bom_ctrl)
    for yy in (cy_ - cw_ / 2 + 25, cy_ + cw_ / 2 - 25):
        for zz in (z0c + 25, z1c - 25):
            P.add("Frame fixing 6 x 60, controller box to brick", z.aim(z.frame_fixing(6, 60), (xf - cw, yy, zz), (1, 0, 0)), "hdpe_natural", kind="fastener", bom=bom_ctrl)
    # PCBs: main board with MOSFET drivers and logger on four standoffs; the microcontroller module on it
    bx0 = xf - cw - 12
    pcb = z.box(bx0 - 1.6, bx0, cy_ - 70, cy_ + 70, cz_ - 40, cz_ + 60)
    for yy in (cy_ - 62, cy_ + 62):
        for zz in (cz_ - 32, cz_ + 52):
            pcb = pcb - Pos(bx0 - 0.8, yy, zz) * Rot(0, 90, 0) * Cyl(1.6, 3)
    P.add("Controller main board, FR4 with MOSFET drivers and memory card", pcb, "fr4", kind="bought", bom=bom_ctrl)
    for yy in (cy_ - 62, cy_ + 62):
        for zz in (cz_ - 32, cz_ + 52):
            so = Pos(bx0 + (12) / 2, yy, zz) * Rot(0, 90, 0) * (Cyl(3, 12) - Cyl(1.5, 12))
            P.add("PCB standoff, nylon M3 x 12", so, "hdpe_natural", kind="bought", bom=bom_ctrl)
            P.add("Lid screw M3 x 6, board to standoff box", z.aim(z.pan_screw(3, 6), (bx0 - 1.6, yy, zz), (1, 0, 0)), "stainless", kind="fastener", bom=bom_ctrl)
    mcu = z.box(bx0 - 1.6 - 12, bx0 - 1.6 - 10.4, cy_ - 26, cy_ + 26, cz_ - 10, cz_ + 15) + \
        z.box(bx0 - 1.6 - 10.4, bx0 - 1.6, cy_ - 26, cy_ - 23, cz_ - 10, cz_ + 15) + z.box(bx0 - 1.6 - 10.4, bx0 - 1.6, cy_ + 23, cy_ + 26, cz_ - 10, cz_ + 15)
    P.add("Microcontroller module on pin headers", mcu, "fr4", kind="bought", bom=bom_ctrl)
    term = z.box(bx0 - 1.6 - 10, bx0 - 1.6, cy_ - 60, cy_ + 60, cz_ - 38, cz_ - 28)
    P.add("Screw terminal block, fans, pump, sensors and supply", z.eased(term, 0.5), "hdpe_natural", kind="bought", bom=bom_ctrl)
    for yy in (cy_ - 40, cy_ + 40):
        g = Pos(xf - cd_ / 2, yy, z0c - 6) * (Cyl(10, 12) - Cyl(4, 12)) + Pos(xf - cd_ / 2, yy, z0c + 3) * Cyl(7.5, 6)
        P.add("Cable gland M16, nylon, into the controller box", g, "hdpe_black", kind="bought", bom=bom_ctrl)
    lamp = (Pos(lx, ly, z1c + lft / 2) * Cyl(lfl / 2, lft) + Pos(lx, ly, z1c - (cw + 3) / 2) * Cyl(lh / 2 - 0.5, cw + 3 + 0.01)
            + Pos(lx, ly, z1c + lft + (ldh - ldome / 2) / 2) * Cyl(ldome / 2, ldh - ldome / 2))
    from build123d import Sphere
    lamp = lamp + Pos(lx, ly, z1c + lft + ldh - ldome / 2) * Sphere(ldome / 2)
    P.add("Mode lamp, 22 mm three-color panel lamp", lamp, "polycarbonate", kind="bought", bom=bom_ctrl)
    sd, sn, st_, sp_, sz0, sr_, sdx, sy0 = p["SHIELD"]
    scx = xf - sdx
    zt = sz0 + sp_ * (sn - 1) + st_
    za0 = zt + 4                                       # arm above the top plate, stud hung from it
    arm = z.eased(z.box(scx - 10, xf - 3, sy0 - 10, sy0 + 10, za0, za0 + 10), 0.5)
    tab = z.box(xf - 3, xf, sy0 - 20, sy0 + 20, za0 - 25, za0 + 35)
    for zz in (za0 - 15, za0 + 25):
        tab = tab - Pos(xf - 1.5, sy0, zz) * Rot(0, 90, 0) * Cyl(3.5, 5)
    stud = Pos(scx, sy0, (sz0 - 10 + za0 + 10) / 2) * Cyl(sr_, za0 + 10 - sz0 + 10)
    P.add("Sensor arm, bent aluminium strip", (arm + z.eased(tab, 0.5)) - stud, "aluminium", bom=bom_ctrl)
    for zz in (za0 - 15, za0 + 25):
        P.add("Frame fixing 6 x 50, sensor arm to brick", z.aim(z.frame_fixing(6, 50), (xf - 3, sy0, zz), (1, 0, 0)), "hdpe_natural", kind="fastener", bom=bom_ctrl)
    P.add("Shield stud, stainless M6", stud, "stainless", kind="fastener", bom=bom_ctrl)
    for k in range(sn):
        pl = Pos(scx, sy0, sz0 + sp_ * k + st_ / 2) * (Cyl(sd / 2, st_) - Cyl(sr_, st_ + 1))
        if k < sn - 1:
            pl = pl - Pos(scx, sy0, sz0 + sp_ * k + st_ / 2) * Cyl(sd / 2 - 8, st_ + 1)
        P.add(f"Sensor shield plate {k + 1}, white plastic 46 mm", pl, "hdpe_natural", kind="bought", bom=bom_ctrl)
    sens = z.box(scx - 7, scx + 7, sy0 - 9 - 3 - 0.5, sy0 - 3 - 0.5, sz0 + 3, sz0 + 22)
    P.add("Outside temperature and RH sensor module", z.eased(sens, 0.5), "hdpe_natural", kind="bought", bom=bom_ctrl)
    # inside sensor on the aisle face of the right rack's middle post, about 1.5 m up (ZBX-BLD-001 s3.19.1)
    ya = p["IN_W"] / 2 - p["RACK_D"]                    # aisle face of the right rack's inner posts
    zs0 = p["FLOOR"] + 1500
    sc = z.aim(z.pan_screw(4, 30), (0, ya - 18, zs0 + 30), (0, 1, 0))
    ins = z.hollow_box(-20, 20, ya - 18, ya, zs0, zs0 + 60, 1.5, None, 1.0) - sc
    P.add("Inside temperature and RH sensor in a vented case", ins, "hdpe_natural", kind="bought", bom=bom_ctrl)
    P.add("Wood screw 4 x 30 pan head, inside sensor to rack post timber", sc, "zinc_plated", kind="fastener", bom=bom_ctrl)
    # power box: ventilated steel box with a plain door
    y0, y1, zb0, zb1 = -970.0, -750.0, 1000.0, 1300.0
    pb = z.hollow_box(xf - 100 + 1.5, xf, y0, y1, zb0, zb1, 1.5, "-x", 2.0)
    for k in range(4):
        zz = zb0 + 60 + k * 40
        for yy in (y0, y1):
            pb = pb - Pos(xf - 50, yy, zz) * Box(60, 4, 8)
    for yy in (y0 + 30, y1 - 30):
        for zz in (zb0 + 30, zb1 - 30):
            pb = pb - Pos(xf - 0.75, yy, zz) * Rot(0, 90, 0) * Cyl(3.5, 3)
    for xx in (xf - 30, xf - 75):
        pb = pb - Pos(xx, y1 - 25, zb0 + 0.75) * Cyl(8, 3)
    P.add("Power box, ventilated painted steel 100 x 220 x 300", pb, "painted_steel", kind="bought", bom=bom_power)
    door = z.box(xf - 100, xf - 98.5, y0, y1, zb0, zb1)
    for yy in (y0 + 10, y1 - 10):
        for zz in (zb0 + 10, zb1 - 10):
            door = door - Pos(xf - 99.25, yy, zz) * Rot(0, 90, 0) * Cyl(2.2, 3)
    P.add("Power box plain door, painted steel", z.eased(door, 0.5), "painted_steel", kind="bought", bom=bom_power)
    for yy in (y0 + 10, y1 - 10):
        for zz in (zb0 + 10, zb1 - 10):
            P.add("Lid screw 4 x 12, door to power box", z.aim(z.pan_screw(4, 10), (xf - 100, yy, zz), (1, 0, 0)), "stainless", kind="fastener", bom=bom_power)
    for yy in (y0 + 30, y1 - 30):
        for zz in (zb0 + 30, zb1 - 30):
            P.add("Frame fixing 6 x 60, power box to brick", z.aim(z.frame_fixing(6, 60), (xf - 1.5, yy, zz), (1, 0, 0)), "hdpe_natural", kind="fastener", bom=bom_power)
    batt = z.eased(z.box(xf - 96, xf - 8, y0 + 20, y0 + 171, zb0 + 1.5, zb0 + 1.5 + 95), 3.0)
    P.add("Battery, 12.8 V 12 Ah LiFePO4 with BMS", batt, "matte_black", kind="bought", bom=bom_power)
    cc = z.eased(z.box(xf - 48, xf - 8, y0 + 40, y0 + 180, zb1 - 100, zb1 - 10), 2.0)
    P.add("Charge controller, 20 A PWM", cc, "pe_tank_white", kind="bought", bom=bom_power)
    fh = z.eased(z.box(xf - 33, xf - 8, y1 - 40, y1 - 15, zb0 + 140, zb0 + 200), 1.0)
    P.add("Fuse holder, 15 A battery and 5 A load circuit", fh, "hdpe_black", kind="bought", bom=bom_power)
    for xx in (xf - 30, xf - 75):
        g = Pos(xx, y1 - 25, zb0 - 6) * (Cyl(10, 12) - Cyl(4, 12)) + Pos(xx, y1 - 25, zb0 + 1.5 + 3) * Cyl(7.5, 6)
        P.add("Cable gland M16, nylon, into the power box", g, "hdpe_black", kind="bought", bom=bom_power)


def _racks(P, p, C, bom=12, brackets=True):
    """Two racks: posts, rails and slats as separate pieces, every rail and slat screw, the wall brackets
    with their screws and fixings."""
    z = _zp()
    d = derived(p)
    fl = p["FLOOR"]
    hl, hw = p["IN_L"] / 2, p["IN_W"] / 2
    rl, rd, rp = p["RACK_L"], p["RACK_D"], p["RACK_POST"]
    rw, rh = p["RAIL"]
    sw, st = p["SLAT"]
    rack_h = max(p["SHELVES"]) + 350
    for s in (-1, 1):
        side = "left" if s < 0 else "right"
        yc = s * (hw - rd / 2)
        yi = rd / 2 - rp
        pxs = (-rl / 2 + rp / 2, 0, rl / 2 - rp / 2)
        for i, x in enumerate(pxs):
            for sy in (-1, 1):
                P.add(f"Rack {side} post {i + 1}{'a' if sy < 0 else 'b'}, treated timber 50 x 50",
                      z.sawn(x - rp / 2, x + rp / 2, *sorted((yc + sy * yi, yc + sy * (yi + rp))), fl, fl + rack_h, 2.0), "timber", bom=bom)
        for zsh in p["SHELVES"]:
            zs = fl + zsh
            for sy in (-1, 1):
                ya, yb = sorted((yc + sy * (yi - rw), yc + sy * yi))
                P.add(f"Rack {side} rail at {zsh:.0f} mm, treated timber 50 x 75", z.sawn(-rl / 2, rl / 2, ya, yb, zs - st - rh, zs - st, 2.0), "timber", bom=bom)
                for x in pxs:
                    for dz in (-rh / 4, rh / 4):
                        P.add("Wood screw 5 x 80, rail to post timber", z.aim(z.wood_screw(5, 80), (x, yc + sy * (yi - rw), zs - st - rh / 2 + dz), (0, sy, 0)),
                              "zinc_plated", kind="fastener", bom=bom)
            pitch = (rl - 2 * rp - sw) / (p["SLATS"] - 1)
            for k in range(p["SLATS"]):
                x = -rl / 2 + rp + sw / 2 + k * pitch
                P.add(f"Rack {side} slat, treated timber 95 x 25", z.sawn(x - sw / 2, x + sw / 2, yc - yi, yc + yi, zs - st, zs, 1.5), "timber", bom=bom)
                for sy in (-1, 1):
                    P.add("Nail 2.8 x 50, slat to rail timber", z.aim(z.nail(2.8, 50), (x, yc + sy * (yi - rw / 2), zs), (0, 0, -1)), "galvanised", kind="fastener", bom=bom)
        for x in (-rl / 2, rl / 2):
            if not brackets:
                break
            xo = 1 if x > 0 else -1
            zz = fl + rack_h - 35
            sc = z.aim(z.pan_screw(5, 50), (x + xo * 3, s * (hw - 20), zz), (-xo, 0, 0))
            ff = z.aim(z.frame_fixing(6, 60), (x + xo * 20, s * (hw - 3), zz), (0, s, 0))
            br = _rack_bracket(x, xo, s * hw, s, fl + rack_h)
            P.add(f"Rack {side} wall bracket, steel angle 40 x 40 x 3", z.eased(br, 0.6) - sc - ff, "galvanised", kind="bought", bom=bom)
            P.add("Wood screw 5 x 50 pan head, bracket to post timber", sc, "zinc_plated", kind="fastener", bom=bom)
            P.add("Frame fixing 6 x 60, bracket to brick", ff, "hdpe_natural", kind="fastener", bom=bom)


def _crates(P, p, bom=13, n_shelf=None):
    z = _zp()
    fl = p["FLOOR"]
    hw = p["IN_W"] / 2
    rd = p["RACK_D"]
    n, cl_ = n_shelf or p["CRATES_PER_SHELF"], p["CRATE_L"]
    for s in (-1, 1):
        yc = s * (hw - rd / 2)
        for zsh in p["SHELVES"]:
            for k in range(n):
                x = -(n - 1) * cl_ / 2 + k * cl_
                c = z.hollow_box(x - cl_ / 2 + 15, x + cl_ / 2 - 15, yc - p["CRATE_W"] / 2 + 5, yc + p["CRATE_W"] / 2 - 5, fl + zsh, fl + zsh + p["CRATE_H"] - 10, 4.0, "+z", 3.0)
                P.add("Produce crate, ventilated plastic, user supplied", c, "hdpe_natural", kind="bought", bom=bom)


# ------------------------------------------------------------------------------------------------ option A
def option_a(p=PARAMS, with_bom=True):
    P = _Parts(with_bom)
    C = build_components(p)
    _footing_walls_fill(P, p, C, "Dry rice husk with lime", "rice_husk")
    _door(P, p, C)
    _ceiling(P, p, C)
    _fan_box(P, p, C)
    _roof(P, p, C)
    _panel(P, p, C)
    _pad(P, p, C)
    _sump(P, p, C)
    _controls(P, p, C)
    _racks(P, p, C)
    _crates(P, p)
    return P


# ------------------------------------------------------------------------------------------------ option B
PARAMS_B = {   # option B first-order sizes (ZBX-OPT-001); room, walls, door, ceiling, roof and racks as option A
    "TANK_XY": (2400.0, -350.0), "STAND_H": 2200.0, "STAND_A": 700.0, "SHS": (40.0, 3.0),   # tank base above the drip ring
    "DRIP_OD": 20.0, "VENT_LOW": (200.0, 200.0, 300.0),      # low inlet vent in the pad end wall: w, h, centre height
    "STACK_OD": 110.0, "STACK_UP": 300.0, "STACK_XY": (-1000.0, 350.0),   # roof-space stack through the ceiling at the door end
}


def option_b(p=PARAMS, with_bom=False):
    """Passive wet-wall chamber: option A's room with wet sand in the cavity, a perforated drip ring on the sand,
    a 200 L header tank on a welded stand, a low inlet vent in the pad end wall and a ventilation stack through
    the ceiling; no fans, pump, pad, panel or controller."""
    import cad_parts as cp
    z = _zp()
    from build123d import Cylinder as Cyl, Sphere
    q = dict(p)
    q["PAD_W"], q["PAD_H"] = PARAMS_B["VENT_LOW"][0] - 2 * p["LINING"], PARAMS_B["VENT_LOW"][1] - 2 * p["LINING"]
    q["PAD_Z"] = PARAMS_B["VENT_LOW"][2] + p["FLOOR"]
    P = _Parts(with_bom)
    C = build_components(q)
    _footing_walls_fill(P, q, C, "Wet sand", "wet_sand")
    _door(P, q, C)
    _ceiling(P, q, C, fan_box=False)
    _roof(P, q, C)
    _racks(P, q, C)
    d = derived(q)
    xb, top = d["out_l"] / 2, d["top"]
    for k, s in enumerate(C["pad_lining"][1]):
        P.add(f"Low vent lining {k + 1}, treated timber 20 mm", z.eased(s, 1.5), "timber")
    vw, vh, vz = PARAMS_B["VENT_LOW"]
    from build123d import Box as Bx
    mesh = Pos(xb + 5.0, 0, vz + p["FLOOR"]) * Rot(0, 0, 90) * Pos(0, 0, -vh / 2 + 10) * cp.mesh_panel(vw - 20, vh - 20, 12.5, 1.2, frame=10)
    P.add("Low vent insect mesh, galvanised 12.5 mm", mesh, "galvanised", kind="bought")
    # drip ring: perforated PVC laid on the sand at the cavity mid-line, under the capping course
    leaf, cav = q["LEAF"], q["CAV"]
    ix, iy = q["IN_L"] / 2 + leaf, q["IN_W"] / 2 + leaf
    zc = top - q["CAP"] - 30
    od = PARAMS_B["DRIP_OD"]
    m = cav / 2
    pts = [(-ix - m, -iy - m), (ix + m, -iy - m), (ix + m, iy + m), (-ix - m, iy + m), (-ix - m, -iy - m)]
    ring, env = None, None
    for k, (a, b) in enumerate(zip(pts[:-1], pts[1:])):
        a2 = (a[0] - (od / 2 if b[0] > a[0] else -od / 2 if b[0] < a[0] else 0), a[1] - (od / 2 if b[1] > a[1] else -od / 2 if b[1] < a[1] else 0), zc)
        tb = z.tube_between(a2, (b[0], b[1], zc), od, 2.0)
        eb = z.tube_between(a2, (b[0], b[1], zc), od + 1)
        ring = tb if ring is None else ring.fuse(tb)
        env = eb if env is None else env.fuse(eb)
    P.add("Drip ring, perforated PVC 20 mm with elbows", ring, "pvc")
    # the drip ring sits in a channel left in the sand under the capping course
    for prt in P:
        if "cavity fill" in prt["name"]:
            prt["shape"] = prt["shape"] - env
    tx, ty = PARAMS_B["TANK_XY"]
    H, A = PARAMS_B["STAND_H"], PARAMS_B["STAND_A"]
    s_a, s_t = PARAMS_B["SHS"]
    pad_t = 100.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            lx, ly = tx + sx * (A / 2 - s_a / 2), ty + sy * (A / 2 - s_a / 2)
            _stand_foot(P, lx, ly, H, s_a, s_t, pad_t)
    _stand_top(P, tx, ty, H, A, s_a, s_t)
    # gravity feed: down from the tank's bottom tap outside the end wall, then in through the outer leaf to the ring
    xr_ = tx - A / 2 - s_a / 2 - 13                     # outside the stand's cross rail
    feed = z.tube_between((xr_, ty, H + 60), (xr_, ty, zc - 12.5), 25, 2.5).fuse(
        z.tube_between((xr_ + 12.5, ty, zc), (ix + m + od / 2, ty, zc), 25, 2.5))
    feed = feed.fuse(Pos(xr_, ty, zc) * Sphere(12.5) - Pos(xr_, ty, zc) * Sphere(10))
    tap = z.tube_between((tx - 299, ty, H + 60), (xr_ + 12.5, ty, H + 60), 25, 2.5)
    P.add("Feed pipe, PVC 25 mm, tank to drip ring", feed.fuse(tap), "pvc")
    bore = z.tube_between((xr_, ty, zc), (ix + m + od / 2 - 1, ty, zc), 26)
    for prt in P:
        if prt["name"].startswith("Outer brick leaf, pad end") or prt["name"].endswith("cavity fill, pad end"):
            prt["shape"] = prt["shape"] - bore
    dial = Pos(-d["out_l"] / 2, 600, 1500) * Rot(0, -90, 0) * (Cyl(50, 25).moved(Pos(0, 0, 12.5)) + (Cyl(53, 6) - Cyl(46, 6)).moved(Pos(0, 0, 25)))
    ff = z.aim(z.frame_fixing(6, 50), (-d["out_l"] / 2 - 25, 600, 1500), (1, 0, 0))
    P.add("Dial thermometer and hygrometer, outside face", dial - ff, "stainless", kind="bought")
    P.add("Frame fixing 6 x 50, dial to brick", ff, "hdpe_natural", kind="fastener")
    # ventilation stack through the ceiling boards at the door end, between two purlins, with a cowl
    (sxs, sys_), so = PARAMS_B["STACK_XY"], PARAMS_B["STACK_OD"]
    for prt in P:
        if prt["name"].startswith("Ceiling") and ("board" in prt["name"] or "insulation" in prt["name"]):
            prt["shape"] = prt["shape"] - Pos(sxs, sys_, top + 60) * Cyl(so / 2 + 1, 200)
    hstack = q["JOIST"][1] + q["DECK_T"] + PARAMS_B["STACK_UP"]
    stack = Pos(sxs, sys_, top + 1) * cp.round_tube(so, 3.2, hstack)
    P.add("Ventilation stack, PVC 110 mm", stack, "pvc")
    cowl = Pos(sxs, sys_, top + 1 + hstack + 30) * (Cyl(110, 4) + Pos(0, 0, -20) * (Cyl(110, 40) - Cyl(106, 40)))
    P.add("Stack rain cowl, galvanised", cowl, "galvanised", kind="bought")
    return P


def _stand_foot(P, lx, ly, H, s_a, s_t, pad_t=100.0):
    """One leg of a header-tank stand: concrete pad, base plate, SHS leg, weld and two anchors."""
    import cad_parts as cp
    z = _zp()
    anchors = [Pos(lx + hx, ly + hy, 6) * cp.anchor_bolt(10, 80) for hx, hy in ((35, 35), (-35, -35))]
    padc = z.eased(z.box(lx - 100, lx + 100, ly - 100, ly + 100, -pad_t, 0), 4.0)
    for a_ in anchors:
        padc = padc - a_
    P.add("Stand pad, concrete 200 x 200", padc, "concrete")
    P.add("Stand leg, painted steel SHS 40 x 40 x 3", Pos(lx, ly, 6) * cp.shs(s_a, s_t, H - 6 - s_a), "painted_steel")
    P.add("Stand base plate, steel 100 x 100 x 6", Pos(lx, ly, 0) * cp.sheet(100, 100, 6, holes=[(35, 35, 12), (-35, -35, 12)]), "painted_steel")
    P.add("Weld, leg to base plate, painted steel", Pos(lx, ly, 6) * _sq_weld(s_a, 4.0), "painted_steel", kind="weld")
    for a_ in anchors:
        P.add("Concrete anchor M10, stand base plate", a_, "galvanised", kind="fastener")


def _stand_top(P, tx, ty, H, A, s_a, s_t):
    """Top frame of a header-tank stand (two rails, two cross rails, leg welds) and the 200 L drum on it."""
    import cad_parts as cp
    for nm, yy in (("front", ty - A / 2 + s_a / 2), ("back", ty + A / 2 - s_a / 2)):
        P.add(f"Stand top rail {nm}, painted steel SHS 40 x 40 x 3", Pos(tx - A / 2, yy, H - s_a / 2) * Rot(0, 90, 0) * cp.shs(s_a, s_t, A), "painted_steel")
    for nm, xx in (("left", tx - A / 2 + s_a / 2), ("right", tx + A / 2 - s_a / 2)):
        P.add(f"Stand cross rail {nm}, painted steel SHS 40 x 40 x 3", Pos(xx, ty - A / 2 + s_a, H - s_a / 2) * Rot(-90, 0, 0) * cp.shs(s_a, s_t, A - 2 * s_a), "painted_steel")
    for sx in (-1, 1):
        for sy in (-1, 1):
            lx, ly = tx + sx * (A / 2 - s_a / 2), ty + sy * (A / 2 - s_a / 2)
            P.add("Weld, leg to top rail, painted steel", Pos(lx, ly, H - s_a) * _sq_weld(s_a, 4.0), "painted_steel", kind="weld")
    P.add("Header tank, 200 L drum with bung tap", Pos(tx, ty, H) * cp.drum_200l(), "pe_tank_silver", kind="bought")


def _sq_weld(a, leg):
    """Fillet weld round a square tube a x a standing on a plate at z = 0 (four straight beads)."""
    import cad_parts as cp
    out = None
    for k in range(4):
        b = Rot(0, 0, 90 * k) * Pos(-a / 2, -a / 2, 0) * Rot(0, 0, -90) * cp.weld_fillet(a, leg)
        out = b if out is None else out + b
    return out


# ------------------------------------------------------------------------------------------------ option C
PARAMS_C = {   # option C first-order sizes (ZBX-OPT-001): same 2.4 x 1.5 x 2.0 m room and racks
    "SLAB_T": 100.0, "POST": 75.0, "CHAR_T": 100.0, "WALL_H": 2000.0, "MESH_P": 12.5, "MESH_D": 1.6,
    "RAFTER": (50.0, 100.0), "VENT_D": 300.0, "TANK_XY": (2050.0, -700.0), "STAND_H": 2250.0,   # tank base above the drip pipes
}


def option_c(p=PARAMS, with_bom=False):
    """Charcoal-wall wind cooler: timber frame on a concrete slab, walls of lump charcoal 100 mm thick between
    inner and outer welded meshes, a drip pipe threaded through the posts along every wall top fed from a header
    tank, a sheeted roof on rafters with a turbine ventilator, a meshed charcoal door, and option A's racks."""
    import cad_parts as cp
    z = _zp()
    from build123d import Cylinder as Cyl
    P = _Parts(with_bom)
    C = build_components(p)
    pc = PARAMS_C
    hl, hw = p["IN_L"] / 2, p["IN_W"] / 2
    tp, ct = pc["POST"], pc["CHAR_T"]
    md = pc["MESH_D"]
    mt = 2 * md                                       # mesh panel depth (two wire layers)
    st = pc["SLAB_T"]
    wh = pc["WALL_H"]
    ox, oy = hl + mt + ct + mt, hw + mt + ct + mt       # outside faces of the outer meshes
    slab = z.box(-ox - 150, ox + 150, -oy - 150, oy + 150, 0, st)
    zb, ztp = st, st + wh
    xs_p = (-hl - mt - ct / 2, 0.0, hl + mt + ct / 2)
    ys_p = (-hw - mt - ct / 2, hw + mt + ct / 2)
    posts = [(x, y) for x in xs_p for y in ys_p] + [(hl + mt + ct / 2, 0.0)]   # the door is in the middle of the door end
    zc = ztp - 30
    runs = [((-hl - mt - ct / 2, ys_p[0]), (hl + mt + ct / 2, ys_p[0])), ((-hl - mt - ct / 2, ys_p[1]), (hl + mt + ct / 2, ys_p[1])),
            ((xs_p[2], -hw + 60), (xs_p[2], hw - 60))]
    pipes = [z.tube_between((a[0], a[1], zc), (b[0], b[1], zc), 20, 2.0) for a, b in runs]
    bores = [z.tube_between((a[0], a[1], zc), (b[0], b[1], zc), 21) for a, b in runs]
    anchors = []
    for k, (x, y) in enumerate(posts):
        post = z.sawn(x - tp / 2, x + tp / 2, y - tp / 2, y + tp / 2, zb + 30, ztp, 2.0)
        for b_ in bores:
            post = post - b_
        P.add(f"Wall post {k + 1}, treated timber 75 x 75", post, "timber")
        base = z.box(x - tp / 2 - 3, x + tp / 2 + 3, y - 20, y + 20, zb, zb + 6)
        anc = base + z.box(x - tp / 2 - 3, x - tp / 2, y - 20, y + 20, zb, zb + 120) + z.box(x + tp / 2, x + tp / 2 + 3, y - 20, y + 20, zb, zb + 120)
        pts_a = [Pos(x, y, zb + 6) * cp.anchor_bolt(12, 80)]     # under the post, which stands 24 mm clear on the bracket
        for a_ in pts_a:
            anc = anc - Pos(0, 0, 0) * a_
        for sx in (-1, 1):
            anc = anc - Pos(x + sx * (tp / 2 + 1.5), y, zb + 80) * Rot(0, 90, 0) * Cyl(5.0, 5)
        P.add("Post base, galvanised steel U bracket", anc, "galvanised", kind="bought")
        for a_ in pts_a:
            P.add("Concrete anchor M12, post base", a_, "galvanised", kind="fastener")
            anchors.append(a_)
        for sx in (-1, 1):
            P.add("Coach screw M8 x 50, post base into post timber", z.aim(cp.coach_screw(8, 50), (x + sx * (tp / 2 + 3), y, zb + 80), (-sx, 0, 0)),
                  "galvanised", kind="fastener")
    for a_ in anchors:
        slab = slab - a_
    P.add("Floor slab, concrete 100 mm", slab, "concrete")
    # top plates round the frame, over the charcoal layer
    tx0, tx1 = -hl - mt - ct, hl + mt + ct
    ty0, ty1 = -hw - mt - ct, hw + mt + ct
    for nm, bxs in (("long left", (tx0, tx1, ty0, ty0 + ct)), ("long right", (tx0, tx1, ty1 - ct, ty1)),
                    ("door end", (tx0, tx0 + ct, ty0 + ct, ty1 - ct)), ("back end", (tx1 - ct, tx1, ty0 + ct, ty1 - ct))):
        P.add(f"Top plate {nm}, treated timber 100 x 50", z.sawn(*bxs, ztp, ztp + 50, 2.0), "timber")
    for x, y in posts:
        for dd in (-22, 22):
            pt_ = (x + dd, y, ztp + 50) if abs(y) < 1 else (x, y + dd, ztp + 50)      # clear of the drip pipe bored through the post
            P.add("Nail 4 x 100, top plate to post timber", z.aim(z.nail(4, 100), pt_, (0, 0, -1)), "galvanised", kind="fastener")
    # charcoal walls, cut round the posts, their bases and the drip pipes, leaving the 800 x 1800 door opening
    dw, dh = 800.0, 1800.0
    cut = None
    for x, y in posts:
        b = z.box(x - tp / 2 - 1, x + tp / 2 + 1, y - tp / 2 - 1, y + tp / 2 + 1, zb, ztp + 60) + z.box(x - tp / 2 - 45, x + tp / 2 + 45, y - 25, y + 25, zb, zb + 130)
        cut = b if cut is None else cut + b
    for b_ in bores:
        cut = cut + b_
    door_cut = z.box(-ox - 10, -hl + 10, -dw / 2 - 40, dw / 2 + 40, zb - 1, zb + dh + 40)
    chars = [("long left", z.box(-hl - mt, hl + mt, -hw - mt - ct, -hw - mt, zb, ztp)),
             ("long right", z.box(-hl - mt, hl + mt, hw + mt, hw + mt + ct, zb, ztp)),
             ("door end", z.box(-hl - mt - ct, -hl - mt, -hw - mt, hw + mt, zb, ztp)),
             ("back end", z.box(hl + mt, hl + mt + ct, -hw - mt, hw + mt, zb, ztp))]
    for nm, ch in chars:
        ch = ch - cut - door_cut
        if nm == "door end":
            ch = ch - z.box(-ox, -hl, -dw / 2 - 40, dw / 2 + 40, zb + dh + 40, ztp + 1)
        P.add(f"Charcoal wall {nm}, lump charcoal 100 mm", ch, "charcoal")
    P.add("Charcoal over the door head, lump charcoal", z.eased(z.box(-hl - mt - ct, -hl - mt, -dw / 2 - 40, dw / 2 + 40, zb + dh + 41, ztp), 2.0), "charcoal")
    # meshes: rods within mt of the charcoal faces (room side face 0.1 mm off the room boundary)

    def mesh_y(x0, x1, ylo):
        """Mesh panel parallel to XZ whose wires occupy y from ylo to ylo + 3.2."""
        pnl = cp.mesh_panel(x1 - x0 - 20, wh - 20, pc["MESH_P"], md)
        return Pos((x0 + x1) / 2, ylo + md / 2, zb + 10) * pnl

    def mesh_x(y0, y1, xlo, h=None, z0=None):
        """Mesh panel parallel to YZ whose wires occupy x from xlo to xlo + 3.2."""
        pnl = cp.mesh_panel(y1 - y0 - 20, (h or wh) - 20, pc["MESH_P"], md)
        return Pos(xlo + 2.4, (y0 + y1) / 2, (z0 if z0 is not None else zb) + 10) * Rot(0, 0, 90) * pnl
    for sgn, nm in ((-1, "left"), (1, "right")):
        lo_in = hw + 0.1 if sgn > 0 else -hw - 0.1 - 3.2
        lo_out = hw + mt + ct + 0.1 if sgn > 0 else -(hw + mt + ct + 0.1) - 3.2
        P.add(f"Inner mesh, long wall {nm}, galvanised welded 12.5 mm", mesh_y(-hl, hl, lo_in), "galvanised", kind="bought")
        P.add(f"Outer mesh, long wall {nm}, galvanised welded 12.5 mm", mesh_y(-ox, ox, lo_out), "galvanised", kind="bought")
    P.add("Inner mesh, back end wall, galvanised welded 12.5 mm", mesh_x(-hw, hw, hl + 0.1), "galvanised", kind="bought")
    P.add("Outer mesh, back end wall, galvanised welded 12.5 mm", mesh_x(-oy + 20, oy - 20, hl + mt + ct + 0.1), "galvanised", kind="bought")
    for sgn, nm in ((-1, "left"), (1, "right")):
        ya, yb = sorted((sgn * (dw / 2 + 45), sgn * hw))
        P.add(f"Inner mesh, door end {nm}, galvanised welded 12.5 mm", mesh_x(ya, yb, -hl - 0.1 - 3.2), "galvanised", kind="bought")
        ya, yb = sorted((sgn * (dw / 2 + 45), sgn * (oy - 20)))
        P.add(f"Outer mesh, door end {nm}, galvanised welded 12.5 mm", mesh_x(ya, yb, -(hl + mt + ct + 0.1) - 3.2), "galvanised", kind="bought")
    for x, y in posts:
        for zz in (zb + 300, zb + 1000, zb + 1700):
            if abs(abs(y) - ys_p[1]) < 1:
                sgn = 1 if y > 0 else -1
                P.add("Nail 2.5 x 30 staple, outer mesh to post timber", z.aim(z.nail(2.5, 30), (x + 20, sgn * (oy + 0.1), zz), (0, -sgn, 0)), "galvanised", kind="fastener")
            else:
                sgn = 1 if x > 0 else -1
                P.add("Nail 2.5 x 30 staple, outer mesh to post timber", z.aim(z.nail(2.5, 30), (sgn * (ox + 0.1), y + 20, zz), (-sgn, 0, 0)), "galvanised", kind="fastener")
    # door: jambs and head across the wall thickness, a framed leaf holding a charcoal panel, two hinges
    for nm, (ya, yb) in (("jamb left", (-dw / 2 - 40, -dw / 2)), ("jamb right", (dw / 2, dw / 2 + 40))):
        P.add(f"Door frame {nm}, treated timber 40 x 110", z.sawn(-ox, -hl, ya, yb, zb, zb + dh + 40, 1.5), "timber")
    P.add("Door frame head, treated timber 40 x 110", z.sawn(-ox, -hl, -dw / 2, dw / 2, zb + dh, zb + dh + 40, 1.5), "timber")
    dx0, dx1 = -ox + 5, -hl - 5
    leaf = z.box(dx0, dx1, -dw / 2 + 3, dw / 2 - 3, zb + 5, zb + dh - 3) - z.box(dx0 - 1, dx1 + 1, -dw / 2 + 50, dw / 2 - 50, zb + 50, zb + dh - 50)
    P.add("Door leaf frame, treated timber 50 x 100", leaf, "timber")
    P.add("Door charcoal panel, lump charcoal", z.eased(z.box(dx0 + 4, dx1 - 4, -dw / 2 + 50, dw / 2 - 50, zb + 50, zb + dh - 50), 3.0), "charcoal")
    for sgn in (-1, 1):
        P.add(f"Door panel mesh {'outer' if sgn < 0 else 'inner'}, galvanised welded 12.5 mm",
              mesh_x(-dw / 2 + 50, dw / 2 - 50, dx0 if sgn < 0 else dx1 - 3.2, h=dh - 100, z0=zb + 50), "galvanised", kind="bought")
    for kn_z in (zb + 300, zb + 1500):
        kn, pin = cp.butt_hinge(100, 32, 1.5, 5, open_deg=0)
        kn = kn - pin
        P.add("Door hinge, 100 mm steel butt", Pos(dx0 + 4, -dw / 2 + 1.5, kn_z - 50) * kn, "zinc_plated", kind="bought")
        P.add("Door hinge pin", Pos(dx0 + 4, -dw / 2 + 1.5, kn_z - 50) * pin, "zinc_plated", kind="fastener")
        for zz in (kn_z - 30, kn_z + 30):
            P.add("Wood screw 4 x 30, hinge to frame timber", z.aim(z.wood_screw(4, 30), (dx0 + 20, -dw / 2, zz), (0, -1, 0)), "zinc_plated", kind="fastener")
            P.add("Wood screw 4 x 30, hinge to door timber", z.aim(z.wood_screw(4, 30), (dx0 + 20, -dw / 2 + 3, zz), (0, 1, 0)), "zinc_plated", kind="fastener")
    for k, pp in enumerate(pipes):
        P.add(f"Drip pipe run {k + 1}, perforated PVC 20 mm, through the posts", pp, "pvc")
    # roof: rafters over the top plates, two box-profile sheets, a turbine ventilator over a 300 mm throat
    rw_, rh_ = pc["RAFTER"]
    zr = ztp + 50
    span_y = (ty0 - 300, ty1 + 300)
    xr = [tx0 + 25, -hl / 2 - 100, hl / 2 + 100, tx1 - 25]
    for k, x in enumerate(xr):
        P.add(f"Rafter {k + 1}, treated timber 50 x 100", z.sawn(x - rw_ / 2, x + rw_ / 2, span_y[0], span_y[1], zr, zr + rh_, 2.0), "timber")
        for y in (ty0 + ct / 2, ty1 - ct / 2):
            P.add("Coach screw M8 x 140, rafter to top plate timber", z.aim(cp.coach_screw(8, 140), (x, y, zr + rh_ - 8), (0, 0, -1)), "galvanised", kind="fastener")
    vd = pc["VENT_D"]
    roof_len = tx1 - tx0 + 600
    throat_cut = Pos(0, 0, zr + rh_) * Cyl(vd / 2 + 2, 200)
    for k, xc in enumerate((-roof_len / 4, roof_len / 4)):
        sh = Pos(xc, (span_y[0] + span_y[1]) / 2, zr + rh_ + 12.75) * z.corrugated(span_y[1] - span_y[0], roof_len / 2 - 1, t=0.5, pitch=190.0, depth=24.5)
        P.add(f"Roof sheet {k + 1}, box-profile galvanised steel 0.5 mm", sh - throat_cut, "galvanised")
    for x in xr:
        for y in (span_y[0] + 150, span_y[1] - 150):
            P.add("Roofing screw 6 x 100, sheet to rafter timber", z.aim(z.roofing_screw(6, 100), (x, y, zr + rh_ + 25), (0, 0, -1)), "galvanised", kind="fastener")
    throat = Pos(0, 0, zr + rh_) * cp.round_tube(vd, 1.0, 180)
    P.add("Turbine ventilator throat, galvanised 300 mm", throat, "galvanised", kind="bought")
    head = Pos(0, 0, zr + rh_ + 183) * Cyl(vd / 2 + 40, 6)
    for k in range(18):
        head = head + Pos(0, 0, zr + rh_ + 186) * Rot(0, 0, 20 * k) * Pos(vd / 2 + 30, 0, 110) * Rot(0, 0, 30) * Box(60, 1.5, 220)
    head = head + Pos(0, 0, zr + rh_ + 186 + 223) * Cyl(vd / 2 + 40, 6)
    P.add("Turbine ventilator head, galvanised 300 mm", head, "galvanised", kind="bought")
    # header tank on a welded stand beside the back wall, gravity feed to the drip pipes
    tx, ty = pc["TANK_XY"]
    H = pc["STAND_H"]
    A, s_a, s_t = 700.0, 40.0, 3.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            _stand_foot(P, tx + sx * (A / 2 - s_a / 2), ty + sy * (A / 2 - s_a / 2), H, s_a, s_t)
    _stand_top(P, tx, ty, H, A, s_a, s_t)
    xr_ = tx - A / 2 - s_a / 2 - 13
    feed = z.tube_between((xr_, ty, H + 60), (xr_, ty, zc - 12.5), 25, 2.5).fuse(
        z.tube_between((xr_ - 12.5, ty, zc), (ox + 5, ty, zc), 25, 2.5)).fuse(
        z.tube_between((tx - 299, ty, H + 60), (xr_ + 12.5, ty, H + 60), 25, 2.5))
    P.add("Feed pipe, PVC 25 mm, tank to drip pipes (to a tee at the back wall)", feed, "pvc")
    sc = z.aim(z.wood_screw(5, 50), (-ox - 25, -dw / 2 - 20, 1500), (1, 0, 0))
    dial = Pos(-ox, -dw / 2 - 20, 1500) * Rot(0, -90, 0) * (Cyl(50, 25).moved(Pos(0, 0, 12.5)) + (Cyl(53, 6) - Cyl(46, 6)).moved(Pos(0, 0, 25)))
    P.add("Dial thermometer and hygrometer on the door jamb", dial - sc, "stainless", kind="bought")
    P.add("Wood screw 5 x 50, dial to jamb timber", sc, "zinc_plated", kind="fastener")
    _racks(P, dict(p, FLOOR=st), C, brackets=False)
    return P


from build123d import Box, Location, Plane, Pos, Rot, Vector  # noqa: E402,F811  (used by the option builders)


def components(option=CHOSEN):
    """Kit 1.9: the detailed parts of one option, as cad_parts.part() dicts (BOM lines on the chosen option)."""
    return list({"A": option_a, "B": option_b, "C": option_c}[option]())


def _export_stl():
    import copy
    from build123d import Compound, export_stl
    import cad_parts as cp
    root = Path(__file__).resolve().parents[1]
    (root / "stl").mkdir(exist_ok=True)
    parts = [q for q in components(CHOSEN) if q["kind"] != "context"]
    groups = {"zeerbox-assembly": parts,
              "zeerbox-structure": [q for q in parts if q["bom"] in UNITS["zeerbox-structure"]],
              "zeerbox-cooling-kit": [q for q in parts if q["bom"] in UNITS["zeerbox-cooling-kit"]]}
    for name, ps in groups.items():
        export_stl(Compound([copy.copy(q["shape"]) for q in ps if q["kind"] in ("made", "bought")]), str(root / "stl" / f"{name}.stl"),
                   tolerance=0.2, angular_tolerance=0.35)
    for opt in OPTIONS:
        real = [q for q in components(opt) if q["kind"] != "context"]
        print(f"option {opt}: {len(real)} parts, {sum(cp.mass_kg(q) for q in real) / 1000:.2f} t")
    print("wrote cad/stl/*.stl (chosen design, made and bought parts, 0.2 mm chord)")


if __name__ == "__main__":
    if "--check" in sys.argv:
        n, fails = check()
        sys.exit(1 if fails else 0)
    _export_stl()
