#!/usr/bin/env python3
"""
etc_calculator.py
=============================================================================
Mount Abu Slit Spectrograph Exposure Time & Sensitivity Calculator (ETC)
Physical Research Laboratory (PRL), Mount Abu Observatory (Gurushikhar)

Supports both:
  1. Mt. Abu 1.2m Cassegrain Telescope (f/13, f = 15,600 mm)
  2. Mt. Abu 2.5m Telescope (f/8, f = 20,000 mm)

Detectors: Sony IMX571 sCMOS (ZWO ASI2600MM Pro) in HCG mode (RN = 1.45 e-)
Modes:
  - Mode 1: Medium-Resolution / Kinematics (R ~ 1060, 75 um slit)
  - Mode 2: Low-Resolution / Faint-Object (R ~ 530, 150 um slit)

Zero external dependencies: Pure Python standard library (math, sys, argparse).
=============================================================================
"""

import sys
import math
import argparse

# =============================================================================
# OPTICAL & TELESCOPE CONSTANTS
# =============================================================================
ZERO_MAG_FLUX = 1000.0          # photons / cm^2 / s / Angstrom at V = 0, 5500 A
T_ATM = 0.85                   # Atmospheric transmission at zenith, Mt Abu (1680 m)
T_TEL = 0.77                   # Telescope Primary + Secondary (0.88 * 0.88)
ETA_OPTICS = 0.655             # M1(0.98)*FSM(0.98)*BS(0.92)*Col(0.98)*FGL(0.92)*VPH(0.85)*Cam(0.98)
QE_SENSOR = 0.85               # IMX571 peak QE at 600 nm
RN_HCG = 1.45                  # Readout noise in High Conversion Gain mode (e- RMS)
DARK_CURRENT = 0.0005          # Dark current at -10 deg C (e- / pixel / s)
PIXEL_SIZE_UM = 3.76           # IMX571 pixel pitch (microns)
F_CAM = 100.0                  # Camera focal length (mm)
F_COL = 200.0                  # Collimator focal length (mm)
DEMAG = F_CAM / F_COL          # Demagnification (0.5x)
DISPERSION_A_PX = 0.616        # 600 l/mm VPH linear dispersion (Angstroms / pixel)

MOON_SKY_BRIGHTNESS = {
    "dark": 21.2,              # New Moon, Zenith, Dark Sky (mag / arcsec^2)
    "grey": 19.5,              # Quarter Moon (mag / arcsec^2)
    "bright": 18.0             # Full Moon (mag / arcsec^2)
}


def get_telescope_params(d_tel):
    """Return effective area (cm^2) and plate scale (arcsec/mm)."""
    if d_tel <= 1.5:
        # Mt. Abu 1.2m Cassegrain (f/13)
        # Linear obstruction ~33% (11% area)
        a_eff = math.pi * (120.0 / 2.0)**2 * (1.0 - 0.11) # cm^2 (~10,066 cm^2)
        plate_scale = 13.22 # arcsec / mm
        name = "Mt. Abu 1.2m Cassegrain (f/13)"
    else:
        # Mt. Abu 2.5m Cassegrain (f/8)
        # Linear obstruction ~30% (9% area)
        a_eff = math.pi * (250.0 / 2.0)**2 * (1.0 - 0.09) # cm^2 (~44,670 cm^2)
        plate_scale = 10.31 # arcsec / mm
        name = "Mt. Abu 2.5m Telescope (f/8)"
    return a_eff, plate_scale, name


def calculate_spectrograph_snr(
    d_tel=1.2,
    t_exp=1800.0,
    mag_v=18.0,
    r_power=530,
    slit_um=150,
    seeing_arcsec=1.5,
    moon="dark",
    tip_tilt=True,
    binning_spatial=2
):
    """
    Computes Signal-to-Noise Ratio (SNR) per spectral resolution element.
    """
    a_eff, plate_scale, _ = get_telescope_params(d_tel)
    sky_v = MOON_SKY_BRIGHTNESS.get(moon.lower(), 21.2)
    
    # Slit projected onto sky
    slit_arcsec = (slit_um / 1000.0) * plate_scale
    
    # Effective seeing (FSM tip-tilt centroid lock on 1.2m narrows effective long-exposure PSF)
    if tip_tilt and d_tel <= 1.5:
        eff_seeing = seeing_arcsec * 0.82
    else:
        eff_seeing = seeing_arcsec
        
    sigma = eff_seeing / 2.355
    eta_slit = math.erf((slit_arcsec / 2.0) / (math.sqrt(2.0) * sigma))
    
    # Total efficiency from top of atmosphere to detector electrons
    eta_tot = T_ATM * T_TEL * ETA_OPTICS * eta_slit * QE_SENSOR
    
    # Spectral resolution element width (Angstroms) at 6000 A
    dlambda = 6000.0 / r_power
    
    # Target photon count
    flux_target = ZERO_MAG_FLUX * (10.0 ** (-0.4 * mag_v))
    s_target = flux_target * dlambda * a_eff * eta_tot * t_exp
    
    # Sky background photon count
    flux_sky = ZERO_MAG_FLUX * (10.0 ** (-0.4 * sky_v))
    ext_height_arcsec = max(slit_arcsec, 1.8 * eff_seeing)
    sky_solid_angle = slit_arcsec * ext_height_arcsec
    
    # Sky fills the slit (no slit loss factor)
    eta_sky = T_ATM * T_TEL * ETA_OPTICS * 1.0 * QE_SENSOR
    b_sky = flux_sky * sky_solid_angle * dlambda * a_eff * eta_sky * t_exp
    
    # Detector extraction area in binned pixels
    px_disp = (slit_um * DEMAG) / PIXEL_SIZE_UM
    ext_px = (DEMAG * (ext_height_arcsec / plate_scale) * 1000.0) / PIXEL_SIZE_UM
    n_pix = px_disp * (ext_px / binning_spatial)
    
    # Noise terms
    var_source = s_target
    var_sky = b_sky
    var_detector = n_pix * (RN_HCG**2 + DARK_CURRENT * t_exp)
    tot_noise = math.sqrt(var_source + var_sky + var_detector)
    
    snr = s_target / tot_noise if tot_noise > 0 else 0.0
    
    return {
        "snr": snr,
        "s_target": s_target,
        "b_sky": b_sky,
        "tot_noise": tot_noise,
        "eta_slit": eta_slit,
        "slit_arcsec": slit_arcsec,
        "eff_seeing": eff_seeing,
        "dlambda": dlambda,
        "n_pix": n_pix
    }


def find_limiting_magnitude(
    d_tel=1.2,
    t_exp=1800.0,
    target_snr=10.0,
    r_power=530,
    slit_um=150,
    seeing_arcsec=1.5,
    moon="dark",
    tip_tilt=True,
    binning_spatial=2
):
    """Binary search root-finder to determine limiting V magnitude for target SNR."""
    low, high = 5.0, 26.0
    for _ in range(35):
        mid = (low + high) / 2.0
        res = calculate_spectrograph_snr(
            d_tel=d_tel,
            t_exp=t_exp,
            mag_v=mid,
            r_power=r_power,
            slit_um=slit_um,
            seeing_arcsec=seeing_arcsec,
            moon=moon,
            tip_tilt=tip_tilt,
            binning_spatial=binning_spatial
        )
        if res["snr"] > target_snr:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def find_required_exposure_time(
    d_tel=1.2,
    mag_v=18.0,
    target_snr=10.0,
    r_power=530,
    slit_um=150,
    seeing_arcsec=1.5,
    moon="dark",
    tip_tilt=True,
    binning_spatial=2
):
    """Binary search root-finder to determine exposure time (seconds) for target SNR."""
    low, high = 0.5, 360000.0  # 0.5 sec to 100 hours
    for _ in range(40):
        mid = (low + high) / 2.0
        res = calculate_spectrograph_snr(
            d_tel=d_tel,
            t_exp=mid,
            mag_v=mag_v,
            r_power=r_power,
            slit_um=slit_um,
            seeing_arcsec=seeing_arcsec,
            moon=moon,
            tip_tilt=tip_tilt,
            binning_spatial=binning_spatial
        )
        if res["snr"] < target_snr:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def print_comparison_tables():
    """Generates the master sensitivity comparison table between 1.2m and 2.5m."""
    t_exps = [60, 300, 900, 1800, 3600, 7200]
    snrs = [3, 5, 10, 30, 100]
    
    print("\n" + "=" * 90)
    print("MT. ABU OBSERVATORY SLIT SPECTROGRAPH — MASTER SENSITIVITY COMPARISON")
    print("Mount Abu 1.2m Cassegrain (f/13)  vs  Mount Abu 2.5m Telescope (f/8)")
    print("Dark Sky (V_sky = 21.2 mag/arcsec^2), Median Seeing (1.5 arcsec), IMX571 (HCG mode)")
    print("=" * 90)
    
    modes = [
        ("MODE 2: LOW-RESOLUTION (R ~ 530, Delta_lambda = 11.3 A, 150 um Slit)", 530, 150),
        ("MODE 1: MEDIUM-RESOLUTION (R ~ 1060, Delta_lambda = 5.7 A, 75 um Slit + FSM)", 1060, 75)
    ]
    
    for mode_title, r_power, slit_um in modes:
        print(f"\n>>> {mode_title}")
        header_12 = " | ".join([f"SNR={s:>3}" for s in snrs])
        header_25 = " | ".join([f"SNR={s:>3}" for s in snrs])
        print(f"             [ Mt. Abu 1.2m Telescope ]             |             [ Mt. Abu 2.5m Telescope ]")
        print(f"  t_exp (s) | {header_12} | {header_25}")
        print("  " + "-" * 86)
        
        for t in t_exps:
            row_12 = []
            row_25 = []
            for s in snrs:
                m12 = find_limiting_magnitude(1.2, t, s, r_power, slit_um, 1.5, "dark", True)
                m25 = find_limiting_magnitude(2.5, t, s, r_power, slit_um, 1.5, "dark", False)
                row_12.append(f"{m12:7.2f}")
                row_25.append(f"{m25:7.2f}")
            print(f"  {t:7d} s | " + " ".join(row_12) + " | " + " ".join(row_25))
    print("\n" + "=" * 90 + "\n")


def run_self_verification():
    """Runs automated unit verification checks."""
    print("Running automated verification tests...")
    
    # 1. 2.5m should be strictly deeper than 1.2m
    m12 = find_limiting_magnitude(1.2, 1800, 10, 530, 150)
    m25 = find_limiting_magnitude(2.5, 1800, 10, 530, 150)
    assert m25 > m12, f"2.5m ({m25}) must be deeper than 1.2m ({m12})"
    delta_m = m25 - m12
    assert 0.7 <= delta_m <= 1.4, f"Delta m ({delta_m:.2f}) expected between 0.7 and 1.4 mag"
    print(f"  [PASS] Aperture scaling: 1.2m = {m12:.2f} mag, 2.5m = {m25:.2f} mag (Delta = +{delta_m:.2f} mag)")
    
    # 2. Exposure time inverse solver check
    texp_calc = find_required_exposure_time(1.2, m12, 10, 530, 150)
    assert abs(texp_calc - 1800.0) < 5.0, f"Calculated t_exp ({texp_calc}) should match 1800 s"
    print(f"  [PASS] Bidirectional solver consistency: 1800 s -> {m12:.2f} mag -> {texp_calc:.1f} s")
    
    # 3. Mode 2 (R~530) should be deeper than Mode 1 (R~1060) due to wider dispersion element
    m_low = find_limiting_magnitude(1.2, 1800, 10, 530, 150)
    m_med = find_limiting_magnitude(1.2, 1800, 10, 1060, 75)
    assert m_low > m_med, f"Low-res mode ({m_low}) must be deeper than medium-res ({m_med})"
    print(f"  [PASS] Resolution trade-off: R~530 = {m_low:.2f} mag, R~1060 = {m_med:.2f} mag")
    
    # 4. Moonlight degradation check
    m_dark = find_limiting_magnitude(1.2, 1800, 10, 530, 150, moon="dark")
    m_bright = find_limiting_magnitude(1.2, 1800, 10, 530, 150, moon="bright")
    assert m_dark > m_bright, "Dark sky must be deeper than bright moon"
    print(f"  [PASS] Lunar sky penalty: Dark = {m_dark:.2f} mag, Full Moon = {m_bright:.2f} mag (Delta = -{m_dark-m_bright:.2f} mag)")
    
    print("\nALL AUTOMATED VERIFICATION TESTS PASSED SUCCESSFULLY!\n")


def main():
    parser = argparse.ArgumentParser(
        description="Mount Abu Observatory Slit Spectrograph Exposure Time & Sensitivity Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  1. Calculate SNR for an 18.5 mag star in 1800s on 1.2m telescope:
     python3 etc_calculator.py --tel 1.2 --mode 530 --mag 18.5 --texp 1800

  2. Find limiting magnitude for SNR=10 in 1800s on 2.5m telescope:
     python3 etc_calculator.py --tel 2.5 --mode 530 --texp 1800 --snr 10

  3. Find exposure time needed to achieve SNR=30 on a 17.5 mag target:
     python3 etc_calculator.py --tel 1.2 --mode 1060 --mag 17.5 --snr 30

  4. Print full sensitivity tables comparing 1.2m vs 2.5m:
     python3 etc_calculator.py --table
        """
    )
    parser.add_argument("--tel", type=float, default=1.2, choices=[1.2, 2.5], help="Telescope diameter in meters (1.2 or 2.5)")
    parser.add_argument("--mode", type=int, default=530, choices=[530, 1060], help="Resolving power mode: 530 (150 um slit) or 1060 (75 um slit)")
    parser.add_argument("--slit", type=int, default=None, help="Slit width in microns (default: 150 for mode 530, 75 for mode 1060)")
    parser.add_argument("--mag", type=float, default=None, help="Target star V-band magnitude")
    parser.add_argument("--texp", type=float, default=None, help="Exposure time in seconds")
    parser.add_argument("--snr", type=float, default=None, help="Desired target Signal-to-Noise Ratio (SNR)")
    parser.add_argument("--seeing", type=float, default=1.5, help="Atmospheric seeing FWHM in arcseconds (default: 1.5)")
    parser.add_argument("--moon", type=str, default="dark", choices=["dark", "grey", "bright"], help="Moon phase: dark, grey, or bright")
    parser.add_argument("--no-guiding", action="store_true", help="Disable active FSM tip-tilt centroid guiding")
    parser.add_argument("--table", action="store_true", help="Print comprehensive 1.2m vs 2.5m comparison tables")
    parser.add_argument("--verify", action="store_true", help="Run automated test and verification suite")

    args = parser.parse_args()

    if args.verify:
        run_self_verification()
        return

    if args.table:
        print_comparison_tables()
        return

    # Determine default slit if not specified
    slit_um = args.slit
    if slit_um is None:
        slit_um = 75 if args.mode == 1060 else 150
        
    tip_tilt = not args.no_guiding
    _, _, tel_name = get_telescope_params(args.tel)

    print("\n" + "=" * 70)
    print("MT. ABU OBSERVATORY SPECTROGRAPH EXPOSURE TIME CALCULATOR")
    print("=" * 70)
    print(f"Telescope:        {tel_name}")
    print(f"Observing Mode:   R ~ {args.mode} (Slit: {slit_um} um)")
    print(f"Seeing / Moon:    {args.seeing}\" seeing | {args.moon.upper()} sky ({MOON_SKY_BRIGHTNESS[args.moon]} mag/arcsec^2)")
    print(f"Tip-Tilt Guiding: {'ACTIVE (FSM Centroid Lock)' if tip_tilt and args.tel <= 1.5 else 'Passive / Open Loop'}")
    print("-" * 70)

    # Calculation logic branches
    if args.mag is not None and args.texp is not None:
        # Case 1: Compute SNR
        res = calculate_spectrograph_snr(
            d_tel=args.tel,
            t_exp=args.texp,
            mag_v=args.mag,
            r_power=args.mode,
            slit_um=slit_um,
            seeing_arcsec=args.seeing,
            moon=args.moon,
            tip_tilt=tip_tilt
        )
        print(f"Target Magnitude: V = {args.mag:.2f}")
        print(f"Exposure Time:    {args.texp:.1f} s ({args.texp/60.0:.1f} min)")
        print(f">>> EXPECTED SNR: {res['snr']:.2f} per resolution element ({res['dlambda']:.1f} A)")
        print(f"    Signal (e-):  {res['s_target']:.1f}")
        print(f"    Sky (e-):     {res['b_sky']:.1f}")
        print(f"    Total Noise:  {res['tot_noise']:.1f} e-")
        print(f"    Slit Throughput: {res['eta_slit']*100.0:.1f}%")

    elif args.texp is not None and args.snr is not None:
        # Case 2: Compute Limiting Magnitude
        lim_mag = find_limiting_magnitude(
            d_tel=args.tel,
            t_exp=args.texp,
            target_snr=args.snr,
            r_power=args.mode,
            slit_um=slit_um,
            seeing_arcsec=args.seeing,
            moon=args.moon,
            tip_tilt=tip_tilt
        )
        print(f"Exposure Time:    {args.texp:.1f} s ({args.texp/60.0:.1f} min)")
        print(f"Target SNR:       {args.snr:.1f}")
        print(f">>> LIMITING MAG: V = {lim_mag:.2f} mag")

    elif args.mag is not None and args.snr is not None:
        # Case 3: Compute Required Exposure Time
        req_texp = find_required_exposure_time(
            d_tel=args.tel,
            mag_v=args.mag,
            target_snr=args.snr,
            r_power=args.mode,
            slit_um=slit_um,
            seeing_arcsec=args.seeing,
            moon=args.moon,
            tip_tilt=tip_tilt
        )
        print(f"Target Magnitude: V = {args.mag:.2f}")
        print(f"Target SNR:       {args.snr:.1f}")
        print(f">>> REQUIRED TIME:{req_texp:.1f} s ({req_texp/60.0:.1f} min / {req_texp/3600.0:.2f} hours)")

    else:
        print("Please provide one of the following combinations:")
        print("  1. --mag [V] --texp [sec]  -> computes expected SNR")
        print("  2. --texp [sec] --snr [N]  -> computes limiting magnitude")
        print("  3. --mag [V] --snr [N]   -> computes required exposure time")
        print("  4. --table                 -> prints full comparison tables")
        print("Run with --help for all options.")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
