#!/bin/sh

data=$1

cd ${data}
mkdir -p olds
mv mask mask_cihp new_params new_vertices params vertices annots_python2.npy annots.npy match_info.json *.mp4 *.py *.npy annots.json olds/

if [[ ! -d keypoints2d ]]; then
    ln -s keypoints2d openpose
fi
mv annots olds/

mkdir images
mv Camera* images

exit 0
