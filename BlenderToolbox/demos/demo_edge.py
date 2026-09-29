import sys, os
#sys.path.append(os.path.join(os.path.abspath(os.getcwd()),'..')) # change this to your path to “path/to/BlenderToolbox/
sys.path.append(os.path.join(os.path.abspath(os.getcwd())))
import BlenderToolBox as bt
import bpy, bmesh
import numpy as np


'''
    "image_resolution": [1080, 1080],  # recommend >1080 for paper figures
    "number_of_samples": 300,  # recommend >200 for paper figures

bunny:
    location = (0.91, -0.68, 0.1)  # (UI: click mesh > Transform > Location)
    rotation = (351, -0.366, 91.4)  # (UI: click mesh > Transform > Rotation)
    scale = (1.5, 1.5, 1.5)  # (UI: click mesh > Transform > Scale)

bob:
    location = (0, 0, 0.686)  # (UI: click mesh > Transform > Location)
    rotation = (-100, -190, -28)  # (UI: click mesh > Transform > Rotation)
    scale = (1.5, 1.5, 1.5)  # (UI: click mesh > Transform > Scale)

cat0:
    location = (0.318092, -0.244489, -0.005273)  # (UI: click mesh > Transform > Location)
    rotation = (-182, -179, -59.8)  # (UI: click mesh > Transform > Rotation)
    scale = (0.019, 0.019, 0.019)  # (UI: click mesh > Transform > Scale)

cat0:
    location = (0.318092, -0.244489, -0.005273)  # (UI: click mesh > Transform > Location)
    rotation = (-182, -179, -59.8)  # (UI: click mesh > Transform > Rotation)
    scale = (0.019, 0.019, 0.019)  # (UI: click mesh > Transform > Scale)
'''

def render(meshPath, outPath):
    # outputPath = os.path.join(cwd, './demo_edge.png')  # make it abs path for windows

    ## initialize blender
    imgRes_x = 1280
    imgRes_y = 1280
    numSamples = 300
    exposure = 1.5
    bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

    ## read mesh (choose either readPLY or readOBJ)
    # meshPath = '/work/Users/zhuzhiwei/neuralSubdiv-master/data_meshes/objs_original/subdiv_fn500/bunny_f500_ns4_nm10/subd0/01.obj'
    # outputPath = meshPath[:-4] + '.png'

    location = (1.2479, 0.1286, 0.191)  # (UI: click mesh > Transform > Location)
    rotation = (-196, -188, -54)  # (UI: click mesh > Transform > Rotation)
    scale = (0.009, 0.009, 0.009)  # (UI: click mesh > Transform > Scale)
    mesh = bt.readMesh(meshPath, location, rotation, scale)

    ## set shading (uncomment one of them)
    bpy.ops.object.shade_smooth()

    ## subdivision
    bt.subdivision(mesh, level=0)

    # # set material
    edgeThickness = 0.005
    edgeColor = bt.colorObj((0, 0, 0, 0), 0.5, 1.0, 1.0, 0.0, 0.0)
    meshRGBA = (1, 1, 1, 0)
    AOStrength = 1.0
    bt.setMat_edge(mesh, edgeThickness, edgeColor, meshRGBA, AOStrength)

    ## set invisible plane (shadow catcher)
    bt.invisibleGround(shadowBrightness=0.9)

    ## set camera (recommend to change mesh instead of camera, unless you want to adjust the Elevation)
    camLocation = (3, 0, 2)
    lookAtLocation = (0, 0, 0.5)
    focalLength = 45  # (UI: click camera > Object Data > Focal Length)
    cam = bt.setCamera(camLocation, lookAtLocation, focalLength)

    ## set light
    lightAngle = (6, -30, -155)
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
    meshPath = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002_subdiv_fn800/centaur0__sf_f800_ns3_nm30/subd0/01.obj'
    fig_dir = '/work/Users/zhuzhiwei/tools/BlenderToolbox/fig/'

    for i in range(0, 1):
        if i > 0:
            meshPath = meshPath.replace('subd'+str(i-1), 'subd'+str(i))
        outputPath = meshPath[:-4] + '_edge.png'
        outputPath = os.path.join(fig_dir, outputPath.split('dataset/mesh/')[-1])
        # outputPath = outputPath.replace('bob_f500_ns4_nm10', 'bob_f500_ns4_nm10_png')
        outputDir = os.path.dirname(outputPath)
        os.path.exists(outputDir) or os.makedirs(outputDir)
        render(meshPath, outputPath)