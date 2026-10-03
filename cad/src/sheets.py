"""ZeerBox general arrangement drawing ZBX-DWG-001 (Rev P4).

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
          rev="P4", author="Amish Chadha", date="2026-10-02", concept=True, scale=1 / 50,
          material="Fired brick, dry rice husk fill, timber, corrugated steel; 12 V kit. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the TRL 3 model (ZBX-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "150 mm pad; dry rice husk cavity fill; R3 80 % (DDR-002)", "2026-09-25", "AC"),
                     ("P3", "Footings, lintels, framed ceiling and roof, ceiling fans (DDR-003)", "2026-10-02", "AC"),
                     ("P4", "Controller mode lamp; six-plate sensor shield (DEC-001)", "2026-10-02", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 36, 140, 74, label="Isometric view", sublabel="Not to scale; crates hidden")
s.add_notes("Key dimensions (mm) and data", [
    f"Overall {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} H (roof, posts, sump, panel)",
    f"Room {P['IN_L']:.0f} x {P['IN_W']:.0f} x {P['IN_H']:.0f} H inside; {D['room_volume_m3']:.1f} m3",
    f"Walls {P['LEAF']:.0f} + {P['CAV']:.0f} dry rice husk + {P['LEAF']:.0f} = {D['wall']:.0f}; outside {D['out_l']:.0f} x {D['out_w']:.0f}",
    f"Strip footing {P['FOOT_W']:.0f} x {P['FOOT_T']:.0f}; floor {P['FLOOR']:.0f} brick on sand; wall top {D['top']:.0f}",
    f"Ceiling: {P['JOIST'][0]:.0f} x {P['JOIST'][1]:.0f} joists, {P['INS_T']:.0f} insulation, {P['DECK_T']:.0f} boards",
    f"Shade roof {P['ROOF_L']:.0f} x {P['ROOF_W']:.0f}, {P['ROOF_CLEAR']:.0f} clear over ceiling, {P['ROOF_PITCH_DEG']:.0f} deg",
    f"Beams {P['BEAM'][0]:.0f} x {P['BEAM'][1]:.0f}, purlins {P['PURLIN'][0]:.0f} x {P['PURLIN'][1]:.0f}; 4 posts {P['POST_D']:.0f} dia",
    f"Post footings {P['FOOTING']:.0f} sq x {P['FOOTING_DEPTH']:.0f} deep",
    f"Door {P['DOOR_W']:.0f} x {P['DOOR_H']:.0f} clear, lined reveal, opens out, inside release",
    f"Pad {P['PAD_W']:.0f} x {P['PAD_H']:.0f} x {P['PAD_T']:.0f}, center {P['PAD_Z']:.0f} above ground",
    f"2 fans {P['FAN_D']:.0f} dia in a ceiling fan box, {abs(P['FAN_X']):.0f} from the room center",
    f"Controller {P['CTRL'][0]:.0f} x {P['CTRL'][1]:.0f} x {P['CTRL'][2]:.0f} clear lid, {P['LAMP'][0]:.0f} mode lamp; {P['SHIELD'][1]}-plate sensor shield",
    f"Racks {P['RACK_L']:.0f} x {P['RACK_D']:.0f}; shelves {', '.join(f'{z:.0f}' for z in P['SHELVES'])} above floor",
    f"Aisle {D['aisle']:.0f}; {D['crates']} crates; 150 W panel {P['PANEL_L']:.0f} x {P['PANEL_W']:.0f}",
    "Design day: store 24.3 °C, 10.7 K drop, about 560 m3/h (CAL-001)",
    "At risk at TRL 3: R3 (store RH 81 %, 77 % unfavorable, vs 80 %)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=127, width=140)
s.save(ROOT / "cad/drawings/ZBX-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/ZBX-DWG-001.svg, .pdf, .png")
