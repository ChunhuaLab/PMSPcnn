# outfile ./fix
import os
import sys
import struct 
import numpy as np
import pandas as pd
# fix pdb structure
from pandas.core.frame import DataFrame


def input_para():
    pdbname = sys.argv[1]
    workdir=sys.argv[2]
    pdbid = sys.argv[3]
    return pdbname,workdir,pdbid
 
# only extrat atom    
def modifypdb(name1,name2):
        pdbname = open(name1)
        outfile = open(name2,"w")
        lines = pdbname.read().splitlines()
        PRO = []
        for line in lines:
            if line[0:4] == 'ATOM':
                 outfile.write(line+'\n')
        outfile.close()
#only extrat CA for a residue
def readpdb(name,workdir):
    file_name=workdir + '/'+name
    pdbname = open(file_name)
    lines = pdbname.read().splitlines()
    PRO = []
    n=0
    for i in range(0,len(lines)):
        line = lines[i]
        if line[0:4] == 'ATOM':
            AtomType = line[13:15]
            wild_name=line[17:20]
            chain = line[21:22]
            resid_num = line[22:26]
            if AtomType == 'CA':
                n=n+1
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                PRO.append([n,chain,resid_num.strip(),wild_name,AtomType,x,y,z])
                continue
            else:
                continue
        else:
            continue 
    
    outname='./'+workdir+'/'+name[0:len(name)-4]+'_CA.txt'
    np.savetxt(outname,PRO,delimiter=',',fmt ='%s')
    return PRO


def main():
    dit = {'GLY':'G','ALA':'A','VAL':'V','LEU':'L',
      'ILE':'I','SER':'S','THR':'T','PRO':'P',
        'ASP':'D','ASN':'N','GLU':'E','GLN':'Q',
          'LYS':'K','ARG':'R','CYS':'C','MET':'M',
            'HIS':'H','TRP':'W','PHE':'F','TYR':'Y'}
    pdbname,workdir,pdbid =input_para()
    print('begin compute : '+pdbname)
    file_pdb=workdir + '/'+pdbname
    
    pdb_CA=readpdb(pdbname,workdir)
    #print(pdb_CA.shape)
    CA_file=DataFrame(pdb_CA)
    sequence=CA_file[0:][3]
    
    a=[]
    for x in sequence:
       m=dit[x]
       a.append(m)
    sequence=np.transpose(a)
    
    seq= ''.join(sequence)
    #spot
    with open(file_pdb[:-4]+'.fasta',"w") as filename:
       filename.write( '>'+pdbname[:-4]+'\n')
       filename.write( seq )
    filename.close()
    
    #spot
    with open("fasta_test.txt","a") as filename1:
       filename1.write( 'inputs/'+pdbname[:-4]+".fasta"+'\n')
    filename1.close()
    #psaia
#    psaia_workdir='H:\Feature\psaia\pdbfile\\'
#    with open(pdbid+'.fls',"a") as filename2:
#          filename2.write( psaia_workdir+pdbname+'\n')
#    filename2.close()
    
if __name__ == "__main__":
    main()
