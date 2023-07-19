#!/bin/bash

# setting up path for vmd-1,9,3
cd ../data/software/vmd-1.9.3/
./configure

cd src
make install
chmod 077 /usr/local/lib/vmd/vmd_LINUXAMD64



