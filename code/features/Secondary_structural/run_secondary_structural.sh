# !/bin/bash

# Input: ./run_secondary_structural.sh  $pdbid

pdbid=$1
csv_name=$1.csv
cp ../../code/example/$csv_name ../Secondary_structural
mkdir inputs
mkdir results
cp PMPCNN/code/features/Gen_seq/fasta_test.txt ../PMPCNN/code/softwares/SPOT-1D-LM/file_lists
cp PMPCNN/code/features/Gen_seq/fasta/*.fasta ../PMPCNN/code/softwares/SPOT-1D-LM/inputs
cd SPOT-1D-LM
bash run_SPOT-1D-LM.sh file_lists/fasta_test.txt cpu cpu cpu
mv results ../Secondary_structural
cd ..
python extrat_feature.py $pdbid w
python extrat_feature.py $pdbid m
python Feature_contact.py

