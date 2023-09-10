# PMSPcnn: Predicting protein stability changes upon single point mutations with convolutional neural network.

PMSPcnn is an effective and unbiased predictor of protein stability changes ΔΔG caused by single point mutations.

Authors: Xiaohan Sun, Shuang Yang, Zhixiang Wu, Jingjie Su, Fangrui Hu, Fubin Chang, Chunhua Li. 

The performance process includes three steps: installation, feature extraction and prediction.

Here, taking a protein with PDB ID 1lni for example to show the prediction process, whose A chain residue mutation N39D causes protein stability change ΔΔG = 1.5 kcal/mol. In the following description, the input and output file names will contain “1lni_A_39_N_D”.  

## Step 1 Installation
* Matlab version: R2021a 
* VMD version: 1.9.3
* Python version: 3.8
  pip install scikit-learn ==1.0.1; pip install keras == 2.7.0; pip install numpy == 1.18.5; pip install scipy == 1.4.1
* R-tda package
  install.packages(pkgs = "TDA")
* SPOT_1D_LM
  Go to  https://github.com/jas-preet/SPOT-1D-LM.git download and install the program SPOT_1D_LM in "Secondary_structural".
* Psaia.exe 
  Go to the Website：https://sourceforge.net/projects/psaia/ to download and install the program psaia.exe.


## Step 2 Feature extraction

### Topology characteristics

This step requires two files: 1lniX.pdb and 1lni.csv.
* 1lniX.pdb is the predicted structure of 1lni constructed by Alphafold2.
* The content of 1lni.csv includes pdbid, chain, residue number, wildname and mutname. 
Run the following command:

```{bash}
./PMSPcnn/code/features/Topology/run_topology.sh 1lni
```
  
### Generating sequence

Extract the mutant sequence from the generated structure.
Run the following command: 

```{bash}
./PMSPcnn/code/features/Gen_seq/run_seq.sh 1lni
```

### PSSM and SNB_PSSM

Go to the website https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome to get a pssm file named 1lni.asn.

Run the following command: 

```{bash}
./PMSPcnn/code/features/PSSM/run_pssm.sh 1lni
```
  
### Secondary_structural

Run the following commands:

```{bash}
conda activate spot_1d_lm

./PMSPcnn/code/features/Secondary_structural/run_secondary_structural.sh

conda deactivate
```

### DPX and CX

Go to the Website：https://sourceforge.net/projects/psaia/ to download and install the program psaia.exe.
* Run “psaia.exe”.
* Step by step, selecet "Structure Analyser", then under it select "Analysis Type" and then select "Analyse by Chain". All parameters are set to default.  
* Input the pdb file 1lni.pdb,1lni_39_N_D_mut.pdb (files in PMSPcnn/code/features/Topology/pdbfile) to the program.
* Click “run” to get the result, i.e.,1lni.tbl and 1lni_39_N_D_mut.tbl.
Run the following command:

```{bash}
./PMSPcnn/code/features/DPX_CX/run_dpx_cx.sh 1lni
```

### Physicochemical_characteristics

AA index is from the website: https://www.genome.jp/aaindex/.
Run the following command:

```{bash}
./PMSPcnn/code/features/DPX_CX/run_phy_cha.sh 1lni
```
The output file is "AA_direct.npy".

### Feature integration

After all features are extracted, all the feature files obtained. 
Run the following command: 

```{bash}
python ./PMSPcnn/code/features/feature_integrate.py
```

## Step 3 Prediction
Run the following command:

```{bash}
python ./PMSPcnn/predict.py
```
The finally output is shown in  "./result/predcit_value.txt".

The predicted value of 1lni_39_N_L is 1.52755897 kcal/mol.

If you want to predict more stability changes caused by mutations, construct a file like 1lni.csv with multiple lines describing the mutation information (PDB ID, chain, mutation residue number, residue type before mutation, residue type after mutation), and then perform the same process.


## Help

For any questions, please contact us by xiaohansun@emails.bjut.edu.cn.



## References
* Singh J, Paliwal K, Litfin T et al. Reaching alignment-profile-based accuracy in predicting protein secondary and tertiary structural properties without alignment, Sci Rep 2022;12:7607.
* Humphrey W, Dalke A, Schulten K. VMD: visual molecular dynamics, J Mol Graph 1996;14:33-38, 27-28.
* Liu Y, Gong W, Yang Z et al. SNB-PSSM: A spatial neighbor-based PSSM used for protein-RNA binding site prediction, JOURNAL OF MOLECULAR RECOGNITION 2021;34:e2887.
* Cheng CW, Su EC, Hwang JK et al. Predicting RNA-binding sites of proteins using support vector machines and evolutionary information, BMC BIOINFORMATICS 2008;9 Suppl 12:S6.
* Liu Y, Gong W, Zhao Y et al. aPRBind: protein-RNA interface prediction by combining sequence and I-TASSER model-based structural features learned with convolutional neural networks, BIOINFORMATICS 2021;37:937-942.
* Kawashima S, Pokarowski P, Pokarowska M et al. AAindex: amino acid index database, progress report 2008, NUCLEIC ACIDS RESEARCH 2008;36:D202-D205.
