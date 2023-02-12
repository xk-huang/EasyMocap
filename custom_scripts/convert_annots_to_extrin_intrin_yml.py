#%%
import os
import argparse
import os.path as osp

import numpy as np
import cv2

if osp.basename(os.getcwd()) == "custom_scripts":
    os.chdir("../")

from easymocap.mytools.camera_utils import write_extri, write_intri, read_camera


print(f"pwd: {os.getcwd()}")

parser = argparse.ArgumentParser()
parser.add_argument("--base_dir", type=str, help="The base directory of the dataset.")
args = parser.parse_args()


# base_dir = "data/zju_mocap/CoreView_377/"
base_dir = args.base_dir
print(f"Convert to extrin.yml and intrin.yml in {base_dir}.")

intrin_yml_path = osp.join(base_dir, "intri.yml")
extrin_yml_path = osp.join(base_dir, "extri.yml")

if osp.exists(intrin_yml_path):
    intrin_yml_path = osp.join(base_dir, "intri.from_annots.yml")
    old_intrin_yml_path = osp.join(base_dir, "intri.yml")
else:
    old_intrin_yml_path = None
if osp.exists(extrin_yml_path):
    extrin_yml_path = osp.join(base_dir, "extri.from_annots.yml")
    old_extrin_yml_path = osp.join(base_dir, "extri.yml")
else:
    old_extrin_yml_path = None

annots_path = osp.join(base_dir, "annots.npy")

#%%
annots = np.load(annots_path, allow_pickle=True).item()

annots_cameras = annots["cams"]
annots_ims = annots["ims"]
names = [osp.dirname(i) for i in annots_ims[0]["ims"]]

cameras = {}

for key in annots_cameras.keys():
    if not isinstance(annots_cameras[key][0], np.ndarray):
        for idx, _data in enumerate(annots_cameras[key]):
            annots_cameras[key][idx] = np.array(_data, dtype='float64')
        print(f"{key}[0]: {type(annots_cameras[key][0])}")

num_cameras = len(names)
assert num_cameras == len(annots_cameras["K"]), f"num_cameras: {num_cameras}, len(annots_cameras['K']): {len(annots_cameras['K'])}"

for camera_id in range(num_cameras):
    camera = {}
    # "K", "T", "R", "D"
    camera["K"] = annots_cameras["K"][camera_id]
    camera["T"] = annots_cameras["T"][camera_id] / 1000.  # # [XXX] The T is measured in mm in NeuralBody. Convert it to m.
    camera["R"] = annots_cameras["R"][camera_id]
    camera["dist"] = annots_cameras["D"][camera_id].reshape(1, 5)
    camera["Rvec"] = cv2.Rodrigues(annots_cameras["R"][camera_id])[0]

    cameras[names[camera_id]] = camera

# %%
write_extri(extrin_yml_path, cameras)
write_intri(intrin_yml_path, cameras)
# %%

if old_intrin_yml_path is not None and old_extrin_yml_path is not None:
    gt_cameras = read_camera(old_intrin_yml_path, old_extrin_yml_path)
    test_cameras = read_camera(intrin_yml_path, extrin_yml_path)
    
#%%
if old_intrin_yml_path is not None and old_extrin_yml_path is not None:
    print("Check the correctness of the conversion.")
    for key in gt_cameras.keys():
        if not isinstance(gt_cameras[key], dict):
            continue

        for key2 in gt_cameras[key].keys():
            _gt_camera = gt_cameras[key][key2]
            _test_camera = test_cameras[key][key2]

            if not np.allclose(_gt_camera, _test_camera):
                print(f"\n{key}, {key2}, {np.max(np.abs(_gt_camera - _test_camera)):e}")
            if not np.allclose(_test_camera, _gt_camera):
                print(f"{key}, {key2}, {np.max(np.abs(_test_camera - _gt_camera)):e}")

                if key2 == "P":
                    print("P denote projection matrix. cams[cam]['K'] @ cams[cam]['RT'], the error is acceptable.")


# %%
