set -e

base_dir=data/zju_mocap/zju_mocap_easymocap_smpl
target_dir=data/zju_mocap/zju_mocap_easymocap_smplh

for dir in `ls $base_dir`; do
    mkdir -p $target_dir/$dir
    for target_name in images extri.yml intri.yml; do
        if [[ ! -f "$target_dir/$dir/$target_name" ]] && [[ ! -d "$target_dir/$dir/$target_name" ]] ; then
            echo "ln -s ../../../../$base_dir/$dir/$target_name $target_dir/$dir/$target_name"
            ln -s "../../../../$base_dir/$dir/$target_name" "$target_dir/$dir/$target_name"
        else
            echo "$target_dir/$dir/$target_name already exists"
        fi
    done
done