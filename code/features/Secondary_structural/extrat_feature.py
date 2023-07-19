import numpy as np
import os,sys
import shutil
import pandas as pd


def readspot(filename):
  #pssm_name=pdbid+'_SNBPSSM.csv'
  data = pd.read_csv(filename,header=None)
  data=np.array(data)
  #print(data.shape)
  return data


  
  
def judge_residue(pdbCA_name,pdbid,residnum,wild):
    dit = {'GLY':'G','ALA':'A','VAL':'V','LEU':'L',
      'ILE':'I','SER':'S','THR':'T','PRO':'P',
        'ASP':'D','ASN':'N','GLU':'E','GLN':'Q',
          'LYS':'K','ARG':'R','CYS':'C','MET':'M',
            'HIS':'H','TRP':'W','PHE':'F','TYR':'Y'}
    pdb_format = '17s3s2s4s55s'  
    w = []
    data_name=pdbCA_name
    for line in open(data_name):
        line=line.strip('\n').split(',')
        num=line[0]
        #chain=line[1]
        resid_num=line[2]
        wild_name=line[3]
        
        if resid_num == residnum and dit[wild_name] == wild:
           w.append(residnum)
           a=int(num)
        else:
          continue
    if len(w):
      return a
    else:
      return 0  
      
def input_para():
    pdbid =sys.argv[1]
    type_ =sys.argv[2]
    
    return pdbid,type_

def main():

    pdbid,type_pdb=input_para()
    
    data_name=pdbid+'.csv'
    workdir= './results/'
    nofile=[]
    wrong=[]
    spot_feature=np.zeros([1, 19])
    
    for line in open(data_name):
       feature_spot=np.zeros([1, 19])
       line=line.strip('\n').split(',')
       pdbid=line[0]
       #chain=line[1]
       residnum=line[2]
       wildname=line[3]
       mutname=line[4]
       residue_type = pdbid+'_'+residnum+'_'+wildname+'_'+mutname
       alpha_pdb=workdir+pdbid+'.csv'
       mutation_pdb=workdir+residue_type+'_mut.csv'
       pdbCA_name1='../Gen_seq/pdb_CA/'+pdbid + '_CA.txt'
       pdbCA_name2='../Gen_seq/pdb_CA/'+residue_type + '_mut_CA.txt'
       
       if type_pdb == "w":
          if os.path.exists(alpha_pdb):
            spot=readspot(alpha_pdb)
            num=judge_residue(pdbCA_name1,pdbid,residnum,wildname)
            if num != -1 and spot[num][1]==wildname:
               feature_spot=spot[num]
               feature_spot=feature_spot[4:].reshape(1,19)
               spot_feature=np.concatenate((spot_feature,feature_spot),axis=0)

            else:
                wrong.append(residue_type)
          else:
            nofile.append(alpha_pdb)
       #mut # 1iob_CA.txt,1bni_CA.txt and 5pti_CA.txt file replacement when calculating mutations
       else:
          if os.path.exists(mutation_pdb):
            spot=readspot(mutation_pdb)
            num=judge_residue(pdbCA_name2,pdbid,residnum,mutname)
            if num != -1 and spot[num][1]==mutname:
               feature_spot=spot[num]
               feature_spot=feature_spot[4:].reshape(1,19)
               spot_feature=np.concatenate((spot_feature,feature_spot),axis=0)

            else:
                wrong.append(residue_type)
          else:
            nofile.append(mutation_pdb)
         
    Spot_name= 'Spot_'+type_pdb
    print(Spot_name)
    Spot=np.delete(spot_feature,0,axis=0)
    print(Spot.shape)
    
    np.save(Spot_name+".npy", Spot)
    return print('no exists file in pdbfile:',nofile)
    
if __name__ == '__main__':
  main()

   