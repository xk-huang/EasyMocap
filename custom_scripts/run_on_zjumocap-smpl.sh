set -e

dir=data/zju_mocap/zju_mocap_easymocap_smpl

for name in `ls $dir`; do
    data="$dir/${name}/"
    bash custom_scripts/convert_zjumocap_to_easymocap.sh ${data} > /dev/null 2>&1
    bash custom_scripts/run_easymocap.sh ${data} smpl
done
