"""
解压gz文件
"""

import gzip
import glob
from tqdm import tqdm

data_dir = "/Volumes/HDD/Data/ztd/ztd/"

# total = len(glob.glob(data_dir+"*/20[1|2]*/*.trop.gz"))

# print(total)


for fp in tqdm(glob.iglob(data_dir+"*/20[1|2]*/*.trop.gz")):
    out_fp = fp[:-3]
    with gzip.GzipFile(fp) as gfile:
        with open(out_fp, "wb+") as f:
            f.write(gfile.read())