  # cat isometric
catPath = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002_subdiv_fn800/cat3__sf_f800_ns3_nm30/subd0/10.obj'
cat_subd3_Path = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat__sf_f800_ns3_nm30/b1_6_v18_1_Char_f64_n10_s3/test_e24/cat3__sf_f800_ns3_nm30/test_origin/subd3/10.obj'
cat0_subd0 = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002_subdiv_fn800/cat0__sf_f800_ns3_nm30/subd0/01.obj'
# 1093600 nonisometric
meshPath = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_manifold/1093600.obj'
mesh1093600Path = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_manifold/1093600/1093600_f1000_subd0_27_1thin1fat.obj'
mesh1093600_subd0_Path = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_manifold_subdiv_fn1000/1093600_f1000_ns3_nm30/subd0/27.obj'
#mesh1093600Path = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/1093600_f1000_ns3_nm30/b1_6_v18_1_Char_f64_t24v6_l002_s3/test_e380/1093600_f1000_ns3_nm30/27_2fat_subd3.obj'



# bob
bob_subd0 = '/work/Users/zhuzhiwei/neuralSubdiv-master/data_meshes/bob_f600_ns3_nm100/subd0/001.obj'
bob_subd1 = '/work/Users/zhuzhiwei/neuralSubdiv-master/data_meshes/bob_f600_ns3_nm100/subd1/001.obj'
bob_subd2 = '/work/Users/zhuzhiwei/neuralSubdiv-master/data_meshes/bob_f600_ns3_nm100/subd2/001.obj'
bob_subd3 = '/work/Users/zhuzhiwei/neuralSubdiv-master/data_meshes/bob_f600_ns3_nm100/subd3/001.obj'
list_bob = [bob_subd0, bob_subd1, bob_subd2, bob_subd3]
name_bob = ['bob_subd0', 'bob_subd1', 'bob_subd2', 'bob_subd3']

bunny_subd0_path = '/work/Users/zhuzhiwei/dataset/mesh/ns_original_subdiv_fn600/bunny_f600_ns3_nm10/subd0/03.obj'

# dog7
dog7_21_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002_subdiv_fn800/dog7__sf_f800_ns3_nm30/subd3/08.obj'
dog7_21_subd2 = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002_subdiv_fn800/dog7__sf_f800_ns3_nm30/subd2/21.obj'
gt_Path = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002/dog7__sf.obj'
subd0_Path = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002_subdiv_fn800/dog7__sf_f800_ns3_nm30/subd0/21.obj'
subd3_Path = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002_subdiv_fn800/dog7__sf_f800_ns3_nm30/subd3/08.obj'
dog7_21_dict = {
    'loop': '/work/Users/zhuzhiwei/dataset/mesh/loop/toscahires-asci_sf_l05_e0002_subdiv_fn800/dog7__sf_f800_ns3_nm30/subd3/21.obj',
    'butterfly': '/work/Users/zhuzhiwei/dataset/mesh/butterfly/toscahires-asci_sf_l05_e0002_subdiv_fn800/dog7__sf_f800_ns3_nm30/subd3/21.obj',
    'mod_butterfly': '/work/Users/zhuzhiwei/dataset/mesh/modified_butterfly/toscahires-asci_sf_l05_e0002_subdiv_fn800/dog7__sf_f800_ns3_nm30/subd3/21.obj',
    'midpoint': '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002_subdiv_fn800/dog7__sf_f800_ns3_nm30/subd0/21.obj',
    'neuralSubdiv': '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/class9all__sf_f800_ns3_nm30_valid/b1_anchor_f64_n10_s3/test_e27/dog7__sf_f800_ns3_nm30/test_origin/subd3/21.obj'
}
dog7_21_ours1= '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/dog7__sf_f800_ns3_nm30/b1_6_f64_t24v6_l002_s3/test_e269/dog7__sf_f800_ns3_nm30/test_origin/subd3/21.obj'
dog7_21_ours= '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/dog7__sf_f800_ns3_nm30/b1_6_f64_t24v6_l002_s3/test_e380/dog7__sf_f800_ns3_nm30/test_origin/subd3/21.obj'
dog7_21_ns = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/class9all__sf_f800_ns3_nm30_valid/b1_anchor_f64_n10_s3/test_e27/dog7__sf_f800_ns3_nm30/test_origin/subd3/21.obj'
# wolf0 different shape
wolf0 = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002/wolf0__sf.obj'
root_dir = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/'
root_subd3_dir = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/wolf_t0v12_f800_ns3_nm30/b1_6_v18_1_Char_f64_l002_s3/test_e40/'

sudb0_panda = root_dir + 'panda.obj'
sudb3_panda = root_subd3_dir + 'panda_subd3.obj'

subd0_lion = root_dir + 'lion.obj'
subd3_lion = root_subd3_dir + 'lion_subd3.obj'

subd0_101634 = root_dir + '101634.obj'  # 球状宝石
subd3_101634 = root_subd3_dir + '101634_subd3.obj'

subd0_59197 = root_dir + '59197.obj' # 抱腿怪兽
subd3_59197 = root_subd3_dir + '59197_subd3.obj'

subd0_53754 = root_dir + '53754.obj' # 弯曲水管
subd3_53754 = root_subd3_dir + '53754_subd3.obj'

# style transfer
subd0_bunny = '/work/Users/zhuzhiwei/dataset/mesh/ns_ftetwild_subdiv_fr0.06/bunny/subd0/01.obj'
subd3_bunny_58238 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/58238_fr06_ns3_nm10/b1_6_v18_1_Char_f64_s3/test_e277/bunny/01_subd3.obj' # 三角凸起
subd3_bunny_bob = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_6_v18_1_Char_f64_s3/test_e265/bunny/01_subd3.obj' # 平滑
subd3_bunny_88654 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/88654_fr06_ns3_nm10/b1_6_v18_1_Char_f64_s3/test_e142/bunny/01_subd3.obj' # 粗糙
subd3_bunny_50880 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/50880_fr06_ns3_nm10/b1_6_v18_1_Char_f64_s3/test_e285/bunny/01_subd3.obj' # 圆球
subd3_bunny_91655 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/91655_fr06_ns3_nm10/b1_6_v18_1_Char_f64_s3/test_e72/bunny/01_subd3.obj' # 尖锐
subd3_bunny_113958 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/113958_fr06_ns3_nm10/b1_6_v18_1_Char_f64_s3/test_e86/bunny/01_subd3.obj' # 突起

bob = '/work/Users/zhuzhiwei/dataset/mesh/ns_ftetwild/bob.obj'
path_58238 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_manifold/58238/58238.obj'
path_91655 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_manifold/91655/91655.obj'
path_98938 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_manifold/98938/98938.obj'
path_92896 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_manifold/92896/92896.obj'
path_113958 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_manifold/113958/113958.obj'


# thingi10k
## neural subdiv failed
subd0_368 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/test/subd0/368.obj'
subd3_368 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/gt/subd3/368.obj'
ns_368_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_anchor_f64_s3/test_e66/test564/test/subd3/368.obj'
ours_368_subd1 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/test/subd3/368.obj'
loop_368_subd1 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/loop/subd3/368.obj'
butterfly_368_subd1 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/butterfly/subd3/368.obj'
mod_butterfly_368_subd1 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/modified_butterfly/subd3/368.obj'

# 正常
# thingi10k_ns_regular
subd0_454 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/test/subd0/454.obj'
subd3_454 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/gt/subd3/454.obj'
ns_454_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_anchor_f64_s3/test_e66/test564/test/subd3/454.obj'
ours_454_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/test/subd3/454.obj'
loop_454_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/loop/subd3/454.obj'
butterfly_454_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/butterfly/subd3/454.obj'
mod_butterfly_454_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/modified_butterfly/subd3/454.obj'

list_454 = [subd3_454, ns_454_subd3, loop_454_subd3, butterfly_454_subd3, mod_butterfly_454_subd3]
name_454 = ['subd3_454','ns_454_subd3', 'loop_454_subd3', 'butterfly_454_subd3', 'mod_butterfly_454_subd3']

subd0_416 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/test/subd0/416.obj'
subd3_416 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/gt/subd3/416.obj'
ns_416_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_anchor_f64_s3/test_e66/test564/test/subd3/416.obj'
ours_416_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/test/subd3/416.obj'
loop_416_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/loop/subd3/416.obj'
butterfly_416_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/butterfly/subd3/416.obj'
mod_butterfly_416_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/modified_butterfly/subd3/416.obj'

list_416 = [subd3_416, ns_416_subd3, loop_416_subd3, butterfly_416_subd3, mod_butterfly_416_subd3]
name_416 = ['subd3_416','ns_416_subd3', 'loop_416_subd3', 'butterfly_416_subd3', 'mod_butterfly_416_subd3']

subd0_053 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/test/subd0/053.obj'
subd3_053 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/gt/subd3/053.obj'
ns_053_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_anchor_f64_s3/test_e66/test564/test/subd3/053.obj'
ours_053_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/test/subd3/053.obj'
loop_053_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/loop/subd3/053.obj'
butterfly_053_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/butterfly/subd3/053.obj'
mod_butterfly_053_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/modified_butterfly/subd3/053.obj'

list_053 = [subd3_053, ns_053_subd3, loop_053_subd3, butterfly_053_subd3, mod_butterfly_053_subd3]
name_053 = ['subd3_053','ns_053_subd3', 'loop_053_subd3', 'butterfly_053_subd3', 'mod_butterfly_053_subd3']

subd0_250 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/test/subd0/250.obj'
subd3_250 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/gt/subd3/250.obj'
ns_250_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_anchor_f64_s3/test_e66/test564/test/subd3/250.obj'
ours_250_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/test/subd3/250.obj'
loop_250_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/loop/subd3/250.obj'
butterfly_250_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/butterfly/subd3/250.obj'
mod_butterfly_250_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/modified_butterfly/subd3/250.obj'

list_250 = [subd3_250, ns_250_subd3, loop_250_subd3, butterfly_250_subd3, mod_butterfly_250_subd3]
name_250 = ['subd3_250','ns_250_subd3', 'loop_250_subd3', 'butterfly_250_subd3', 'mod_butterfly_250_subd3']

subd0_217 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/test/subd0/217.obj'
subd3_217 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/gt/subd3/217.obj'
ns_217_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_anchor_f64_s3/test_e66/test564/test/subd3/217.obj'
ours_217_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/test/subd3/217.obj'
loop_217_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/loop/subd3/217.obj'
butterfly_217_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/butterfly/subd3/217.obj'
mod_butterfly_217_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/modified_butterfly/subd3/217.obj'

list_217 = [subd3_217, ns_217_subd3, loop_217_subd3, butterfly_217_subd3, mod_butterfly_217_subd3]
name_217 = ['subd3_217','ns_217_subd3', 'loop_217_subd3', 'butterfly_217_subd3', 'mod_butterfly_217_subd3']

ns_horse14_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/class9all__sf_f800_ns3_nm30_valid/b1_anchor_f64_n10_s3/test_e37/horse14__sf_f800_ns3_nm30/test_origin/subd3/01.obj'
ours_horse14_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/class9all__sf_f800_ns3_nm30_valid/b1_6_18_1_Char_f64_n10_s3/test_e157/horse14__sf_f800_ns3_nm30/test_origin/subd3/01.obj'
loop_horse14_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/loop/toscahires-asci_sf_l05_e0002_subdiv_fn800/horse14__sf_f800_ns3_nm30/subd3/01.obj'
butterfly_horse14_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/butterfly/toscahires-asci_sf_l05_e0002_subdiv_fn800/horse14__sf_f800_ns3_nm30/subd3/01.obj'
mod_butterfly_horse14_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/modified_butterfly/toscahires-asci_sf_l05_e0002_subdiv_fn800/horse14__sf_f800_ns3_nm30/subd3/01.obj'
horse14_subd0 = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002_subdiv_fn800/horse14__sf_f800_ns3_nm30/subd0/01.obj'
horse14_gt = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002/horse14__sf.obj'
horse14_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002_subdiv_fn800/horse14__sf_f800_ns3_nm30/subd3/01.obj'
list_horse14 = [horse14_gt, ns_horse14_subd3, loop_horse14_subd3, butterfly_horse14_subd3, mod_butterfly_horse14_subd3]
name_horse14 = ['horse14_gt', 'ns_horse14_subd3', 'loop_horse14_subd3', 'butterfly_horse14_subd3', 'mod_butterfly_horse14_subd3']
ns_dog7_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/class9all__sf_f800_ns3_nm30_valid/b1_anchor_f64_n10_s3/test_e37/dog7__sf_f800_ns3_nm30/test_origin/subd3/21.obj'


bunny_subd0 = '/work/Users/zhuzhiwei/dataset/mesh/ns_original_subdiv_fn600/bunny_f600_ns3_nm10/subd0/03.obj'
bunny_subd1 =  '/work/Users/zhuzhiwei/dataset/mesh/ns_original_subdiv_fn600/bunny_f600_ns3_nm10/subd1/03.obj'
bunny_subd2 =  '/work/Users/zhuzhiwei/dataset/mesh/ns_original_subdiv_fn600/bunny_f600_ns3_nm10/subd2/03.obj'
bunny_subd3 =  '/work/Users/zhuzhiwei/dataset/mesh/ns_original_subdiv_fn600/bunny_f600_ns3_nm10/subd3/03.obj'
bunny_gt = '/work/Users/zhuzhiwei/dataset/mesh/ns_ftetwild/bunny.obj'
list_bunny = [ bunny_subd1, bunny_subd2, bunny_subd3]
name_bunny = ['bunny_subd1', 'bunny_subd2', 'bunny_subd3']

# limit surface
l_ns_dog7_subd1 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat0__sf_f800_ns3_nm30/b1_anchor_f64_t24v6_l002_s2/test_e297/dog7/21_subd1.obj'
l_ns_dog7_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat0__sf_f800_ns3_nm30/b1_anchor_f64_t24v6_l002_s2/test_e297/dog7/21_subd2.obj'
l_ns_dog7_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat0__sf_f800_ns3_nm30/b1_anchor_f64_t24v6_l002_s2/test_e297/dog7/21_subd3.obj'
l_ns_dog7_subd4 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat0__sf_f800_ns3_nm30/b1_anchor_f64_t24v6_l002_s2/test_e297/dog7/21_subd4.obj'

list_l_ns_dog7 = [l_ns_dog7_subd1, l_ns_dog7_subd2, l_ns_dog7_subd3, l_ns_dog7_subd4]

l_ours_dog7_subd1 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat0__sf_f800_ns3_nm30/b1_6_18_1_Char_f64_t24v6_l002_s2/test_e297/dog7/21_subd1.obj'

cactus_subd0 = '/work/Users/zhuzhiwei/dataset/mesh/ns_ftetwild_subdiv_fr0.06/cactus/subd0/01.obj'
ns_cactus_subd1 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat_t12679_v0__sf_f800_ns3_nm30/b1_anchor_f64_l002_s2/test_e295/cactus_subd1.obj'
ns_cactus_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat_t12679_v0__sf_f800_ns3_nm30/b1_anchor_f64_l002_s2/test_e295/cactus_subd2.obj'
ns_cactus_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat_t12679_v0__sf_f800_ns3_nm30/b1_anchor_f64_l002_s2/test_e295/cactus_subd3.obj'
ns_cactus_subd4 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat_t12679_v0__sf_f800_ns3_nm30/b1_anchor_f64_l002_s2/test_e295/cactus_subd4.obj'
list_ns_cactus = [ns_cactus_subd1, ns_cactus_subd2, ns_cactus_subd3, ns_cactus_subd4]
name_ns_cactus = ['ns_cactus_subd1', 'ns_cactus_subd2', 'ns_cactus_subd3', 'ns_cactus_subd4']

ours_cactus_subd1 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_6_char_f64_t24v6_l002_s2/test_e255/cactus/01_subd1.obj'
ours_cactus_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_6_char_f64_t24v6_l002_s2/test_e255/cactus/01_subd2.obj'
ours_cactus_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_6_char_f64_t24v6_l002_s2/test_e255/cactus/01_subd3.obj'
ours_cactus_subd4 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_6_char_f64_t24v6_l002_s2/test_e255/cactus/01_subd4.obj'
list_ours_cactus = [ours_cactus_subd1, ours_cactus_subd2, ours_cactus_subd3, ours_cactus_subd4]
name_ours_cactus = ['ours_cat0_subd1', 'ours_cat0_subd2', 'ours_cat0_subd3', 'ours_cat0_subd4']

ours_1717684_subd1='/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_6_char_f64_t24v6_l002_s2/test_e255/1717684_sf_01_subd4_subd1.obj'
ours_1717684_subd2='/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_6_char_f64_t24v6_l002_s2/test_e255/1717684_sf_01_subd4_subd2.obj'
ours_1717684_subd3='/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_6_char_f64_t24v6_l002_s2/test_e255/1717684_sf_01_subd4_subd3.obj'
ours_1717684_subd4='/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_6_char_f64_t24v6_l002_s2/test_e255/1717684_sf_01_subd4_subd4.obj'
list_ours_1717684 = [ours_1717684_subd1, ours_1717684_subd2, ours_1717684_subd3, ours_1717684_subd4]
name_ours_1717684 = ['ours_1717684_subd1', 'ours_1717684_subd2', 'ours_1717684_subd3', 'ours_1717684_subd4']

ns_1717684_subd1='/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_anchor_f64_t24v6_l002_s2/test_e299/1717684_sf_01_subd4_subd1.obj'
ns_1717684_subd2='/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_anchor_f64_t24v6_l002_s2/test_e299/1717684_sf_01_subd4_subd2.obj'
ns_1717684_subd3='/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_anchor_f64_t24v6_l002_s2/test_e299/1717684_sf_01_subd4_subd3.obj'
ns_1717684_subd4='/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_anchor_f64_t24v6_l002_s2/test_e299/1717684_sf_01_subd4_subd4.obj'
list_ns_1717684 = [ns_1717684_subd1, ns_1717684_subd2, ns_1717684_subd3, ns_1717684_subd4]
name_ns_1717684 = ['ns_1717684_subd1', 'ns_1717684_subd2', 'ns_1717684_subd3', 'ns_1717684_subd4']

ns_fish_subd1 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_anchor_f64_t24v6_l002_s2/test_e299/fish/01_subd1.obj'
ns_fish_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_anchor_f64_t24v6_l002_s2/test_e299/fish/01_subd2.obj'
ns_fish_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_anchor_f64_t24v6_l002_s2/test_e299/fish/01_subd3.obj'
ns_fish_subd4 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_anchor_f64_t24v6_l002_s2/test_e299/fish/01_subd4.obj'
list_ns_fish = [ns_fish_subd1, ns_fish_subd2, ns_fish_subd3, ns_fish_subd4]
name_ns_fish = ['ns_fish_subd1', 'ns_fish_subd2', 'ns_fish_subd3', 'ns_fish_subd4']

ours_fish_subd1 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_6_char_f64_t24v6_l002_s2/test_e255/fish/01_subd1.obj'
ours_fish_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_6_char_f64_t24v6_l002_s2/test_e255/fish/01_subd2.obj'
ours_fish_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_6_char_f64_t24v6_l002_s2/test_e255/fish/01_subd3.obj'
ours_fish_subd4 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_6_char_f64_t24v6_l002_s2/test_e255/fish/01_subd4.obj'
list_ours_fish = [ours_fish_subd1, ours_fish_subd2, ours_fish_subd3, ours_fish_subd4]
name_ours_fish = ['ours_fish_subd1', 'ours_fish_subd2', 'ours_fish_subd3', 'ours_fish_subd4']

fish_subd0 = '/work/Users/zhuzhiwei/dataset/mesh/ns_ftetwild_subdiv_fr0.06/fish/subd0/01.obj'

panda_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/panda.obj'
panda_subd2 = '/work/Users/zhuzhiwei/dataset/mesh/free3d-animal/animal-3kk/Panda_f1000_ns3_nm50/subd2/04.obj'
loop_panda_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/loop/panda/panda_subd3.obj'
butterfly_panda_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/butterfly/panda/panda_subd3.obj'
mod_butterfly_panda_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/modified_butterfly/panda/panda_subd3.obj'
ns_panda_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_fr06_ns3_nm10/b1_anchor_f64_t24v6_l002_s2/test_e299/panda/01_subd3.obj'

list_panda = [loop_panda_subd3, butterfly_panda_subd3, mod_butterfly_panda_subd3, ns_panda_subd3]
name_panda = ['loop_panda_subd3', 'butterfly_panda_subd3', 'mod_butterfly_panda_subd3', 'ns_panda_subd3']
ours_panada_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat0__sf_f800_ns3_nm30/b1_6_f64_t24v6_l002ld50_s3/test_e132/panda_subd3.obj'


# 快速收敛
f_ns_panda_subd3='/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat0__sf_f800_ns3_nm30/b1_anchor_f64_t1v1_l002_s3/test_e299/panda_subd3.obj'
f_ours_panda_subd3='/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat0__sf_f800_ns3_nm30/b1_6_f64_t1v1_l002_s3/test_e298/panda_subd3.obj'
f_ns_lion_subd3='/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat0__sf_f800_ns3_nm30/b1_anchor_f64_t1v1_l002_s3/test_e299/lion_subd3.obj'
f_ours_lion_subd3='/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat0__sf_f800_ns3_nm30/b1_6_f64_t1v1_l002_s3/test_e298/lion_subd3.obj'
lion_subd2 = '/work/Users/zhuzhiwei/dataset/mesh/free3d-animal/animal-3kk/Lion_f1000_ns3_nm50/subd2/04.obj'


rockerArm_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/rockerArm.obj'
rockerArm_gt = '/work/Users/zhuzhiwei/neuralSubdiv-master/data_meshes/objs_original/rocker_arm.obj'
midpoint_rockerArm_subd1 =  '/work/Users/zhuzhiwei/dataset/mesh/midpoint/rockerArm/rockerArm_subd1.obj'
loop_rockerArm_subd1 = '/work/Users/zhuzhiwei/dataset/mesh/loop/rockerArm/rockerArm_subd1.obj'
butterfly_rockerArm_subd1 ='/work/Users/zhuzhiwei/dataset/mesh/butterfly/rockerArm/rockerArm_subd1.obj'
mod_butterfly_rockerArm_subd1 = '/work/Users/zhuzhiwei/dataset/mesh/modified_butterfly/rockerArm/rockerArm_subd1.obj'
ours_rockerArm_subd1 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bunny_f500_ns2_nm200/b1_6_f64_t180v20_l002_s2/test_e377/rockerArm_subd1.obj'
ours1_rockerArm_subd1 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bunny_f500_ns2_nm200/b1_6_f64_t180v20_l2_l002_s2/test_e200/rockerArm_subd1.obj'
ns_rockerArm_subd1 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bunny_f500_ns2_nm200/b1_anchor_f32_t180v20_l002_s2/test_e114/rockerArm_subd1.obj'

tbunny_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/bunny.obj'
tbunny_gt = '/work/Users/zhuzhiwei/dataset/mesh/ns_original/bunny.obj'
loop_tbunny_subd2 = '/work/Users/zhuzhiwei/dataset/mesh/loop/bunny/bunny_subd2.obj'
butterfly_tbunny_subd2 = '/work/Users/zhuzhiwei/dataset/mesh/butterfly/bunny/bunny_subd2.obj'
mod_butterfly_tbunny_subd2 = '/work/Users/zhuzhiwei/dataset/mesh/modified_butterfly/bunny/bunny_subd2.obj'
ns_tbunny_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_anchor_f32_t180v20_l002_s2/test_e196/bunny_subd2.obj'
ours_tbunny_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_6_f64_t180v20_l002_s2/test_e101/bunny_subd2.obj'

ns_tbunny_f800_04_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_anchor_f32_t180v20_l002_s2/test_e196/bunny_f800_04_subd2.obj'
ours_tbunny_f800_04_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_6_f64_t180v20_l002_s2/test_e101/bunny_f800_04_subd2.obj'

tbunny_f800_10_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/bunny_f800_10.obj'
ours_tbunny_f800_10_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_6_t180v20_l002_s2/test_e101/bunny_f800_10_subd2.obj'
ns_tbunny_f800_10_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_anchor_t180v20_l002_s2/test_e196/bunny_f800_10_subd2.obj'
loop_tbunny_f800_10_subd2 = '/work/Users/zhuzhiwei/dataset/mesh/loop/bunny_f800_10/bunny_f800_10_subd2.obj'
butterfly_tbunny_f800_10_subd2 = '/work/Users/zhuzhiwei/dataset/mesh/butterfly/bunny_f800_10/bunny_f800_10_subd2.obj'
mod_butterfly_tbunny_f800_10_subd2 = '/work/Users/zhuzhiwei/dataset/mesh/modified_butterfly/bunny_f800_10/bunny_f800_10_subd2.obj'


ns_spot_099_head2_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/spot_f300_ns2_nm100/b1_anchor_t80_ll2_s2/test_e660/spot_099_head2_subd2.obj'
ns_spot_099_body2_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/spot_f300_ns2_nm100/b1_anchor_t80_ll2_s2/test_e660/spot_099_body2_subd2.obj'
ours_spot_099_head2_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/spot_f300_ns2_nm100/b1_6_t80_ll2_s2/test_e83/spot_099_head2_subd2.obj'
ours_spot_099_body2_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/spot_f300_ns2_nm100/b1_6_t80_ll2_s2/test_e83/spot_099_body2_subd2.obj'
spot_099_head2_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/spot_099_head2.obj'
spot_099_body2_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/spot_099_body2.obj'
spot_gt = '/work/Users/zhuzhiwei/dataset/mesh/ns_ftetwild/spot.obj'

ns_bob_59197_f2000_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_anchor_t180v20_l002_s2/test_e196/59197_f2000_subd2.obj'
ns_bob_59197_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_anchor_t180v20_l002_s2/test_e196/59197_subd2.obj'
ns_bob_101634_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_anchor_t180v20_l002_s2/test_e196/101634_subd2.obj'
ours_bob_59197_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_6_t180v20_l002_s2/test_e101/59197_subd2.obj'
ours_bob_101634_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_6_t180v20_l002_s2/test_e101/101634_subd2.obj'

cat6_gt = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002/cat6__sf.obj'
cat0_01_subd0 = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002_subdiv_fn800/cat0__sf_f800_ns3_nm30/subd0/01.obj'
cat1_01_subd0 = '/work/Users/zhuzhiwei/dataset/mesh/toscahires-asci_sf_l05_e0002_subdiv_fn800/cat1__sf_f800_ns3_nm30/subd0/01.obj'
ns_cat6_cat0_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/centaur_f800_ns2_nm180/b1_anchor_f32_t144v36_l002_s2/test_e699/cat0__sf_f800_ns3_nm30/test_origin/subd2/01.obj'
ours_cat6_cat0_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat6__sf_f1000_ns2_nm100/b1_6_t80_ll2_s2/test_e461/cat0__sf_f800_ns3_nm30/test_origin/subd2/01.obj'
ns_cat6_cat1_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/centaur_f800_ns2_nm180/b1_anchor_f32_t144v36_l002_s2/test_e699/cat1__sf_f800_ns3_nm30/test_origin/subd2/01.obj'
ours_cat6_cat1_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/cat6__sf_f1000_ns2_nm100/b1_6_t80_ll2_s2/test_e461/cat1__sf_f800_ns3_nm30/test_origin/subd2/01.obj'

owl_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/owl.obj'
ns_bob_owl_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_anchor_t180v20_l002_s2/test_e196/owl_subd2.obj'
ours_bob_owl_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_6_t180v20_l002_s2/test_e101/owl_subd2.obj'
fish_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/fish_f800.obj'
ns_bob_fish_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_anchor_t180v20_l002_s2/test_e196/fish_f800_subd2.obj'
ours_bob_fish_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_6_t180v20_l002_s2/test_e101/fish_f800_subd2.obj'
subd0_1093600 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/1093600_f1000.obj'
ours_bob_1093600_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_6_t180v20_l002_s2/test_e101/1093600_f1000_subd2.obj'
ns_bob_1093600_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_anchor_t180v20_l002_s2/test_e196/1093600_f1000_subd2.obj'
fish_gt = '/work/Users/zhuzhiwei/dataset/mesh/ns_ftetwild/fish.obj'


ns_095_41984_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/41984_sf_f600_ns2_nm100/b1_anchor_t80_ll2_s2/test_e401//095_subd3.obj'
ours_095_subd1 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/919994_sf_f800_ns2_nm100/b1_6_t80_lchar_s2/test_e374/095_subd1.obj'
loop_095_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/loop/subd3//095.obj'
butterfly_095_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/butterfly/subd3/095.obj'
mod_butterfly_095_subd3 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/modified_butterfly/subd3/095.obj'
subd0_095 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/test/subd0/095.obj'
subd3_095 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/gt/subd3//095.obj'
ours_41984_095_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/41984_sf_f600_ns2_nm100/b1_6_t80_lchar_s2/test_e370/095_subd2.obj'
ns_095_spot_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/spot_f300_ns2_nm100/b1_anchor_t80_ll2_s2/test_e660/095_subd3.obj'
ns_095_919994_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/919994_sf_f800_ns2_nm100/b1_anchor_t80_lchar_s2/test_e378/095_subd3.obj'
our_095_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/test/subd3/095.obj'
ours_095_spot_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/spot_f300_ns2_nm100/b1_6_t80_ll2_s2/test_e83//095_subd3.obj'
subd0_271 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface_5550_subdiv_fr0.06_pkl/test/subd0/271.obj'
ns_271_spot_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/spot_f300_ns2_nm100/b1_anchor_t80_ll2_s2/test_e660/271_subd3.obj'
ours_271_spot_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/spot_f300_ns2_nm100/b1_6_t80_ll2_s2/test_e83//271_subd3.obj'
subd3_271 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/test564/gt/subd3//271.obj'

gt_919994 = '/work/Users/zhuzhiwei/dataset/mesh/10k_surface//919994_sf.obj'
ns_095_10k_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_anchor_f64_s3/test_e66/test564/test/subd2/095.obj'

elephant_005_subd2 = '/work/Users/zhuzhiwei/neuralSubdiv-master/data_meshes/cartoon_elephant_10/subd2/005.obj'
elephant_005_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/elephant_005.obj'
elephant_005_smallhead_longleg_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/elephant_005_smallhead_longleg.obj'
elephant_005_smallbody_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/elephant_005_smallbody.obj'
ours_bob_elephant_005_smallhead_longleg = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_6_t180v20_l002_s2/test_e101/elephant_005_smallhead_longleg_subd2.obj'
ours_bob_elephant_005_smallbody = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_6_t180v20_l002_s2/test_e101/elephant_005_smallbody_subd2.obj'

ns_bob_elephant_005_smallhead_longleg = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_anchor_t180v20_l002_s2/test_e196/elephant_005_smallhead_longleg_subd2.obj'
ns_bob_elephant_005_smallbody = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bob_f200_ns2_nm200/b1_anchor_t180v20_l002_s2/test_e196/elephant_005_smallbody_subd2.obj'


cube_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/cube.obj'
bunny_cube_subd1 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bunny_f500_ns2_nm200/b1_ours_t160_lchar_s2/test_e252/cube_subd1.obj'
bunny_cube_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bunny_f500_ns2_nm200/b1_ours_t160_lchar_s2/test_e252/cube_subd2.obj'
bunny_cube_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/bunny_f500_ns2_nm200/b1_ours_t160_lchar_s2/test_e252/cube_subd3.obj'

thingi10k_cube_subd1 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/cube_subd1.obj'
thingi10k_cube_subd2 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/cube_subd2.obj'
thingi10k_cube_subd3 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/jobs/10k_surface_5550_subdiv_fr0.06/b1_6_v18_1v1_char_f64_s3/test_e94/cube_subd3.obj'

sphere_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/sphere.obj'
sphere12_subd0 = '/work/Users/zhuzhiwei/project/neuralSubdivSurfaces/data_meshes/sphere12.obj'