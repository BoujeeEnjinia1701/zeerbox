"""ZeerBox concept media from the kit 1.9 D3 model (option A, the constructable design).

Run from the repo root:  python cad/src/concept_media.py [all|web]
With no argument (or "all") it draws the concept views with .kit/concept.py render_all: hero, cutaway, exploded,
flow and the blueprint sheet, from the made and bought parts (fasteners and welds do not show at concept scale and
would multiply the memory the hidden-line views need). "web" exports media/model.glb and media/viewer.html from the
same parts (with the fasteners the file passes the 20 MB the website allows), in a fresh process so no finer mesh
cached by the renders is reused.
Geometry comes from components(CHOSEN) in cad/src/model.py; figures come from ZBX-CAL-001
(python docs/04-calcs/sizing.py). CONCEPT, NOT FOR FABRICATION.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parents[1] / ".kit"), str(HERE)]
import concept as K  # noqa: E402
from concept import Part, render_all, human_figure  # noqa: E402
import model as M  # noqa: E402

STYLE = {   # bom: (color for the concept views)
    1: "#B45F3C", 2: "#D8B26E", 3: "#E5E7EB", 4: "#94A3B8", 5: "#A16207", 6: "#0F766E", 7: "#2563EB", 8: "#111827",
    9: "#7C3AED", 10: "#1E3A8A", 11: "#16A34A", 12: "#CA8A04", 13: "#65A30D", 15: "#9CA3AF", 16: "#78350F",
    17: "#475569", 18: "#64748B",
}
NAMES = {   # bom: callout name (BOM line titles, short)
    1: "Double brick walls, floor and lintels", 2: "Dry rice husk cavity fill", 3: "Insulated ceiling",
    4: "Shade roof: sheets, posts and footings", 5: "Insulated door", 6: "Cellulose pad, frame, header, gutter",
    7: "Sump drum, 12 V pump and hoses", 8: "Exhaust fans, 12 V DC (pair)", 9: "Controller and RH/T sensors",
    10: "Solar panel, 150 W", 11: "Power box: charger, LiFePO4, fuses", 12: "Shelving racks", 13: "Produce crates (user supplied)",
    15: "Wall strip footing", 16: "Door lining, stops and fan box", 17: "Roof beams and purlins", 18: "Panel mounting frames",
}
# Concept views show the store above ground: footings are drawn in the general arrangement and the build plan.
BELOW_GROUND = ("Wall strip footing", "Post footing", "Anchor bar")


def parts(fasteners=True):
    out = []
    for p in M.components(M.CHOSEN):
        if p["kind"] == "context" or any(p["name"].startswith(k) for k in BELOW_GROUND):
            continue
        if not fasteners and p["kind"] in ("fastener", "weld"):
            continue
        b = p["bom"]
        out.append(Part(NAMES.get(b, p["name"]), p["shape"], STYLE.get(b, p["color"]), b, tuple(p["explode"])))
    return out


def everything():
    person = human_figure(1750.0, x=0.0, y=-M.derived()["out_w"] / 2 - 1100.0)
    person.name = "1.75 m person"
    return render_all(
        parts(fasteners=False), project="ZeerBox", title="Walk-in evaporative store concept", dwg_no="ZBX-DWG-010", date="2026-10-24", rev="P2",
        key_figures=["Room 2.4 x 1.5 x 2.0 m, 7.2 m3; 24 crates, 480 kg; top shelf 1.40 m",
                     "Design day 35 °C, 30 % RH: supply 23.1 °C, store 24.3 °C (ZBX-CAL-001)",
                     "About 560 m3/h through a 150 mm pad; store RH about 81 % (PR-003 80 %, at risk)",
                     "372 Wh/day from a 150 W panel (41 % margin); about 43 L water/day",
                     "Kit $300, value-engineering target $300; structure $574 separate (indicative)",
                     "Model detail D3: every part, fixing and weld (cad/fidelity.json)"],
        scale_figure=False, context=[person], web_model=False,
        cut_exclude=(NAMES[4], NAMES[10], NAMES[18]),
        flow={"title": "air and water path on the design day, 35 °C and 30 % RH (estimates, ZBX-CAL-001)", "unit": "",
              "stages": [("Outside air", "35 °C, 30 % RH"), ("Wetted pad (6)", "32 L/day evaporated"),
                         ("Supply air", "23.1 °C, 87 % RH"), ("Store and produce", "gains about 440 W"),
                         ("Ceiling exhaust fans (8)", "560 m³/h at 25.5 °C")]},
    )


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode == "web":
        print(K.export_web_model(parts(fasteners=False), "media", title="ZeerBox: Walk-in evaporative store concept"))
    else:
        print(everything())
