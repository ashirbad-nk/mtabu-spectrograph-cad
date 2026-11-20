"""
export_render_meshes.py
Exports high-resolution, optimized STL meshes from the Direct-Focus master assembly
for photorealistic Blender Cycles rendering.
Uses MeshPart with controlled deflection to keep mesh files clean, lightweight (<20 MB),
and crisp for raytracing.
"""

import os
import sys

sys.path.insert(0, os.getcwd())

import FreeCAD as App
import Part
import MeshPart
import build_master_assembly as bma

OUTPUT_DIR = "render_meshes"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def export_optimized_stl(shape, path, lin_defl=0.3, ang_defl=0.25):
    """Export shape as an optimized STL mesh with controlled deflection."""
    mesh = MeshPart.meshFromShape(shape, LinearDeflection=lin_defl, AngularDeflection=ang_defl)
    mesh.write(path)
    print(f"Exported: {path} ({os.path.getsize(path):,} B, {mesh.CountFacets:,} facets)")


def export_meshes():
    print(f"\n=== Generating Optimized Mesh Geometry in '{OUTPUT_DIR}' (Direct Focus) ===")

    doc = App.newDocument("ExportDoc")
    grp_beams = doc.addObject("App::DocumentObjectGroup", "Optical_Beams")
    grp_optics = doc.addObject("App::DocumentObjectGroup", "Optics")
    grp_ref = doc.addObject("App::DocumentObjectGroup", "Reference")

    bma.build_optical_beams(doc, grp_beams)
    placed_solids = bma.load_and_place_components(doc, grp_optics)
    flange = bma.build_flange_reference(doc, grp_ref)

    # 1. Beams
    beam_shapes = [o.Shape for o in grp_beams.Group if hasattr(o, "Shape")]
    if beam_shapes:
        comp_beams = Part.makeCompound(beam_shapes)
        p = os.path.join(OUTPUT_DIR, "optical_beams.stl")
        export_optimized_stl(comp_beams, p, lin_defl=0.5, ang_defl=0.35)

    # 2. Cameras (C_FF ASI6200MM, C_GD ASI290MM, C_SPEC ASI2600MM)
    cam_keys = ["C_FF_ASI6200MM", "C_GD_ASI290MM", "C_SPEC_ASI2600MM"]
    cam_shapes = [placed_solids[k] for k in cam_keys if k in placed_solids]
    if cam_shapes:
        comp_cams = Part.makeCompound(cam_shapes)
        p = os.path.join(OUTPUT_DIR, "cameras_zwo.stl")
        export_optimized_stl(comp_cams, p, lin_defl=0.4, ang_defl=0.3)

    # 3. Optics (M1, FSM, Calibration Stage, BS, SLIT, L_COL, FGL475, VPH, L_CAM)
    optic_keys = [
        "M1_PiercedMirror", "FSM_PI_S335", "M_CAL_FlipMirror", "CAL_LinearStage_Envelope",
        "BS_Pellicle_92_8", "SLIT_CFS1_M", "SLIT_DualSlide_Assembly", "SLIT_150um", "L_COL_f200",
        "FGL475_OctaveFilter", "VPH_Grating_600lmm", "L_CAM_f100"
    ]
    optic_shapes = [placed_solids[k] for k in optic_keys if k in placed_solids]
    if optic_shapes:
        comp_optics = Part.makeCompound(optic_shapes)
        p = os.path.join(OUTPUT_DIR, "optics_and_mounts.stl")
        export_optimized_stl(comp_optics, p, lin_defl=0.3, ang_defl=0.25)

    # 4. Flange reference ring
    p = os.path.join(OUTPUT_DIR, "flange_reference_ring.stl")
    export_optimized_stl(flange, p, lin_defl=0.5, ang_defl=0.35)

    print("\nAll render meshes successfully generated with optimal geometry density!\n")


if __name__ == "__main__":
    export_meshes()
