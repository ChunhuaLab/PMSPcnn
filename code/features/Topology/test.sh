# !/bin/bash
# 
# ./run_topology.sh $pdbid $chain $residuse $wildname $mutname


# <path> needs to be changed to your own path.



# Input
cutoff=12
Bin=1.0
# Input

pdbname=$1X.pdb
csv_name=$1.csv


#4.jplex

cd mutation_PH
for dir in `ls /home/sunxiaohan/data/PMPCNN/code/features/Topology/mutation_PH`
  do
    cp ../gen_feature_h0_reverse.py $dir
    cd $dir
    echo "begin compute" $dir
   
    python gen_feature_h0_reverse.py $cutoff $Bin
    
    cd ..
    
  done
cd ..

#cp ./pdbfile/$1.pdb ../Gen_seq
#cp ./pdbfile/*mut.pdb ../Gen_seq

#rm -r mutation_PH