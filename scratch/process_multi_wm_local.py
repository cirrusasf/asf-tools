import glob

from asf_tools.water_map import make_water_map

for vv_file in glob.glob('*VV.tif'):
    vh_file = vv_file.replace('VV.tif', 'VH.tif')
    hand_file = vv_file.replace('VV.tif', 'WM_HAND.tif')    
    out_file = vv_file.replace('VV.tif', 'WM.tif')

    make_water_map(out_file, vv_file, vh_file)

print('completed ...')
