"""ZeerBox sizing and first-principles checks (ZBX-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number that ZBX-CAL-001 quotes and writes docs/04-calcs/results.csv.
Geometry comes from PARAMS in cad/src/model.py; prices come from bom/bom.csv;
the budget comes from project.yaml. All values are estimates for a paper design.
"""
import csv
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, derived  # noqa: E402

D = derived()
PATM = 101325.0          # Pa, sea level
CPA, CPV, HFG0 = 1006.0, 1860.0, 2.501e6   # J/(kg K), J/(kg K), J/kg at 0 C
HFG = 2.43e6             # J/kg near 25 to 30 C
RA = 287.05              # J/(kg K)

# ------------------------------------------------------------------ psychrometrics


def p_ws(t):
    """Saturation vapor pressure over water, Pa (ASHRAE Fundamentals 2017, eq. 6, 0 to 200 C)."""
    T = t + 273.15
    c8, c9, c10, c11, c12, c13 = -5.8002206e3, 1.3914993, -4.8640239e-2, 4.1764768e-5, -1.4452093e-8, 6.5459673
    return math.exp(c8 / T + c9 + c10 * T + c11 * T ** 2 + c12 * T ** 3 + c13 * math.log(T))


def w_from_rh(t, rh):
    pw = rh * p_ws(t)
    return 0.621945 * pw / (PATM - pw)


def rh_from_w(t, w):
    pw = w * PATM / (0.621945 + w)
    return pw / p_ws(t)


def wet_bulb(t, rh):
    """Thermodynamic wet-bulb temperature by bisection on the ASHRAE humidity-ratio relation."""
    w = w_from_rh(t, rh)
    lo, hi = -10.0, t
    for _ in range(80):
        tw = (lo + hi) / 2
        ws = w_from_rh(tw, 1.0)
        wc = ((2501 - 2.326 * tw) * ws - 1.006 * (t - tw)) / (2501 + 1.86 * t - 4.186 * tw)
        lo, hi = (tw, hi) if wc < w else (lo, tw)
    return (lo + hi) / 2


def dew_point(w):
    lo, hi = -20.0, 60.0
    for _ in range(80):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if w_from_rh(m, 1.0) < w else (lo, m)
    return (lo + hi) / 2


def rho_air(t, w):
    return PATM / (RA * (t + 273.15) * (1 + 1.6078 * w)) * (1 + w)


# ------------------------------------------------------------------ inputs

DESIGN = {"t": 35.0, "rh": 0.30}
HOURS_COOL, HOURS_EVE = 10.0, 2.0         # R7 design day
LOAD_KG, FRESH_KG, FRESH_T = 480.0, 100.0, 32.0

# Thermal resistances, m2 K/W
R_SI, R_SE = 0.13, 0.04
K_BRICK, K_SAND_DRY, K_SAND_WET = 0.70, 0.30, 1.5      # W/(m K)
R_LEAF = P["LEAF"] / 1000 / K_BRICK

SCEN = {   # favorable, central, unfavorable
    "fav": dict(eff06=0.80, wall_eff=0.60, resp=0.10, p0=70.0, leaks=30.0, sun=0.0, attic=38.0, ground=28.0, transp=0.005),
    "cen": dict(eff06=0.75, wall_eff=0.50, resp=0.15, p0=60.0, leaks=50.0, sun=20.0, attic=40.0, ground=30.0, transp=0.010),
    "unf": dict(eff06=0.70, wall_eff=0.30, resp=0.25, p0=50.0, leaks=80.0, sun=60.0, attic=43.0, ground=32.0, transp=0.020),
}
FAN_FREE = 400.0       # m3/h free air per fan (BOM line 8)
FAN_W = 12.0           # W per fan at full speed, taken as constant (conservative)
PAD_DP_1 = 15.0        # Pa across a wet 100 mm pad at 1.0 m/s face velocity (assumption, to confirm with supplier data)
PAD_DP_N = 1.8         # exponent on face velocity
K_OUTLET = 4.0         # velocity heads lost at guards and shutters, on the fan-opening velocity
SHUTTER_PA = 5.0       # Pa to hold two gravity shutters open
U_CEIL = 1 / (R_SI + 0.05 / 0.06 + 0.02 / 0.13 + 0.10)   # 50 mm straw, boards, upper film
U_DOOR = 1 / (R_SI + 0.05 / 0.04 + 2 * 0.012 / 0.13 + R_SE)
U_FLOOR = 1 / (R_SI + P["FLOOR"] / 1000 / K_BRICK + 0.10)   # brick on compacted sand, to ground at ground temperature


def areas():
    L, W, H = P["IN_L"] / 1000, P["IN_W"] / 1000, P["IN_H"] / 1000
    openings = D["door_area_m2"] + D["pad_area_m2"] + D["fan_area_m2"]
    a_wall_in = 2 * (L + W) * H - openings
    a_wall_out = 2 * (D["out_l"] + D["out_w"]) / 1000 * D["top"] / 1000 - openings
    return dict(wall_in=a_wall_in, wall_out=a_wall_out, ceil=L * W, floor=L * W, door=D["door_area_m2"])


A = areas()
U_IN_WET = 1 / (R_SI + R_LEAF + P["CAV"] / 2000 / K_SAND_WET)           # cavity node to room
U_OUT_WET = 1 / (R_SE + R_LEAF)                                          # outside air to wet cavity
U_WALL_DRY = 1 / (R_SI + 2 * R_LEAF + P["CAV"] / 1000 / K_SAND_DRY + R_SE)


def pad_eff(v, eff06, depth_m=P["PAD_T"] / 1000):
    """Pad saturation effectiveness. NTU scales as depth x v^-0.2 (h ~ v^0.8, mass flow ~ v), calibrated at 0.6 m/s, 100 mm."""
    ntu06 = -math.log(1 - eff06)
    return 1 - math.exp(-ntu06 * (depth_m / 0.1) * (0.6 / v) ** 0.2)


def operating_point(p0, n_fans=2, speed=1.0, rho=1.15, depth_m=P["PAD_T"] / 1000):
    """Fans in parallel with a linear curve p = p0 s^2 (1 - Q/(n Qf s)); returns Q in m3/s and pressure in Pa."""
    qf = n_fans * FAN_FREE * speed / 3600

    def sys_dp(q):
        v_pad = q / D["pad_area_m2"]
        v_fan = q / (D["fan_area_m2"] * n_fans / 2)
        return PAD_DP_1 * (depth_m / 0.1) * v_pad ** PAD_DP_N + SHUTTER_PA * (n_fans / 2) + K_OUTLET * 0.5 * rho * v_fan ** 2

    lo, hi = 0.0, qf
    for _ in range(80):
        q = (lo + hi) / 2
        fan = p0 * speed ** 2 * (1 - q / qf)
        lo, hi = (q, hi) if fan > sys_dp(q) else (lo, q)
    return q, sys_dp(q)


def u_dry(k_fill):
    return 1 / (R_SI + 2 * R_LEAF + P["CAV"] / 1000 / k_fill + R_SE)


K_HUSK = 0.06          # W/(m K), loose rice husk, dry (assumption)


def store(t_out, rh_out, s, wet_cavity=True, depth_m=P["PAD_T"] / 1000, k_fill=K_SAND_DRY):
    """Steady design-hour balance of the store in evaporative cooling mode."""
    twb = wet_bulb(t_out, rh_out)
    w_out = w_from_rh(t_out, rh_out)
    q, dp = operating_point(s["p0"], depth_m=depth_m)
    v = q / D["pad_area_m2"]
    e = pad_eff(v, s["eff06"], depth_m)
    t_sup = t_out - e * (t_out - twb)
    w_sup = w_out + CPA * (t_out - t_sup) / (HFG0 + CPV * t_sup - 4186 * twb) * (1 + 0 * w_out)
    rho = rho_air(t_sup, w_sup)
    m = q * rho / (1 + w_sup)                                  # dry-air mass flow, kg/s
    t_cav = t_out - s["wall_eff"] * (t_out - twb) if wet_cavity else None
    t_room = t_sup + 2.0
    for _ in range(60):
        if wet_cavity:
            walls = U_IN_WET * A["wall_in"] * (t_cav - t_room)
        else:
            walls = u_dry(k_fill) * A["wall_in"] * (t_out - t_room)
        gains = {
            "walls": walls,
            "sun on walls": s["sun"],
            "ceiling": U_CEIL * A["ceil"] * (s["attic"] - t_room),
            "floor": U_FLOOR * A["floor"] * (s["ground"] - t_room),
            "door leaf": U_DOOR * A["door"] * (t_out - t_room),
            "respiration": LOAD_KG * s["resp"],
            "field heat": FRESH_KG * 3900 * max(FRESH_T - t_room, 0) / (8 * 3600),
            "door openings and leaks": s["leaks"],
        }
        qtot = sum(gains.values())
        rise = qtot / (m * (CPA + CPV * w_sup))
        t_new = t_sup + rise / 2
        if abs(t_new - t_room) < 1e-6:
            break
        t_room = t_new
    w_prod = LOAD_KG * s["transp"] / 86400 / m                 # moisture from produce water loss
    w_room = w_sup + w_prod / 2
    return dict(twb=twb, w_out=w_out, q=q, dp=dp, v=v, eff=e, t_sup=t_sup, w_sup=w_sup,
                rh_sup=rh_from_w(t_sup, w_sup), m=m, t_cav=t_cav, gains=gains, qtot=qtot, rise=rise,
                t_room=t_room, t_exh=t_sup + rise, rh_room=rh_from_w(t_room, w_room),
                rh_exh=rh_from_w(t_sup + rise, w_sup + w_prod), drop=t_out - t_room,
                ach=q * 3600 / D["room_volume_m3"], pad_evap_kgh=m * (w_sup - w_out) * 3600)


def fmt(x, n=1):
    return f"{x:,.{n}f}"


results = []   # (req, quantity, value, target, status)


def res(req, what, value, target, status):
    results.append((req, what, value, target, status))


out = []
pr = out.append

# ------------------------------------------------------------------ 1 geometry (R1)
pr("== 1 Geometry and capacity (R1) ==")
crates = D["crates"]
pr(f"room {P['IN_L']:.0f} x {P['IN_W']:.0f} x {P['IN_H']:.0f} mm, volume {D['room_volume_m3']:.2f} m3; outside {D['out_l']:.0f} x {D['out_w']:.0f} mm")
pr(f"crates {crates}, produce {crates * 20:.0f} kg; aisle {D['aisle']:.0f} mm; shelves at {', '.join(f'{z/1000:.2f}' for z in P['SHELVES'])} m above floor")
top_crate = (max(P["SHELVES"]) + P["CRATE_H"]) / 1000
pr(f"top crate top {top_crate:.2f} m; clearance to ceiling {P['IN_H']/1000 - top_crate:.2f} m")
# shelf rail bending: two 50 x 75 mm rails per shelf, span between the three rack legs
span = (P["RACK_L"] / 2 - P["RACK_POST"]) / 1000
w_line = P["CRATES_PER_SHELF"] * 22 * 9.81 / 2 / (P["RACK_L"] / 1000)
b, h, E = 0.050, 0.075, 9e9
M = w_line * span ** 2 / 8
sig = M / (b * h ** 2 / 6) / 1e6
defl = 5 * w_line * span ** 4 / (384 * E * b * h ** 3 / 12) * 1000
pr(f"shelf rail: span {span:.3f} m, {w_line:.0f} N/m, M {M:.0f} N m, stress {sig:.2f} MPa (allow about 7), deflection {defl:.2f} mm")
res("R1", "Crates on shelves; highest shelf", f"{crates} crates ({crates*20} kg); top shelf {max(P['SHELVES'])/1000:.2f} m",
    "20 or more crates; no lift above 1.6 m", "Met" if crates >= 20 and max(P["SHELVES"]) <= 1600 else "Not met")

# ------------------------------------------------------------------ 2 psychrometrics and heat balance (R2, R3)
pr("\n== 2 Design point, pad and heat balance (R2, R3) ==")
pr(f"U values W/(m2 K): wet cavity inner {U_IN_WET:.2f}, outer {U_OUT_WET:.2f}, dry wall {U_WALL_DRY:.2f}, ceiling {U_CEIL:.2f}, door {U_DOOR:.2f}, floor {U_FLOOR:.2f}")
pr(f"areas m2: inner wall net {A['wall_in']:.2f}, outer wall net {A['wall_out']:.2f}, ceiling {A['ceil']:.2f}, door {A['door']:.2f}")
R = {k: store(DESIGN["t"], DESIGN["rh"], s) for k, s in SCEN.items()}
c = R["cen"]
pr(f"outside 35 C, 30 % RH: wet bulb {c['twb']:.2f} C, W {c['w_out']*1000:.2f} g/kg, depression {35 - c['twb']:.2f} K")
for k in ("fav", "cen", "unf"):
    r = R[k]
    pr(f"[{k}] Q {r['q']*3600:.0f} m3/h ({r['q']*3600/1.699:.0f} cfm) at {r['dp']:.1f} Pa; pad {r['v']:.2f} m/s, eff {r['eff']*100:.1f} %; "
       f"supply {r['t_sup']:.2f} C {r['rh_sup']*100:.0f} %; cavity {r['t_cav']:.2f} C; gains {r['qtot']:.0f} W; rise {r['rise']:.2f} K; "
       f"room {r['t_room']:.2f} C {r['rh_room']*100:.0f} %; exhaust {r['t_exh']:.2f} C {r['rh_exh']*100:.0f} %; drop {r['drop']:.2f} K; ACH {r['ach']:.0f}")
pr("central heat gains, W: " + ", ".join(f"{k} {v:.0f}" for k, v in c["gains"].items()) + f"; total {c['qtot']:.0f}")
dry = store(35, 0.30, SCEN["cen"], wet_cavity=False)
pr(f"dry sand cavity (central): walls {dry['gains']['walls']:.0f} W, total {dry['qtot']:.0f} W, room {dry['t_room']:.2f} C, drop {dry['drop']:.2f} K")
dry_u = store(35, 0.30, SCEN["unf"], wet_cavity=False)
pr(f"dry sand cavity (unfavorable loads): walls {dry_u['gains']['walls']:.0f} W vs wet {R['unf']['gains']['walls']:.0f} W; drop {dry_u['drop']:.2f} K vs {R['unf']['drop']:.2f} K")
husk = store(35, 0.30, SCEN["cen"], wet_cavity=False, k_fill=K_HUSK)
husk_u = store(35, 0.30, SCEN["unf"], wet_cavity=False, k_fill=K_HUSK)
pr(f"rice husk cavity, U {u_dry(K_HUSK):.2f}: central walls {husk['gains']['walls']:.0f} W, room {husk['t_room']:.2f} C, drop {husk['drop']:.2f} K; unfavorable drop {husk_u['drop']:.2f} K; no cavity water")
for d_mm in (150.0,):
    r150 = store(35, 0.30, SCEN["cen"], depth_m=d_mm / 1000)
    pr(f"150 mm pad (central, same fans, pressure drop scaled with depth): Q {r150['q']*3600:.0f} m3/h, eff {r150['eff']*100:.1f} %, supply RH {r150['rh_sup']*100:.0f} %, room {r150['t_room']:.2f} C, RH {r150['rh_room']*100:.0f} %, drop {r150['drop']:.2f} K")
# effectiveness that would put mean room RH at 85 % with the central temperature rise
need = None
for e_try in [x / 1000 for x in range(700, 1000)]:
    t_sup = 35 - e_try * (35 - c["twb"])
    w_sup = c["w_out"] + CPA * (35 - t_sup) / (HFG0 + CPV * t_sup - 4186 * c["twb"])
    if rh_from_w(t_sup + c["rise"] / 2, w_sup) >= 0.85:
        need = e_try
        break
pr(f"pad effectiveness needed for 85 % mean RH at the central rise of {c['rise']:.2f} K: {need*100:.1f} %" if need else
   f"85 % mean RH not reachable at the central rise of {c['rise']:.2f} K even with a saturating pad")
if need:
    ntu_need = -math.log(1 - need)
    ntu_100 = -math.log(1 - SCEN["cen"]["eff06"]) * (0.6 / c["v"]) ** 0.2
    pr(f"pad depth for {need*100:.1f} % at {c['v']:.2f} m/s: about {100 * ntu_need / ntu_100:.0f} mm (before the lower airflow of a deeper pad)")
pr(f"produce transpiration adds {LOAD_KG * SCEN['cen']['transp'] / 86400 / c['m'] * 1000:.2f} g/kg to the airstream (central)")
max_rise = None
t_sat = c["twb"]
w_sat = w_from_rh(t_sat, 1.0)
for r10 in range(0, 100):
    if rh_from_w(t_sat + r10 / 20, w_sat) < 0.85:
        max_rise = (r10 - 1) / 20 * 2
        break
pr(f"even with saturated supply at {t_sat:.1f} C, the store mean must stay within {max_rise/2:.2f} K of supply (rise {max_rise:.1f} K) for 85 % RH")
res("R2", "Mean store air below outside air, design point", f"{c['drop']:.1f} K ({R['unf']['drop']:.1f} to {R['fav']['drop']:.1f} K); store {c['t_room']:.1f} C",
    "8 K or more", "Met" if R["unf"]["drop"] >= 8 else ("At risk" if c["drop"] >= 8 else "Not met"))
res("R3", "Mean store RH while cooling", f"{c['rh_room']*100:.0f} % ({R['unf']['rh_room']*100:.0f} to {R['fav']['rh_room']*100:.0f} %)",
    "85 % or more", "Met" if c["rh_room"] >= 0.85 else "Not met")

# ------------------------------------------------------------------ 3 humid weather and controller (R4, R5)
pr("\n== 3 Off-design weather and control (R4, R5) ==")
cases = [(35, 0.30), (38, 0.15), (32, 0.50), (30, 0.60), (30, 0.75)]
off = []
for t, rh in cases:
    r = store(t, rh, SCEN["cen"])
    dep = t - r["twb"]
    mode = "Evaporative cooling" if dep >= 4 else "Hold by day, night ventilation"
    off.append((t, rh, r, dep, mode))
    pr(f"{t:.0f} C {rh*100:.0f} %: wb {r['twb']:.1f} C, depression {dep:.1f} K, supply {r['t_sup']:.1f} C, room {r['t_room']:.1f} C, drop {r['drop']:.1f} K, room RH {r['rh_room']*100:.0f} %, mode {mode}")
hold_q = D["room_volume_m3"] * 1.0
low_q, _ = operating_point(SCEN["cen"]["p0"], n_fans=1, speed=0.3)
pr(f"hold mode: 1 ACH needs {hold_q:.1f} m3/h; one fan at 30 % speed gives about {low_q*3600:.0f} m3/h ({low_q*3600/D['room_volume_m3']:.0f} ACH) at about {FAN_W*0.3**3:.2f} W shaft-scaled (take 2 W with driver losses)")
res("R4", "Humid-weather detection and mode change", "Threshold 4 K wet-bulb depression; 30 C, 75 % RH gives "
    f"{off[-1][3]:.1f} K and switches to hold; lamp shows mode", "Detect under 4 K and switch, with indicator", "Met (logic review; bench test later)")
res("R5", "Guard and minimum ventilation", f"Pump off at 95 % RH for 60 min; hold mode about {low_q*3600/D['room_volume_m3']:.0f} ACH at about 2 W",
    "Pump stop rule; 1 ACH or more with produce inside", "Met (logic review; bench test later)")
res("R6", "Tomato shelf life", "No calculation basis; ZECC data (about 1.8 times) come from a cooler, more humid chamber",
    "1.5 times ambient or more", "Not verifiable at TRL 3")

# ------------------------------------------------------------------ 4 energy (R7)
pr("\n== 4 Energy and solar (R7) ==")
PSH, LOSS = 5.0, 0.30
PUMP_W, CTRL_W = 6.0, 1.0
e_fans = 2 * FAN_W * (HOURS_COOL + HOURS_EVE)
e_pump = PUMP_W * HOURS_COOL
e_ctrl = CTRL_W * 24
e_day = e_fans + e_pump + e_ctrl
batt_wh = 12.8 * 12
batt_use = batt_wh * 0.8
night = 2 * FAN_W * HOURS_EVE + CTRL_W * (24 - HOURS_COOL)
pr(f"loads: fans {e_fans:.0f} Wh, pump {e_pump:.0f} Wh, controller {e_ctrl:.0f} Wh; total {e_day:.0f} Wh/day; peak load {2*FAN_W+PUMP_W+CTRL_W:.0f} W")
for pw in (100, 150):
    y = pw * PSH * (1 - LOSS)
    pr(f"{pw} W panel: {y:.0f} Wh/day, margin {(y/e_day - 1)*100:.0f} %")
y150 = 150 * PSH * (1 - LOSS)
pr(f"battery {batt_wh:.0f} Wh, usable {batt_use:.0f} Wh; after sunset need {night:.0f} Wh ({night/batt_use*100:.0f} % of usable); "
   f"full-speed night ventilation beyond the 2 h evening run lasts {(batt_use - night)/(2*FAN_W):.1f} h more")
isc = 9.0
pr(f"150 W panel Isc about {isc:.1f} A; 1.25 x Isc = {1.25*isc:.1f} A, so the PWM controller must be 20 A (10 A too small)")
for mm2 in (1.5, 2.5):
    rwire = 0.0172 / mm2 * 2 * 6.0
    pr(f"PV cable {mm2} mm2, 6 m run: {rwire:.3f} ohm, drop {rwire*8.3:.2f} V at 8.3 A ({rwire*8.3/17.5*100:.1f} % of Vmp), loss {rwire*8.3**2:.1f} W")
pr(f"charge current up to about 8.3 A into a 12 Ah pack = {8.3/12:.2f} C; BMS charge limit must be 10 A or more")
res("R7", "Design-day energy from one PV panel", f"{e_day:.0f} Wh/day needed; 150 W panel gives {y150:.0f} Wh/day ({(y150/e_day-1)*100:.0f} % margin)",
    "10 h cooling plus 2 h evening, no grid", "Met")

# ------------------------------------------------------------------ 5 water (R8)
pr("\n== 5 Water (R8) ==")
pad_l = c["pad_evap_kgh"] * HOURS_COOL
cav_w = U_OUT_WET * A["wall_out"] * (35 - c["t_cav"])
cav_l = cav_w * 12 * 3600 / HFG
bleed = 4.0
total_w = pad_l + cav_l + bleed
sump_gross = math.pi * (P["SUMP_D"] / 2000) ** 2 * P["SUMP_H"] / 1000 * 1000
sump_work = 60.0
pad_len = P["PAD_W"] / 1000
flow_lpm = 6.0 * pad_len
hyd = 1000 * 9.81 * 2.0 * flow_lpm / 60000
pr(f"pad evaporation {c['pad_evap_kgh']:.2f} kg/h, {pad_l:.1f} L over {HOURS_COOL:.0f} h; unfavorable {R['unf']['pad_evap_kgh']*HOURS_COOL:.1f} L, favorable {R['fav']['pad_evap_kgh']*HOURS_COOL:.1f} L")
pr(f"cavity: {cav_w:.0f} W through the outer leaf over 12 h equivalent = {cav_l:.1f} L/day (allowance in TRL 2: 20 L)")
pr(f"bleed and cleaning {bleed:.0f} L; total {total_w:.1f} L/day")
pr(f"sump {sump_gross:.0f} L gross, {sump_work:.0f} L working; pad and bleed per day {pad_l + bleed:.1f} L")
pr(f"pad wetting flow {flow_lpm:.1f} L/min (6 L/min per m of pad length, assumed); hydraulic power at 2 m head {hyd:.2f} W; at 20 % pump efficiency {hyd/0.2:.1f} W")
res("R8", "Water per design day; sump capacity", f"{total_w:.0f} L/day (pad {pad_l:.0f}, cavity {cav_l:.0f}, bleed {bleed:.0f}); sump {sump_work:.0f} L for {pad_l + bleed:.0f} L of pad use",
    "70 L or less; sump at least one day", "Met" if total_w <= 70 and sump_work >= pad_l + bleed else "Not met")

# ------------------------------------------------------------------ 6 electrical safety (R9)
pr("\n== 6 Electrical (R9) ==")
i_load = (2 * FAN_W + PUMP_W + CTRL_W) / 12.8
pr(f"load current {i_load:.1f} A; charge current up to 8.3 A; 15 A terminal fuse above both, below the 1.5 mm2 cable rating")
res("R9", "12 V DC, fused, guarded, door opens from inside", "12.8 V system, 15 A terminal fuse; guards both faces; inside release (design review)",
    "12 V DC, fused, guarded, inside release", "Met (design review)")
res("R10", "Local build; 30 min part swaps", "Masonry, timber and generic 12 V parts; swap times and parts survey need the partner",
    "Local trades; swap in 30 min or less", "Not verifiable at TRL 3")

# ------------------------------------------------------------------ 7 structure (R11)
pr("\n== 7 Structure (R11) ==")
RHO_BRICK, RHO_SAND = 1800.0, 1900.0
nominal = (0.240 * 0.085)          # 230 x 110 x 75 brick with 10 mm joints, laid on bed, one leaf
leaf_area_out = 2 * ((D["out_l"] - P["LEAF"]) + (D["out_w"] - P["LEAF"])) / 1000 * D["top"] / 1000
leaf_area_in = 2 * ((P["IN_L"] + P["LEAF"]) + (P["IN_W"] + P["LEAF"])) / 1000 * D["top"] / 1000
open_both = 2 * (D["door_area_m2"] + D["pad_area_m2"] + D["fan_area_m2"])
wall_bricks = (leaf_area_out + leaf_area_in - open_both) / nominal
floor_bricks = A["floor"] / (0.240 * 0.125)
bricks = (wall_bricks + floor_bricks) * 1.10
wall_vol = (leaf_area_out + leaf_area_in - open_both) * P["LEAF"] / 1000
cav_vol = (2 * ((P["IN_L"] + 2 * P["LEAF"] + P["CAV"]) + (P["IN_W"] + 2 * P["LEAF"] + P["CAV"])) / 1000 * D["top"] / 1000
           - (D["door_area_m2"] + D["pad_area_m2"] + D["fan_area_m2"])) * P["CAV"] / 1000
mass_walls = wall_vol * RHO_BRICK
mass_sand = cav_vol * RHO_SAND
line_load = (mass_walls + mass_sand) * 9.81 / (2 * (D["out_l"] + D["out_w"]) / 1000 - 2 * P["LEAF"] / 1000)
bearing = line_load / 0.45
pr(f"bricks: walls {wall_bricks:.0f}, floor {floor_bricks:.0f}, with 10 % waste {bricks:.0f}")
pr(f"brick volume {wall_vol:.2f} m3, {mass_walls/1000:.1f} t; wet sand {cav_vol:.2f} m3, {mass_sand/1000:.1f} t")
pr(f"wall line load {line_load/1000:.1f} kN/m; on a 450 mm strip footing {bearing/1000:.0f} kPa (firm soils allow about 100 kPa or more)")
V_WIND, CP_NET, RHO_W = 30.0, 1.5, 1.2
q_w = 0.5 * RHO_W * V_WIND ** 2
roof_a = D["roof_area_m2"]
uplift = CP_NET * q_w * roof_a
sheet_w = 5.0 * 9.81 * roof_a
per_post = (uplift - sheet_w) / 4
fdn = (P["FOOTING"] / 1000) ** 2 * P["FOOTING_DEPTH"] / 1000 * 23500
fdn400 = 0.4 ** 2 * P["FOOTING_DEPTH"] / 1000 * 23500
pr(f"roof uplift at {V_WIND:.0f} m/s gust, net Cp {CP_NET}: q {q_w:.0f} Pa, {uplift/1000:.1f} kN on {roof_a:.1f} m2; sheet weight {sheet_w/1000:.2f} kN; per post {per_post/1000:.2f} kN")
pr(f"footing {P['FOOTING']:.0f} x {P['FOOTING']:.0f} x {P['FOOTING_DEPTH']:.0f} mm concrete: {fdn/1000:.2f} kN (factor {fdn/per_post:.2f}); a 400 mm footing gives {fdn400/1000:.2f} kN (factor {fdn400/per_post:.2f})")
res("R11", "Durability: structure 10 years, pad and fans 3 years", f"Wall bearing {bearing/1000:.0f} kPa; post footings {fdn/per_post:.1f} x uplift at 30 m/s; pad and fan life from supplier data not yet available",
    "10 years structure; 3 years pad, fans, pump", "Not verifiable at TRL 3")

# ------------------------------------------------------------------ 8 cost (R12)
pr("\n== 8 Cost (R12) ==")
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
rows = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
groups = {"structure": (1, 2, 3, 4, 5, 12), "kit": (6, 7, 8, 9, 10, 11, 14), "crates": (13,)}
tot = {g: 0.0 for g in groups}
for r in rows:
    n = int(r["item"].split()[0])
    for g, ks in groups.items():
        if n in ks:
            tot[g] += int(r["qty"]) * float(r["unit_cost_usd"])
for g, v in tot.items():
    pr(f"{g}: ${v:,.2f}")
pr(f"store total, crates excluded: ${tot['structure'] + tot['kit']:,.2f}; kit against budget ${budget:.0f}: {tot['kit']/budget*100:.0f} % used, ${budget - tot['kit']:.0f} left")
res("R12", "Cooling equipment kit cost (structure costed separately)", f"Kit ${tot['kit']:.0f}; structure ${tot['structure']:.0f} (separate); crates ${tot['crates']:.0f} (user supplied)",
    f"Kit ${budget:.0f} or less", "Met" if tot["kit"] <= budget else "Not met")

# ------------------------------------------------------------------ results
pr("\n== Results against requirements ==")
for r in results:
    pr(" | ".join(r))
print("\n".join(out))
with (Path(__file__).parent / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["req", "quantity", "value", "target", "status"])
    w.writerows(results)
print("wrote docs/04-calcs/results.csv")
