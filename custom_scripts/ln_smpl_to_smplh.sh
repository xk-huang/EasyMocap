set -e

base_dir=data/zju_mocap/zju_mocap_easymocap_smpl
target_dir=data/zju_mocap/zju_mocap_easymocap_smplh

for dir in `ls $base_dir -U`; do
    mkdir -p $target_dir/$dir
    ln -s "../../../../$base_dir/$dir/images/" "$target_dir/$dir/images"
    ln -s "../../../../$base_dir/$dir/extri.yml" "$target_dir/$dir/extri.yml"
    ln -s "../../../../$base_dir/$dir/intri.yml" "$target_dir/$dir/intri.yml"
done