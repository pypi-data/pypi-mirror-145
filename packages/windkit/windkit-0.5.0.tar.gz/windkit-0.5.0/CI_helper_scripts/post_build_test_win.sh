#!/bin/bash
for python_ver in "3.8" "3.9"
do
echo "======================================================================"
echo "Building conda enviroment 'test_env' :"
echo "python="$python_ver
echo "windkit="$VERSION
echo "======================================================================"
echo ""

mamba create -n test_env python=$python_ver pytest
conda init bash
source activate test_env
mamba install -c $LOCAL_CONDA_CHANNEL windkit=$VERSION --offline --override-channels
cd test
pytest --ignore-glob=*_old.py -v
cd -
conda deactivate
conda env remove -n test_env
rm -fr "C:\ProgramData\Miniconda3\envs\test_env" # because conda remove does not del folder!
done
exit 0
