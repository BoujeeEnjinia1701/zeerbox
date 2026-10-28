"""ZeerBox repo helpers for the kit 1.9 model (STANDARDS section 24): materials the kit library lacks,
timber and masonry pieces with broken edges, wood and roofing fasteners, ring welds, corrugated sheet.

Used by cad/src/model.py only. Every function returns a build123d solid in millimetres. Fasteners are
built like .kit/cad_parts.py builds them: head on the XY plane at z = 0, shank down -Z; place them with
aim(shape, point, direction), which turns the shank onto 'direction' with the head at 'point'.

PRELIMINARY, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import (Box, Cylinder, Cone, Location, Plane, Polygon, Pos, Rot, Sketch, Circle, Vector,  # noqa: E402
                       extrude, revolve, Axis)
import cad_parts as cp  # noqa: E402
from cad_parts import break_edges  # noqa: E402

# Materials the kit library does not have (kit gap, reported in docs/REVIEW.md). Registered at import so
# cad_parts.part() and cad_parts.mass_kg() accept them; each uses an existing photoreal render class.
# name: (colour, render class, density kg/m3)
EXTRA_MATERIALS = {
    "fired_brick":   ("#A85A3A", "paper", 1800),      # fired clay brick with mortar joints (ZBX-CAL-001 s10)
    "rice_husk":     ("#D8B26E", "coir", 120),        # loose dry rice husk with lime (ZBX-CAL-001 s10)
    "wet_sand":      ("#8A7656", "sand", 1900),       # option B cavity fill, kept wet
    "charcoal":      ("#26241F", "matte_black", 250), # option C lump charcoal, bulk density (estimate)
    "cellulose_pad": ("#C29B5E", "fabric", 60),       # corrugated cellulose pad, dry (estimate)
    "straw_board":   ("#D9C27A", "coir", 100),        # ceiling insulation (ZBX-CAL-001 Table 1)
    "pvc":           ("#E6E6E0", "hdpe", 1400),       # drip header, conduit
    "fr4":           ("#1F5F3A", "hdpe", 1850),       # printed circuit boards
}
for _k, _v in EXTRA_MATERIALS.items():
    cp.MATERIALS.setdefault(_k, _v)


# ----------------------------------------------------------------------------------------- placement
def aim(shape, point, direction):
    """Place a part built along -Z from its head at the origin so its shank runs along 'direction' from 'point'."""
    d = Vector(*direction).normalized()
    up = -d
    x = Vector(1, 0, 0) if abs(up.X) < 0.9 else Vector(0, 1, 0)
    x = (x - up * x.dot(up)).normalized()
    return Location(Plane(origin=Vector(*point), x_dir=x, z_dir=up)) * shape


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def sawn(x0, x1, y0, y1, z0, z1, r=2.0):
    """A sawn timber piece (or a cut board): the four arrises along its length eased by an r mm chamfer, the
    cut ends left square, as a planed and cross-cut piece is."""
    from build123d import chamfer
    b = box(x0, x1, y0, y1, z0, z1)
    dims = [abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)]
    ax = (Axis.X, Axis.Y, Axis.Z)[dims.index(max(dims))]
    r = min(r, min(dims) / 3)
    try:
        return chamfer(b.edges().filter_by(ax), r)
    except Exception:
        return break_edges(b, r)


def eased(shape, r=2.0):
    return break_edges(shape, r)


# ----------------------------------------------------------------------------------------- fasteners
def wood_screw(d, length):
    """Countersunk wood screw (ISO 7049 type head proportions), head flush at z = 0, shank down -Z, gimlet point."""
    dk = 2.0 * d
    head = Pos(0, 0, -d * 0.6) * Cone(d / 2, dk / 2, d * 0.6, align=None)
    shank = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    tip = Pos(0, 0, -length - d * 0.6) * Cone(0.05, d / 2, d * 1.2, align=None)
    return head + shank + tip


def nail(d, length):
    """Round wire nail driven flush: flat head from z -d/2 to 0, shank down -Z."""
    head = Pos(0, 0, -d * 0.25) * Cylinder(d, d * 0.5)
    return head + Pos(0, 0, -length / 2) * Cylinder(d / 2, length)


def pan_screw(d, length):
    """Pan-head machine or self-tapping screw: head above z 0 (height 0.6 d, diameter 2 d), shank down -Z."""
    head = Pos(0, 0, d * 0.3) * Cylinder(d, d * 0.6)
    return break_edges(head, d * 0.15) + Pos(0, 0, -length / 2) * Cylinder(d / 2, length)


def roofing_screw(d=6, length=100):
    """Self-drilling roofing screw with a hex washer head and an EPDM sealing washer under it (head above z 0)."""
    seal = Pos(0, 0, 1.5) * (Cylinder(8, 3) - Cylinder(d / 2, 3))
    head = Pos(0, 0, 3) * cp._hex(8, 5)
    shank = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    return seal + head + shank


def frame_fixing(d=8, length=80):
    """Nylon frame plug with its screw, as one bought fixing: collar at z 0, plug down -Z into a drilled hole."""
    collar = Pos(0, 0, 0.75) * Cylinder(d * 0.85, 1.5)
    plug = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    head = Pos(0, 0, 1.5 + 1.5) * Cylinder(d * 0.75, 3)
    return collar + plug + head


def wall_tie(length, d=4.0):
    """Galvanised wire wall tie along +X from 0 to length, its ends bent at right angles in the plane of the bed
    joint as keys in each leaf's mortar (bedded in both leaves' mortar joints)."""
    from build123d import Compound
    leg = Pos(length / 2, 0, 0) * Rot(0, 90, 0) * Cylinder(d / 2, length - 2 * d)
    ends = [Pos(x, 0, 0) * Rot(90, 0, 0) * Cylinder(d / 2, 40) for x in (d / 2, length - d / 2)]
    return Compound([leg] + ends)


# ----------------------------------------------------------------------------------------- joints
def ring_weld(r, leg, z0, z1):
    """Weld bead round the top of a vertical tube of outside radius r, from z0 on the tube wall up to z1 under
    the plate it carries, flaring out by 'leg' at the plate: a triangle revolved about Z."""
    tri = Plane.XZ * Polygon((r, z0), (r + leg, z1), (r, z1), align=None)
    return revolve(tri, Axis.Z, 360)


def hurricane_tie(w=35.0, t=1.5, up=110.0, down=110.0, gap=50.0):
    """Galvanised hurricane tie: a strip bent over the purlin's 'gap' wide top, legs 'up' long on each side, drawn
    in the XZ plane centred on x = 0, thickness along Y from 0 to w. Returns the strap; legs hang down -Z."""
    a = box(-gap / 2 - t, -gap / 2, 0, w, -up, 0)
    b = box(gap / 2, gap / 2 + t, 0, w, -down, 0)
    top = box(-gap / 2 - t, gap / 2 + t, 0, w, 0, t)
    return break_edges(a + b + top, 0.4)


def strap(length, w=30.0, t=2.0, holes=2, d=6.0):
    """Flat galvanised strap along +Z from 0 to length, width along Y centred, thickness along +X, with holes."""
    s = box(0, t, -w / 2, w / 2, 0, length)
    for k in range(holes):
        z = length * (k + 1) / (holes + 1)
        s = s - Pos(t / 2, 0, z) * Rot(0, 90, 0) * Cylinder(d / 2, t + 2)
    return break_edges(s, 0.4)


# ----------------------------------------------------------------------------------------- sheet
def corrugated(length, width, t=0.5, pitch=76.0, depth=18.0):
    """Box-profile (trapezoidal) roof sheet: profile across X (width), run along Y (length), mid-depth at z = 0.
    Thickness t is drawn as an offset of the profile."""
    n = max(1, int(round(width / pitch)))
    pitch = width / n
    crest, flank = pitch * 0.30, pitch * 0.12
    pts = []
    x0 = -width / 2
    for i in range(n):
        xa = x0 + i * pitch
        pts += [(xa, -depth / 2), (xa + flank, depth / 2), (xa + flank + crest, depth / 2), (xa + 2 * flank + crest, -depth / 2)]
    pts.append((x0 + width, -depth / 2))
    top = pts
    bot = [(x, z - t) for x, z in reversed(pts)]
    prof = Plane.XZ * Polygon(*(top + bot), align=None)
    s = extrude(prof, length / 2, both=True)
    return s


def crest_x(width, pitch=76.0):
    """x of the crest centres of corrugated(width)."""
    n = max(1, int(round(width / pitch)))
    p = width / n
    return [-width / 2 + i * p + p * 0.12 + p * 0.15 for i in range(n)]


def hollow_box(x0, x1, y0, y1, z0, z1, wall, open_face=None, r=2.0):
    """A moulded box with wall thickness 'wall'; open_face one of '+z', '-z', '+x', '-x', '+y', '-y' or None (closed)."""
    outer = box(x0, x1, y0, y1, z0, z1)
    ix0, ix1, iy0, iy1, iz0, iz1 = x0 + wall, x1 - wall, y0 + wall, y1 - wall, z0 + wall, z1 - wall
    e = 1.0
    if open_face == "+z": iz1 = z1 + e
    if open_face == "-z": iz0 = z0 - e
    if open_face == "+x": ix1 = x1 + e
    if open_face == "-x": ix0 = x0 - e
    if open_face == "+y": iy1 = y1 + e
    if open_face == "-y": iy0 = y0 - e
    return break_edges(outer, r) - box(ix0, ix1, iy0, iy1, iz0, iz1)


def tube_between(a, b, od, t=None):
    """Round tube (or solid rod if t is None) from point a to point b."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    pl = Plane(origin=a, z_dir=d.normalized())
    if t is None:
        return pl.location * (Pos(0, 0, d.length / 2) * Cylinder(od / 2, d.length))
    return pl.location * extrude(Sketch() + Circle(od / 2) - Circle(od / 2 - t), d.length)
