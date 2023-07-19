# outfile ./fix
import os
import sys 


def input_para():
    pdbid = sys.argv[1]
    return pdbid

pdbname=input_para()
nofile=[]

filename=pdbname+'X.pdb'
if os.path.exists(filename):
    print('Begin compute cut pssm...'+pdbname)
    line1='matlab -nodisplay -r "pdbid=' + "'"+pdbname+"'"+'; clash"'
    os.system(line1)
    
else:
    nofile.append(filename)
