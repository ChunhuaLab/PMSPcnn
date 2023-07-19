import numpy as np
import os,sys
import shutil

#PSSM features
def input_para():
    pdbid = sys.argv[1]
    return pdbid
    
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
    
    

def read_file(filename):
  data=[]
  files=open(filename)
  for line in files.readlines():
     line=line.strip('\n').split(',')
     data.append(line)
  files.close()
  return data


def main():
    
    
#    dit={1:'C',2:'D',3:'E',4:'F',5:'G',6:'H',7:'I',8:'K',9:'L',10:'M', \
#         11:'N',12:'P',13:'Q',14:'R',15:'S',16:'T',17:'V',18:'W',19:'A' ,20:'Y'}
    dit={'C':1,'D':2,'E':3,'F':4,'G':5,'H':6,'I':7,'K':8,'L':9,'M':10, \
         'N':11,'P':12,'Q':13,'R':14,'S':15,'T':16,'V':17,'W':18,'A':19 ,'Y':20}
    nofile=[]
    wrong=[]
    
    #data_name='test.csv'
    #data_name='p53_myoglobin.csv'
    pdbid=input_para()
    data_name=pdbid+'.csv'
    #workdir= './PSSM/'
    os.system('cp ../../../example/'+data_name+' ../PSSM')  
    
    #cutoff=12
    nofile=[]
    pssm_wrong=[]
    pdb_wrong=[]
    
    PSSM=np.zeros([1, 3])
    for line in open(data_name):
       feature_pssm=np.zeros([1, 3])
       line=line.strip('\n').split(',')
       pdbid=line[0]
       #chain=line[1]
       residnum=line[2]
       wildname=line[3]
       mutname=line[4]
       pssmfile=pdbid + '_cut.csv'
       pdbCA_name='../../Gen_seq/pdb_CA/'+pdbid + '_CA.txt'
       if os.path.exists(pssmfile) and os.path.exists(pdbCA_name):
         pssm=read_file(pssmfile)
         
         num=judge_residue(pdbCA_name,pdbid,residnum,wildname)
#         print('num',num,pdbid)
#         print(pssm[num-1][1])
#         print('dit',dit[mutname]+1)
         if num != 0 and pssm[num-1][1]==wildname:

           feature_pssm[0,0]=pssm[num-1][dit[wildname]+1]
           feature_pssm[0,1]=pssm[num-1][dit[mutname]+1]
           feature_pssm[0,2]=feature_pssm[0,0]-feature_pssm[0,1]
#           print(feature_pssm)
           
           PSSM=np.concatenate((PSSM,feature_pssm),axis=0)
           
         else:
            pdb_wrong.append(pdbid+'_'+residnum+'_'+wildname)
       
       else:
         nofile.append(pdbCA_name)
         
    PSSM=np.delete(PSSM,0,axis=0)
    np.save("PSSM_cut_direct.npy", PSSM)
  
    #np.savetxt("PSSM_cut.csv", PSSM_all,delimiter=",",fmt='%f')
   

    return print('wrong residue or wild in pdb:',pdb_wrong)
    
    data_name.close() 
    
if __name__ == '__main__':
  main()

   