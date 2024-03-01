import argparse
import glob
import os
from functools import partial

import pandas as pd
import numpy as np
import nibabel as nib
import torch
from tqdm import tqdm as std_tqdm

tqdm = partial(std_tqdm, dynamic_ncols=True)

from utils.load_model import load_model
from utils.cropping import cropping
from utils.predict import prediction
from utils.preprocessing import preprocessing
from utils.stripping import stripping


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="input folder")
    parser.add_argument("-o", help="output folder")
    parser.add_argument("-m", help="model path")
    return parser.parse_args()

def main():
    print(
        "\n#######################################################################\n"
        "Please cite the following paper when using LatNet:\n"
        "Kei Nishimaki, Hitoshi Iyatomi, Kenichi Oishi (2024).\n"
        "A Neural Network Approach to Identify Left-Right Orientation of Anatomical Brain MRI.\n"
        "paper: https://www.medrxiv.org/content/10.1101/2024.01.18.24301494v1.\n"
        "#######################################################################\n"
        )
    opt = create_parser()
    device = torch.device("cuda") if torch.cuda.is_available() else "cpu"
    cnet, ssnet, cnn1, cnn2, cnn3, cnn4, cnn5 = load_model(opt, device)

    print("load complete !!")
    pathes = sorted(glob.glob(os.path.join(opt.i, "**/*.nii"), recursive=True))
    os.makedirs(opt.o, exist_ok=True)
    for path in tqdm(pathes):
        data = preprocessing(path)
        #voxel = np.flip(data.get_fdata().astype("float32"), 0)
        #data = nib.Nifti1Image(voxel.astype(np.float32), affine=data.affine)
        cropped = cropping(data, cnet, device)
        stripped = stripping(cropped, data, ssnet, device)
        pred = prediction(stripped, data, cnn1, cnn2, cnn3, cnn4, cnn5, opt, device)

        save = os.path.splitext(os.path.basename(path))[0]
        df = pd.DataFrame([save, pred], index=["Name", "Probability"]).T
        df.to_csv(os.path.join(opt.o, f"{save}.csv"), index=False)
        del data
        os.remove(f"N4/N4.nii")

if __name__ == "__main__":
    main()