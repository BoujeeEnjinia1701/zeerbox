"""ZeerBox parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl, and prints the key dimensions.

Massing-plus level of detail: correct interfaces and main dimensions, not
fabrication detail. Coordinates in mm. X runs along the store (door and fans at
-X, pad at +X), Y across it, Z up, ground at Z = 0. The storage room is centered
on the origin in plan. Figures and checks are in ZBX-CAL-001
(python docs/04-calcs/sizing.py), which reads PARAMS and derived() from here.

PRELIMINARY, NOT FOR FABRICATION.
"""
import math
from pathlib import Path

# Top-level parameters (mm unless stated). Edit these, not the geometry below.
PARAMS = {
    # storage room, inside faces of the inner brick leaf
    "IN_L": 2400.0, "IN_W": 1500.0, "IN_H": 2000.0,
    "FLOOR": 100.0,            # brick floor on compacted sand; top of floor above ground
    "LEAF": 115.0,             # fired-brick leaf (DDR-001 item 9 still open: fired brick is the working choice)
    "CAV": 75.0,               # wet sand cavity
    # openings
    "DOOR_W": 800.0, "DOOR_H": 1800.0,
    "FAN_D": 250.0, "FAN_Y": 575.0, "FAN_Z": 1650.0,   # two exhaust fans beside the door
    "PAD_W": 600.0, "PAD_H": 500.0, "PAD_T": 100.0, "PAD_Z": 1250.0,  # pad center height above ground
    # ceiling and shade roof
    "CEIL_T": 120.0,           # boards, 50 mm straw or foam, vapor sheet, joists
    "ROOF_CLEAR": 450.0,       # air gap between ceiling and roof sheet
    "ROOF_L": 3900.0, "ROOF_W": 3000.0, "ROOF_PITCH_DEG": 4.0,
    "POST_D": 90.0, "POST_X": 1850.0, "POST_Y": 1400.0,
    "FOOTING": 500.0, "FOOTING_DEPTH": 600.0,          # concrete post footing, square side and depth (CAL-001 section 8)
    # racks and crates
    "RACK_L": 2200.0, "RACK_D": 450.0, "RACK_POST": 50.0,
    "SHELVES": (300.0, 850.0, 1400.0),                 # shelf top heights above the floor
    "CRATE_L": 500.0, "CRATE_W": 350.0, "CRATE_H": 300.0, "CRATES_PER_SHELF": 4,
    # water
    "SUMP_D": 380.0, "SUMP_H": 600.0,                  # about 68 L gross, 60 L working
    # solar (150 W panel, DDR-001 item 2)
    "PANEL_L": 1480.0, "PANEL_W": 670.0, "PANEL_T": 35.0, "PANEL_TILT_DEG": 15.0,
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
    return {
        "wall": wall, "out_l": out_l, "out_w": out_w, "top": top, "ceil_top": ceil_top,
        "roof_z": roof_z, "aisle": aisle,
        "room_volume_m3": p["IN_L"] * p["IN_W"] * p["IN_H"] / 1e9,
        "pad_area_m2": p["PAD_W"] * p["PAD_H"] / 1e6,
        "fan_area_m2": fan_area,
        "door_area_m2": p["DOOR_W"] * p["DOOR_H"] / 1e6,
        "crates": 2 * len(p["SHELVES"]) * p["CRATES_PER_SHELF"],
        "top_shelf_m": max(p["SHELVES"]) / 1000,
        "roof_area_m2": p["ROOF_L"] * p["ROOF_W"] / 1e6,
    }


def _tube(a, b, r):
    from build123d import Plane, Solid, Vector
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def build_parts(p=PARAMS):
    """Return {bom_no: (name, shape)} for the modelled BOM lines (item 14, wiring and plumbing, is not modelled)."""
    from build123d import Box, Cylinder, Pos, Rot
    d = derived(p)
    wall, out_l, out_w, top = d["wall"], d["out_l"], d["out_w"], d["top"]
    xf, xb = -out_l / 2, out_l / 2
    leaf, fl = p["LEAF"], p["FLOOR"]

    def block(l, w):
        return Pos(0, 0, top / 2) * Box(l, w, top)

    openings = (Pos(xf, 0, fl + p["DOOR_H"] / 2) * Box(2 * wall + 40, p["DOOR_W"], p["DOOR_H"])
                + Pos(xb, 0, p["PAD_Z"]) * Box(2 * wall + 40, p["PAD_W"], p["PAD_H"]))
    for s in (-1, 1):
        openings = openings + Pos(xf, s * p["FAN_Y"], p["FAN_Z"]) * Rot(0, 90, 0) * Cylinder(p["FAN_D"] / 2, 2 * wall + 40)

    parts = {}
    # 1 Double brick walls and floor
    outer = block(out_l, out_w) - block(out_l - 2 * leaf, out_w - 2 * leaf)
    inner = block(p["IN_L"] + 2 * leaf, p["IN_W"] + 2 * leaf) - block(p["IN_L"], p["IN_W"])
    floor = Pos(0, 0, fl / 2) * Box(p["IN_L"], p["IN_W"], fl)
    parts[1] = ("Double brick walls and floor", outer + inner - openings + floor)

    # 2 Wet sand cavity fill with the perforated wetting pipe along the top
    sand = block(out_l - 2 * leaf, out_w - 2 * leaf) - block(p["IN_L"] + 2 * leaf, p["IN_W"] + 2 * leaf) - openings
    parts[2] = ("Wet sand cavity fill", sand)

    # 3 Insulated ceiling slab over the walls
    parts[3] = ("Insulated ceiling", Pos(0, 0, top + p["CEIL_T"] / 2) * Box(out_l, out_w, p["CEIL_T"]))

    # 4 Shade roof on four posts
    rz, px, py = d["roof_z"], p["POST_X"], p["POST_Y"]
    rise = math.tan(math.radians(p["ROOF_PITCH_DEG"]))
    roof = Pos(0, 0, rz) * Rot(p["ROOF_PITCH_DEG"], 0, 0) * Box(p["ROOF_L"], p["ROOF_W"], 25)
    for sx in (-1, 1):
        for sy in (-1, 1):
            roof = roof + _tube((sx * px, sy * py, 0), (sx * px, sy * py, rz - 15 + sy * py * rise), p["POST_D"] / 2)
    parts[4] = ("Shade roof on posts", roof)

    # 5 Insulated door with seal, in the front opening
    parts[5] = ("Insulated door with seal",
                Pos(xf + 30, 0, fl + p["DOOR_H"] / 2) * Box(50, p["DOOR_W"] - 10, p["DOOR_H"] - 10))

    # 6 Cellulose pad in a frame on the back wall, with drip header and return gutter
    pt, pw, ph, pz = p["PAD_T"], p["PAD_W"], p["PAD_H"], p["PAD_Z"]
    pad_x = xb + pt / 2 + 10
    frame = Pos(pad_x, 0, pz) * (Box(pt + 20, pw + 100, ph + 100) - Box(pt + 40, pw, ph))
    header = Pos(pad_x, 0, pz + ph / 2 + 80) * Rot(90, 0, 0) * Cylinder(16, pw + 160)
    gutter = Pos(pad_x + 10, 0, pz - ph / 2 - 80) * (Box(150, pw + 160, 60) - Pos(0, 0, 15) * Box(120, pw + 140, 60))
    media = Pos(pad_x, 0, pz) * Box(pt, pw, ph)
    parts[6] = ("Cellulose pad, frame, header, gutter", frame + header + gutter + media)

    # 7 Sump drum with 12 V pump, feed and return hoses
    dx, dy, dr, dh = xb + 450, -750.0, p["SUMP_D"] / 2, p["SUMP_H"]
    hz = pz + ph / 2 + 80
    sump = (Pos(dx, dy, dh / 2) * Cylinder(dr, dh)
            + _tube((dx, dy, dh), (dx, dy, hz), 12)
            + _tube((dx, dy, hz), (pad_x, -pw / 2 - 60, hz), 12)
            + _tube((pad_x + 10, -pw / 2 - 60, pz - ph / 2 - 80), (dx, dy + 60, dh - 20), 16))
    parts[7] = ("Sump drum, 12 V pump and hoses", sump)

    # 8 Two 250 mm 12 V DC exhaust fans with guards and shutters, beside the door
    fr = p["FAN_D"] / 2
    fans = None
    for s in (-1, 1):
        f = (Pos(xf - 35, s * p["FAN_Y"], p["FAN_Z"]) * Rot(0, 90, 0) * (Cylinder(fr + 15, 90) - Cylinder(fr - 5, 100))
             + Pos(xf - 35, s * p["FAN_Y"], p["FAN_Z"]) * Rot(0, 90, 0) * Cylinder(45, 80)
             + Pos(xf - 85, s * p["FAN_Y"], p["FAN_Z"]) * Box(10, p["FAN_D"] + 40, p["FAN_D"] + 40))   # shutter
        fans = f if fans is None else fans + f
    parts[8] = ("Exhaust fans, 12 V DC (pair)", fans)

    # 9 Controller with the outside sensor in a small radiation shield
    parts[9] = ("Controller and RH/T sensors",
                Pos(xf - 40, 860, 1150) * Box(80, 200, 250) + Pos(xf - 60, 860, 1350) * Box(40, 40, 60))

    # 10 Solar panel, 150 W, on the shade roof
    parts[10] = ("Solar panel, 150 W",
                 Pos(0, -300, rz + 150) * Rot(-p["PANEL_TILT_DEG"], 0, 0) * Box(p["PANEL_L"], p["PANEL_W"], p["PANEL_T"]))

    # 11 Power box: PWM charge controller, 12.8 V LiFePO4 battery and fuse
    parts[11] = ("Power box: charger, LiFePO4, fuse", Pos(xf - 50, -860, 1150) * Box(100, 220, 300))

    # 12 Timber racks, three levels, along both long walls
    rl, rd, rp = p["RACK_L"], p["RACK_D"], p["RACK_POST"]
    rack_h = max(p["SHELVES"]) + 350
    racks = None
    for s in (-1, 1):
        yc = s * (p["IN_W"] / 2 - rd / 2)
        for z in p["SHELVES"]:
            sh = Pos(0, yc, fl + z - 12.5) * Box(rl, rd, 25)
            racks = sh if racks is None else racks + sh
        for x in (-rl / 2 + rp / 2, 0, rl / 2 - rp / 2):
            for y in (yc - rd / 2 + rp / 2, yc + rd / 2 - rp / 2):
                racks = racks + Pos(x, y, fl + rack_h / 2) * Box(rp, rp, rack_h)
    parts[12] = ("Shelving racks", racks)

    # 13 Produce crates (user supplied)
    n, cl = p["CRATES_PER_SHELF"], p["CRATE_L"]
    crates = None
    for s in (-1, 1):
        yc = s * (p["IN_W"] / 2 - rd / 2)
        for z in p["SHELVES"]:
            for k in range(n):
                x = -(n - 1) * cl / 2 + k * cl
                c = Pos(x, yc, fl + z + p["CRATE_H"] / 2) * Box(cl - 30, p["CRATE_W"] - 10, p["CRATE_H"] - 10)
                crates = c if crates is None else crates + c
    parts[13] = ("Produce crates (user supplied)", crates)
    return parts


UNITS = {
    "zeerbox-structure": (1, 2, 3, 4, 5, 12),           # built by the mason and carpenter
    "zeerbox-cooling-kit": (6, 7, 8, 9, 10, 11),        # the $300 equipment kit (DDR-001 item 1)
}


def assembly(parts=None, include_crates=True):
    from build123d import Compound
    parts = parts or build_parts()
    return Compound([parts[k][1] for k in sorted(parts) if include_crates or k != 13])


if __name__ == "__main__":
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
        export_stl(shp, str(root / "stl" / f"{name}.stl"))
    bb = shapes["zeerbox-assembly"].bounding_box()
    print(f"assembly bounding box: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    for k, v in derived().items():
        print(f"  {k:16s} {v:10.3f}" if isinstance(v, float) else f"  {k:16s} {v}")
    for k in sorted(parts):
        print(f"  item {k:2d}  {parts[k][0]:40s} volume {parts[k][1].volume / 1e9:8.3f} m3")
    print("wrote cad/step/*.step and cad/stl/*.stl")
