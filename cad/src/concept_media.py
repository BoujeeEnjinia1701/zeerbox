"""ZeerBox concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. X runs along the chamber (door at -X, pad wall at +X), Y across it,
Z up, ground at Z = 0. The storage room is centered on the origin in plan.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all, human_figure

# Storage room, inside faces of the inner brick leaf
IN_L, IN_W, IN_H = 2400.0, 1500.0, 2000.0
FLOOR = 100.0                  # brick floor on compacted sand
LEAF, CAV = 115.0, 75.0        # brick leaf and wet sand cavity
WALL = 2 * LEAF + CAV          # 305 mm double wall
OUT_L, OUT_W = IN_L + 2 * WALL, IN_W + 2 * WALL
TOP = FLOOR + IN_H             # top of walls, 2,100 mm
XF, XB = -OUT_L / 2, OUT_L / 2  # front (door) and back (pad) outer faces

DOOR_W, DOOR_H = 800.0, 1800.0
FAN_R, FAN_Y, FAN_Z = 130.0, 575.0, 1650.0
PAD_W, PAD_H, PAD_T, PAD_Z = 600.0, 500.0, 100.0, 1250.0   # pad center height


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def ring(l, w):
    """Solid block of plan size l x w over the wall height."""
    return Pos(0, 0, TOP / 2) * Box(l, w, TOP)


# openings cut through every wall layer
openings = (Pos(XF, 0, FLOOR + DOOR_H / 2) * Box(2 * WALL + 40, DOOR_W, DOOR_H)
            + Pos(XB, 0, PAD_Z) * Box(2 * WALL + 40, PAD_W, PAD_H))
for s in (-1, 1):
    openings = openings + Pos(XF, s * FAN_Y, FAN_Z) * Rot(0, 90, 0) * Cylinder(FAN_R, 2 * WALL + 40)

# 1 Double brick walls (outer and inner leaves) and brick floor
outer_leaf = ring(OUT_L, OUT_W) - ring(OUT_L - 2 * LEAF, OUT_W - 2 * LEAF)
inner_leaf = ring(IN_L + 2 * LEAF, IN_W + 2 * LEAF) - ring(IN_L, IN_W)
floor = Pos(0, 0, FLOOR / 2) * Box(IN_L, IN_W, FLOOR)
walls = outer_leaf + inner_leaf - openings + floor

# 2 Wet sand in the 75 mm cavity (kept damp from a perforated pipe)
sand = ring(OUT_L - 2 * LEAF, OUT_W - 2 * LEAF) - ring(IN_L + 2 * LEAF, IN_W + 2 * LEAF) - openings

# 3 Insulated ceiling slab over the walls
ceiling = Pos(0, 0, TOP + 60) * Box(OUT_L, OUT_W, 120)

# 4 Shade roof on four posts, 450 mm above the ceiling, wide overhang
RX, RY, RZ = 1850.0, 1400.0, 2650.0
roof = Pos(0, 0, RZ) * Rot(4, 0, 0) * Box(2 * RX + 200, 2 * RY + 200, 25)
for sx in (-1, 1):
    for sy in (-1, 1):
        roof = roof + tube3((sx * RX, sy * RY, 0), (sx * RX, sy * RY, RZ - 15 + sy * RY * math.sin(math.radians(4))), 45)

# 5 Insulated timber door with seal, in the front opening
door = Pos(XF + 30, 0, FLOOR + DOOR_H / 2) * Box(50, DOOR_W - 10, DOOR_H - 10)

# 6 Cellulose pad in a frame on the back wall, with drip header and gutter
pad_x = XB + PAD_T / 2 + 10
frame = Pos(pad_x, 0, PAD_Z) * (Box(PAD_T + 20, PAD_W + 100, PAD_H + 100) - Box(PAD_T + 40, PAD_W, PAD_H))
header = Pos(pad_x, 0, PAD_Z + PAD_H / 2 + 80) * Rot(90, 0, 0) * Cylinder(18, PAD_W + 160)
gutter = Pos(pad_x + 10, 0, PAD_Z - PAD_H / 2 - 80) * (Box(150, PAD_W + 160, 60) - Pos(0, 0, 15) * Box(120, PAD_W + 140, 60))
pad_media = Pos(pad_x, 0, PAD_Z) * Box(PAD_T, PAD_W, PAD_H)

# 7 Sump drum (60 L) with 12 V pump, feed hose and return
DX, DY, DR, DH = XB + 450, -750.0, 200.0, 620.0
drum = Pos(DX, DY, DH / 2) * Cylinder(DR, DH)
hose = (tube3((DX, DY, DH), (DX, DY, PAD_Z + PAD_H / 2 + 80), 12)
        + tube3((DX, DY, PAD_Z + PAD_H / 2 + 80), (pad_x, -PAD_W / 2 - 60, PAD_Z + PAD_H / 2 + 80), 12)
        + tube3((pad_x + 10, -PAD_W / 2 - 60, PAD_Z - PAD_H / 2 - 80), (DX, DY + 60, DH - 20), 16))
sump = drum + hose

# 8 Two 250 mm 12 V DC exhaust fans in the front wall, beside the door
fans = None
for s in (-1, 1):
    f = (Pos(XF - 35, s * FAN_Y, FAN_Z) * Rot(0, 90, 0) * (Cylinder(FAN_R + 15, 90) - Cylinder(FAN_R - 5, 100))
         + Pos(XF - 35, s * FAN_Y, FAN_Z) * Rot(0, 90, 0) * Cylinder(45, 80))
    fans = f if fans is None else fans + f

# 9 Controller with inside and outside humidity and temperature sensors
controller = (Pos(XF - 40, 860, 1150) * Box(80, 200, 250)
              + Pos(XF - 60, 860, 1350) * Box(40, 40, 60))          # outside sensor in a small shield

# 10 Solar panel, 100 W, on the shade roof
panel = Pos(0, -300, RZ + 150) * Rot(-15, 0, 0) * Box(1000, 670, 35)

# 11 Power box: PWM charge controller, 12.8 V LiFePO4 battery and fuse
power = Pos(XF - 50, -860, 1150) * Box(100, 220, 300)

# 12 Timber shelving racks, three levels, both long walls
racks = None
SHELF_Z = (FLOOR + 250, FLOOR + 800, FLOOR + 1350)
RD, RL = 450.0, 2200.0
for s in (-1, 1):
    yc = s * (IN_W / 2 - RD / 2)
    r = None
    for z in SHELF_Z:
        sh = Pos(0, yc, z - 12) * Box(RL, RD, 25)
        r = sh if r is None else r + sh
    for px in (-RL / 2 + 25, 0, RL / 2 - 25):
        for py in (yc - RD / 2 + 25, yc + RD / 2 - 25):
            r = r + Pos(px, py, FLOOR + 850) * Box(40, 40, 1700)
    racks = r if racks is None else racks + r

# 13 Produce crates, 24 of about 500 x 350 x 300 mm
crates = None
for s in (-1, 1):
    yc = s * (IN_W / 2 - RD / 2)
    for z in SHELF_Z:
        for k in range(4):
            c = Pos(-750 + k * 500, yc, z + 150) * Box(470, 340, 290)
            crates = c if crates is None else crates + c

parts = [
    Part("Double brick walls and floor", walls, "#B45F3C", 1),
    Part("Wet sand cavity fill", sand, "#D8B26E", 2, (0, 0, 900)),
    Part("Insulated ceiling", ceiling, "#E5E7EB", 3, (0, 0, 3900)),
    Part("Shade roof on posts", roof, "#94A3B8", 4, (0, 0, 4900)),
    Part("Insulated door with seal", door, "#A16207", 5, (-1300, -2600, 0)),
    Part("Cellulose pad, frame, header, gutter", frame + header + gutter + pad_media, "#0F766E", 6, (800, 0, 0)),
    Part("Sump drum, 12 V pump and hoses", sump, "#2563EB", 7, (1500, -500, 0)),
    Part("Exhaust fans, 12 V DC (pair)", fans, "#111827", 8, (-1300, -2600, 1200)),
    Part("Controller and RH/T sensors", controller, "#7C3AED", 9, (-1300, -5000, 200)),
    Part("Solar panel, 100 W", panel, "#1E3A8A", 10, (0, 0, 5600)),
    Part("Power box: charger, LiFePO4, fuse", power, "#16A34A", 11, (-1300, -1300, 2600)),
    Part("Shelving racks", racks, "#CA8A04", 12, (600, -3300, 0)),
    Part("Produce crates (user supplied)", crates, "#65A30D", 13, (0, 0, 3100)),
]

# 1.75 m person in front of the long wall, placed by hand so no roof post hides it
person = human_figure(1750.0, x=0.0, y=-OUT_W / 2 - 1100.0)
person.name = "1.75 m person"

render_all(
    parts, project="ZeerBox", title="Walk-in evaporative store concept", dwg_no="ZBX-DWG-010",
    key_figures=["Room 2.4 x 1.5 x 2.0 m, about 7.2 m3; 24 crates, about 480 kg (estimate)",
                 "Design day 35 °C, 30 % RH: supply about 25 °C, room about 26 °C (estimate)",
                 "About 650 m3/h through a 0.3 m2 pad; about 30 W of fans and pump (estimate)",
                 "About 55 L of water per design day (estimate)",
                 "About $575 in parts; equipment kit about $235 (indicative)"],
    scale_figure=False, context=[person],
    cut_exclude=("Shade roof on posts", "Solar panel, 100 W"),
    flow={"title": "air and water path on the design day, 35 °C and 30 % RH (all values are estimates)", "unit": "",
          "stages": [("Outside air", "35 °C, 30 % RH"), ("Wetted pad (6)", "31 L/day evaporated"),
                     ("Supply air", "25 °C, 74 % RH"), ("Store and produce", "gains about 550 W"),
                     ("Exhaust fans (8)", "650 m³/h at 27.5 °C")]},
)
