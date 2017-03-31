#!/bin/bash

# Color codes {{{
NONE="\[\033[0m\]"    # unsets color to term's fg color

# regular colors
K="\[\033[0;30m\]"    # black
R="\[\033[0;31m\]"    # red
G="\[\033[0;32m\]"    # green
Y="\[\033[0;33m\]"    # yellow
B="\[\033[0;34m\]"    # blue
M="\[\033[0;35m\]"    # magenta
C="\[\033[0;36m\]"    # cyan
W="\[\033[0;37m\]"    # white

# emphasized (bolded) colors
EMK="\[\033[1;30m\]"
EMR="\[\033[1;31m\]"
EMG="\[\033[1;32m\]"
EMY="\[\033[1;33m\]"
EMB="\[\033[1;34m\]"
EMM="\[\033[1;35m\]"
EMC="\[\033[1;36m\]"
EMW="\[\033[1;37m\]"

# background colors
BGK="\[\033[40m\]"
BGR="\[\033[41m\]"
BGG="\[\033[42m\]"
BGY="\[\033[43m\]"
BGB="\[\033[44m\]"
BGM="\[\033[45m\]"
BGC="\[\033[46m\]"
BGW="\[\033[47m\]"
# }}}

# Varibles {{{
TMP_ROOT="$HOME/opensim-bootstrap"
PYTHON_PACKAGES='python python-dev python-setuptools python-pip'
SWIG_DEPS='build-essential libpcre3-dev'
SIMBODY_DEPS='cmake-qt-gui liblapack-dev freeglut3-dev libxi-dev libxmu-dev doxygen'

# URLs
SWIG_TWO='https://downloads.sourceforge.net/project/swig/swig/swig-2.0.10/swig-2.0.10.tar.gz?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fswig%2Ffiles%2Fswig%2Fswig-2.0.10%2F'
OPENSIM_URL='https://hashhar.github.io/temp/opensim-simbody-latest.tar.gz'

# Packages
SWIG_SRC_PKG="$TMP_ROOT/swig.tar.gz"
SWIG_SRC="$TMP_ROOT/swig-2.0.10"

OPENSIM_SIMBODY_SRC_PKG="$TMP_ROOT/opensim-simbody-latest.tar.gz"
OPENSIM_SRC="$TMP_ROOT/opensim-src"
SIMBODY_SRC="$TMP_ROOT/simbody-src"

# Build Trees
SIMBODY_BUILD="$TMP_ROOT/simbody-build"
OPENSIM_BUILD="$TMP_ROOT/opensim-build"

# Installtion Prefixes
SIMBODY_INSTALL="$HOME/simbody"
OPENSIM_INSTALL="$HOME/opensim"
# }}}

# Setup {{{
# Only works with Python2.
sudo apt install -y $PYTHON_PACKAGES wget

mkdir $TMP_ROOT
# }}}

# Swig 2.0.10 {{{
wget $SWIG_TWO -O $SWIG_SRC_PKG \
	&& tar -zxvf $SWIG_SRC_PKG -C $TMP_ROOT \
	&& cd $SWIG_SRC

# Check dependencies
sudo apt install -y $SWIG_DEPS

# Remove swig if already installed.
swig -version | grep -q "2.0.10"
if [ $? -ne 0 ]; then
	sudo apt purge -y --autoremove swig
fi

# Compile and install
./configure \
	&& make \
	&& sudo make install
# }}}

# Simbody and OpenSim source package {{{
wget $OPENSIM_URL -O $OPENSIM_SIMBODY_SRC_PKG \
	&& tar -zxvf $OPENSIM_SIMBODY_SRC_PKG -C $TMP_ROOT
# }}}

# Simbody {{{
sudo apt install -y $SIMBODY_DEPS
mkdir $SIMBODY_BUILD \
	&& cd $SIMBODY_BUILD
cmake $SIMBODY_SRC -DCMAKE_INSTALL_PREFIX=$SIMBODY_INSTALL -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_VISUALIZER=on

make doxygen \
	&& make -j4 \
	&& make -j4 install

echo "export SIMBODY_HOME=$SIMBODY_INSTALL" >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$SIMBODY_HOME/lib' >> ~/.bashrc
. ~/.bashrc
# }}}

# OpenSim {{{
mkdir $OPENSIM_BUILD \
	&& cd $OPENSIM_BUILD
cmake $OPENSIM_SRC -DCMAKE_INSTALL_PREFIX=$OPENSIM_INSTALL -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_PYTHON_WRAPPING=on -DCMAKE_PREFIX_PATH=$SIMBODY_INSTALL

make -j4 \
	&& make -j4 install

echo "export OPENSIM_HOME=$OPENSIM_INSTALL" >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$OPENSIM_HOME/lib' >> ~/.bashrc

. ~/.bashrc

cd $OPENSIM_INSTALL/sdk/python \
	&& sudo python setup.py install \
	&& sudo pip install ipython

. ~/.bashrc
# }}}
