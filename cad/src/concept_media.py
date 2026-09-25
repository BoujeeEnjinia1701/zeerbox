"""ZeerBox concept media from the TRL 3 parametric model.

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from cad/src/model.py; figures come from ZBX-CAL-001
(python docs/04-calcs/sizing.py). Not for fabrication.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / ".kit"))
sys.path.insert(0, str(HERE))
from concept import Part, render_all, human_figure  # noqa: E402
from model import build_parts, derived  # noqa: E402

STYLE = {   # bom: (color, exploded-view offset in mm)
    1: ("#B45F3C", (0, 0, 0)),
    2: ("#D8B26E", (0, 0, 900)),
    3: ("#E5E7EB", (0, 0, 3900)),
    4: ("#94A3B8", (0, 0, 4900)),
    5: ("#A16207", (-1300, -2600, 0)),
    6: ("#0F766E", (800, 0, 0)),
    7: ("#2563EB", (1500, -500, 0)),
    8: ("#111827", (-1300, -2600, 1200)),
    9: ("#7C3AED", (-1300, -5000, 200)),
    10: ("#1E3A8A", (0, 0, 5600)),
    11: ("#16A34A", (-1300, -1300, 2600)),
    12: ("#CA8A04", (600, -3300, 0)),
    13: ("#65A30D", (0, 0, 3100)),
}

model = build_parts()
parts = [Part(name, shape, STYLE[k][0], k, STYLE[k][1]) for k, (name, shape) in sorted(model.items())]

if __name__ == "__main__":
    # 1.75 m person in front of the long wall, placed by hand so no roof post hides it
    person = human_figure(1750.0, x=0.0, y=-derived()["out_w"] / 2 - 1100.0)
    person.name = "1.75 m person"
    render_all(
        parts, project="ZeerBox", title="Walk-in evaporative store concept", dwg_no="ZBX-DWG-010",
        key_figures=["Room 2.4 x 1.5 x 2.0 m, 7.2 m3; 24 crates, 480 kg; top shelf 1.40 m",
                     "Design day 35 °C, 30 % RH: supply 24.8 °C, store 25.9 °C (ZBX-CAL-001)",
                     "About 580 m3/h through a 0.3 m2 pad; store RH about 71 % (R3 not met)",
                     "372 Wh/day from a 150 W panel (41 % margin); about 44 L water/day",
                     "Kit $260 against $300; structure $360 costed separately (indicative)"],
        scale_figure=False, context=[person],
        cut_exclude=("Shade roof on posts", "Solar panel, 150 W"),
        flow={"title": "air and water path on the design day, 35 °C and 30 % RH (estimates, ZBX-CAL-001)", "unit": "",
              "stages": [("Outside air", "35 °C, 30 % RH"), ("Wetted pad (6)", "28 L/day evaporated"),
                         ("Supply air", "24.8 °C, 75 % RH"), ("Store and produce", "gains about 420 W"),
                         ("Exhaust fans (8)", "580 m³/h at 27 °C")]},
    )
