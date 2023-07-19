# !/bin/bash
# 
# ./run_topology.sh $pdbid 


# <path> needs to be changed to your own path.

cutoff=12
Bin=1.0

# Input

pdbname=$1X.pdb
csv_name=$1.csv

rm -r pdbfile
mkdir pdbfile
mkdir Results
cp ../../example/$pdbname ./pdbfile
cp ../../example/$csv_name ../Topology


#1.fix 
for file in `ls pdbfile`
  do
    python fix.py $file
  done

#2. mutation
python mutation.py $cutoff $csv_name

#3.cloud
python gen_pointclouds.py $csv_name

#4.jplex
mkdir mutation_PH
mv ./pdbfile/mutation_PH  ../Topology/

cd mutation_PH
for dir in `ls /home/sunxiaohan/data/PMPCNN/code/features/Topology/mutation_PH`
  do
    cp ../Construct_jplex_mutation.m $dir
    cp ../java.opts $dir
    cp ../Construct_Feature_tda.py $dir
    cp ../PH_Alpha.R $dir
    cp ../gen_feature_h0.py $dir
    cp ../gen_feature_h12.py $dir
    cd $dir
    echo "begin compute" $dir
    matlab -nodisplay -r "run Construct_jplex_mutation.m"
    python Construct_Feature_tda.py 
    python gen_feature_h0.py $cutoff $Bin
    python gen_feature_h12.py 
    #cp *.npy  ../../Results
    cd ..
    
  done
cd ..

python Integration_file.py $csv_name $cutoff
python Feature_contact.py $csv_name $cutoff $Bin

cp ./pdbfile/$1.pdb ../Gen_seq
cp ./pdbfile/*mut.pdb ../Gen_seq