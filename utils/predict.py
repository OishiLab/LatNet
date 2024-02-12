import ants
import nibabel as nib
import numpy as np
import torch
from nibabel import processing
from torch import nn
import os
def normalize(voxel):
    nonzero = voxel[voxel>0]
    voxel = np.clip(voxel, 0, np.mean(nonzero)+np.std(nonzero)*3)
    voxel = (voxel - np.min(voxel)) / (np.max(voxel) - np.min(voxel))
    voxel = (voxel * 2) - 1
    return voxel.astype("float32")

def prediction(stripped, data, cnn1, cnn2, cnn3, cnn4, cnn5, opt, device):
    stripped = ants.from_nibabel(nib.Nifti1Image(stripped.astype(np.float32), affine=data.affine))
    mni = ants.from_nibabel(nib.as_closest_canonical(nib.load(os.path.join(opt.m, "MNI_FULL.nii"))))
    tx = ants.registration(mni, stripped, type_of_transform = "Rigid")
    rigid = nib.as_closest_canonical(ants.to_nibabel(tx["warpedmovout"]))
    rigid = processing.conform(rigid, out_shape=(80, 112, 80), voxel_size=(2.0, 2.0, 2.0), order=1)
    rigid = normalize(rigid.get_fdata().astype("float32"))[np.newaxis][np.newaxis].astype("float32")
    rigid = torch.tensor(rigid, requires_grad=False).to(device)
    
    pred1 = torch.softmax(cnn1(rigid), dim=1)[0][1]
    pred2 = torch.softmax(cnn2(rigid), dim=1)[0][1]
    pred3 = torch.softmax(cnn3(rigid), dim=1)[0][1]
    pred4 = torch.softmax(cnn4(rigid), dim=1)[0][1]
    pred5 = torch.softmax(cnn5(rigid), dim=1)[0][1]
    pred = ((pred1 + pred2 + pred3 + pred4 + pred5) / 5).item()
    return pred
        