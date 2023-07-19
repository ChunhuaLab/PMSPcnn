import os,sys
import shutil
import numpy as np

def int_para():
    data_name=sys.argv[1]
    cutoff=sys.argv[2]
    return data_name,cutoff
    
def file_extrat(file_name,outpath):
    file_path='mutation_PH/'+file_name
    if os.path.exists(file_path):
         pri_cnn='./'+file_path+'/X_h0.npy'
         mv_cnn = './'+outpath+'/'+file_name+'_h0.npy'
         shutil.copyfile(pri_cnn,mv_cnn)
         pri_h12='./'+file_path+'/X_h12.npy'
         mv_h12 = './'+outpath+'/'+file_name+'_h12.npy'
         shutil.copyfile(pri_h12,mv_h12)
         
#         pri_cnn_R='./'+file_path+'/X_h0_R.npy'
#         mv_cnn_R = './'+outpath+'/'+file_name+'_h0_R.npy'
#         shutil.copyfile(pri_cnn_R,mv_cnn_R)
#         pri_h12_R='./'+file_path+'/X_h12_R.npy'
#         mv_h12_R = './'+outpath+'/'+file_name+'_h12_R.npy'
#         shutil.copyfile(pri_h12_R,mv_h12_R)
#         
    else:
         print('no file:',file_path)

def main():
    Feature_cnn=[]
    Feature_h12=[]
    Y_2646=[]
    wrong=[]
    data_name,cutoff=int_para()
   
    
    outdir='File_extract'
    os.system('mkdir '+outdir)
    
    for line in open(data_name):
         line=line.strip('\n').split(',')
         pdbid=line[0]
         pdbid=pdbid[0:4]
         chain=line[1]
         resid=line[2]
         wildname=line[3]
         mutname=line[4]
         #ddg=line[5]
         file_name= pdbid+'_'+resid+'_'+wildname+'_'+mutname
         #print(file_name)
         #files of the same type are grouped together
         file_extrat(file_name,outdir)
    
if __name__ == '__main__':
  main()

   