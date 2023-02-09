#!/bin/sh

data=$1

cd ${data}
mkdir -p olds
mv mask mask_cihp new_params new_vertices params vertices annots_python2.npy annots.npy match_info.json *.mp4 *.py *.npy annots.json olds/

if [[ -d keypoints2d ]]; then
    ln -s keypoints2d openpose
fi
mv annots olds/

mkdir images
mv Camera* images

# Special case for CoreView_313 and CoreView_315

relink_dir() {
    target_dir=$1
    echo "relinking: $target_dir"

    if [[ ! -d "${target_dir}" ]] && [[ ! -d olds/"${target_dir}" ]]; then
        echo "ERROR: neither ${target_dir} nor olds/${target_dir} exist"
        exit 1
    elif [[ ! -d "${target_dir}" ]]; then
        mkdir -p "${target_dir}"

    elif [[ ! -d olds/"${target_dir}" ]]; then
        mv -i  -- "${target_dir}"/ olds/
        mkdir -p "${target_dir}"
    fi

    find olds/"${target_dir}" -maxdepth 1 -mindepth 1 -type d | sort | while iFS= read -r full_sub; do
        sub=$(basename "$full_sub")
        mkdir -p "${target_dir}"/"$sub"
        echo "processing: $full_sub -> ${target_dir}/$sub" 

        cnt=0
        for file in $(ls "$full_sub" | sort); do
            # mv -i -- $sub/$file $sub/$(printf %06d cnt).jpg"$extension"
            extension="${file##*.}"
            if [[ ! -f ./"${target_dir}"/"$sub"/$(printf %06d $cnt)."$extension" ]]; then
                ln -s ../../"$full_sub"/"$file"  ./"${target_dir}"/"$sub"/$(printf %06d $cnt)."$extension"
            # else
            #     md5_before=$(md5sum ./"${target_dir}"/"$sub"/$(printf %06d $cnt)."$extension" | awk '{print $1}')
            #     md5_after=$(md5sum "$full_sub"/"$file" | awk '{print $1}')
            #     if [[ $md5_before != $md5_after ]]; then
            #         echo "ERROR: md5sum of ${target_dir} before and after is not the same"
            #         echo "before: " $md5_before
            #         echo "after: " $md5_after
            #         exit 1
            #     fi
            fi
            cnt=$(( cnt + 1 ))
        done 

        num_files_before=$(ls ./"${target_dir}"/"$sub" | wc -l)
        num_files_after=$(ls "$full_sub" | wc -l)
        if [[ $num_files_before -ne $num_files_after ]]; then
            echo "ERROR: number of files before and after is not the same"
            echo "before: " $num_files_before
            echo "after: " $num_files_after
            exit 1
        else
            echo "number of files before and after is the same: " $num_files_before
        fi
    done
}

if [[ "$(basename ${data})" = "CoreView_313" ]] || [[ "$(basename ${data})" = "CoreView_315" ]]; then
    echo $data is CoreView_313 or CoreView_315, the "extri.yml" and "intr.yml" are missing, the images, keypoints2d are not named after numbers
    relink_dir images
    relink_dir keypoints2d

fi

exit 0
