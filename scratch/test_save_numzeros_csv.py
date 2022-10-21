from asf_tools.hand.save_numzeros_csv import *


flistfile = "flist.txt"

with open(flistfile, "r") as f:
    filelist = f.readlines()

out_dir = "."

for file in filelist:

    file = file.rstrip()

    dem_name = file.split('/')

    out_file = dem_name[-1].replace('DEM.tif', 'num_zeros.txt')

    if not os.path.exists(out_file):
        num_zeros = find_number_zeros_hand(file, out_dir)

        log.info(f'Saving to {out_file}')

        with open(out_file, 'w') as f:
            for i in range(0, len(num_zeros)):
                f.write(str(num_zeros[i]) + '\n')


