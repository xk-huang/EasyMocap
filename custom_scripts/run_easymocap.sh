#!/bin/sh
set -e

data=$1
mode=$2

openpose=/workspace/openpose/
python3 apps/preprocess/extract_keypoints.py ${data} --mode openpose --openpose ${openpose} --hand --face

if [[ $mode = 'smpl' ]]; then
    if [[ -f "${data}/output-smpl-3d/smplmesh.mp4" ]]; then
        echo "Already processed: ${data}"
        exit 0
    fi
    python3 apps/demo/mocap.py ${data} --work mv1p --subs_vis "$(ls ${data}/images | head -1)"
elif [[ $mode == 'smplh' ]]; then
    if [[ -f "${data}/output-smplh-3d/smplmesh.mp4" ]]; then
        echo "Already processed: ${data}"
        exit 0
    fi
    python3 apps/demo/mocap.py ${data} --work mv1p-smplh --subs_vis "$(ls ${data}/images | head -1)"
else
    echo "Unknown mode: ${mode}"
    exit 1
fi