"""
export_render_meshes.py
Exports high-resolution categorized STL meshes from the Direct-Focus master assembly
for photorealistic Blender rendering.
"""

import os
import sys

sys.path.insert(0, os.getcwd())

import FreeCAD as App
import Part
import build_master_assembly as bma

OUTPUT_DIR = "render_meshes"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def export_meshes():
    print(f"\n=== Generating Mesh Geometry in '{OUTPUT_DIR}' (Direct Focus) ===")

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
        comp_beams.exportStl(p)
        print(f"Exported: {p} ({os.path.getsize(p):,} B)")

    # 2. Cameras (C_FF ASI6200MM, C_GD ASI290MM, C_SPEC ASI2600MM)
    cam_keys = ["C_FF_ASI6200MM", "C_GD_ASI290MM", "C_SPEC_ASI2600MM"]
    cam_shapes = [placed_solids[k] for k in cam_keys if k in placed_solids]
    if cam_shapes:
        comp_cams = Part.makeCompound(cam_shapes)
        p = os.path.join(OUTPUT_DIR, "cameras_zwo.stl")
        comp_cams.exportStl(p)
        print(f"Exported: {p} ({os.path.getsize(p):,} B)")

    # 3. Optics (M1, FSM, M_CAL, BS, SLIT, L_COL, VPH, L_CAM)
    optic_keys = [
        "M1_PiercedMirror", "FSM_PI_S335", "M_CAL_FlipMirror",
        "BS_Pellicle_92_8", "SLIT_150um", "L_COL_f200",
        "VPH_Grating_600lmm", "L_CAM_f100"
    ]
    optic_shapes = [placed_solids[k] for k in optic_keys if k in placed_solids]
    if optic_shapes:
        comp_optics = Part.makeCompound(optic_shapes)
        p = os.path.join(OUTPUT_DIR, "optics_and_mounts.stl")
        comp_optics.exportStl(p)
        print(f"Exported: {p} ({os.path.getsize(p):,} B)")

    # 4. Flange reference ring
    p = os.path.join(OUTPUT_DIR, "flange_reference_ring.stl")
    flange.exportStl(p)
    print(f"Exported: {p} ({os.path.getsize(p):,} B)")

    print("\nAll render meshes successfully generated!\n")


if __name__ == "__main__":
    export_meshes()
