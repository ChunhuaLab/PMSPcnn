# !/bin/bash

# Input: ./run_seq.sh $pdbid 


pdbid=$1


mkdir pdb_CA
mkdir fasta
workdir='pdb_CA'
cp *.pdb $workdir


for file in `ls ./$workdir`
  do
    python gen_CA.py $file $workdir $pdbid
  done
mv ./pdb_CA/*.fasta ./fasta

rm *.pdb