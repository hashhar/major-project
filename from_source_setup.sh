sudo apt-get install -y doxygen git swig python-dev cmake-gui build-essential python-pip freeglut3-dev libxi-dev libxmu-dev liblapack-dev

git clone https://github.com/opensim-org/opensim-core.git ~/opensim-core-source && cd ~/opensim-core-source && git checkout v4.0.0_alpha || exit

mkdir ~/opensim-core-dependencies-build
cd ~/opensim-core-dependencies-build/ || exit
cmake ~/opensim-core-source/dependencies/ \
	-DCMAKE_INSTALL_PREFIX="~/opensim_dependencies_install" \
	-DCMAKE_BUILD_TYPE=Release
make -j8

mkdir ~/opensim-core-build
cd ~/opensim-core-build/ || exit
cmake ~/opensim-core-source \
	-DCMAKE_INSTALL_PREFIX="~/opensim_install" \
	-DCMAKE_BUILD_TYPE=Release \
	-DOPENSIM_DEPENDENCIES_DIR="~/opensim_dependencies_install" \
	-DBUILD_PYTHON_WRAPPING=ON \
	-DBUILD_JAVA_WRAPPING=OFF \
	-DWITH_BTK=ON \
	-DBUILD_TESTING=OFF \
	-DOPENSIM_DOXYGEN_USE_MATHJAX=ON \
	-DOPENSIM_INSTALL_UNIX_FHS=OFF \
	-DOPENSIM_COPY_SIMBODY=ON
make doxygen
make -j8
make -j8 install
echo 'export PATH=~/opensim_install/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/opensim_install/sdk/lib' >> ~/.bashrc
source ~/.bashrc

cd ~/opensim_install/sdk/python || exit
sudo /usr/bin/python2 setup.py install
sudo /usr/bin/pip2 install ipython
pip install git+https://github.com/kidzik/osim-rl.git
pip install keras-rl tensorflow h5py

