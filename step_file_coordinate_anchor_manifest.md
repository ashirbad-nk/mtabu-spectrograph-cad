{
  "project": "Mt. Abu 1.2m Slit Spectrograph, Tip-Tilt Guider & Annular Field Imager (Compacted Direct-Focus Architecture)",
  "units": "mm",
  "coordinate_frame": {
    "handedness": "right-handed",
    "origin": [0.0, 0.0, 0.0],
    "origin_definition": "Virtual straight-through focal point of telescope f/13 beam (350 mm downstream of Cassegrain flange)",
    "incoming_telescope_direction": [0.0, 0.0, 1.0],
    "cassegrain_mounting_flange_z_mm": -350.0,
    "flange_clear_aperture_id_mm": 100.0
  },
  "stations": [
    {
      "id": "M1_PiercedMirror",
      "description": "2-inch flat mirror at Z=-200 mm with central hole bored at 45 deg, reflecting converging annular field to ASI6200MM focus",
      "step_file": "step_files/PF20-03-P01-Step.step",
      "custom_operation": "Boolean subtract 18.0 mm cylinder along [0,0,1] + rear chamfer",
      "anchor_mm": [0.0, 0.0, -200.0],
      "surface_normal": [0.707107, 0.0, -0.707107],
      "local_datum_rule": "Front reflective face center at local (0,0,0), normal along +Z"
    },
    {
      "id": "C_FF_ASI6200MM",
      "description": "ZWO ASI6200MM Pro Full-Frame Camera placed directly at the reflected telescope f/13 focal plane (zero relay lenses, zero fold mirrors)",
      "step_file": "step_files/ASI6200MM_Pro.step",
      "anchor_mm": [200.0, 0.0, -200.0],
      "sensor_facing_normal": [-1.0, 0.0, 0.0],
      "local_datum_rule": "Sensor active plane at local (0,0,0)"
    },
    {
      "id": "FSM_PI_S335",
      "description": "PI S-335.2SHM2 Fast Steering Mirror in central converging beam at Z=-90 mm, folding beam +Z -> +Y directly to slit focus",
      "step_file": "step_files/S-335_2SHM2.step",
      "anchor_mm": [0.0, 0.0, -90.0],
      "surface_normal": [0.0, 0.707107, -0.707107],
      "local_datum_rule": "Front mirror reflective face center at local (0,0,0), normal along +Z"
    },
    {
      "id": "M_CAL_FlipMirror",
      "description": "Thorlabs MFF101/M motorized flip mirror for calibration lamp injection ahead of slit",
      "step_file": "step_files/MFF101_M-Step.step",
      "anchor_mm": [0.0, 30.0, -90.0],
      "optical_axis": [0.0, 1.0, 0.0],
      "local_datum_rule": "Deployed mirror center at (0,30,-90)"
    },
    {
      "id": "BS_Pellicle_92_8",
      "description": "25.4 mm 8R/92T pellicle beamsplitter splitting 8% to guider focus and 92% to spectrograph slit",
      "step_file": "step_files/BP108-Step.step",
      "anchor_mm": [0.0, 55.0, -90.0],
      "surface_normal": [0.0, -0.707107, 0.707107],
      "local_datum_rule": "Pellicle membrane center at local (0,0,0), normal along +Z"
    },
    {
      "id": "C_GD_ASI290MM",
      "description": "ZWO ASI290MM Mini guider camera at the 8% reflected focal plane",
      "step_file": "step_files/ASI290MM_Mini.step",
      "anchor_mm": [0.0, 55.0, -55.0],
      "sensor_facing_normal": [0.0, 0.0, -1.0],
      "local_datum_rule": "Sensor plane at local (0,0,0)"
    },
    {
      "id": "SLIT_150um",
      "description": "150 um x 3 mm mounted slit placed at the EXACT telescope f/13 focal plane (350 mm total path from flange)",
      "step_file": "step_files/S150R-Step.step",
      "anchor_mm": [0.0, 90.0, -90.0],
      "optical_axis": [0.0, 1.0, 0.0],
      "local_datum_rule": "Slit blade center at local (0,0,0)"
    },
    {
      "id": "L_COL_f200",
      "description": "30 mm dia, f=200 mm achromatic collimator producing 15.4 mm collimated beam",
      "step_file": "step_files/AC300-200-A-Step.step",
      "anchor_mm": [0.0, 290.0, -90.0],
      "optical_axis": [0.0, 1.0, 0.0],
      "local_datum_rule": "Lens optical center at local (0,0,0)"
    },
    {
      "id": "VPH_Grating_600lmm",
      "description": "Wasatch 600 l/mm @ 600 nm VPH transmission grating in KM200PM/M mount (compacted to 50 mm past collimator)",
      "step_file": "step_files/KM200PM_M-Step.step",
      "anchor_mm": [0.0, 340.0, -90.0],
      "surface_normal": [-0.180519, 0.983571, 0.0],
      "diffracted_beam_dir": [-0.355107, 0.934826, 0.0],
      "local_datum_rule": "Grating center at local (0,0,0)"
    },
    {
      "id": "L_CAM_f100",
      "description": "50.8 mm dia, f=100 mm camera doublet focusing dispersed spectrum (compacted to 45 mm past grating)",
      "step_file": "step_files/AC508-100-A-Step.step",
      "anchor_mm": [-15.98, 382.07, -90.0],
      "optical_axis": [-0.355107, 0.934826, 0.0],
      "local_datum_rule": "Lens optical center at local (0,0,0)"
    },
    {
      "id": "C_SPEC_ASI2600MM",
      "description": "ZWO ASI2600MM Pro APS-C Cooled Mono Science Camera recording spectrum (f=100 mm from camera doublet)",
      "step_file": "step_files/ASI2600MM_Pro.step",
      "anchor_mm": [-51.49, 475.55, -90.0],
      "sensor_facing_normal": [0.355107, -0.934826, 0.0],
      "local_datum_rule": "Sensor plane at local (0,0,0)"
    }
  ]
}
