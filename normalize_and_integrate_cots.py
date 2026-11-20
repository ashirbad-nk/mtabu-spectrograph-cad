"""
normalize_and_integrate_cots.py
Normalizes official vendor CAD STEP files and updates the COTS step library.
"""

import sys
import os
import Part
import FreeCAD as App

REPO_DIR = "/home/ashirbad/Documents/codes/lowresspec"
EXTRACTED_DIR = os.path.join(REPO_DIR, "cad_extracted")
ZWO_DIR = os.path.join(REPO_DIR, "cad_zip", "zwo_Step")
STEP_OUT_DIR = os.path.join(REPO_DIR, "step_files")

os.makedirs(STEP_OUT_DIR, exist_ok=True)

print("--- 1. Normalizing Thorlabs PF20-03-P01 (2-inch Protected-Ag Mirror) ---")
pf_src = os.path.join(EXTRACTED_DIR, "PF20-03-P01-Step.step")
if os.path.exists(pf_src):
    s = Part.read(pf_src)
    # Translate front reflective face center to (0, 0, 0)
    s.translate(App.Vector(5.999482, -0.647071, -8.726234))
    pf_out = os.path.join(STEP_OUT_DIR, "PF20-03-P01-Step.step")
    s.exportStep(pf_out)
    print(f"  Exported {pf_out}: BoundBox dim {s.BoundBox.XLength:.1f}x{s.BoundBox.YLength:.1f}x{s.BoundBox.ZLength:.1f}")

print("--- 2. Normalizing Thorlabs S150K (Mounted 150um Slit) ---")
slit_src = os.path.join(EXTRACTED_DIR, "S150K-Step.step")
if os.path.exists(slit_src):
    s = Part.read(slit_src)
    # Rotate -90 deg around Y so optical axis points along +Z, front face at Z = 0
    s.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), -90)
    slit_out = os.path.join(STEP_OUT_DIR, "S150K-Step.step")
    s.exportStep(slit_out)
    # Also keep S150R-Step.step alias pointing to S150K for backwards compatibility
    s.exportStep(os.path.join(STEP_OUT_DIR, "S150R-Step.step"))
    print(f"  Exported {slit_out}: BoundBox dim {s.BoundBox.XLength:.1f}x{s.BoundBox.YLength:.1f}x{s.BoundBox.ZLength:.1f}")

print("--- 3. Normalizing Thorlabs BP108 (25.4mm Pellicle Beamsplitter) ---")
bp_src = os.path.join(EXTRACTED_DIR, "BP108-Step.step")
if os.path.exists(bp_src):
    s = Part.read(bp_src)
    bp_out = os.path.join(STEP_OUT_DIR, "BP108-Step.step")
    s.exportStep(bp_out)
    print(f"  Exported {bp_out}: BoundBox dim {s.BoundBox.XLength:.1f}x{s.BoundBox.YLength:.1f}x{s.BoundBox.ZLength:.1f}")

print("--- 4. Normalizing Thorlabs FGL400M (GG400 Longpass Filter) ---")
flt_src = os.path.join(EXTRACTED_DIR, "FGL400M-Step.step")
if os.path.exists(flt_src):
    s = Part.read(flt_src)
    # Rotate 90 deg around Y so optical axis is along +Z
    s.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)
    flt_out = os.path.join(STEP_OUT_DIR, "FGL400M-Step.step")
    s.exportStep(flt_out)
    print(f"  Exported {flt_out}: BoundBox dim {s.BoundBox.XLength:.1f}x{s.BoundBox.YLength:.1f}x{s.BoundBox.ZLength:.1f}")

print("--- 5. Normalizing Thorlabs AC508-100-A (50.8mm, f=100mm Doublet) ---")
cam_src = os.path.join(EXTRACTED_DIR, "AC508-100-A-Step.step")
if os.path.exists(cam_src):
    s = Part.read(cam_src)
    cam_out = os.path.join(STEP_OUT_DIR, "AC508-100-A-Step.step")
    s.exportStep(cam_out)
    print(f"  Exported {cam_out}: BoundBox dim {s.BoundBox.XLength:.1f}x{s.BoundBox.YLength:.1f}x{s.BoundBox.ZLength:.1f}")

print("--- 6. Normalizing ZWO ASI6200MM Pro & ASI2600MM Pro from Official STEP ---")
zwo_src = os.path.join(ZWO_DIR, "2600-6200-2400 stp.STEP")
if os.path.exists(zwo_src):
    s = Part.read(zwo_src)
    # Translate sensor to (0, 0, 0): front face at Y=34.59, sensor depth 17.5 mm -> sensor Y = 17.09
    s.translate(App.Vector(0.0, -17.0906, 0.0))
    # Rotate +90 around X so front faces +Z (incoming light from +Z into sensor at origin)
    s.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), 90)
    
    asi6200_out = os.path.join(STEP_OUT_DIR, "ASI6200MM_Pro.step")
    asi2600_out = os.path.join(STEP_OUT_DIR, "ASI2600MM_Pro.step")
    s.exportStep(asi6200_out)
    s.exportStep(asi2600_out)
    print(f"  Exported {asi6200_out} and {asi2600_out}: BoundBox dim {s.BoundBox.XLength:.1f}x{s.BoundBox.YLength:.1f}x{s.BoundBox.ZLength:.1f}")
    bb = s.BoundBox
    print(f"    Sensor at (0,0,0); Front flange at Z={bb.ZMax:.1f} mm, Rear face at Z={bb.ZMin:.1f} mm")

print("--- 7. Building Thorlabs AC254-200-A (25.4mm, f=200mm Doublet) ---")
# Collimator lens: 25.4mm OD, 6.0mm center thickness, centered at origin
d_col = Part.makeCylinder(12.7, 6.0, App.Vector(0, 0, -3.0), App.Vector(0, 0, 1))
col_out = os.path.join(STEP_OUT_DIR, "AC254-200-A-Step.step")
d_col.exportStep(col_out)
# Also keep AC300-200-A-Step.step alias
d_col.exportStep(os.path.join(STEP_OUT_DIR, "AC300-200-A-Step.step"))
print(f"  Exported {col_out}")

print("--- 8. Building Linear Stage Reserved Envelope (In-house calibration slide) ---")
# User requested: "filter flipper too expensive will design our linear stage, leave space."
# Reserve 40mm (X) x 25mm (Y) x 30mm (Z) envelope for linear slide carriage
stage_env = Part.makeBox(40.0, 20.0, 30.0, App.Vector(-20.0, -10.0, -15.0))
stage_out = os.path.join(STEP_OUT_DIR, "CAL_LinearStage_Envelope.step")
stage_env.exportStep(stage_out)
print(f"  Exported {stage_out}")

print("Normalization and COTS step library update complete.")
