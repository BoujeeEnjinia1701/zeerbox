"""ZeerBox product model for Cycles renders (STANDARDS sections 12 and 24), TRL 3, kit 1.9.

Every product part is components(CHOSEN) from cad/src/model.py as it is: the D3 model of option A with its
footings, brick leaves, rice husk fill, lintels, lined door and pad openings, framed ceiling, fan box and fans,
posts, beams, purlins, box-profile sheets, panel frames and panel, pad, header, gutter, sump, controller,
sensor shield, power box, racks, crates and every fixing. Only context is added: produce in the crates and a
1.75 m mannequin standing on the ground by the door for scale. The site itself (dry soil, sky and sun) is
the photoreal outdoor scene, with ground level at model z = 0 (RENDER_VIEWS "args"); the strip footing and
the post footings reach below it.

Groups: "shell" (everything above ground), "foundation" (footings, below ground: hidden by the site ground,
shown in the exploded view), "roof" (sheets, panel, its frames and their fixings, left out of the open-top
view), "ceiling" (boards and insulation, also left out of it) and "context" (produce, mannequin).
APPEARANCE AND DESIGN MODEL ARE THE SAME GEOMETRY. CONCEPT, NOT FOR FABRICATION.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

import model as M  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402
from build123d import Box, Pos, Rot  # noqa: E402

TITLE = "ZeerBox: solar-powered walk-in evaporative cooling store"

_SITE = ["--scene=outdoor", "--ground=soil", "--ground-z=0", "--sun=55,-15", "--lens=40"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "roof", "ceiling", "context", "foundation"], "explode": False, "el": 16, "az": -40,
     "args": _SITE,
     "note": "Site render in the dry season from the front right and a little above (about 16 deg elevation): the store on "
             "dry soil with the wetted pad, drip header, gutter and sump drum on the near end, the 150 W panel on the shade "
             "roof, and a 1.75 m person standing by the door at the far end for scale"},
    {"name": "studio", "groups": ["shell", "roof", "ceiling"], "explode": False, "el": 24, "az": -55,
     "note": "Studio render from the front right and above (about 24 deg elevation): brick store, shade roof on four "
             "posts with the panel on its aluminium frames, pad and sump at the near end; footings not shown"},
    {"name": "open-top", "groups": ["shell", "context"], "explode": False, "el": 55, "az": -60,
     "note": "Open-top view from above (about 55 deg elevation) with the roof sheets, panel, ceiling boards and insulation "
             "lifted away: joists, fan box with its two fans at the door end, racks with 24 crates of produce either side "
             "of the aisle, and the pad in the far wall"},
    {"name": "exploded", "groups": ["shell", "roof", "ceiling", "foundation"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): panel, roof, ceiling and rice husk "
             "fill lifted off the brick walls; pad, header, gutter and sump at right; door, controller and power box at "
             "left; fans lifted above the ceiling; racks and crates pulled out in front"},
]

ROOF_KEYS = ("Roof sheet", "Roofing screw 6 x 100, sheet", "Solar panel", "Panel frame", "panel frame leg", "panel to top rail",
             "base rail through sheet")
CEIL_KEYS = ("Ceiling board", "Ceiling insulation", "Nail 2.8 x 60, board")
FOUND_KEYS = ("Wall strip footing", "Post footing", "Anchor bar")


def _group(name):
    if any(k in name for k in FOUND_KEYS):
        return "foundation"
    if any(k in name for k in ROOF_KEYS):
        return "roof"
    if any(k in name for k in CEIL_KEYS):
        return "ceiling"
    return "shell"


def context():
    """Produce in every crate and a mannequin by the door, standing on the ground (z = 0)."""
    P = M.PARAMS
    out = []
    fl, hw, rd = P["FLOOR"], P["IN_W"] / 2, P["RACK_D"]
    n, cl_ = P["CRATES_PER_SHELF"], P["CRATE_L"]
    colors = ("#B8382B", "#C9472E", "#3F7A2E", "#A8342A")       # tomatoes, peppers, okra
    k = 0
    for s in (-1, 1):
        yc = s * (hw - rd / 2)
        for zsh in P["SHELVES"]:
            for i in range(n):
                x = -(n - 1) * cl_ / 2 + i * cl_
                heap = Pos(x, yc, fl + zsh + 4 + 120) * Box(cl_ - 50, P["CRATE_W"] - 30, 240)
                heap = break_edges(heap, 40)
                out.append(part("Produce in crate (context)", heap, "epdm", kind="context", group="context", color=colors[k % 4]))
                k += 1
    try:
        import context_parts
        xf = -M.derived()["out_l"] / 2
        man = Pos(xf - 900, -1100, 0) * Rot(0, 0, -35) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        if p["kind"] == "context":
            continue
        q = dict(p)
        q["group"] = _group(p["name"])
        out.append(q)
    return out + context()


if __name__ == "__main__":
    ps = product_parts()
    from collections import Counter
    print(len(ps), "parts;", dict(Counter(p["group"] for p in ps)))
