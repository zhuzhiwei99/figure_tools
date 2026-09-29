import sys, os
#sys.path.append(os.path.join(os.path.abspath(os.getcwd()),'..')) # change this to your path to “path/to/BlenderToolbox/
sys.path.append(os.path.join(os.path.abspath(os.getcwd())))
import BlenderToolBox as bt
import bpy, bmesh
import numpy as np


'''
    !!!!!
    Only need to modify the matrrail and the meshPath !
    !!!!!
    "image_resolution": [1080, 1080],  # recommend >1080 for paper figures
    "number_of_samples": 300,  # recommend >200 for paper figures
    
    imgRes_x = 1280
    imgRes_y = 1280
    numSamples = 300

'''



def render(meshPath, outPath, mat='edge'):
    # outputPath = os.path.join(cwd, './demo_edge.png')  # make it abs path for windows

    ## initialize blender
    imgRes_x = 1280
    imgRes_y = 1280
    # imgRes_x = 1920
    # imgRes_y = 1920
    numSamples = 600
    exposure = 1.5
    bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

    ## read mesh (choose either readPLY or readOBJ)
    # meshPath = '/work/Users/zhuzhiwei/neuralSubdiv-master/data_meshes/objs_original/subdiv_fn500/bunny_f500_ns4_nm10/subd0/01.obj'
    # outputPath = meshPath[:-4] + '.png'

    # !!!!!!!!!!!!!! change here !!!!!!!!!!!!!!
    location = (0.6, 0, 0.8)  # (UI: click mesh > Transform > Location)
    rotation = (0, 0, 0)  # (UI: click mesh > Transform > Rotation)
    scale = (0.8, 0.8, 0.8)  # (UI: click mesh > Transform > Scale)

    mesh = bt.readMesh(meshPath, location, rotation, scale)

    ## set shading (uncomment one of them)
    #bpy.ops.object.shade_smooth()

    ## subdivision
    #bt.subdivision(mesh, level=1)

    # !!!!!!!!!!!!!! change here !!!!!!!!!!!!!!
    # # set material
    if mat == 'edge':
         # demo_edge
        edgeThickness = 0.005
        edgeColor = bt.colorObj((0, 0, 0, 0), 0.5, 1.0, 1.0, 0.0, 0.0)  # RGBA hue saturation value birghtness contrast
        meshRGBA = (1, 1, 1, 0)
        AOStrength = 0 # 环境光遮蔽，数值越大越暗
        bt.setMat_edge(mesh, edgeThickness, edgeColor, meshRGBA, AOStrength)
    elif mat == 'plastic':
        # demo_plastic
        meshColor = bt.colorObj(bt.derekBlue, 0.5, 1.0, 1.0, 0.0, 2.0)
        bt.setMat_plastic(mesh, meshColor)
    elif mat == 'balloon':
        # demo_ballon
        meshColor = bt.colorObj(bt.derekBlue, 0.5, 1.0, 1.0, 0.0, 3)
        AOStrength = 0.0
        bt.setMat_balloon(mesh, meshColor, AOStrength)
    elif mat == 'green':
        # demo_singleColor
        meshColor = bt.colorObj((107.0/255, 166.0/255, 68.0/255, 1), 0.5, 0.5, 1.0, 0.0, 2.0)
        AOStrength = 0.0
        bt.setMat_singleColor(mesh, meshColor, AOStrength)
    elif mat == 'gray':
        # demo_singleColor
        meshColor = bt.colorObj((180.0/255, 180.0/255, 180.0/255, 1), 0.5, 0.5, 1.0, 0.0, 2.0)
        AOStrength = 1.0
        # meshColor = bt.colorObj((180.0 / 255, 180.0 / 255, 180.0 / 255, 1), 0.5, 0.5, 1.0, 0.0, 1.0)
        # AOStrength = 1.0
        bt.setMat_singleColor(mesh, meshColor, AOStrength)
    elif mat == 'yellow':
        # demo_singleColor
        meshColor = bt.colorObj((242.0 / 255, 182.0 / 255, 0.0 / 255, 1), 0.5, 0.5, 1.0, 0.0, 1.0)
        AOStrength = 1.0
        bt.setMat_singleColor(mesh, meshColor, AOStrength)
    elif mat == 'green_lite':
        # demo_singleColor
        meshColor = bt.colorObj((185.0 / 255, 255.0 / 255, 221.0 / 255, 1), 0.5, 0.5, 1.0, 0.0, 1.0)
        AOStrength = 1.0
        bt.setMat_singleColor(mesh, meshColor, AOStrength)
    elif mat == 'balloon_edge':
        edgeThickness = 0.003
        edgeColor = bt.colorObj((0, 0, 0, 0), 0.5, 1.0, 1.0, 0.0, 1.0)  # RGBA hue saturation value birghtness contrast(越小越暗)
        meshRGBA = (88 / 255, 188 / 255, 226 / 255, 1)
        AOStrength = 0  # 环境光遮蔽，数值越大越暗
        bt.setMat_edge(mesh, edgeThickness, edgeColor, meshRGBA, AOStrength)
    else:
        pass



    ## set invisible plane (shadow catcher)
    bt.invisibleGround(shadowBrightness=0.9)

    ## set camera (recommend to change mesh instead of camera, unless you want to adjust the Elevation)
    camLocation = (3, 0, 2)
    lookAtLocation = (0, 0, 0.5)
    focalLength = 45  # (UI: click camera > Object Data > Focal Length)

    cam = bt.setCamera(camLocation, lookAtLocation, focalLength)

    ## set light
    lightAngle = (6, -30, -155)
    # lightAngle = (217, 222, 11.3)
    strength = 2
    shadowSoftness = 0.3
    sun = bt.setLight_sun(lightAngle, strength, shadowSoftness)

    ## set ambient light
    bt.setLight_ambient(color=(0.1, 0.1, 0.1, 1))

    ## set gray shadow to completely white with a threshold
    bt.shadowThreshold(alphaThreshold=0.05, interpolationMode='CARDINAL')

    ## save blender file so that you can adjust parameters in the UI
    bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test.blend')

    ## save rendering
    bt.renderImage(outPath, cam)


if __name__ == '__main__':
    from test_mesh_path import *

    #  cmd: blender --background --python zzw_blender_render.py


    fig_dir = '/work/Users/zhuzhiwei/project/BlenderToolbox/fig/gear_20240912'
    os.path.exists(fig_dir) or os.makedirs(fig_dir)
    # sub0_f600_59197 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/59197_f600_01.obj'
    # gt_59197 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface/59197_sf.obj'
    # bunny_59197 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bunny_f500_ns2_nm200/b1_ours_t160_lchar_s2/test_e252/59197_f600_01_subd2.obj'
    #mat = 'yellow'
    #mat = 'balloon'
    #mat = 'green'
    #mat = 'green_lite'
    mat = 'balloon_edge'
    gear_41984_path = '/work/Users/zhuzhiwei/project/mesh/NeuralMeshRefinement/data_meshes/refined/netparams_b1_t96_v17_e8/'
    bunny_path = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bunny_f500_ns2_nm200/b1_ours_t160_lchar_s2/test_e252/'
    thingi10k_path = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94'

    gear_919994_path = '/work/Users/zhuzhiwei/project/mesh/NeuralMeshRefinement/data_meshes/coarse/gear_netparams/'
    bunny_path = '/work/Users/zhuzhiwei/project/mesh/NeuralMeshRefinement/data_meshes/coarse/bunny_netparams/'
    thingi10k_path = '/work/Users/zhuzhiwei/project/mesh/NeuralMeshRefinement/jobs/thingi10k/thingi10k_netparams/'

    gear_41984_new = '/work/Users/zhuzhiwei/project/mesh/NeuralMeshRefinement_forreview/data_meshes/coarse/netparams_b1_t96_v17_e399/'
    gear_919994_new = '/work/Users/zhuzhiwei/project/mesh/NeuralMeshRefinement_forreview/data_meshes/coarse/netparams_b1_t10_v10_e499/'

    ours_path = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bunny_f500_ns2_nm200/b1_ours_t160_ll2_s2/test_e442/'
    global_path = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bunny_f500_ns2_nm200/b1_global_t160_ll2_s2/test_e323/'

    gt_41984 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface/41984_sf.obj'

    # imgPath = os.path.join(fig_dir, 'gt_41984_' + mat + '.png')
    # render(gt_41984, imgPath, mat)


    for i in range(1, 4):
        meshPath = os.path.join(gear_41984_path, 'sphere_subd'+str(i)+'.obj')
        imgPath = os.path.join(fig_dir,  'sphere_subd'+str(i)+'_' + mat + '.png')
        render(meshPath, imgPath, mat)
    # imgPath = os.path.join(fig_dir,  'cube_subd0'+'_' + mat + '.png')
    # render(cube_subd0, imgPath, mat)


    # for items in dog7_21_dict.items():
    #     method = items[0]
    #     imgPath = os.path.join(fig_dir,  'dog7_subd3_' + mat +'_'+method+ '.png')
    #     render(items[1], imgPath, mat)
    #
    # # .replace('subd2','subd3') .replace('subd3','subd2')
    # for i in range(4,5):
    #     meshPath = mod_butterfly_tbunny_f800_10_subd2.replace('subd2', 'subd'+str(i))
    #     name = 'mod_butterfly_tbunny_f800_10_subd2'.replace('subd2', 'subd'+str(i))
    #     imgPath = os.path.join(fig_dir, name+'_' + mat + '.png')
    #     render(meshPath, imgPath, mat)

    # mat = 'gray'
    # for i in range(len(list_horse14)):
    #     meshPath = list_horse14[i]
    #     name = name_horse14[i]
    #     imgPath = os.path.join(fig_dir, name+'_' + mat + '_1920_300.png')
    #     render(meshPath, imgPath, mat)
    # outputPath = os.path.join(fig_dir, '0003_0_1093600_f1000_subd0_27_2thin_' +mat+'.png')
    # outputDir = os.path.dirname(outputPath)
    # os.path.exists(outputDir) or os.makedirs(outputDir)
    # render(meshPath, outputPath, mat)
#  cmd: blender --background --python zzw_blender_render.py
#     for meshPath in mesh_path_dict.items():
#         method = meshPath[0]
#         imgPath = os.path.join(fig_dir,  '21_subd3_' + mat +'_'+method+ '.png')
#         render(meshPath[1], imgPath, mat)