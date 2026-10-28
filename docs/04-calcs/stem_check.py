"""ZeerBox STEM check calculations (ZBX-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv and refreshes Table 1 of docs/01b-stem-check.md (between the
STM_TABLE markers). Option A rows (S) screen the claims of the existing design against independent
first-order estimates; the numbers being checked come from the calculation note ZBX-CAL-001
(docs/04-calcs/sizing.py, imported here, which reads cad/src/model.py). Option B rows (B) and option C
rows (C) screen the two other concept options of ZBX-OPT-001 at first order. All values are estimates.
"""
import contextlib
import io
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "docs/04-calcs")]
from stem_check import Check, G, WITHIN, PLAUSIBLE, FIX, FAILS, limits  # noqa: E402,F401

with contextlib.redirect_stdout(io.StringIO()):
    import sizing as CAL  # noqa: E402  ZBX-CAL-001

c = Check(ROOT / "docs/04-calcs/stem_results.csv")
cen, unf = CAL.R["cen"], CAL.R["unf"]
T_OUT, RH_OUT = 35.0, 0.30

# ------------------------------------------------------------------------------------------- option A
e8 = (8.0 + cen["rise"] / 2) / (T_OUT - cen["twb"])     # effectiveness at which the drop falls to 8 K, central heat load
# S1 wet bulb: independent empirical fit (Stull 2011), not the ASHRAE iteration CAL uses
rh = RH_OUT * 100
tw_stull = (T_OUT * math.atan(0.151977 * (rh + 8.313659) ** 0.5) + math.atan(T_OUT + rh) - math.atan(rh - 1.676331)
            + 0.00391838 * rh ** 1.5 * math.atan(0.023101 * rh) - 4.686035)
c.order_of_magnitude("S1", "Outside wet-bulb temperature at the 35 °C, 30 % RH design point is 21.5 °C", "Physics", "Thermodynamics",
                     claimed=round(cen["twb"], 2), estimate=tw_stull, unit="°C", factor=1.05,
                     law="Psychrometrics; independent check with the Stull (2011) wet-bulb fit", closed_by="ZBX-CAL-001 s4")
c.claim("S2", "Air leaving the pad (23.1 °C) stays above the wet-bulb temperature, the limit of direct evaporative cooling", "Physics", "Thermodynamics",
        "Adiabatic saturation: direct evaporative cooling cannot go below the wet bulb", round(cen["t_sup"], 2), round(cen["twb"], 2), "°C",
        rule="above", closed_by="ZBX-CAL-001 s4")
c.cited("S3", "A 150 mm cellulose pad reaches about 88 % saturation effectiveness at 0.52 m/s face velocity", "Physics", "Heat transfer",
        "NTU model calibrated to 75 % at 0.6 m/s for 100 mm (CAL assumption); maker data for deeper pads show 90 % or more (CELdek)",
        f"Within the range makers publish; the chosen pad's own chart is not yet in hand (ZBX-DEC-001 to confirm 2). The drop is set by it: PR-002 (8 K) holds down to about {e8 * 100:.0f} % effectiveness (independent review)", PLAUSIBLE, closed_by="")
q = cen["q"]
c.claim("S4", "Two 400 m³/h fans deliver about 563 m³/h through the pad, shutters and guards", "Physics", "Fluid mechanics",
        "A bound only: fan delivery cannot exceed the free-air flow of the two fans in parallel (800 m³/h); the operating point itself rests on S5", round(q * 3600), 2 * CAL.FAN_FREE, "m³/h",
        closed_by="ZBX-CAL-001 s3")
c.cited("S5", "The fan curve and the wet pad's pressure drop give the 18 Pa operating point", "Physics", "Fluid mechanics",
        "Straight-line fan curve to a 50 to 70 Pa shut-off; wet 100 mm pad 15 Pa at 1.0 m/s (CAL assumptions)",
        "Assumed curves; supplier data for the chosen fan and pad needed (ZBX-DEC-001 to confirm 2). At only about 18 Pa, a 3 m/s wind on the pad wall (about 5 Pa) moves the flow by 15 to 20 %, and in hold mode (one fan at 30 %, about 5 Pa shut-off) it can stall or reverse the flow (independent review)", PLAUSIBLE, closed_by="")
rise_est = cen["qtot"] / (1.15 * q * 1006)
c.order_of_magnitude("S6", "Store air warms about 2.35 K from supply to exhaust while it absorbs the 443 W heat load", "Physics", "Thermodynamics",
                     claimed=round(cen["rise"], 2), estimate=rise_est, unit="K", factor=1.2,
                     law="Steady-flow energy balance, rise = Q / (rho V cp), rho 1.15 kg/m3", closed_by="ZBX-CAL-001 s4")
c.claim("S7", "Mean store air is 10.7 K below outside air at the design point", "Physics", "Thermodynamics",
        "The store cannot be cooler than the supply air, so the drop is below effectiveness x wet-bulb depression (tighter bound, independent review)", round(cen["drop"], 2),
        round(cen["eff"] * (T_OUT - cen["twb"]), 2), "K", closed_by="ZBX-CAL-001 s4; rests on S3")
m_dry = q * 1.15
evap_est = m_dry * 1006 * (T_OUT - cen["t_sup"]) / 2.43e6 * 3600 * CAL.HOURS_COOL
c.order_of_magnitude("S8", "The pad evaporates about 32 L of water on the design day (10 h of cooling)", "Physics", "Thermodynamics",
                     claimed=round(CAL.pad_l, 1), estimate=evap_est, unit="L", factor=1.2,
                     law="Latent heat taken up equals the sensible heat given up by the air, h_fg 2.43 MJ/kg", closed_by="ZBX-CAL-001 s8")
# S9 store RH with Magnus saturation pressure and a moisture balance, independent of the ASHRAE functions
es = lambda t: 611.2 * math.exp(17.62 * t / (243.12 + t))
w_out = 0.622 * RH_OUT * es(T_OUT) / (101325 - RH_OUT * es(T_OUT))
w_sup = w_out + 1006 * (T_OUT - cen["t_sup"]) / 2.45e6
w_room = w_sup + CAL.LOAD_KG * CAL.SCEN["cen"]["transp"] / 86400 / cen["m"] / 2
pw = w_room * 101325 / (0.622 + w_room)
c.order_of_magnitude("S9", "Mean store RH is about 81 % while cooling at the design point", "Physics", "Thermodynamics",
                     claimed=round(cen["rh_room"] * 100, 1), estimate=pw / es(cen["t_room"]) * 100, unit="%", factor=1.05,
                     law="Moisture balance with the Magnus saturation pressure", closed_by="ZBX-CAL-001 s5; rests on S3 (about 1 point of RH per point of effectiveness)")
c.balance("S10", "One 150 W panel covers the 372 Wh design day (10 h cooling, 2 h evening ventilation)", "Engineering and technology", "Power and link budgets",
          inputs={"panel at 5 peak sun hours, 30 % losses": CAL.y150}, outputs={"fans": CAL.e_fans, "pump": CAL.e_pump, "controller": CAL.e_ctrl},
          unit="Wh/day", law=f"Energy balance; at 40 % losses (PWM, dust, harmattan haze, cable) the panel gives {150 * 5 * 0.6:.0f} Wh, still {150 * 5 * 0.6 / CAL.e_day * 100 - 100:.0f} % over (independent review)", closed_by="ZBX-CAL-001 s7")
eta_panel = CAL.P["PANEL_L"] * CAL.P["PANEL_W"] / 1e6
c.claim("S11", "A 150 W panel of 1,480 x 670 mm", "Physics", "Optics and radiation",
        "Module efficiency at 1,000 W/m2 below the Shockley-Queisser limit for one junction", round(150 / (eta_panel * 1000), 3),
        limits.SHOCKLEY_QUEISSER, "", closed_by="BOM line 10")
c.balance("S12", "The 12.8 V, 12 Ah battery carries the 62 Wh used after sunset", "Chemistry", "Electrochemistry and batteries",
          inputs={"usable at 80 % depth of discharge": CAL.batt_use}, outputs={"evening fans and controller": CAL.night}, unit="Wh",
          law="Energy balance", closed_by="ZBX-CAL-001 s7")
c.claim("S13", "A 20 A PWM charge controller suits the 150 W panel", "Engineering and technology", "Standards practice",
        "Controller rating at least 1.25 x the panel's short-circuit current (9 A); it must also have a LiFePO4 charge profile (about 14.2 to 14.4 V), no lead-acid temperature compensation and a low-voltage disconnect (BOM line 11)", 20.0, 1.25 * CAL.isc, "A", rule="above", closed_by="ZBX-CAL-001 s7")
c.claim("S14", "Two 12 W fans move 563 m³/h at about 18 Pa", "Physics", "Fluid mechanics",
        "Air power Q x dp cannot exceed the 24 W of electrical input (implied fan efficiency about 12 %, usual for small axial fans)",
        round(q * cen["dp"], 2), 2 * CAL.FAN_W, "W", closed_by="ZBX-CAL-001 s3")
c.claim("S15", "A 6 W pump lifts 3.6 L/min to the header 2 m up", "Physics", "Fluid mechanics",
        "Hydraulic power rho g H Q cannot exceed the electrical input", round(CAL.hyd, 2), CAL.PUMP_W, "W", closed_by="ZBX-CAL-001 s8")
# S16 load-circuit cable protection. The TRL 3 design fused the 1.5 mm2 load cable only by the 15 A battery
# terminal fuse; that failed (record below). Fix: a 5 A fuse on the load circuit, 2.5 mm2 battery leads (ZBX-DEC-001 D1).
IZ_15_B1, IZ_25_B1, K_45 = 17.5, 24.0, 0.79      # A, two loaded PVC conductors in conduit on a wall (method B1); 45 °C factor
iz_load = IZ_15_B1 * K_45
c.claim("S16", "The 1.5 mm² load cable in the 45 °C roof space is protected by its fuse", "Physics", "Electromagnetism and circuits",
        "Fuse rating I_n <= derated cable capacity I_z (IEC 60364-5-52 tables B.52.4 and B.52.14, to confirm against the edition used); 5 A load fuse at the source end of the run after the fix; both fuses DC rated with a breaking capacity above the battery's short-circuit current (D5)",
        5.0, round(iz_load, 1), "A", closed_by="ZBX-DEC-001 D1 (fix under the standing instruction); ZBX-CAL-001 s9")
c.claim("S17", "Each roof post footing holds down its share of the uplift at a 30 m/s gust", "Physics", "Mechanics and statics",
        "Footing weight against net uplift per post, with a factor of at least 1.5, at a 30 m/s gust and a mean net Cp of 1.5; the factor falls below 1.5 above about 32 m/s, and edge zones of a canopy reach Cp about 2 (independent review; ZBX-DEC-001 D7)", round(CAL.fdn / CAL.per_post, 2), 1.5, "", rule="above",
        closed_by="ZBX-CAL-001 s10")
c.claim("S18", "The 50 x 150 mm purlins carry the uplift on a 0.7 m strip over 3.7 m", "Physics", "Strength of materials",
        "Simply supported beam, sigma = M / Z; sawn softwood about 7 MPa allowed (grade to confirm); at an edge-zone Cp of 2.0 the stress reaches about 6.9 MPa (D7)", round(CAL.sig_pu, 2), CAL.SIG_ALLOW, "MPa", margin=0.1,
        closed_by="ZBX-CAL-001 s10")
c.claim("S19", "The 75 x 150 mm roof beams span 2.8 m between posts", "Physics", "Strength of materials",
        "Simply supported beam under the uplift less the sheet weight", round(CAL.sig_be, 2), CAL.SIG_ALLOW, "MPa", closed_by="ZBX-CAL-001 s10")
c.claim("S20", "Each purlin end needs a tie of 2 kN rated uplift", "Engineering and technology", "Standards practice",
        "Tie load from the purlin's uplift, half at each end; edge purlins carry more and the nails must hold the rating in the timber (D7)", round(CAL.tie / 1000, 2), 2.0, "kN", closed_by="ZBX-CAL-001 s10; ZBX-DEC-001 to confirm 4")
c.claim("S21", "Shelf rails carry four 22 kg crates over 1.05 m", "Physics", "Strength of materials",
        "Simply supported 50 x 75 mm rail, sigma = M / Z", round(CAL.sig, 2), 7.0, "MPa", closed_by="ZBX-CAL-001 s2")
c.claim("S22", "The 7 t of brick bears on a 450 mm strip footing", "Physics", "Mechanics and statics",
        "Bearing pressure against about 100 kPa allowed on firm soil; not valid on expansive clay or collapsible sand, so the site soil is to check", round(CAL.bearing / 1000, 1), 100.0, "kPa", closed_by="ZBX-CAL-001 s10")
c.order_of_magnitude("S23", "Dry loose rice husk conducts about 0.06 W/(m·K)", "Physics", "Heat transfer",
                     claimed=0.06, estimate=0.07, unit="W/(m·K)", law="Measured 0.065 to 0.075 W/(m·K) for rice husk insulators (Cigarruista Solis et al. 2024)",
                     closed_by="ZBX-CAL-001 s4.1 (at 0.075 the wall gain rises by about 14 W, about 0.1 K in the store; the review recommends 0.07 central and 0.06 to 0.09 in the scenarios at the next CAL revision)")
resp_est = 15 * 5 * 2.96e-3            # moderate class at 5 °C (Kader), about 5 x at 25 °C, 2.96 mW per mg CO2/(kg h)
c.order_of_magnitude("S24", "Mixed produce near 25 °C gives off about 0.15 W/kg of respiration heat", "Biology", "Plant and animal biology",
                     claimed=0.15, estimate=resp_est, unit="W/kg",
                     law="Respiration classes at 5 °C (Kader 2002), about 5 x at 25 °C; 10.7 J per mg CO2 from glucose oxidation", closed_by="ZBX-CAL-001 s4 (at 0.22 W/kg the store is about 0.2 K warmer, inside the unfavorable case at 0.25 W/kg)")
c.cited("S25", "Tomato shelf life rises at least 1.5 times over ambient storage in the dry season", "Biology", "Plant and animal biology",
        "Zero energy cool chambers raised tomato shelf life from 6 to 11 days (e-planet 18(2)); D-Lab Mali reported 10 days against 2 to 4 for peppers and eggplant",
        "Evidence comes from cooler, more humid passive chambers; a paired storage trial with the partner is needed (TRL 4)", PLAUSIBLE, closed_by="")
c.cited("S26", "Produce loses 0.5 to 2 % of its mass a day as water vapor, adding about 0.3 g/kg to the airstream", "Biology", "Plant and animal biology",
        "Transpiration allowance bracketing leafy and fruit crops; it moves store RH by under 2 percentage points",
        "Bracketed by the favorable and unfavorable cases", PLAUSIBLE, closed_by="ZBX-CAL-001 s5 (scenarios)")
c.cited("S27", "A covered, shaded sump drained weekly, a daily bleed and a pad dried out at the end of every cooling day keep Legionella growth low", "Biology", "Microbiology",
        "WHO, Legionella and the prevention of legionellosis (2007): stagnant warm water (25 to 45 °C), sediment and biofilm favour growth; drain, clean and keep systems dry. Exposure route: the pad's drift is carried through the room past people entering",
        "Controls follow the guidance: daily dry-out (pump off 60 min before the fans stop) and the bleed added (D5); fans run 10 min before entry; disinfection of the sump proposed (D8); sump water never touches produce", WITHIN, closed_by="ZBX-PRC-001 Safety; ZBX-DEC-001 D5")
resp_co2 = CAL.LOAD_KG * 0.15 / 2.96e-3 / 1e6 * 1000      # g/h of CO2 at the central respiration heat
ach1 = CAL.D["room_volume_m3"] * 1.0
ppm_1ach = resp_co2 / 1.80 / 1000 / ach1 * 1e6          # CO2 at about 1.80 g/L near 25 °C (independent review)
c.claim("S28", "With at least one air change an hour the store's CO2 stays below a 5,000 ppm workplace limit", "Biology", "Human physiology and biomechanics",
        "Steady-state CO2 rise = produce CO2 / ventilation; 480 kg at about 50 mg CO2/(kg h)", round(ppm_1ach + 420), 5000, "ppm",
        closed_by="ZBX-CAL-001 s6 (hold mode about 8 ACH)")
c.cited("S29", "Fired brick in the pad wall stays strong when wet", "Chemistry", "Materials and polymer chemistry",
        "Fired clay is a ceramic and does not soften in water, unlike unfired earth", "Material review", WITHIN, closed_by="ZBX-DEC-001 (fired brick)")
c.cited("S30", "Aluminium panel frames with stainless bolts on a galvanised roof do not corrode in a dry inland climate", "Chemistry", "Electrochemistry and batteries",
        "Zinc and aluminium sit close in the galvanic series; small stainless fasteners in a large aluminium area corrode little in dry, unpolluted air",
        "Aluminium is anodic to stainless, so EPDM isolating washers go under every stainless bolt on the aluminium frames by default (D5); inspection each season", WITHIN, closed_by="ZBX-DEC-001 D5; ZBX-BLD-001 section 3.13")
c.cited("S31", "A lithium iron phosphate battery with a BMS, kept shaded and charged between 0 and 45 °C, is safe in this duty", "Chemistry", "Electrochemistry and batteries",
        "LiFePO4 has a higher thermal-runaway onset than cobalt-based cells; makers limit charging to about 0 to 45 °C. In a shaded box on the outside wall at 35 to 40 °C air, charging at 0.69 C self-heats the pack toward that limit, so the BMS may stop charging at midday (independent review)",
        "Safe, because the BMS stops charging; the energy lost on the hottest days is to assess. Moving the power box into the cooled store is proposed to Amish (ZBX-DEC-001 D6)", PLAUSIBLE, closed_by="")
# S32 sensor error against the 4 K threshold: +-3 % RH and +-0.5 K at 30 °C, 75 % RH
dep = lambda t, r: t - CAL.wet_bulb(t, r)
err = max(abs(dep(30 + dt, 0.75 + dr) - dep(30, 0.75)) for dt in (-0.5, 0.5) for dr in (-0.03, 0.03))
c.claim("S32", "Low-cost sensors resolve the 4 K wet-bulb depression threshold", "Engineering and technology", "Sensing resolution",
        "Depression error from +-3 % RH and +-0.5 K at 30 °C, 75 % RH, against a quarter of the threshold; sun on an unshielded sensor would add 2 to 3 K, so the six-plate shield and a field calibration at TRL 4 are part of the claim", round(err, 2), 1.0, "K",
        closed_by="ZBX-CAL-001 s6")
c.order_of_magnitude("S33", "563 m³/h is 331 cfm and about 78 air changes an hour in the 7.2 m³ room", "Mathematics", "Units and dimensional analysis",
                     claimed=331, estimate=563 / 1.699, unit="cfm", factor=1.01, law="1 cfm = 1.699 m3/h", closed_by="ZBX-CAL-001 s3")
c.order_of_magnitude("S34", "The favorable to unfavorable range of the drop (9.8 to 11.4 K) brackets the inputs varied in the three scenarios (pad effectiveness, wall wetting, respiration, fan shut-off, leaks, sun, roof space, ground, transpiration); husk conductivity, the pad pressure-drop law, wind on the pad and sensor error are not varied (independent review)", "Mathematics", "Statistics and uncertainty",
                     claimed=round(cen["drop"], 2), estimate=(CAL.R["fav"]["drop"] + unf["drop"]) / 2, unit="K", factor=1.1,
                     law="Three-scenario bracketing of every uncertain input (CAL Table 1)", closed_by="ZBX-CAL-001 s4")
c.cited("S35", "The shaded roof space stays near 40 °C (38 to 43 °C) on the design day", "Physics", "Heat transfer",
        "Allowance for a ventilated 450 mm gap under a sunlit sheet roof; ceiling gain 46 W in the central case",
        "Assumption; a roof-space temperature log is needed (TRL 4)", PLAUSIBLE, closed_by="")
c.cited("S36", "The battery covers the controller and hold-mode ventilation through cloudy spells", "Engineering and technology", "Power and link budgets",
        "123 Wh usable; hold mode about 2 W plus the 1 W controller lasts about 40 h with no sun; beyond that the fans stop and the room is sealed",
        "A passive vent for the no-power case is proposed to Amish (ZBX-DEC-001 D3)", PLAUSIBLE, closed_by="")

c.claim("S37", "The daily bleed keeps the pad water at no more than 4 cycles of concentration, so hard water does not scale the pad", "Chemistry", "Inorganic chemistry",
        "Cycles of concentration = (evaporation + bleed) / bleed; cellulose pads scale above about 3 to 5 cycles in typical water (independent review). The TRL 3 design's 4 L bleed gave about 9 cycles; fixed (D5)",
        round((CAL.pad_l + CAL.bleed) / CAL.bleed, 2), 4.0, "cycles", closed_by="ZBX-DEC-001 D5; ZBX-CAL-001 s8 (bleed 10.6 L, total 43 L/day)")

# ------------------------------------------------------------------------------------------- option B
# First-order balance of a passive wet-wall chamber with option A's room: cavity held at the outside temperature
# minus half the wet-bulb depression (ZECC data), room ventilated by a low vent and a roof stack.
twb = cen["twb"]
t_cav = T_OUT - 0.5 * (T_OUT - twb)
A_in = CAL.A["wall_in"] + CAL.D["pad_area_m2"]          # no pad opening in option B (a small vent instead)
U_in = CAL.U_IN_WET
vent_area, h_stack = 0.02, 1.6                           # m2 each opening, m between them


def b_room():
    t = t_cav
    for _ in range(80):
        dT = max(T_OUT - t, 0.1)
        qv = 0.6 * vent_area * math.sqrt(2 * G * h_stack * dT / (t + 273.15))   # stack flow, cool room drains out of the low vent
        gains = (U_in * A_in * (t_cav - t) + CAL.U_CEIL * CAL.A["ceil"] * (40 - t) + CAL.U_FLOOR * CAL.A["floor"] * (30 - t)
                 + CAL.U_DOOR * CAL.A["door"] * (T_OUT - t) + CAL.LOAD_KG * 0.15 + 100 * 3900 * max(32 - t, 0) / (8 * 3600) + 50
                 + qv * 1.15 * 1006 * (T_OUT - t))
        # walls remove heat to the wet cavity when the room is warmer than it: solve the balance by relaxation
        t_new = t + gains / (U_in * A_in + qv * 1.15 * 1006 + 50) * 0.3
        if abs(t_new - t) < 1e-5:
            break
        t = t_new
    return t, qv


t_b, qv_b = b_room()
c.order_of_magnitude("B1", "Option B holds the full room about 3 K below outside air at the design point", "Physics", "Heat transfer",
                     claimed=3.0, estimate=T_OUT - t_b, unit="K",
                     law="Wall-to-wet-cavity balance with stack ventilation; ZECCs measured 4.4 to 5.0 K monthly mean, 7.25 K best day (e-planet 18(2))",
                     closed_by="ZBX-OPT-001 first-order numbers")
# water: evaporation from the wet outer leaf, h_c about 10 W/(m2 K), surface near the cavity temperature
w_s = 0.622 * es(t_cav) / (101325 - es(t_cav))
evap_b = 10 / 1006 * (w_s - w_out) * CAL.A["wall_out"] * 3600 * 10 * 0.5     # half the face effectively wet
c.order_of_magnitude("B2", "Option B uses about 70 L of water a day", "Physics", "Heat transfer",
                     claimed=70.0, estimate=evap_b + 12, unit="L", law="Evaporation from the wet outer leaf (Lewis relation) plus the cavity's conduction loss",
                     closed_by="ZBX-OPT-001 first-order numbers")
c.claim("B3", "A low vent and a roof stack of 0.02 m² each give option B at least one air change an hour", "Physics", "Fluid mechanics",
        "Stack flow Q = Cd A sqrt(2 g h dT / T), Cd 0.6, 1.6 m between openings; the room is cooler than outside, so cool air drains out of the low vent and 35 °C air enters at the stack (direction noted by the independent review)", round(qv_b * 3600 / CAL.D["room_volume_m3"], 1), 1.0, "ACH",
        rule="above", closed_by="ZBX-OPT-001 first-order numbers")
c.cited("B4", "Option B keeps the room humid (55 to 90 % RH)", "Physics", "Thermodynamics",
        "A moisture balance with produce transpiration alone and the B3 flow gives about 55 % RH (independent review); ZECCs report high humidity because their inner faces are wet",
        "Depends on how wet the inner leaf runs; to assess", PLAUSIBLE, closed_by="")
c.cited("B5", "A damp, slowly ventilated chamber grows mold on walls and produce unless cleaned and aired", "Biology", "Microbiology",
        "High humidity and little air movement favour mold; D-Lab notes cleaning and airing practice", "Practice; no growth figure claimed", PLAUSIBLE, closed_by="")

# ------------------------------------------------------------------------------------------- option C
q_turb = 250.0 / 3600            # m3/s from one 300 mm turbine ventilator in a light wind (assumption; no rated figure found)
eff_c = 0.75                     # wetted charcoal wall saturation effectiveness (Wayua et al. 2012: 74 to 87 %)
t_sup_c = T_OUT - eff_c * (T_OUT - twb)
gains_c = 443.0 - 85 + 160       # option A's gains, light timber walls in place of insulated brick (estimate)
rise_c = gains_c / (1.15 * q_turb * 1006)
drop_c = T_OUT - (t_sup_c + rise_c / 2)
c.cited("C1", "Option C holds the room about 7 K below outside air at the design point, in a light wind", "Physics", "Thermodynamics",
        "Wet-wall effectiveness 0.75 (Wayua et al. 2012 measured 74 to 87 % and 10.5 K at 14:00) and a heat balance on the ventilator flow",
        f"First-order {drop_c:.1f} K at 250 m³/h; conditional on C2, so it cannot be closed while C2 is open (independent review)", PLAUSIBLE, closed_by="")
c.cited("C2", "A 300 mm turbine ventilator draws about 250 m³/h in a light wind", "Physics", "Fluid mechanics",
        "Wind-driven extraction; no rated airflow found in the maker listing checked (MKT); calm days give little flow",
        "To assess with the maker's chart; option C's cooling scales with it", PLAUSIBLE, closed_by="")
evap_c = 1.15 * q_turb * 1006 * (T_OUT - t_sup_c) / 2.43e6 * 3600 * 10
c.order_of_magnitude("C3", "Option C uses about 40 L of water a day", "Physics", "Thermodynamics",
                     claimed=40.0, estimate=evap_c + 20, unit="L", law="Latent heat balance on the ventilator flow plus drip losses of about 20 L",
                     closed_by="ZBX-OPT-001 first-order numbers")
c.cited("C4", "Galvanised mesh lasts in permanently wet charcoal", "Chemistry", "Electrochemistry and batteries",
        "Wet carbon is an electrical conductor and noble to zinc; contact can speed corrosion of the galvanising", "Mesh life to assess; stainless or plastic mesh is the fallback",
        PLAUSIBLE, closed_by="")
c.cited("C5", "Wet charcoal walls stay free of mold and smell", "Biology", "Microbiology",
        "Permanently wet organic-carbon media can grow mold; charcoal coolers are washed and the charcoal replaced", "Practice to confirm with users", PLAUSIBLE, closed_by="")

state = c.write()

# Refresh Table 1 of the STEM check document
doc = ROOT / "docs/01b-stem-check.md"
if doc.exists():
    rows = ["| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in c.rows:
        rows.append("| " + " | ".join([r["id"], r["claim"], r["field"], r["branch"], r["law"], r["check"], r["verdict"], r["closed_by"] or "Open"]) + " |")
    text = doc.read_text(encoding="utf-8")
    new = re.sub(r"<!-- STM_TABLE -->.*?<!-- /STM_TABLE -->", "<!-- STM_TABLE -->\n" + "\n".join(rows) + "\n<!-- /STM_TABLE -->", text, flags=re.S)
    doc.write_text(new, encoding="utf-8")

if __name__ == "__main__":
    print(f"Record of the fix (ZBX-DEC-001 D1): before it, the 1.5 mm² load cable was protected only by the 15 A battery fuse, "
          f"above its derated capacity of {iz_load:.1f} A in a 45 °C roof space ({IZ_15_B1} A x {K_45})")
    print(f"Option B: room {t_b:.1f} °C, stack flow {qv_b * 3600:.0f} m³/h; water about {evap_b + 12:.0f} L/day")
    print(f"Option C: supply {t_sup_c:.1f} °C, rise {rise_c:.1f} K, drop {drop_c:.1f} K; water about {evap_c + 20:.0f} L/day")
    print(f"S36: no-sun ventilation {CAL.batt_use / 3.0:.0f} h at 3 W; CO2 at 1 ACH {ppm_1ach + 420:.0f} ppm; "
          f"sealed 12 h {resp_co2 * 12 / 1.80 / 1000 / CAL.D['room_volume_m3'] * 100:.1f} % CO2")
