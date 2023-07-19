# PMSPcnn: Predicting changes of single point missense mutations on protein stability based on convolutional neural network.
PMSPcnn is a quite exceptional unbiased predictor predictor of ΔΔG for single-point mutations.

Authors: Xiaohan Sun, Shuang Yang, Zhixiang Wu, Jingjie Su, Fangrui Hu, Fubin Chang, Chunhua Li*. 


The performance process includes three steps: install, feature extraction and prediction.
## Installation
* Matlab version: R2021a 
* VMD version: 1.9.3
* Python version: 3.8
* For python package: pip install scikit-learn ==1.0.1;pip install keras == 2.7.0;pip install numpy == 1.18.5;pip install scipy == 1.4.1.
* For R-tda package:
  install.packages(pkgs = "TDA")
* Install SPOT_1D_LM
Go to  https://github.com/jas-preet/SPOT-1D-LM.git download and install the program SPOT_1D_LM in "Secondary_structural"
* Install psaia.exe 
Go to the Website£ºhttps://sourceforge.net/projects/psaia/ to download and install the program psaia.exe.

The 1lni A 39 N D as the following example. Its experimental ddg value is 1.5 kcal/mol.
## Feature extraction

### Topology characteristics
This step requires two files:1lniX.pdb and 1lni.csv.
1lniX.pdb is the 3D structure of 1lni constructed by Alphafold2.
The content of 1lni.csv includes pdbid, chain, residue, wildname mutname. 
Run the following commands:
```{bash}
cd PMSPcnn/code/features/Topology/ 
./run_topology.sh 1lni
```
The output files are "X_h0.np" and "X_h12.npy" shown in "./Results".
  
### Generating sequence
Extract the mutant sequence from the generated structure.
Run the following commands: 
```{bash}
cd PMSPcnn/code/features/Gen_seq/"
./run_seq.sh 1lni
```
The output files "1lni.fasta" and "1lni_39_N_D_mut.fasta" in "./fasta".
The output files "1lni_CA.txt" and "1lni_39_N_L_mut_CA.txt" in "./pdb_CA","fasta_test.txt".

### PSSM and SNB_PSSM
Go to the website https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome to get a pssm file named 1lni.asn.
Here, select "PSI-BLAST" for "Program Selection" item, and use default parameters for other items.
Then "1lni.asn" is then placed in the "./PMSPcnn/code/features/PSSM/ASN".
Run the following commands: 
```{bash}
cd PMSPcnn/code/features/PSSM/
./run_pssm.sh 1lni
```
The output files are "PSSM_direct.npy" and "PSSM_cut_direct.npy".
  
### Secondary_structural
Enter the previously built environment:spot_1d_lm.
Run the following commands:
```{bash}
conda activate spot_1d_lm
cd PMSPcnn/code/features/Secondary_structural
./run_secondary_structural.sh
conda deactivate
```
The output file is "Spot_direct.npy".

### DPX and CX
Go to the Website：https://sourceforge.net/projects/psaia/ to download and install the program psaia.exe.
* Run “psaia.exe”;
* Step by step, selecet "Structure Analyser", then under it select "Analysis Type" and then select "Analyse by Chain". All parameters are set to default.
* Input the pdb file 1lni.pdb,1lni_39_N_D_mut.pdb (files in PMSPcnn/code/features/Topology/pdbfile) to the program
* Click “run” to get the result, i.e.,1lni.tbl and 1lni_39_N_D_mut.tbl.
* Then put the output files into "PMSPcnn/code/features/DPX_CX/psaia". Run the following commands:
```{bash}
cd PMSPcnn/code/features/DPX_CX
./run_dpx_cx.sh 1lni
```
The output file is "psaia_direct.npy".

### Physicochemical_characteristics
AA index is from the website: https://www.genome.jp/aaindex/.
Run the following commands:
```{bash}
cd PMSPcnn/code/features/DPX_CX
./run_phy_cha.sh 1lni
```
Then you can obtain a file called "AA_direct.npy".

## Feature integration
After all features are extracted, all the feature files obtained. 
Run the following command: 
```{bash}
python feature_integrate.py
```
Then obtained "X_test_nor.npy" file.

## Prediction
Run the following command:
```{bash}
python predict.py
```
Then the finally output shown in  "./result/predcit_value.txt".
The predicted value of 1lni_39_N_L is 1.52755897
If you want to predict several mutations, add them to the pdbid.csv file.

## Help
For any questions, please contact us by chunhuali@bjut.edu.cn.





## References
* Singh J, Paliwal K, Litfin T et al. Reaching alignment-profile-based accuracy in predicting protein secondary and tertiary structural properties without alignment, Sci Rep 2022;12:7607.
* Humphrey W, Dalke A, Schulten K. VMD: visual molecular dynamics, J Mol Graph 1996;14:33-38, 27-28.
* Liu Y, Gong W, Yang Z et al. SNB-PSSM: A spatial neighbor-based PSSM used for protein-RNA binding site prediction, JOURNAL OF MOLECULAR RECOGNITION 2021;34:e2887.
* Cheng CW, Su EC, Hwang JK et al. Predicting RNA-binding sites of proteins using support vector machines and evolutionary information, BMC BIOINFORMATICS 2008;9 Suppl 12:S6.
* Liu Y, Gong W, Zhao Y et al. aPRBind: protein-RNA interface prediction by combining sequence and I-TASSER model-based structural features learned with convolutional neural networks, BIOINFORMATICS 2021;37:937-942.
* Kawashima S, Pokarowski P, Pokarowska M et al. AAindex: amino acid index database, progress report 2008, NUCLEIC ACIDS RESEARCH 2008;36:D202-D205.
