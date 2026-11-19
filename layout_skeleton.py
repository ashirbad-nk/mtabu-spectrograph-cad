"""
layout_skeleton.py
Deterministic 3D Optical Ray & Mechanical Envelope Generator for the
Mt. Abu 1.2m Slit Spectrograph, Tip-Tilt Guider & Annular Field Imager
(Direct-Focus Architecture).

Run inside FreeCAD (Macro -> Execute or `freecadcmd layout_skeleton.py`).
Generates:
  1. Exact 3D optical ray paths for all branches (Annular Direct-Focus, Guider, Spectrograph)
  2. Parametric 3D mechanical envelopes (Pierced mirror at Z=-200, FSM at Z=-90, Slit at focus)
  3. Telescope Cassegrain reference ring at Z=-350 mm
  4. Automated pair-wise minimum clearance / collision audit (`distToShape`)
"""

import math
import FreeCAD as App
import Part

DOC_NAME = "MtAbu_1p2m_Spectrograph_Guider"


def get_or_create_doc(name):
    if name in App.listDocuments():
        App.closeDocument(name)
    return App.newDocument(name)


def vec(t):
    if isinstance(t, App.Vector):
        return t
    return App.Vector(float(t[0]), float(t[1]), float(t[2]))


def unit(v):
    if not isinstance(v, App.Vector):
        v = vec(v)
    l = v.Length
    if l == 0:
        raise ValueError("Zero-length vector")
    return App.Vector(v.x / l, v.y / l, v.z / l)


def rot_from_z_to(target_dir):
    """Return FreeCAD.Rotation aligning local +Z to target_dir."""
    z_axis = App.Vector(0, 0, 1)
    t = unit(target_dir)
    return App.Rotation(z_axis, t)


def make_cylinder_between(p1, p2, radius):
    p1v, p2v = vec(p1), vec(p2)
    diff = p2v.sub(p1v)
    length = diff.Length
    if length < 1e-6:
        return None
    cyl = Part.makeCylinder(radius, length, p1v, unit(diff))
    return cyl


def make_disk_at(center, normal, radius, thickness, center_on_front_face=True):
    c = vec(center)
    n = unit(normal)
    if center_on_front_face:
        start_pt = c
        ext_dir = n.multiply(-1.0)
    else:
        start_pt = c.sub(n.multiply(thickness / 2.0))
        ext_dir = n
    return Part.makeCylinder(radius, thickness, start_pt, ext_dir)


def make_pierced_mirror(center, normal, outer_diam=50.8, thickness=9.5, hole_diam=18.0, beam_dir=(0, 0, 1)):
    c = vec(center)
    n = unit(normal)
    b = unit(vec(beam_dir))

    blank = Part.makeCylinder(outer_diam / 2.0, thickness, c, n.multiply(-1.0))

    # Bore hole along incoming telescope beam axis (+Z) passing through center
    bore_len = thickness * 4.0
    bore_start = c.sub(b.multiply(bore_len / 2.0))
    hole_cyl = Part.makeCylinder(hole_diam / 2.0, bore_len, bore_start, b)

    # Rear chamfer cone starting 2 mm behind front reflective surface
    chamfer_start = c.add(b.multiply(2.0))
    chamfer_cone = Part.makeCone(hole_diam / 2.0, hole_diam / 2.0 + 4.0, bore_len / 2.0, chamfer_start, b)

    cut_tool = hole_cyl.fuse(chamfer_cone)
    pierced = blank.cut(cut_tool)
    return pierced


def add_part(doc, group, name, shape, color=(0.75, 0.78, 0.82), transparency=0):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    group.addObject(obj)
    if App.GuiUp and hasattr(obj, "ViewObject"):
        obj.ViewObject.ShapeColor = color
        obj.ViewObject.Transparency = transparency
    return obj


def build_layout():
    doc = get_or_create_doc(DOC_NAME)
    grp_rays = doc.addObject("App::DocumentObjectGroup", "Optical_Rays")
    grp_optics = doc.addObject("App::DocumentObjectGroup", "Optics_and_Stages")

    # -------------------------------------------------------------------------
    # 1. EXACT STATION ANCHORS (mm) - DIRECT FOCUS ARCHITECTURE
    # -------------------------------------------------------------------------
    p_flange = (0.0, 0.0, -350.0)      # Cassegrain mounting flange reference
    p_m1 = (0.0, 0.0, -200.0)          # 2" pierced mirror at Z=-200 mm (reflects +Z -> +X)
    p_cff = (200.0, 0.0, -200.0)       # ASI6200MM Pro placed directly at reflected f/13 focus

    p_fsm = (0.0, 0.0, -90.0)          # PI S-335.2SHM2 FSM in converging beam (reflects +Z -> +Y)
    p_mcal = (0.0, 30.0, -90.0)        # Motorized calibration flip mirror
    p_bs = (0.0, 55.0, -90.0)          # 92T / 8R pellicle beamsplitter
    p_cgd = (0.0, 55.0, -55.0)         # ASI290MM Mini guider camera at 8% focus
    p_slit = (0.0, 90.0, -90.0)        # Spectrograph slit at EXACT TELESCOPE FOCUS
    p_lcol = (0.0, 290.0, -90.0)       # Collimator doublet f = 200 mm
    p_vph = (0.0, 340.0, -90.0)        # 600 l/mm VPH grating (compacted to 50 mm past collimator)

    dev_rad = math.radians(20.8)
    d_spec = (-math.sin(dev_rad), math.cos(dev_rad), 0.0)
    p_lcam = (
        p_vph[0] + 45.0 * d_spec[0],
        p_vph[1] + 45.0 * d_spec[1],
        -90.0,
    )
    p_cspec = (
        p_lcam[0] + 100.0 * d_spec[0],
        p_lcam[1] + 100.0 * d_spec[1],
        -90.0,
    )

    # -------------------------------------------------------------------------
    # 2. OPTICAL RAY CENTERLINES
    # -------------------------------------------------------------------------
    rays = [
        ("Ray_01_Telescope_In", p_flange, p_m1, 2.5, (1.0, 0.85, 0.1)),
        ("Ray_02_Annular_DirectFocus", p_m1, p_cff, 3.5, (0.2, 0.8, 1.0)),
        ("Ray_03_Central_to_FSM", p_m1, p_fsm, 2.3, (1.0, 0.35, 0.1)),
        ("Ray_04_FSM_to_Slit", p_fsm, p_slit, 2.3, (1.0, 0.35, 0.1)),
        ("Ray_05_Guider_8pct", p_bs, p_cgd, 1.5, (0.2, 1.0, 0.3)),
        ("Ray_06_Slit_to_VPH", p_slit, p_vph, 3.0, (1.0, 0.5, 0.1)),
        ("Ray_07_VPH_to_SpecCam", p_vph, p_cspec, 3.0, (0.8, 0.3, 1.0)),
    ]
    for rname, a, b, rad, col in rays:
        cyl = make_cylinder_between(a, b, rad)
        if cyl:
            add_part(doc, grp_rays, rname, cyl, color=col, transparency=40)

    # -------------------------------------------------------------------------
    # 3. MECHANICAL & OPTICAL ENVELOPES
    # -------------------------------------------------------------------------
    solids = {}

    # Cassegrain Interface Flange Reference Ring (at Z = -350 mm, ID 100 mm)
    flange_outer = Part.makeCylinder(140.0, 15.0, vec(p_flange), App.Vector(0, 0, 1))
    flange_bore = Part.makeCylinder(50.0, 25.0, vec((0, 0, -355.0)), App.Vector(0, 0, 1))
    solids["Cassegrain_Flange"] = flange_outer.cut(flange_bore)

    # M1: Pierced mirror at Z=-200, normal (+0.7071, 0, -0.7071), Dia 18 mm hole
    solids["M1_PiercedMirror"] = make_pierced_mirror(
        p_m1, normal=(1.0, 0.0, -1.0), outer_diam=50.8, thickness=9.5, hole_diam=18.0
    )

    # C_FF: ZWO ASI6200MM Pro placed directly at reflected focus (X=200, Y=0, Z=-200)
    # Sensor plane at X=200 facing -X. Flange is at X = 200 - 17.5 = 182.5 mm.
    # Camera body extends from X=182.5 mm along +X by 97 mm to X=279.5 mm.
    p_cff_flange = (p_cff[0] - 17.5, p_cff[1], p_cff[2])
    solids["C_FF_ASI6200MM"] = Part.makeCylinder(45.0, 97.0, vec(p_cff_flange), App.Vector(1.0, 0.0, 0.0))

    # FSM: PI S-335.2SHM2 mirror at Z=-90, normal (0, +0.7071, -0.7071)
    fsm_normal = unit(App.Vector(0.0, 1.0, -1.0))
    fsm_mirror = Part.makeCylinder(12.7, 5.0, vec(p_fsm), fsm_normal.multiply(-1.0))
    fsm_body_start = vec(p_fsm).sub(fsm_normal.multiply(5.0))
    fsm_body = Part.makeCylinder(21.0, 28.0, fsm_body_start, fsm_normal.multiply(-1.0))
    solids["FSM_PI_S335"] = fsm_mirror.fuse(fsm_body)

    # M_CAL: Motorized flip mirror (Thorlabs MFF101/M envelope offset to -X side)
    solids["M_CAL_FlipMirror"] = make_disk_at(
        (-42.0, p_mcal[1], p_mcal[2]), normal=(1.0, 0.0, 0.0), radius=16.0, thickness=22.0, center_on_front_face=False
    )

    # BS: 92T / 8R Pellicle Beamsplitter at Y=55, Z=-90
    solids["BS_Pellicle_92_8"] = make_disk_at(
        p_bs, normal=(0.0, -1.0, 1.0), radius=12.7, thickness=3.0, center_on_front_face=False
    )

    # C_GD: ZWO ASI290MM Mini at 8% guider focus (Y=55, Z=-55). Nosepiece at Z=-63.5.
    p_cgd_front = (p_cgd[0], p_cgd[1], p_cgd[2] - 8.5)
    solids["C_GD_ASI290MM"] = Part.makeCylinder(15.875, 61.0, vec(p_cgd_front), App.Vector(0.0, 0.0, 1.0))

    # SLIT: 150 um precision mounted slit at EXACT FOCUS (Y=90, Z=-90)
    solids["SLIT_150um"] = make_disk_at(
        p_slit, normal=(0.0, 1.0, 0.0), radius=12.7, thickness=6.0, center_on_front_face=False
    )

    # L_COL: Spectrograph collimator f=200 mm at Y=290
    solids["L_COL_f200"] = make_disk_at(
        p_lcol, normal=(0.0, 1.0, 0.0), radius=15.0, thickness=8.0, center_on_front_face=False
    )

    # VPH: 600 l/mm VPH Grating at Y=440
    lit_rad = math.radians(10.4)
    vph_normal = (-math.sin(lit_rad), math.cos(lit_rad), 0.0)
    solids["VPH_Grating_600lmm"] = make_disk_at(
        p_vph, normal=vph_normal, radius=25.4, thickness=6.0, center_on_front_face=False
    )

    # L_CAM: Spectrograph camera lens f=100 mm
    solids["L_CAM_f100"] = make_disk_at(
        p_lcam, normal=d_spec, radius=25.4, thickness=12.0, center_on_front_face=False
    )

    # C_SPEC: ZWO ASI2600MM Pro
    p_cspec_flange = (
        p_cspec[0] - 17.5 * d_spec[0],
        p_cspec[1] - 17.5 * d_spec[1],
        p_cspec[2],
    )
    solids["C_SPEC_ASI2600MM"] = Part.makeCylinder(45.0, 97.0, vec(p_cspec_flange), unit(vec(d_spec)))

    palette = {
        "Cassegrain_Flange": (0.6, 0.63, 0.68),
        "M1_PiercedMirror": (0.85, 0.88, 0.92),
        "C_FF_ASI6200MM": (0.85, 0.15, 0.15),
        "FSM_PI_S335": (0.15, 0.35, 0.75),
        "C_GD_ASI290MM": (0.85, 0.15, 0.15),
        "VPH_Grating_600lmm": (0.2, 0.75, 0.55),
        "C_SPEC_ASI2600MM": (0.85, 0.15, 0.15),
    }

    for sname, shp in solids.items():
        add_part(doc, grp_optics, sname, shp, color=palette.get(sname, (0.6, 0.65, 0.7)), transparency=15)

    doc.recompute()

    # -------------------------------------------------------------------------
    # 4. AUTOMATED PAIR-WISE CLEARANCE & COLLISION AUDIT
    # -------------------------------------------------------------------------
    names = list(solids.keys())
    min_allowed_clearance = 2.0  # mm
    collisions = []
    min_pair = (None, None, float("inf"))

    print("\n=== PAIR-WISE CLEARANCE AUDIT (Direct Focus Architecture) ===")
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            n1, n2 = names[i], names[j]
            dist = solids[n1].distToShape(solids[n2])[0]
            if dist < min_pair[2]:
                min_pair = (n1, n2, dist)
            if dist < min_allowed_clearance:
                collisions.append((n1, n2, dist))
                print(f"[COLLISION / TOO CLOSE] {n1} <-> {n2}: {dist:.2f} mm")

    if not collisions:
        print(f"PASS: 0 collisions detected across {len(names)} components.")
        print(f"Closest non-contacting pair: {min_pair[0]} <-> {min_pair[1]} = {min_pair[2]:.2f} mm")
    print("=========================================================\n")

    fcstd_path = "MtAbu_1p2m_Spectrograph_Guider.FCStd"
    doc.saveAs(fcstd_path)
    print(f"Saved layout model to {fcstd_path}")


if __name__ == "__main__":
    build_layout()
