"""
build_master_assembly.py
Direct-Focus Optical Architecture for the
Mt. Abu 1.2m Slit Spectrograph, Tip-Tilt Guider & Annular Field Imager.

Configuration:
  1. Telescope Cassegrain Flange Reference Ring at Z = -350 mm
  2. Converging beam space between Flange (Z = -350 mm) and Focus (Z = 0 mm)
  3. Pierced Mirror M1 placed in converging beam at Z = -200 mm
     - Reflects converging annular field +X directly onto ZWO ASI6200MM Pro sensor at focus (X = 200, Y = 0, Z = -200)
     - Zero relay lenses, zero fold mirrors!
  4. Central converging beam passes through 18 mm hole in M1 along +Z
  5. PI S-335.2SHM2 FSM placed in converging beam at Z = -90 mm
     - Folds beam +Z -> +Y directly onto the Spectrograph Slit at focus (Y = 90, Z = -90)
     - Zero pupil relay doublets!
  6. 92/8 Pellicle BS and Calibration Flip Mirror placed in converging beam ahead of slit
  7. Guider camera ASI290MM Mini placed directly at the 8% reflected focal plane
  8. Pure optical + camera layout: All extraneous brackets/pedestals/rails removed,
     retaining only the Cassegrain mounting flange reference ring.
"""

import os
import json
import math
import FreeCAD as App
import Part

DOC_NAME = "MtAbu_1p2m_Spectrograph_Guider_Assembly"
MANIFEST_PATH = "step_manifest.json"


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


def add_part_feature(doc, group, name, shape, color=(0.75, 0.78, 0.82), transparency=0):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    group.addObject(obj)
    if App.GuiUp and hasattr(obj, "ViewObject"):
        obj.ViewObject.ShapeColor = color
        obj.ViewObject.Transparency = transparency
    return obj


# =============================================================================
# 1. OPTICAL RAY BEAM GENERATION (DIRECT CONVERGING FOCUS ARCHITECTURE)
# =============================================================================
def build_optical_beams(doc, grp_beams):
    print("Building Direct-Focus 3D optical beam bundles...")

    # Key station anchors
    p_flange = App.Vector(0.0, 0.0, -350.0)
    p_m1 = App.Vector(0.0, 0.0, -200.0)
    p_cff = App.Vector(200.0, 0.0, -200.0)       # Reflected focus for Annular Field Imager
    p_fsm = App.Vector(0.0, 0.0, -90.0)         # FSM in converging beam
    p_bs = App.Vector(0.0, 55.0, -90.0)         # Pellicle beamsplitter
    p_cgd = App.Vector(0.0, 55.0, -55.0)        # 8% Guider camera focus
    p_slit = App.Vector(0.0, 90.0, -90.0)       # EXACT TELESCOPE FOCUS AT SLIT
    p_lcol = App.Vector(0.0, 290.0, -90.0)      # Collimator f = 200 mm
    p_vph = App.Vector(0.0, 340.0, -90.0)       # 600 l/mm VPH grating (compacted to 50 mm past collimator)

    dev_rad = math.radians(20.8)
    d_spec = unit(App.Vector(-math.sin(dev_rad), math.cos(dev_rad), 0.0))
    p_lcam = p_vph.add(d_spec.multiply(45.0))
    p_cspec = p_lcam.add(d_spec.multiply(100.0))

    # 1. Incoming Telescope f/13 Converging Beam (Flange Z=-350 -> M1 Z=-200)
    # At Z=-350: dia ~ 27 mm (radius 13.5 mm). At Z=-200: dia ~ 15.4 mm (radius 7.7 mm)
    cone_tel = Part.makeCone(13.5, 7.7, 150.0, p_flange, App.Vector(0, 0, 1))
    add_part_feature(doc, grp_beams, "Beam_01_Telescope_f13_Flange_to_M1", cone_tel, (1.0, 0.85, 0.2), transparency=45)

    # 2. Reflected Converging Annular Beam (M1 -> ASI6200MM Focus at X=200)
    # Starts at M1 with dia 15.4 mm (radius 7.7 mm) and converges to 0 mm at C_FF sensor
    cone_annular = Part.makeCone(7.7, 0.5, 200.0, p_m1, App.Vector(1, 0, 0))
    add_part_feature(doc, grp_beams, "Beam_02_Annular_Converging_Direct_Focus", cone_annular, (0.2, 0.8, 1.0), transparency=45)

    # 3. Central Converging Beam passing through M1 hole (M1 Z=-200 -> FSM Z=-90)
    # Converges from radius 7.7 mm to radius 3.5 mm at FSM
    cone_central = Part.makeCone(7.7, 3.5, 110.0, p_m1, App.Vector(0, 0, 1))
    add_part_feature(doc, grp_beams, "Beam_03_Central_Hole_to_FSM", cone_central, (1.0, 0.35, 0.1), transparency=45)

    # 4. Folded Converging Beam post-FSM (FSM Y=0 -> Slit Y=90)
    # Converges from radius 3.5 mm at FSM to 0.1 mm at Slit
    cone_to_slit = Part.makeCone(3.5, 0.1, 90.0, p_fsm, App.Vector(0, 1, 0))
    add_part_feature(doc, grp_beams, "Beam_04_FSM_to_Slit_Focus", cone_to_slit, (1.0, 0.35, 0.1), transparency=45)

    # 5. Guider 8% Reflected Converging Beam (BS Y=55 -> ASI290MM Focus Z=-55)
    # Converges from radius 1.4 mm at BS to focus at Guider sensor
    cone_guider = Part.makeCone(1.4, 0.2, 35.0, p_bs, App.Vector(0, 0, 1))
    add_part_feature(doc, grp_beams, "Beam_05_Guider_8pct_Focus", cone_guider, (0.1, 0.95, 0.3), transparency=45)

    # 6. Spectrograph: Diverging f/13 cone from Slit to Collimator (Slit Y=90 -> L_COL Y=290)
    # Diverges from 0.1 mm to 15.4 mm collimated pupil (radius 7.7 mm)
    cone_spec_col = Part.makeCone(0.1, 7.7, 200.0, p_slit, App.Vector(0, 1, 0))
    add_part_feature(doc, grp_beams, "Beam_06_Slit_to_Collimator", cone_spec_col, (0.9, 0.6, 0.1), transparency=45)

    # 7. Spectrograph: Collimated beam (L_COL Y=290 -> VPH Y=340)
    cyl_vph = Part.makeCylinder(7.7, 50.0, p_lcol, App.Vector(0, 1, 0))
    add_part_feature(doc, grp_beams, "Beam_07_Collimated_Pupil_to_VPH", cyl_vph, (0.9, 0.6, 0.1), transparency=45)

    # 8. Spectrograph: 20.8 deg diffracted beam (VPH -> L_CAM, 45 mm length)
    cyl_diffracted = Part.makeCylinder(8.5, 45.0, p_vph, d_spec)
    add_part_feature(doc, grp_beams, "Beam_08_Diffracted_Beam_to_CameraLens", cyl_diffracted, (0.8, 0.2, 0.9), transparency=45)

    # 9. Spectrograph: Camera lens focusing cone (L_CAM -> Science Sensor C_SPEC)
    cone_cam_focus = Part.makeCone(12.5, 9.5, 100.0, p_lcam, d_spec)
    add_part_feature(doc, grp_beams, "Beam_09_Camera_Focus_to_ASI2600MM", cone_cam_focus, (0.8, 0.2, 0.9), transparency=45)


# =============================================================================
# 2. LOAD AND PLACE COTS COMPONENTS FROM MANIFEST
# =============================================================================
def load_and_place_components(doc, grp_optics):
    print("Loading component manifest and placing 3D COTS models...")
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    placed_solids = {}

    for st in manifest["stations"]:
        st_id = st["id"]
        step_path = st["step_file"]
        anchor = vec(st["anchor_mm"])

        if not os.path.exists(step_path):
            raise FileNotFoundError(f"STEP file missing: {step_path}")

        raw_shape = Part.Shape()
        raw_shape.read(step_path)

        # ---------------------------------------------------------------------
        # Custom Pierced Mirror M1 (Dia 18 mm central hole bored along +Z)
        # ---------------------------------------------------------------------
        if st_id == "M1_PiercedMirror":
            rot = rot_from_z_to(vec(st["surface_normal"]))
            placed_mirror = raw_shape.copy()
            placed_mirror.Placement = App.Placement(anchor, rot)

            # Bore 18 mm hole parallel to telescope incoming beam [0, 0, 1]
            b = App.Vector(0, 0, 1)
            bore_len = 40.0
            bore_start = anchor.sub(b.multiply(bore_len / 2.0))
            hole_cyl = Part.makeCylinder(18.0 / 2.0, bore_len, bore_start, b)

            # Rear chamfer cone starting 2 mm inside front face
            chamfer_start = anchor.add(b.multiply(2.0))
            chamfer_cone = Part.makeCone(18.0 / 2.0, 18.0 / 2.0 + 4.0, bore_len / 2.0, chamfer_start, b)

            cut_tool = hole_cyl.fuse(chamfer_cone)
            shape = placed_mirror.cut(cut_tool)
            placed_solids[st_id] = shape

            add_part_feature(doc, grp_optics, st_id, shape, color=(0.85, 0.88, 0.92), transparency=0)
            print(f"Placed {st_id} at {anchor} (custom 18 mm angled bore applied)")
            continue

        # ---------------------------------------------------------------------
        # Determine orientation rotation
        # ---------------------------------------------------------------------
        if "surface_normal" in st:
            target_dir = vec(st["surface_normal"])
        elif "optical_axis" in st:
            target_dir = vec(st["optical_axis"])
        elif "sensor_facing_normal" in st:
            target_dir = vec(st["sensor_facing_normal"])
        else:
            target_dir = App.Vector(0, 0, 1)

        rot = rot_from_z_to(target_dir)

        shape = raw_shape.copy()
        shape.Placement = App.Placement(anchor, rot)
        placed_solids[st_id] = shape

        # Distinct visual styling
        if "Mirror" in st_id or "Pellicle" in st_id:
            color = (0.8, 0.82, 0.85)
        elif "ASI" in st_id:
            color = (0.85, 0.15, 0.15)  # Signature ZWO red
        elif "VPH" in st_id:
            color = (0.2, 0.75, 0.55)  # Holographic green/cyan
        elif "FSM" in st_id:
            color = (0.15, 0.35, 0.75)  # PI blue/steel
        else:
            color = (0.3, 0.32, 0.35)  # Black anodized aluminum

        add_part_feature(doc, grp_optics, st_id, shape, color=color, transparency=0)
        print(f"Placed {st_id} at {anchor} with direction {target_dir}")

    return placed_solids


# =============================================================================
# 3. CASSEGRAIN FLANGE REFERENCE RING (ONLY RETAINED MECHANICAL REFERENCE)
# =============================================================================
def build_flange_reference(doc, grp_ref):
    """
    Builds the clean Cassegrain Interface Reference Ring at Z = -350 mm.
    All brackets, chassis struts, baseplates, and pedestals are removed
    as requested for a clean optical layout.
    """
    print("Building Cassegrain Flange Reference Ring at Z = -350 mm...")
    flange_outer = Part.makeCylinder(140.0, 15.0, App.Vector(0, 0, -350.0), App.Vector(0, 0, 1))
    flange_bore = Part.makeCylinder(50.0, 25.0, App.Vector(0, 0, -355.0), App.Vector(0, 0, 1))
    flange_ring = flange_outer.cut(flange_bore)

    add_part_feature(doc, grp_ref, "Cassegrain_Flange_Reference", flange_ring, (0.6, 0.63, 0.68), transparency=20)
    return flange_ring


# =============================================================================
# 4. PAIR-WISE CLEARANCE AUDIT
# =============================================================================
def run_pairwise_clearance_audit(solids_dict, min_allowed_clearance=2.0):
    print("\n===================================================================")
    print("=== AUTOMATED PAIR-WISE CLEARANCE & COLLISION AUDIT (Direct Focus) ===")
    print("===================================================================")

    names = list(solids_dict.keys())
    collisions = []
    min_pair = (None, None, float("inf"))

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            n1, n2 = names[i], names[j]
            s1, s2 = solids_dict[n1], solids_dict[n2]
            try:
                dist = s1.distToShape(s2)[0]
            except Exception:
                c1, c2 = s1.BoundBox.Center, s2.BoundBox.Center
                c_dist = math.sqrt((c1.x - c2.x)**2 + (c1.y - c2.y)**2 + (c1.z - c2.z)**2)
                r1 = max(s1.BoundBox.XLength, s1.BoundBox.YLength, s1.BoundBox.ZLength) / 2.0
                r2 = max(s2.BoundBox.XLength, s2.BoundBox.YLength, s2.BoundBox.ZLength) / 2.0
                dist = max(0.0, c_dist - r1 - r2)

            if dist < min_pair[2]:
                min_pair = (n1, n2, dist)

            if dist < min_allowed_clearance:
                collisions.append((n1, n2, dist))
                print(f"[COLLISION / WARNING] {n1} <-> {n2}: {dist:.3f} mm (< {min_allowed_clearance} mm)")
            else:
                if dist < 35.0:
                    print(f"  [CLEAR] {n1} <-> {n2}: {dist:.2f} mm")

    print("-------------------------------------------------------------------")
    if not collisions:
        print(f"PASS: 0 collisions detected across {len(names)} components.")
        print(f"Closest non-mating pair: {min_pair[0]} <-> {min_pair[1]} = {min_pair[2]:.2f} mm")
    else:
        print(f"FAILED: {len(collisions)} collision(s) detected!")
    print("===================================================================\n")
    return collisions, min_pair


# =============================================================================
# MASTER BUILD FUNCTION
# =============================================================================
def build_assembly():
    print(f"\n=======================================================")
    print(f"Building Direct-Focus Assembly: {DOC_NAME}")
    print(f"=======================================================\n")

    if DOC_NAME in App.listDocuments():
        App.closeDocument(DOC_NAME)
    doc = App.newDocument(DOC_NAME)

    grp_beams = doc.addObject("App::DocumentObjectGroup", "Optical_Beams_and_Rays")
    grp_optics = doc.addObject("App::DocumentObjectGroup", "Optics_and_Cameras")
    grp_ref = doc.addObject("App::DocumentObjectGroup", "Reference_Geometry")

    # 1. 3D Optical Beam Cones
    build_optical_beams(doc, grp_beams)

    # 2. COTS Stations from Manifest
    placed_solids = load_and_place_components(doc, grp_optics)

    # 3. Telescope Cassegrain Flange Reference Ring
    flange = build_flange_reference(doc, grp_ref)

    doc.recompute()

    # 4. Full clearance audit across all optical solids
    collisions, min_pair = run_pairwise_clearance_audit(placed_solids, min_allowed_clearance=2.0)

    # 5. Save FreeCAD Document
    fcstd_path = f"{DOC_NAME}.FCStd"
    doc.saveAs(fcstd_path)
    print(f"Saved Master FreeCAD Assembly: {fcstd_path}")

    # Export combined STEP file
    all_shapes = list(placed_solids.values()) + [flange]
    compound = Part.makeCompound(all_shapes)
    step_export_path = f"{DOC_NAME}.step"
    compound.exportStep(step_export_path)
    print(f"Exported Master Assembly STEP: {step_export_path} ({os.path.getsize(step_export_path):,} bytes)\n")

    # Export combined STEP file with 3D optical beam rays
    beam_shapes = [obj.Shape for obj in grp_beams.Group if hasattr(obj, "Shape")]
    compound_with_rays = Part.makeCompound(all_shapes + beam_shapes)
    step_rays_path = "MtAbu_1p2m_Spectrograph_Guider_with_Rays.step"
    compound_with_rays.exportStep(step_rays_path)
    print(f"Exported Master Assembly with Rays STEP: {step_rays_path} ({os.path.getsize(step_rays_path):,} bytes)\n")

    return doc, collisions


if __name__ == "__main__":
    build_assembly()
