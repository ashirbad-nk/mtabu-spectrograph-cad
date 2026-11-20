#!/usr/bin/env python3
"""
create_dual_slit_step.py
Generates a realistic, highly detailed 3D B-Rep CAD model of the
Dual-Slit Motorized Linear Slide Assembly and exports it as:
step_files/SLIT_DualSlide_Assembly.step

Station: SLIT at (0, 90, -90) mm
Local coordinate system:
- Local (0,0,0): Center of Slot 1 (active 75 um slit aperture, S75K)
- Local +Z: Optical axis direction (pointing along outgoing beam +Y in master assembly)
- Local +X: Linear sliding axis
  - X = 0: Active Slot 1 (75 um slit S75K)
  - X = +28 mm: Standby Slot 2 (150 um slit S150K)
  - X < -35 mm: NEMA 8 stepper motor actuator and manual override rod
- Local +Y: Slit height axis (height 3 mm along master assembly +Z)
"""

import sys
import os
import math

try:
    import FreeCAD as App
    import Part
except ImportError:
    print("FreeCAD Part module not found directly. Please run via FreeCADCmd.")
    sys.exit(1)

OUTPUT_STEP = "step_files/SLIT_DualSlide_Assembly.step"

def build_dual_slit_assembly():
    print("Building 3D CAD model for Dual-Slit Motorized Slide Assembly...")

    solids = []

    # 1. Base Guide Track (Fixed to instrument chassis)
    # Dimensions: 80 mm long (X), 34 mm tall (Y), 6 mm thick (Z in [-8, -2])
    base_box = Part.makeBox(80.0, 34.0, 6.0, App.Vector(-48.0, -17.0, -8.0))
    # Through-bore for active optical beam at (0, 0)
    base_hole1 = Part.makeCylinder(7.0, 10.0, App.Vector(0.0, 0.0, -9.0), App.Vector(0, 0, 1))
    # Through-bore for standby optical beam at (28, 0)
    base_hole2 = Part.makeCylinder(7.0, 10.0, App.Vector(28.0, 0.0, -9.0), App.Vector(0, 0, 1))
    base_track = base_box.cut(base_hole1).cut(base_hole2)
    solids.append(base_track)

    # Dovetail / Linear Guide Rails (Top and bottom precision steel guide rails)
    rail_top = Part.makeCylinder(2.5, 76.0, App.Vector(-46.0, 13.0, -2.0), App.Vector(1, 0, 0))
    rail_bot = Part.makeCylinder(2.5, 76.0, App.Vector(-46.0, -13.0, -2.0), App.Vector(1, 0, 0))
    solids.append(rail_top)
    solids.append(rail_bot)

    # 2. Sliding Carriage (Houses S75K and S150K mounted slit cells)
    # Dimensions: 56 mm long (X), 30 mm tall (Y), 6 mm thick (Z in [-2, +4])
    # Covers Slot 1 (X=0) and Slot 2 (X=28)
    carriage_box = Part.makeBox(56.0, 30.0, 6.0, App.Vector(-14.0, -15.0, -2.0))
    # Pockets for Thorlabs standard dia 25.4 mm (1-inch) slit cells
    pocket1 = Part.makeCylinder(12.7, 5.0, App.Vector(0.0, 0.0, -1.0), App.Vector(0, 0, 1))
    pocket2 = Part.makeCylinder(12.7, 5.0, App.Vector(28.0, 0.0, -1.0), App.Vector(0, 0, 1))
    # Light through-apertures
    ap_hole1 = Part.makeCylinder(6.0, 10.0, App.Vector(0.0, 0.0, -4.0), App.Vector(0, 0, 1))
    ap_hole2 = Part.makeCylinder(6.0, 10.0, App.Vector(28.0, 0.0, -4.0), App.Vector(0, 0, 1))

    carriage = carriage_box.cut(ap_hole1).cut(ap_hole2)
    solids.append(carriage)

    # 3. Slot 1: Thorlabs S75K Cell (75 um x 3 mm Slit - High-Res R ≈ 1060 Mode)
    # Anodized aluminum cell: dia 25.4 mm, 4.0 mm thick, centered at (0, 0, 0)
    s75_cell = Part.makeCylinder(12.7, 4.0, App.Vector(0.0, 0.0, -1.5), App.Vector(0, 0, 1))
    s75_inner = Part.makeCylinder(5.0, 6.0, App.Vector(0.0, 0.0, -2.5), App.Vector(0, 0, 1))
    s75_ring = s75_cell.cut(s75_inner)
    solids.append(s75_ring)

    # Slit substrate wafer & aperture blades (visual representation of 75 um slit)
    blade1_l = Part.makeBox(4.5, 3.0, 0.2, App.Vector(-4.5375, -1.5, -0.1))
    blade1_r = Part.makeBox(4.5, 3.0, 0.2, App.Vector(0.0375, -1.5, -0.1))
    solids.append(blade1_l)
    solids.append(blade1_r)

    # 4. Slot 2: Thorlabs S150K Cell (150 um x 3 mm Slit - High-Throughput R ≈ 530 Mode)
    # Centered at (28.0, 0, 0)
    s150_cell = Part.makeCylinder(12.7, 4.0, App.Vector(28.0, 0.0, -1.5), App.Vector(0, 0, 1))
    s150_inner = Part.makeCylinder(5.0, 6.0, App.Vector(28.0, 0.0, -2.5), App.Vector(0, 0, 1))
    s150_ring = s150_cell.cut(s150_inner)
    solids.append(s150_ring)

    # Slit substrate wafer & aperture blades (visual representation of 150 um slit)
    blade2_l = Part.makeBox(4.5, 3.0, 0.2, App.Vector(28.0 - 4.575, -1.5, -0.1))
    blade2_r = Part.makeBox(4.5, 3.0, 0.2, App.Vector(28.0 + 0.075, -1.5, -0.1))
    solids.append(blade2_l)
    solids.append(blade2_r)

    # 5. Miniature NEMA 8 Stepper Motor Actuator Envelope
    # Positioned at -X side of base: X in [-72, -48] mm
    # NEMA 8 body: 20 mm x 20 mm x 24 mm long
    motor_mount = Part.makeBox(6.0, 26.0, 24.0, App.Vector(-48.0, -13.0, -14.0))
    solids.append(motor_mount)

    motor_body = Part.makeBox(22.0, 20.0, 20.0, App.Vector(-70.0, -10.0, -12.0))
    motor_boss = Part.makeCylinder(7.5, 3.0, App.Vector(-48.0, 0.0, -2.0), App.Vector(1, 0, 0))
    solids.append(motor_body)
    solids.append(motor_boss)

    # Stainless steel lead screw (M3/M4 x 35 mm long)
    leadscrew = Part.makeCylinder(2.0, 38.0, App.Vector(-48.0, 0.0, -2.0), App.Vector(1, 0, 0))
    solids.append(leadscrew)

    # 6. Manual Override Pushrod & Knurled Knob
    # Extends outward to -X for manual human operation fallback
    pushrod = Part.makeCylinder(2.0, 20.0, App.Vector(-90.0, 0.0, -2.0), App.Vector(1, 0, 0))
    knob = Part.makeCylinder(6.0, 5.0, App.Vector(-95.0, 0.0, -2.0), App.Vector(1, 0, 0))
    solids.append(pushrod)
    solids.append(knob)

    # 7. Electrical Connector & Cable Gland (JST-XH 4-pin for stepper)
    connector = Part.makeBox(6.0, 10.0, 8.0, App.Vector(-68.0, -15.0, -8.0))
    solids.append(connector)

    # Fuse all into single compound / multi-solid shape
    compound = Part.makeCompound(solids)
    
    os.makedirs(os.path.dirname(OUTPUT_STEP), exist_ok=True)
    compound.exportStep(OUTPUT_STEP)
    print(f"Successfully exported {OUTPUT_STEP}")
    print(f"  Solid count: {len(solids)}")
    print(f"  BoundBox: X=[{compound.BoundBox.XMin:.1f}, {compound.BoundBox.XMax:.1f}], "
          f"Y=[{compound.BoundBox.YMin:.1f}, {compound.BoundBox.YMax:.1f}], "
          f"Z=[{compound.BoundBox.ZMin:.1f}, {compound.BoundBox.ZMax:.1f}]")

if __name__ == "__main__":
    build_dual_slit_assembly()
