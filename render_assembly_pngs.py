"""
render_assembly_pngs.py
Renders high-resolution, photorealistic PNG visualizations of the
Mt. Abu 1.2m Direct-Focus Architecture using Blender 5.2 (Cycles engine).
"""

import os
import bpy

# Set units & scene
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'MILLIMETERS'
scene.unit_settings.scale_length = 0.001  # 1 BU = 1 mm

# Clean existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Configure Cycles renderer
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 64
scene.cycles.preview_samples = 16
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = False

# World background / environment
world = bpy.data.worlds.new("StudioWorld")
scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs[0].default_value = (0.04, 0.045, 0.055, 1.0)
    bg_node.inputs[1].default_value = 0.9


def make_principled_mat(name, base_color, roughness=0.3, metallic=0.0, transmission=0.0, emission=(0, 0, 0), emission_str=0.0, alpha=1.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")

    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if "Transmission Weight" in bsdf.inputs:
            bsdf.inputs["Transmission Weight"].default_value = transmission
        elif "Transmission" in bsdf.inputs:
            bsdf.inputs["Transmission"].default_value = transmission
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
            bsdf.inputs["Emission Strength"].default_value = emission_str
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = (*emission, 1.0)
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = emission_str
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
    return mat


# Create shaders
mat_cams = make_principled_mat("Mat_ZWO_Cameras", base_color=(0.85, 0.08, 0.12), roughness=0.22, metallic=0.88)
mat_optics = make_principled_mat("Mat_Optics_Mounts", base_color=(0.25, 0.27, 0.3), roughness=0.28, metallic=0.75)
mat_flange = make_principled_mat("Mat_Flange_Reference", base_color=(0.7, 0.73, 0.78), roughness=0.35, metallic=0.9)
mat_beams = make_principled_mat(
    "Mat_Beams",
    base_color=(0.3, 0.8, 1.0),
    roughness=0.1,
    transmission=0.85,
    emission=(0.25, 0.75, 1.0),
    emission_str=1.3,
    alpha=0.65
)

# Import meshes
mesh_dir = "render_meshes"
assignments = [
    ("cameras_zwo.stl", mat_cams),
    ("optics_and_mounts.stl", mat_optics),
    ("flange_reference_ring.stl", mat_flange),
    ("optical_beams.stl", mat_beams),
]

imported_objs = {}
for fname, mat in assignments:
    fpath = os.path.join(mesh_dir, fname)
    if os.path.exists(fpath):
        bpy.ops.wm.stl_import(filepath=fpath)
        obj = bpy.context.selected_objects[0]
        obj.name = fname.replace(".stl", "")
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        imported_objs[obj.name] = obj
        print(f"Loaded: {obj.name} with material {mat.name}")

# Studio lighting
def add_light(name, light_type, location, energy, size=100.0, color=(1, 1, 1)):
    light_data = bpy.data.lights.new(name=name, type=light_type)
    light_data.energy = energy
    light_data.color = color
    if hasattr(light_data, "size"):
        light_data.size = size
    light_obj = bpy.data.objects.new(name=name, object_data=light_data)
    light_obj.location = location
    bpy.context.collection.objects.link(light_obj)
    return light_obj

add_light("Key_Light", 'AREA', (500.0, 300.0, -500.0), energy=850.0, size=500.0, color=(1.0, 0.96, 0.92))
add_light("Fill_Light", 'AREA', (-500.0, -300.0, 0.0), energy=450.0, size=600.0, color=(0.88, 0.92, 1.0))
add_light("Rim_Light", 'AREA', (0.0, 700.0, 400.0), energy=600.0, size=400.0, color=(0.95, 0.95, 1.0))
add_light("Top_Light", 'POINT', (0.0, 0.0, -600.0), energy=300.0, color=(0.9, 0.92, 0.95))

# Camera setup
cam_data = bpy.data.cameras.new("RenderCam")
cam_obj = bpy.data.objects.new("RenderCam", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

target_empty = bpy.data.objects.new("TargetEmpty", None)
target_empty.location = (50.0, 150.0, -150.0)
bpy.context.collection.objects.link(target_empty)

track = cam_obj.constraints.new(type='TRACK_TO')
track.target = target_empty
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

views = [
    {
        "filename": "render_01_isometric_overview.png",
        "cam_pos": (650.0, -600.0, -550.0),
        "target": (50.0, 200.0, -150.0),
        "focal_len": 48.0,
        "ortho": False
    },
    {
        "filename": "render_02_top_plan_view.png",
        "cam_pos": (50.0, 200.0, -1400.0),
        "target": (50.0, 200.0, -150.0),
        "focal_len": 65.0,
        "ortho": True,
        "ortho_scale": 1100.0
    },
    {
        "filename": "render_03_spectrograph_deck.png",
        "cam_pos": (-350.0, 750.0, 250.0),
        "target": (-25.0, 350.0, -90.0),
        "focal_len": 42.0,
        "ortho": False
    },
    {
        "filename": "render_04_pickoff_and_relay.png",
        "cam_pos": (380.0, 150.0, -380.0),
        "target": (80.0, 20.0, -150.0),
        "focal_len": 55.0,
        "ortho": False
    }
]

print("\n=== RENDERING DIRECT-FOCUS ASSEMBLY VIEWS (Cycles Engine) ===")
for v in views:
    out_path = os.path.abspath(v["filename"])
    scene.render.filepath = out_path

    cam_obj.location = v["cam_pos"]
    target_empty.location = v["target"]

    if v.get("ortho", False):
        cam_data.type = 'ORTHO'
        cam_data.ortho_scale = v.get("ortho_scale", 1100.0)
    else:
        cam_data.type = 'PERSP'
        cam_data.lens = v.get("focal_len", 50.0)

    print(f"Rendering: {v['filename']} ...")
    bpy.ops.render.render(write_still=True)
    print(f"  Saved -> {out_path} ({os.path.getsize(out_path):,} bytes)")

print("\nAll Direct-Focus PNG renders completed successfully!\n")
