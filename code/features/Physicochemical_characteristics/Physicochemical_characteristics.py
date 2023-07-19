import os 
import sys 
import struct
import numpy as np
import pandas as pd


def readfile(filename):
  #pssm_name=pdbid+'_SNBPSSM.csv'
  data = pd.read_csv(filename,header=None)
  data=np.array(data)
   
  #print(data.shape)
  return data

def input_para():

  pdbid=sys.argv[1]    
  
  return pdbid

def main():
   
    pdbid=input_para()
    data_name=pdbid+'.csv'
    AA_name='AA_data.csv'
    AA =readfile(AA_name)
    print(AA.shape)
    #cutoff=12
    AA_feature=np.zeros([1, 9*3])
    AA_W=np.zeros([1, 9])
    AA_M=np.zeros([1, 9])
    
    for line in open(data_name):
       line=line.strip('\n').split(',')
       #pdbid=line[0]
       #chain=line[1]
       #residnum=line[2]
       wildname=line[3]
       mutname=line[4]
       for i in range(1,21):
           if AA[i][0]==wildname:
#              print(AA[i][0])
#              print(AA[i,1:])
              AA_wild=AA[i,1:].reshape(1,9)
              AA_W=np.concatenate((AA_W,AA_wild),axis=0)
           if AA[i][0]==mutname:
              AA_mut =AA[i,1:].reshape(1,9)
              AA_M =np.concatenate((AA_M,AA_mut),axis=0)
           
     
    AA_W=np.delete(AA_W,0,axis=0)
    AA_M=np.delete(AA_M,0,axis=0)
    AA_W=np.asarray(AA_W, dtype = float)
    AA_M=np.asarray(AA_M, dtype = float)
    AA_D=AA_W-AA_M
    #print(AA_W) 
    #print(AA_W.shape,AA_M.shape)
    AA_direct=np.concatenate((AA_W,AA_M,AA_D),axis=1)
    np.save("AA_direct.npy", AA_direct)
   
if __name__ == '__main__':
  main()
