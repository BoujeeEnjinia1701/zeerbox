"""ZeerBox general arrangement drawing ZBX-DWG-001 (Rev P1).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/ZBX-DWG-001.svg, .pdf and .png from the parametric model.
The concept sheet in media/ uses ZBX-DWG-010. Figures quoted in the notes come
from ZBX-CAL-001 (python docs/04-calcs/sizing.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assembly, build_parts, derived  # noqa: E402

parts = build_parts()
asm = assembly(parts, include_crates=False)
bb = asm.bounding_box()
D = derived()

work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="ZeerBox", title="General arrangement, TRL 3 model", dwg_no="ZBX-DWG-001",
          rev="P1", author="Amish Chadha", date="2026-09-25", concept=True, scale=1 / 50,
          material="Fired brick, river sand, timber, corrugated steel; 12 V kit. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the TRL 3 model (ZBX-CAL-001)", "2026-09-25", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 80, label="Isometric view", sublabel="Not to scale; crates hidden")
s.add_notes("Key dimensions (mm) and data", [
    f"Overall {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} H (roof, posts, sump, panel)",
    f"Room {P['IN_L']:.0f} x {P['IN_W']:.0f} x {P['IN_H']:.0f} H inside; {D['room_volume_m3']:.1f} m3",
    f"Walls {P['LEAF']:.0f} + {P['CAV']:.0f} wet sand + {P['LEAF']:.0f} = {D['wall']:.0f}; outside {D['out_l']:.0f} x {D['out_w']:.0f}",
    f"Floor {P['FLOOR']:.0f} brick on sand; wall top {D['top']:.0f}; ceiling {P['CEIL_T']:.0f}",
    f"Shade roof {P['ROOF_L']:.0f} x {P['ROOF_W']:.0f}, {P['ROOF_CLEAR']:.0f} clear over ceiling, {P['ROOF_PITCH_DEG']:.0f} deg",
    f"4 posts {P['POST_D']:.0f} dia, footings {P['FOOTING']:.0f} sq x {P['FOOTING_DEPTH']:.0f} deep",
    f"Door {P['DOOR_W']:.0f} x {P['DOOR_H']:.0f}, inside release, no outside lock",
    f"Pad {P['PAD_W']:.0f} x {P['PAD_H']:.0f} x {P['PAD_T']:.0f}, center {P['PAD_Z']:.0f} above ground",
    f"2 fans {P['FAN_D']:.0f} dia at {P['FAN_Z']:.0f}, {P['FAN_Y']:.0f} each side of door axis",
    f"Racks {P['RACK_L']:.0f} x {P['RACK_D']:.0f}; shelves {', '.join(f'{z:.0f}' for z in P['SHELVES'])} above floor",
    f"Aisle {D['aisle']:.0f}; {D['crates']} crates; 150 W panel {P['PANEL_L']:.0f} x {P['PANEL_W']:.0f}",
    "Design day: store 25.9 °C, 9.1 K drop, about 580 m3/h (CAL-001)",
    "Not met at TRL 3: R3 (store RH 71 % vs 85 %)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=127, width=140)
s.save(ROOT / "cad/drawings/ZBX-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/ZBX-DWG-001.svg, .pdf, .png")
