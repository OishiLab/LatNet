# LatNet
![Figure1](https://github.com/OishiLab/LatNet/assets/64403395/dd95f1ee-97a3-4820-a16b-2fc365453b3b)

[![](http://img.shields.io/badge/medRxiv-10.1101/2024.01.18.24301494-B31B1B.svg)](https://www.medrxiv.org/content/10.1101/2024.01.18.24301494v1)
[![IEEE Xplore](https://img.shields.io/badge/under%20review-Imaging%20Neuroscience-%2300629B%09)](https://janeway.imaging-neuroscience.org/)
[![Python 3.8](https://img.shields.io/badge/OpenMAP-T1-brightgreen.svg)](https://github.com/OishiLab/OpenMAP-T1)

**A Neural Network Approach to Identify Left-Right Orientation of Anatomical Brain MRI**<br>
**Author**: Kei Nishimaki, [Hitoshi Iyatomi](https://iyatomi-lab.info/english-top), [Kenichi Oishi](https://www.hopkinsmedicine.org/profiles/details/kenichi-oishi)<br>

The Russell H. Morgan Department of Radiology and Radiological Science, The Johns Hopkins University School of Medicine, Baltimore, MD, USA <br>
Department of Applied Informatics, Graduate School of Science and Engineering, Hosei University, Tokyo, Japan <br>
The Richman Family Precision Medicine Center of Excellence in Alzheimer's Disease, Johns Hopkins University School of Medicine, Baltimore, MD, USA<br>

**Abstract**: *Left-right orientation misidentification in brain MRIs presents significant challenges due to several factors, including metadata loss or ambiguity, which often occurs during the de-identification of medical images for research, conversion between image formats, software operations that strip or overwrite metadata, and the use of older imaging systems that stored orientation differently. This study presents a novel application of deep learning to enhance the accuracy of left-right orientation identification in anatomical brain MRI scans. The three-dimensional Convolutional Neural Network model was trained using 350 MRIs and evaluated on eight distinct brain MRI databases, totaling 3,384 MRIs, to assess its performance across various conditions, including neurodegenerative diseases. The proposed deep learning framework demonstrated a 99.6% accuracy in identifying the left-right orientation, addressing challenges associated with losing orientation metadata. GradCAM was used to visualize areas of the brain where the model focused, demonstrating the importance of the right planum temporale and surrounding areas in judging left-right orientation. The planum temporale is known to exhibit notable left-right asymmetry related to language functions, underscoring the biological validity of the model. More than half of the ten left-right misidentified MRIs involved notable brain feature variations, such as severe temporal lobe atrophy, arachnoidal cysts adjacent to the temporal lobe, or unusual cerebral torque, indicating areas for further investigation. This approach offers a potential solution to the persistent issue of left-right misorientation in brain MRIs and supports the reliability of neuroscientific research by ensuring accurate data interpretation.*

Paper: Not yet<br>
Submitted for publication in the **Imaging Neuroscience**<br>

## Installation Instructions
0. install python and make virtual environment<br>
python3.9 or later is recommended.

1. Clone this repository, and go into the repository::
```
git clone https://github.com/OishiLab/LatNet.git
cd LatNet
```
2. Please install PyTorch compatible with your environment.<br>
https://pytorch.org/

Once you select your environment, the required commands will be displayed.

![image](https://github.com/OishiLab/LatNet/assets/64403395/7b4b11df-e47d-4377-9ab8-798dc8bade94)

If you want to install an older Pytorch environment, you can download it from the link below.<br>
https://pytorch.org/get-started/previous-versions/

4. Install libraries other than PyTorch:
```
pip install -r requirements.txt
```
5. Please apply and download the pre-trained model from the link below and upload it to your server.
6. You can run LatNet !!

## How to use it
**Using LatNet is straightforward. You don't need to do any preprocessing to the image. All you need to run this code is prepare a 3DT1-weighted image of NifTi. This code includes skull-stripping using [OpenMAP-T1](https://github.com/OishiLab/OpenMAP-T1).**
You can use it in any terminal on your linux system. We provide CPU as well as GPU support. Running on GPU is a lot faster though and should always be preferred. Here is a minimalistic example of how you can use LatNet.

```
python3 main.py -i INPUT_FOLDER -o OUTPUT_FOLDER -m MODEL_FOLDER
```
If you want to specify the GPU, please add ```CUDA_VISIBLE_DEVICES=N```.
```
CUDA_VISIBLE_DEVICES=1 python3 main.py -i INPUT_FOLDER -o OUTPUT_FOLDER -m MODEL_FOLDER
```

## How to download the pretrained model.
You can get the pretrained model from the [this link](https://livejohnshopkins-my.sharepoint.com/:f:/g/personal/koishi2_jh_edu/EvgdNZq4oHtHp71VVLi1DOcBpSK-KobNm4ZduBCzFC3b2g).

## Folder
All images you input must be in NifTi format and have a .nii extension.
```
INPUR_FOLDER/
  ├ A.nii
  ├ B.nii
  ├ *.nii

OUTPUT_FOLDER/
  ├ A.csv
  ├ B.csv
  ├ *.csv

MODEL_FOLDER/
  ├ MNI_FULL.nii
  ├ CNet.pth
  ├ SSNet.pth
  ├ CNN1.pth
  ├ CNN2.pth
  ├ CNN3.pth
  ├ CNN4.pth
  └ CNN5.pth
```

## FAQ
* **How much GPU memory do I need to run LatNet?** <br>
We ran all our experiments on NVIDIA RTX3090 GPUs with 24 GB memory. For inference you will need less, but since inference in implemented by exploiting the fully convolutional nature of CNNs the amount of memory required depends on your image. Typical image should run with less than 4 GB of GPU memory consumption. If you run into out of memory problems please check the following: 1) Make sure the voxel spacing of your data is correct and 2) Ensure your MRI image only contains the head region.

* **Will you provide the training code as well?** <br>
No. The training code is tightly wound around the data which we cannot make public.

## Citation
You need to cite both LatNet and OpenMAP-T1.
```
@article {Nishimaki2024.01.18.24301494,
	author = {Kei Nishimaki and Kengo Onda and Kunpei Ikuta and Yuto Uchida and Susumu Mori and Hitoshi Iyatomi and Kenichi Oishi},
	title = {OpenMAP-T1: A Rapid Deep Learning Approach to Parcellate 280 Anatomical Regions to Cover the Whole Brain},
	elocation-id = {2024.01.18.24301494},
	year = {2024},
	doi = {10.1101/2024.01.18.24301494},
	publisher = {Cold Spring Harbor Laboratory Press},
	URL = {https://www.medrxiv.org/content/early/2024/01/20/2024.01.18.24301494},
	eprint = {https://www.medrxiv.org/content/early/2024/01/20/2024.01.18.24301494.full.pdf},
	journal = {medRxiv}
}
```
