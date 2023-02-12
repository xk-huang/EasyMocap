#%%
import os
import argparse
import os.path as osp
from pathlib import Path
from collections import defaultdict

import numpy as np
import cv2

if osp.basename(os.getcwd()) == "custom_scripts":
    os.chdir("../")

from easymocap.mytools.camera_utils import read_camera


print(f"pwd: {os.getcwd()}")

parser = argparse.ArgumentParser()
parser.add_argument("--base_dir", type=str, help="The base directory of the dataset.")
args = parser.parse_args()


# base_dir = "data/zju_mocap/zju_mocap_easymocap_smpl/CoreView_313"
base_dir = args.base_dir
print(f"Convert to annots.npy in {base_dir}.")

intrin_yml_path = osp.join(base_dir, "intri.yml")
extrin_yml_path = osp.join(base_dir, "extri.yml")
annots_path = osp.join(base_dir, "annots.npy")


cameras = read_camera(intrin_yml_path, extrin_yml_path)

assert list(cameras.keys())[:-1] == cameras["basenames"], f"{list(cameras.keys())[:-1]} != {cameras['basenames']}, check the cameras names in dir and *.yml"
cameras_names = cameras["basenames"]

#%%
cams = defaultdict(list)
for camera_name in cameras_names:
    cams["K"].append(cameras[camera_name]["K"])
    cams["D"].append(cameras[camera_name]["dist"].reshape(5, 1))
    cams["R"].append(cameras[camera_name]["R"])
    cams["T"].append(cameras[camera_name]["T"].reshape(3, 1) * 1000)  # [XXX] The T is measured in mm in NeuralBody. convert to mm.

#%%
imgs_dir = Path(base_dir) / "images"

num_imgs_each_cam = []
for camera_name in cameras_names:
    num_imgs_each_cam.append(
        len(
            list((imgs_dir / camera_name).glob("*.jpg"))
        )
    )
num_imgs = np.min(num_imgs_each_cam)

ims = list()
for i in range(num_imgs):
    ims_ = {}

    ims_["ims"] = []
    for camera_name in cameras_names:
        img_path = osp.join(camera_name, f"{i:06d}.jpg")
        ims_["ims"].append(img_path)

    ims_["kpts2d"] = None

    ims.append(ims_)

#%%
annots = dict(cams=cams, ims=ims)
np.save(annots_path, annots)
print(f"Save annots.npy to {annots_path}.")