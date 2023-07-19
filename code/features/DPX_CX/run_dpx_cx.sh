# !/bin/bash

# Input: ./run_dpx_cx.sh  $pdbid

pdbid=$1
csv_name=$1.csv

cp ../../example/$csv_name ../DPX_CX
#mkdir psaia

python psaia_feature.py $pdbid w
python psaia_feature.py $pdbid m
python Feature_contact.py