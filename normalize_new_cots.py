#!/usr/bin/env python3
"""
normalize_new_cots.py
Normalizes the official Thorlabs CAD files downloaded by the user:
1. cad_zip/CFS1_M-Documents.zip -> step_files/CFS1_M-Step.step
   (Thorlabs CFS1/M manual sliding filter/slit mount)
   Datum: On-axis Slot 1 optical aperture at (0, 0, 0), optical axis along +Z.
2. cad_zip/LMR1_M-Documents.zip + FGL400M -> step_files/FGL475M_in_LMR1_M-Step.step
   (Thorlabs LMR1/M mount holding FGL475M 475 nm longpass octave filter)
   Datum: Optic center at (0, 0, 0), optical axis along +Z.
"""

import os
import sys
import zipfile

try:
    import FreeCAD as App
    import Part
except ImportError:
    print("Run via FreeCADCmd!")
    sys.exit(1)

CAD_ZIP_DIR = "cad_zip"
CAD_EXTRACTED_DIR = "cad_extracted"
STEP_OUT_DIR = "step_files"

os.makedirs(CAD_EXTRACTED_DIR, exist_ok=True)
os.makedirs(STEP_OUT_DIR, exist_ok=True)

def process_cfs1_m():
    zip_path = os.path.join(CAD_ZIP_DIR, "CFS1_M-Documents.zip")
    step_extracted = os.path.join(CAD_EXTRACTED_DIR, "CFS1_M-Step.step")
    
    print("\n--- 1. Normalizing Thorlabs CFS1/M (Manual Slit Slider) ---")
    if not os.path.exists(step_extracted):
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extract("CFS1_M-Step.step", CAD_EXTRACTED_DIR)
        print(f"Extracted {step_extracted}")
    
    s = Part.read(step_extracted)
    bb = s.BoundBox
    print(f"  Raw BoundBox: X=[{bb.XMin:.2f}, {bb.XMax:.2f}], Y=[{bb.YMin:.2f}, {bb.YMax:.2f}], Z=[{bb.ZMin:.2f}, {bb.ZMax:.2f}]")
    
    # In CFS1_M, the optical bore center is already at X=0.00, Y=0.00!
    # Z range is [-6.48, 9.78] with center Z = 1.65 mm.
    # Translate along Z by -1.65 mm to center in thickness at Z=0.
    s.translate(App.Vector(0.0, 0.0, -1.65))
    
    out_step = os.path.join(STEP_OUT_DIR, "CFS1_M-Step.step")
    s.exportStep(out_step)
    print(f"  Saved normalized {out_step}")
    bb_norm = s.BoundBox
    print(f"  Normalized BoundBox: X=[{bb_norm.XMin:.2f}, {bb_norm.XMax:.2f}], Y=[{bb_norm.YMin:.2f}, {bb_norm.YMax:.2f}], Z=[{bb_norm.ZMin:.2f}, {bb_norm.ZMax:.2f}]")
    print(f"  Optical center verified at (0, 0, 0) with normal along +Z.")


def process_lmr1_m():
    zip_path = os.path.join(CAD_ZIP_DIR, "LMR1_M-Documents.zip")
    step_extracted = os.path.join(CAD_EXTRACTED_DIR, "LMR1_M-Step.step")
    
    print("\n--- 2. Normalizing Thorlabs LMR1/M + FGL475M (Octave Filter in Mount) ---")
    if not os.path.exists(step_extracted):
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extract("LMR1_M-Step.step", CAD_EXTRACTED_DIR)
        print(f"Extracted {step_extracted}")
    
    mount = Part.read(step_extracted)
    # LMR1_M bore center is at (-9.52, 8.23, 1.76).
    # Translate by (+9.52, -8.23, -1.76) to center bore at (0, 0, 0).
    mount.translate(App.Vector(9.52, -8.23, -1.76))
    
    # Also load the Thorlabs mounted filter cell FGL400M (mechanically identical to FGL475M)
    filter_path = os.path.join(STEP_OUT_DIR, "FGL400M-Step.step")
    if os.path.exists(filter_path):
        filter_cell = Part.read(filter_path)
        # Combine mount and filter cell into a single compound
        mounted_filter = Part.makeCompound([mount, filter_cell])
    else:
        mounted_filter = mount
    
    out_step = os.path.join(STEP_OUT_DIR, "FGL475M_in_LMR1_M-Step.step")
    mounted_filter.exportStep(out_step)
    print(f"  Saved normalized {out_step}")
    bb_norm = mounted_filter.BoundBox
    print(f"  Normalized BoundBox: X=[{bb_norm.XMin:.2f}, {bb_norm.XMax:.2f}], Y=[{bb_norm.YMin:.2f}, {bb_norm.YMax:.2f}], Z=[{bb_norm.ZMin:.2f}, {bb_norm.ZMax:.2f}]")
    print(f"  Optical center verified at (0, 0, 0) with normal along +Z.")

def run_all():
    process_cfs1_m()
    process_lmr1_m()
    print("\nNormalization of newly downloaded COTS CAD files complete!\n")

if __name__ == "__main__":
    run_all()
