import sys, os

sys.path.append(os.path.join(os.path.abspath(os.getcwd())))  # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt

'''
RENDER A MESH STEP-BY-STEP:
1. copy "template_lazy.py" to your preferred local folder
2. In "template_lazy.py":
    - change "mesh_path" to your desired mesh path
    - change to sys.path.append('path/to/BlenderToolBox/cycles/')
3. run "blender --background --python template_lazy.py" in terminal, then terminate the code when it starts rendering. This step outputs a "test.blend"
4. open "test.blend" with your blender software
5. in blender UI, adjust:
    - "mesh_location", "mesh_rotation", "mesh_scale" of the mesh
6. type in the adjusted mesh parameters from UI to "template_lazy.py"
7. run "blender --background --python template_lazy.py" again (wait a couple minutes) to output your final image
'''

'''
203289
  "mesh_position": (1.00, -0.47, 0.21), # UI: click mesh > Transform > Location
  "mesh_rotation": (2, -25, 360), # UI: click mesh > Transform > Rotation
  "mesh_scale": (1.5,1.5,1.5), # UI: click mesh > Transform > Scale
  "light_angle": (6, -30, -155) # UI: click Sun > Transform > Rotation
'''
work_dir = '/work/Users/zhuzhiwei/neuralSubdiv-master/jobs/'
method_list = ['anchor', 'rnn', 'hfNorm', 'hfNorm_MfV', 'hfNorm_MfV_rnn']
mesh_list = [76947, 1717684, 203289]

arguments_template = {
    "output_path": "./template_lazy.png",
    "image_resolution": [1080, 1080],  # recommend >1080 for paper figures
    "number_of_samples": 300,  # recommend >200 for paper figures
    "mesh_path": "/work/Users/zhuzhiwei/neuralSubdiv-master/jobs/203289_sf_f1000_ns3_nm10/b1_anchor/test_e3000/09_subd3_gt.obj",
    # either .ply or .obj
    "mesh_position": (1.00, -0.50, 0.18),  # UI: click mesh > Transform > Location
    "mesh_rotation": (0, -25, 360),  # UI: click mesh > Transform > Rotation
    "mesh_scale": (1.5, 1.5, 1.5),  # UI: click mesh > Transform > Scale
    "shading": "smooth",  # either "flat" or "smooth"
    "subdivision_iteration": 0,  # integer
    "mesh_RGB": [144.0 / 255, 210.0 / 255, 236.0 / 255],  # mesh RGB
    "light_angle": (6, -30, -155)  # UI: click Sun > Transform > Rotation
}

common_arguments = {
    "image_resolution": [720, 720],  # recommend >1080 for paper figures
    "number_of_samples": 200,  # recommend >200 for paper figures
    "shading": "smooth",  # either "flat" or "smooth"
    "subdivision_iteration": 0,  # integer
    "mesh_RGB": [144.0 / 255, 210.0 / 255, 236.0 / 255],  # mesh RGB
    "light_angle": (6, -30, -155)  # UI: click Sun > Transform > Rotation
}

mesh_arguments = {
    1717684: {
        "mesh_position": (1.10, -0.65, -0.10),  # UI: click mesh > Transform > Location
        "mesh_rotation": (41, 0.6, 92),  # UI: click mesh > Transform > Rotation
        "mesh_scale": (1.6, 1.6, 1.6),  # UI: click mesh > Transform > Scale},
    },

    76947: {
        "mesh_position": (1.00, -0.45, 0.22),  # UI: click mesh > Transform > Location
        "mesh_rotation": (0, -25, 0),  # UI: click mesh > Transform > Rotation
        "mesh_scale": (1.5, 1.5, 1.5),  # UI: click mesh > Transform > Scale
    },

    203289: {
        "mesh_position": (1.00, -0.50, 0.18),  # UI: click mesh > Transform > Location
        "mesh_rotation": (0, -25, 360),  # UI: click mesh > Transform > Rotation
        "mesh_scale": (1.5, 1.5, 1.5),  # UI: click mesh > Transform > Scale
    },
}

for mesh in mesh_list:
    print(mesh)
    arguments = common_arguments.copy()
    arguments.update(mesh_arguments[mesh])
    print(arguments)
    for obj_id in range(7, 8):
        output_dir = os.path.join(work_dir, str(mesh) + '_sf_f1000_ns3_nm10', 'png_'+str(obj_id).zfill(2))
        os.path.exists(output_dir) or os.makedirs(output_dir)
        arguments["mesh_path"] = os.path.join(work_dir, str(mesh) + '_sf_f1000_ns3_nm10', 'b1_anchor', 'test_e3000',
                                              str(obj_id).zfill(2) + '_subd3_gt.obj')
        arguments["output_path"] = os.path.join(output_dir, 'gt_'+str(obj_id).zfill(2)+'_subd3.png')
        bt.render_mesh_default(arguments)

        for method in method_list:
            arguments["mesh_path"] = os.path.join(work_dir, str(mesh) + '_sf_f1000_ns3_nm10', 'b1_' + method,
                                                  'test_e3000',  str(obj_id).zfill(2) + '_subd3.obj')
            arguments["output_path"] = os.path.join(output_dir, 'b1_' + method+'_'+str(obj_id).zfill(2) + '_subd3.png')
            bt.render_mesh_default(arguments)