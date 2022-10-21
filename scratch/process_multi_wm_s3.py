import boto3
import os

from asf_tools.water_map import make_water_map

s3_address = 's3://hyp3-nasa-disasters/USDA'

def produce_water_map(bucket_name, prefix, out_dir):
    s3 = boto3.client('s3')

    s3_result = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter = "/")

    if 'Contents' not in s3_result.keys():
        return None

    for key in s3_result['Contents']:
        filepath = key['Key']
        filename = os.path.basename(filepath)
        prefix = os.path.dirname(filepath)

        if filename.endswith('_VV.tif'):
            print(f"process the {filename}")
            # os.system(f"mkdir -p {prefix}")
            filename_vv = filename
            filename_vh = filename_vv.replace("VV.tif", "VH.tif")
            filename_hand = filename_vv.replace("VV.tif", "WM_HAND.tif")
            out_file = filename_vv.replace("VV.tif", "WM_t2.tif")

            if os.path.exists(os.path.join(out_dir, out_file)):
                continue
            else:
                # download vv.tif and vh.tif
                if not os.path.exists(filename_vv):
                    s3.download_file(bucket_name, os.path.join(prefix, filename_vv), os.path.join(out_dir,filename_vv))
                if not os.path.exists(filename_vh):
                    s3.download_file(bucket_name, os.path.join(prefix, filename_vh), os.path.join(out_dir, filename_vh))

                if not os.path.exists(filename_hand):
                    s3.download_file(bucket_name, os.path.join(prefix, filename_hand), os.path.join(out_dir, filename_hand))
                # process wm.tif
                make_water_map( os.path.join(out_dir, out_file), os.path.join(out_dir, filename_vv),
                                os.path.join(out_dir, filename_vh), hand_raster=os.path.join(out_dir, filename_hand))

    return True

if __name__ == "__main__":
    bucket_name = 'hyp3-nasa-disasters'
    prefix = 'USDA/'
    out_dir = './'
    produce_water_map(bucket_name, prefix, out_dir)
    print("completed ..")
