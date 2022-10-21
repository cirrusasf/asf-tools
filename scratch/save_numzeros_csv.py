import argparse
import logging
import os
import sys


import numpy as np
from asf_tools.hand.cal_hand_by_dem import make_asf_hand
from osgeo import gdal

log = logging.getLogger(__name__)

def find_number_zeros_hand(dem_tile: str, raster_dir, acc_range=np.linspace(50, 1600, 32).astype(int)):
    if raster_dir is None:
        raster_dir = os.getcwd()

    dem_name = dem_tile.split('/')
    hand_base = dem_name[-1].replace('DEM.tif', 'HAND_')

    num_zeros = np.zeros(len(acc_range))
    num_nan = np.zeros(len(acc_range))

    for i, acc_thresh in enumerate(acc_range):
        log.info(acc_thresh)
        try:
            hand_raster = raster_dir + '/' + hand_base + str(acc_thresh) + '.tif'
            hand_array = gdal.Open(str(hand_raster), gdal.GA_ReadOnly).ReadAsArray()
        except:
            print(f'raster for acc={acc_thresh} doesnt exist! Creating')
            hand_raster, acc_raster = make_asf_hand(dem_tile, acc_thresh=acc_thresh)
            hand_array = gdal.Open(str(hand_raster), gdal.GA_ReadOnly).ReadAsArray()
        zeros = np.where(hand_array == 0)
        num_zeros[i] = len(zeros[0])
        nans = np.isnan(hand_array)
        nans_tf = np.where(nans == True)
        num_nan[i] = len(nans_tf[0])

    return num_zeros

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('dem_tile', help='VSICURL path to a Copernicus GLO-30 DEM GeoTIFF to calculate HAND from. '
                                         'Tile must be located in the AWS Open Data bucket `s3://copernicus-dem-30m/`. '
                                         'For more info, see: https://registry.opendata.aws/copernicus-dem/')
    parser.add_argument('-d', '--raster_dir', help='Path to local directory where HAND files are stored')
    parser.add_argument('-v', '--verbose', action='store_true', help='Turn on verbose logging')
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s', level=level)
    log.debug(' '.join(sys.argv))
    log.info(f'Finding number of zeros for {args.dem_tile}')

    acc_range = np.linspace(50, 1600, 32)
    num_zeros = find_number_zeros_hand(args.dem_tile, args.raster_dir)

    out_file = args.raster_dir + 'number_of_zeros.txt'
    log.info(f'Saving to {out_file}')

    with open(out_file, 'w') as f:
        for i in range(0, len(num_zeros)):
            f.write(str(num_zeros[i]) + '\n')
    f.close()


if __name__ == '__main__':
    main()
