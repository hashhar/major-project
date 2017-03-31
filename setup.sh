#!/bin/bash

MINICONDA_URL='https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh'

[ -f /usr/bin/wget ] || sudo apt-get install -y wget
cd ~ && wget $MINICONDA_URL && bash $(basename $MINICONDA_URL) || exit
conda create -n osim -c kidzik opensim git && source activate osim || exit
pip install git+https://github.com/kidzik/osim-rl.git && python -c "import opensim" || exit
pip install keras-rl h5py tensorflow || exit
echo "DONE!"
