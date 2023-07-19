# !/bin/bash

# ./run_phy_cha.sh $pdbid

pdbid=$1
csv_name=$1.csv

cp ../../example/$csv_name ../Physicochemical_characteristics

python Physicochemical_characteristics.py $pdbid 
