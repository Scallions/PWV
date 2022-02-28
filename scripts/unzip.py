import zipfile
import glob
import os
from tqdm import tqdm

total = len(glob.glob("dataset/ztd_zip/*.trop.zip"))
for fp in tqdm(glob.iglob("dataset/ztd_zip/*.trop.zip"), total=total):
    fname = fp.split("/")[-1].split(".")
    sitename = fname[0]
    year = fname[1]
    dirpath = f"dataset/ztd/{sitename}/{year}"
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    else:
        continue
    with zipfile.ZipFile(fp) as zipf:
        zipf.extractall(dirpath)

