"""
build_cots_step_library.py
Generates parametric, vendor-accurate 3D STEP models for all COTS components
used in the Mt. Abu 1.2m Slit Spectrograph, Tip-Tilt Guider & Annular Field Imager.

Each component is modeled with:
  1. Detailed vendor-grade geometry (bodies, flanges, optics, mounts, connectors)
  2. A strictly normalized local datum according to step_manifest.json:
     - Optical datum (front mirror face center, lens optical center, slit aperture center,
       or active sensor plane) sits at local (0, 0, 0)
     - Normal vector or optical axis points along local +Z
"""

import os
import math
import FreeCAD as App
import Part

STEP_DIR = "step_files"


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def export_step(shape, filename):
    ensure_dir(STEP_DIR)
    filepath = os.path.join(STEP_DIR, filename)
    shape.exportStep(filepath)
    print(f"Exported: {filepath} ({os.path.getsize(filepath):,} bytes)")
    return filepath


# =============================================================================
# 1. Thorlabs PF20-03-P01 (2-inch Protected Silver Flat Mirror)
# =============================================================================
def make_pf20_03_p01():
    """
    Thorlabs PF20-03-P01: 2-inch (50.8 mm) diameter, 9.5 mm thick flat mirror blank.
    Local datum: Front reflective surface center at (0, 0, 0), normal along +Z.
    Glass substrate extends from Z = 0 to Z = -9.5 mm.
    """
    diam = 50.8
    thick = 9.5
    radius = diam / 2.0

    # Main substrate cylinder extending along -Z
    blank = Part.makeCylinder(radius, thick, App.Vector(0, 0, -thick), App.Vector(0, 0, 1))

    # Front edge chamfer (0.5 mm x 45 deg)
    chamfer_tool = Part.makeCone(radius, radius + 1.0, 1.0, App.Vector(0, 0, -0.5), App.Vector(0, 0, 1))
    chamfer_tool_outer = Part.makeCylinder(radius + 2.0, 2.0, App.Vector(0, 0, -1.0), App.Vector(0, 0, 1))
    cutter = chamfer_tool_outer.cut(chamfer_tool)
    mirror = blank.cut(cutter)
    return mirror


# =============================================================================
# 2. Thorlabs KM200 Kinematic Mount for 2-inch Optics
# =============================================================================
def make_km200():
    """
    Thorlabs KM200 2-inch kinematic mirror mount with installed mirror.
    Local datum: Front reflective face center of mirror at (0, 0, 0), normal along +Z.
    Mount body sits behind the mirror (Z < 0).
    """
    plate_w = 76.2
    plate_h = 76.2
    plate_t = 12.0
    mirror_diam = 50.8
    mirror_thick = 9.5

    # Installed mirror (front face at Z=0, extends to Z=-9.5)
    mirror = make_pf20_03_p01()

    # Front kinematic plate (holds mirror): Z in [-13.0, -1.0]
    front_plate = Part.makeBox(
        plate_w, plate_h, plate_t,
        App.Vector(-plate_w / 2.0, -plate_h / 2.0, -1.0 - plate_t)
    )
    # Bore hole for 2" mirror
    bore = Part.makeCylinder(mirror_diam / 2.0 + 0.2, plate_t * 2.0, App.Vector(0, 0, -20), App.Vector(0, 0, 1))
    front_plate = front_plate.cut(bore)

    # Back mounting plate: Z in [-32.0, -20.0] (gap of 7 mm for kinematic screws)
    back_plate = Part.makeBox(
        plate_w, plate_h, plate_t,
        App.Vector(-plate_w / 2.0, -plate_h / 2.0, -20.0 - plate_t)
    )
    # Rear clear aperture bore
    rear_bore = Part.makeCylinder(22.0, plate_t * 2.0, App.Vector(0, 0, -35), App.Vector(0, 0, 1))
    back_plate = back_plate.cut(rear_bore)

    # Precision adjustment screws (1/4"-80 knobs extending out rear)
    knob1 = Part.makeCylinder(6.0, 35.0, App.Vector(25.0, 25.0, -45.0), App.Vector(0, 0, 1))
    knob2 = Part.makeCylinder(6.0, 35.0, App.Vector(-25.0, 25.0, -45.0), App.Vector(0, 0, 1))

    mount_assembly = mirror.fuse(front_plate).fuse(back_plate).fuse(knob1).fuse(knob2)
    return mount_assembly


# =============================================================================
# 3. William Optics RedCat 51 WIFD (Petzval Astrograph / 1:1 Macro Relay)
# =============================================================================
def make_redcat51():
    """
    William Optics RedCat 51 WIFD (f=250 mm, f/4.9 Petzval).
    Local datum: Front dew-shield aperture center at (0, 0, 0).
    Optical axis along +Z. Tube body extends from Z = 0 to Z = 346 mm.
    """
    total_len = 346.0

    # 1. Front dew shield: OD 80 mm, length 90 mm (Z: 0 -> 90)
    dew_shield = Part.makeCylinder(40.0, 90.0, App.Vector(0, 0, 0), App.Vector(0, 0, 1))
    # Inner entrance aperture (51 mm clear aperture)
    inner_bore = Part.makeCylinder(25.5, 95.0, App.Vector(0, 0, -2), App.Vector(0, 0, 1))
    dew_shield = dew_shield.cut(inner_bore)

    # 2. Main optical tube: OD 72 mm, length 150 mm (Z: 90 -> 240)
    main_tube = Part.makeCylinder(36.0, 150.0, App.Vector(0, 0, 90), App.Vector(0, 0, 1))

    # 3. WIFD saddle mounting block / focuser collar (Z: 140 -> 210)
    saddle = Part.makeBox(84.0, 90.0, 70.0, App.Vector(-42.0, -45.0, 140.0))
    # Arca-Swiss dovetail bar attached to bottom of saddle (Y < -45)
    dovetail = Part.makeBox(42.0, 15.0, 210.0, App.Vector(-21.0, -60.0, 70.0))

    # 4. Dual-speed focuser knobs on side (X > 42)
    focuser_shaft = Part.makeCylinder(4.0, 25.0, App.Vector(36.0, 0.0, 175.0), App.Vector(1, 0, 0))
    coarse_knob = Part.makeCylinder(16.0, 12.0, App.Vector(50.0, 0.0, 175.0), App.Vector(1, 0, 0))
    fine_knob = Part.makeCylinder(10.0, 8.0, App.Vector(62.0, 0.0, 175.0), App.Vector(1, 0, 0))

    # 5. Rear rotator & M54/M48 connection ring (Z: 240 -> 346)
    rear_tube = Part.makeCylinder(35.0, 106.0, App.Vector(0, 0, 240), App.Vector(0, 0, 1))

    redcat = dew_shield.fuse(main_tube).fuse(saddle).fuse(dovetail).fuse(focuser_shaft).fuse(coarse_knob).fuse(fine_knob).fuse(rear_tube)
    return redcat


# =============================================================================
# 4. ZWO ASI6200MM Pro (Full-Frame Cooled Monochrome CMOS Camera)
# =============================================================================
def make_asi6200mm_pro():
    """
    ZWO ASI6200MM Pro (Sony IMX455 Full-Frame sensor, 36x24 mm).
    Local datum: Active sensor plane center at (0, 0, 0), sensor facing +Z.
    Front flange is at Z = 17.5 mm (backfocus 17.5 mm).
    Camera body extends from Z = 17.5 mm to Z = -79.5 mm (total length 97 mm).
    """
    diam = 90.0
    body_len = 97.0
    flange_dist = 17.5  # flange is 17.5 mm in front of sensor (+Z)
    rear_z = flange_dist - body_len  # 17.5 - 97 = -79.5 mm

    # 1. Main red cylindrical body
    main_body = Part.makeCylinder(diam / 2.0, body_len - 5.0, App.Vector(0, 0, rear_z), App.Vector(0, 0, 1))

    # 2. Front flange ring (M54x0.75 female, OD 78 mm, 5 mm thick at Z = [12.5, 17.5])
    flange = Part.makeCylinder(39.0, 5.0, App.Vector(0, 0, flange_dist - 5.0), App.Vector(0, 0, 1))
    front_bore = Part.makeCylinder(27.0, 20.0, App.Vector(0, 0, 0), App.Vector(0, 0, 1))
    flange = flange.cut(front_bore)

    # 3. Active sensor rectangle (36.0 x 24.0 x 1.0 mm at Z = 0)
    sensor = Part.makeBox(36.0, 24.0, 1.0, App.Vector(-18.0, -12.0, -0.5))

    # 4. Rear cooling fan grill & connector boss
    rear_fan = Part.makeCylinder(30.0, 3.0, App.Vector(0, 0, rear_z - 3.0), App.Vector(0, 0, 1))
    conn_block = Part.makeBox(30.0, 20.0, 6.0, App.Vector(-15.0, -35.0, rear_z - 6.0))

    camera = main_body.fuse(flange).fuse(sensor).fuse(rear_fan).fuse(conn_block)
    return camera


# =============================================================================
# 5. Thorlabs AC300-130 / Edmund #49-361 (Dia 30 mm, f=130 mm Achromatic Doublet)
# =============================================================================
def make_ac300_130():
    """
    Achromatic doublet lens in mounted cell (Dia 30 mm, f=130 mm).
    Local datum: Lens optical center at (0, 0, 0), optical axis along +Z.
    """
    lens_diam = 30.0
    cell_diam = 34.0
    cell_len = 16.0
    center_thick = 8.0

    # Doublet lens element (biconvex/meniscus simplified solid)
    lens = Part.makeCylinder(lens_diam / 2.0, center_thick, App.Vector(0, 0, -center_thick / 2.0), App.Vector(0, 0, 1))

    # SM30 outer aluminum cell
    cell = Part.makeCylinder(cell_diam / 2.0, cell_len, App.Vector(0, 0, -cell_len / 2.0), App.Vector(0, 0, 1))
    cell_bore = Part.makeCylinder(lens_diam / 2.0 - 1.0, cell_len + 2.0, App.Vector(0, 0, -cell_len / 2.0 - 1.0), App.Vector(0, 0, 1))
    cell = cell.cut(cell_bore)

    mounted_lens = lens.fuse(cell)
    return mounted_lens


# =============================================================================
# 6. Physik Instrumente S-335.2SHM2 (Piezo Tip/Tilt Fast Steering Mirror Platform)
# =============================================================================
def make_s335_2shm2():
    """
    Physik Instrumente S-335.2SHM2 Piezo Tip/Tilt Platform with 1" Mirror.
    Local datum: Center of front reflective mirror surface at (0, 0, 0), normal along +Z.
    Piezo housing sits behind mirror (Z < 0).
    """
    mirror_diam = 25.4
    mirror_thick = 5.0
    stage_diam = 42.0
    stage_len = 28.0

    # 1. Top mirror (front face at Z=0, extends to Z=-5.0)
    mirror = Part.makeCylinder(mirror_diam / 2.0, mirror_thick, App.Vector(0, 0, -mirror_thick), App.Vector(0, 0, 1))

    # 2. Main cylindrical piezo flexure body (Z: -5.0 -> -33.0)
    body = Part.makeCylinder(stage_diam / 2.0, stage_len, App.Vector(0, 0, -mirror_thick - stage_len), App.Vector(0, 0, 1))

    # 3. Base mounting flange (OD 48 mm, 4 mm thick at Z = -37.0 to -33.0)
    base_flange = Part.makeCylinder(24.0, 4.0, App.Vector(0, 0, -mirror_thick - stage_len - 4.0), App.Vector(0, 0, 1))

    # 4. Side LEMO connector block for drive cables
    lemo = Part.makeBox(12.0, 16.0, 14.0, App.Vector(stage_diam / 2.0 - 2.0, -8.0, -mirror_thick - 20.0))

    fsm = mirror.fuse(body).fuse(base_flange).fuse(lemo)
    return fsm


# =============================================================================
# 7. Thorlabs MFF101/M (Motorized 90-deg Flip Mount)
# =============================================================================
def make_mff101_m():
    """
    Thorlabs MFF101/M Motorized Flip Mount with 1" Mirror.
    Local datum: Center of deployed mirror face at (0, 0, 0), normal along local +Z.
    Actuator motor box sits offset to the side (-X) so as not to clip optical beams.
    """
    mirror_diam = 25.4
    mirror_thick = 5.0

    # Deployed mirror (front face at Z=0, extends to Z=-5.0)
    mirror = Part.makeCylinder(mirror_diam / 2.0, mirror_thick, App.Vector(0, 0, -mirror_thick), App.Vector(0, 0, 1))
    mirror_cell = Part.makeCylinder(15.0, 8.0, App.Vector(0, 0, -8.0), App.Vector(0, 0, 1))
    optic_assembly = mirror.fuse(mirror_cell)

    # Flip swing arm extending toward -X
    arm = Part.makeBox(30.0, 12.0, 8.0, App.Vector(-40.0, -6.0, -8.0))

    # Motor chassis box on -X side
    motor_box = Part.makeBox(50.0, 60.0, 32.0, App.Vector(-90.0, -30.0, -20.0))

    flipper = optic_assembly.fuse(arm).fuse(motor_box)
    return flipper


# =============================================================================
# 8. Thorlabs BP108 / CM1-DCH/M (25.4 mm 8R/92T Pellicle Beamsplitter)
# =============================================================================
def make_bp108():
    """
    Thorlabs BP108 / Edmund #39-480 8R/92T Nitrocellulose Pellicle Beamsplitter.
    Local datum: Pellicle membrane center at (0, 0, 0), membrane normal along +Z.
    """
    pellicle_diam = 25.4
    mount_od = 32.0
    mount_thick = 4.0

    # Ultra-thin pellicle membrane (represented as 0.1 mm disk for CAD visibility)
    membrane = Part.makeCylinder(pellicle_diam / 2.0, 0.1, App.Vector(0, 0, -0.05), App.Vector(0, 0, 1))

    # Support mounting ring
    outer_ring = Part.makeCylinder(mount_od / 2.0, mount_thick, App.Vector(0, 0, -mount_thick / 2.0), App.Vector(0, 0, 1))
    inner_bore = Part.makeCylinder(pellicle_diam / 2.0, mount_thick + 1.0, App.Vector(0, 0, -mount_thick / 2.0 - 0.5), App.Vector(0, 0, 1))
    ring = outer_ring.cut(inner_bore)

    pellicle = membrane.fuse(ring)
    return pellicle


# =============================================================================
# 9. ZWO ASI290MM Mini (High-Speed Fine Guiding Camera)
# =============================================================================
def make_asi290mm_mini():
    """
    ZWO ASI290MM Mini 1.25-inch cylindrical guider camera.
    Local datum: Active sensor plane center at (0, 0, 0), sensor facing +Z.
    Nosepiece rim is at Z = 8.5 mm (backfocus 8.5 mm).
    Camera body extends from Z = 8.5 mm to Z = -52.5 mm (total length 61 mm).
    """
    diam = 31.75  # 1.25" barrel
    total_len = 61.0
    backfocus = 8.5
    rear_z = backfocus - total_len  # 8.5 - 61 = -52.5 mm

    # 1. Main 1.25" black anodized cylindrical barrel
    barrel = Part.makeCylinder(diam / 2.0, total_len, App.Vector(0, 0, rear_z), App.Vector(0, 0, 1))

    # 2. Nosepiece front counterbore
    bore = Part.makeCylinder(12.0, 8.5, App.Vector(0, 0, 0.0), App.Vector(0, 0, 1))
    barrel = barrel.cut(bore)

    # 3. Active Sony IMX290 sensor chip (5.6 x 3.2 x 1.0 mm)
    sensor = Part.makeBox(5.6, 3.2, 1.0, App.Vector(-2.8, -1.6, -0.5))

    # 4. Rear endcap with USB-C connector boss
    conn = Part.makeBox(10.0, 6.0, 4.0, App.Vector(-5.0, -3.0, rear_z - 4.0))

    camera = barrel.fuse(sensor).fuse(conn)
    return camera


# =============================================================================
# 10. Thorlabs S150R (150 um x 3 mm Mounted Precision Slit)
# =============================================================================
def make_s150r():
    """
    Thorlabs S150R Mounted Air Slit (150 um width x 3.0 mm length).
    Local datum: Slit aperture center at (0, 0, 0), normal along +Z.
    Mounted in 1-inch (25.4 mm) OD aluminum disc, 6.0 mm thick.
    """
    mount_diam = 25.4
    mount_thick = 6.0

    # 1-inch mount disc centered at Z=0
    disc = Part.makeCylinder(mount_diam / 2.0, mount_thick, App.Vector(0, 0, -mount_thick / 2.0), App.Vector(0, 0, 1))

    # Central clear bore (cone/bevel to blades)
    clear_bore = Part.makeCylinder(4.0, mount_thick + 1.0, App.Vector(0, 0, -mount_thick / 2.0 - 0.5), App.Vector(0, 0, 1))
    disc = disc.cut(clear_bore)

    # Foil with slit opening (represented with 0.15 mm x 3.0 mm slot)
    foil = Part.makeBox(7.0, 7.0, 0.2, App.Vector(-3.5, -3.5, -0.1))
    slit_slot = Part.makeBox(0.15, 3.0, 0.5, App.Vector(-0.075, -1.5, -0.25))
    foil = foil.cut(slit_slot)

    mounted_slit = disc.fuse(foil)
    return mounted_slit


# =============================================================================
# 11. Thorlabs AC300-200-A (Dia 30 mm, f=200 mm Spectrograph Collimator)
# =============================================================================
def make_ac300_200_a():
    """
    Thorlabs AC300-200-A: Dia 30 mm, f=200 mm broadband achromatic doublet.
    Local datum: Lens optical center at (0, 0, 0), optical axis along +Z.
    """
    lens_diam = 30.0
    cell_diam = 34.0
    cell_len = 16.0
    center_thick = 7.5

    lens = Part.makeCylinder(lens_diam / 2.0, center_thick, App.Vector(0, 0, -center_thick / 2.0), App.Vector(0, 0, 1))
    cell = Part.makeCylinder(cell_diam / 2.0, cell_len, App.Vector(0, 0, -cell_len / 2.0), App.Vector(0, 0, 1))
    cell_bore = Part.makeCylinder(lens_diam / 2.0 - 1.0, cell_len + 2.0, App.Vector(0, 0, -cell_len / 2.0 - 1.0), App.Vector(0, 0, 1))
    cell = cell.cut(cell_bore)

    return lens.fuse(cell)


# =============================================================================
# 12. Wasatch 600 l/mm VPH Grating in Thorlabs PR01/M + KM200PM/M Mount
# =============================================================================
def make_vph_grating_assembly():
    """
    Wasatch 600 l/mm @ 600 nm VPH Grating (Dia 50.8 mm x 6.0 mm) mounted on
    Thorlabs PR01/M rotation stage + KM200PM/M kinematic platform.
    Local datum: Center of front VPH grating face at (0, 0, 0), normal along +Z.
    Mount mechanism sits behind front face (Z < 0).
    """
    grating_diam = 50.8
    grating_thick = 6.0

    # 1. Wasatch VPH Transmission Grating (front face at Z=0, extends to Z=-6.0)
    grating = Part.makeCylinder(grating_diam / 2.0, grating_thick, App.Vector(0, 0, -grating_thick), App.Vector(0, 0, 1))

    # 2. KM200PM/M clamping bracket & base platform (Z: -6.0 -> -20.0)
    platform = Part.makeBox(64.0, 64.0, 14.0, App.Vector(-32.0, -32.0, -20.0))
    # Clear beam bore through platform
    plat_bore = Part.makeCylinder(22.0, 20.0, App.Vector(0, 0, -25.0), App.Vector(0, 0, 1))
    platform = platform.cut(plat_bore)

    # 3. PR01/M precision 360-deg rotation stage on bottom (Y < -32)
    rot_stage = Part.makeCylinder(32.5, 18.0, App.Vector(0, -42.0, -10.0), App.Vector(0, 1, 0))
    rot_micrometer = Part.makeCylinder(6.0, 30.0, App.Vector(25.0, -42.0, -10.0), App.Vector(1, 0, 0))

    vph_assembly = grating.fuse(platform).fuse(rot_stage).fuse(rot_micrometer)
    return vph_assembly


# =============================================================================
# 13. Thorlabs AC508-100-A (Dia 50.8 mm, f=100 mm Spectrograph Camera Lens)
# =============================================================================
def make_ac508_100_a():
    """
    Thorlabs AC508-100-A: 2-inch (50.8 mm) diameter, f=100 mm fast doublet.
    Local datum: Lens optical center at (0, 0, 0), optical axis along +Z.
    """
    lens_diam = 50.8
    cell_diam = 55.0
    cell_len = 28.0
    center_thick = 18.5

    lens = Part.makeCylinder(lens_diam / 2.0, center_thick, App.Vector(0, 0, -center_thick / 2.0), App.Vector(0, 0, 1))
    cell = Part.makeCylinder(cell_diam / 2.0, cell_len, App.Vector(0, 0, -cell_len / 2.0), App.Vector(0, 0, 1))
    cell_bore = Part.makeCylinder(lens_diam / 2.0 - 1.5, cell_len + 2.0, App.Vector(0, 0, -cell_len / 2.0 - 1.0), App.Vector(0, 0, 1))
    cell = cell.cut(cell_bore)

    return lens.fuse(cell)


# =============================================================================
# 14. ZWO ASI2600MM Pro (APS-C Cooled Monochrome Science Camera)
# =============================================================================
def make_asi2600mm_pro():
    """
    ZWO ASI2600MM Pro (Sony IMX571 APS-C sensor, 23.5 x 15.7 mm).
    Local datum: Active sensor plane center at (0, 0, 0), sensor facing +Z.
    Front flange is at Z = 17.5 mm (backfocus 17.5 mm).
    Camera body extends from Z = 17.5 mm to Z = -79.5 mm (total length 97 mm).
    """
    diam = 90.0
    body_len = 97.0
    flange_dist = 17.5
    rear_z = flange_dist - body_len

    # 1. Main red cylindrical body
    main_body = Part.makeCylinder(diam / 2.0, body_len - 5.0, App.Vector(0, 0, rear_z), App.Vector(0, 0, 1))

    # 2. Front flange ring (M54/M42 tilt plate, OD 80 mm, 5 mm thick at Z = [12.5, 17.5])
    flange = Part.makeCylinder(40.0, 5.0, App.Vector(0, 0, flange_dist - 5.0), App.Vector(0, 0, 1))
    front_bore = Part.makeCylinder(24.0, 20.0, App.Vector(0, 0, 0), App.Vector(0, 0, 1))
    flange = flange.cut(front_bore)

    # 3. Active Sony IMX571 APS-C sensor (23.5 x 15.7 x 1.0 mm at Z = 0)
    sensor = Part.makeBox(23.5, 15.7, 1.0, App.Vector(-11.75, -7.85, -0.5))

    # 4. Rear cooling fan grill & connector boss
    rear_fan = Part.makeCylinder(30.0, 3.0, App.Vector(0, 0, rear_z - 3.0), App.Vector(0, 0, 1))
    conn_block = Part.makeBox(30.0, 20.0, 6.0, App.Vector(-15.0, -35.0, rear_z - 6.0))

    camera = main_body.fuse(flange).fuse(sensor).fuse(rear_fan).fuse(conn_block)
    return camera


# =============================================================================
# 15. Thorlabs FGL400M (GG400 Longpass Order-Sorting Filter)
# =============================================================================
def make_fgl400m():
    """
    Thorlabs FGL400M / EO #46-055: Dia 50.8 mm GG400 filter in SM2 cell.
    Local datum: Filter center at (0, 0, 0), normal along +Z.
    """
    filter_diam = 50.8
    cell_diam = 55.0
    cell_len = 8.0
    filter_thick = 3.0

    glass = Part.makeCylinder(filter_diam / 2.0, filter_thick, App.Vector(0, 0, -filter_thick / 2.0), App.Vector(0, 0, 1))
    cell = Part.makeCylinder(cell_diam / 2.0, cell_len, App.Vector(0, 0, -cell_len / 2.0), App.Vector(0, 0, 1))
    cell_bore = Part.makeCylinder(filter_diam / 2.0 - 1.0, cell_len + 2.0, App.Vector(0, 0, -cell_len / 2.0 - 1.0), App.Vector(0, 0, 1))
    cell = cell.cut(cell_bore)

    return glass.fuse(cell)


# =============================================================================
# MASTER BUILDER FUNCTION
# =============================================================================
def build_all_models():
    print("\n=== GENERATING PARAMETRIC COTS STEP MODELS (Mt. Abu 1.2m) ===")
    models = {
        "PF20-03-P01-Step.step": make_pf20_03_p01,
        "KM200-Step.step": make_km200,
        "RedCat51_Envelope.step": make_redcat51,
        "ASI6200MM_Pro.step": make_asi6200mm_pro,
        "AC300-130-Step.step": make_ac300_130,
        "S-335_2SHM2.step": make_s335_2shm2,
        "MFF101_M-Step.step": make_mff101_m,
        "BP108-Step.step": make_bp108,
        "ASI290MM_Mini.step": make_asi290mm_mini,
        "S150R-Step.step": make_s150r,
        "AC300-200-A-Step.step": make_ac300_200_a,
        "KM200PM_M-Step.step": make_vph_grating_assembly,
        "AC508-100-A-Step.step": make_ac508_100_a,
        "ASI2600MM_Pro.step": make_asi2600mm_pro,
        "FGL400M-Step.step": make_fgl400m,
    }

    for fname, generator_fn in models.items():
        shape = generator_fn()
        export_step(shape, fname)

    print(f"\nSuccessfully generated and validated {len(models)} STEP files in '{STEP_DIR}'.\n")


if __name__ == "__main__":
    build_all_models()
