# !/bin/bash

# Input: ./run_pssm.sh $pdbid 
mkdir ASN

cp ../../example/$1.asn ./ASN
cp ../../example/$1X.pdb ../PSSM
cp ../../example/$1.csv ../PSSM
python pssmviewer.py 
cp ../../example/$1X.pdb ../PSSM/PSSM
cp Single_SNB_PSSM.py ./PSSM
cp clash.m ./PSSM
cp map_pssm.py ./PSSM
cp cut_map_pssm.py ./PSSM
cd PSSM
python Single_SNB_PSSM.py $1
python map_pssm.py $1
python cut_map_pssm.py $1
#cp *_cut.csv ../../PSSM
#cp *.txt ../../PSSM
mv *.npy ../../PSSM
cd ..


