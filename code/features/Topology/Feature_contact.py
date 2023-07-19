import os,sys
import shutil
import numpy as np

def int_para():
    data_name=sys.argv[1]
    cutoff=sys.argv[2]
    Bin = sys.argv[3]
    return data_name,cutoff, float(Bin)

def main():
    
    data_name,cutoff,Bin=int_para()
    max_bin=int(float(cutoff)/Bin)
    Feature_cnn=np.zeros([max_bin, 54]).reshape(1,max_bin,54)
    Feature_h12=np.zeros([1, 378])
    
    Feature_cnn_R=np.zeros([max_bin, 54]).reshape(1,max_bin,54)
    Feature_h12_R=np.zeros([1, 378])
    
    wrong=[]
   
    
    workdir= './File_extract'
    outdir='./Results'
    os.system('mkdir '+outdir)
    
    for line in open(data_name):
         line=line.strip('\n').split(',')
         pdbid=line[0]
         pdbid=pdbid[0:4]
         chain=line[1]
         resid=line[2]
         wildname=line[3]
         mutname=line[4]
         
         file_name= pdbid+'_'+resid+'_'+wildname+'_'+mutname
         #print(file_name)
         file_cnn =workdir+'/'+file_name+'_h0.npy'
         file_h12 = workdir+'/'+file_name+'_h12.npy'
#         
#         file_cnn_R =workdir+'/'+file_name+'_h0_R.npy'
#         file_h12_R = workdir+'/'+file_name+'_h12_R.npy'
#         X_h12=np.load(file_h12)
         if os.path.exists(file_cnn_R) and os.path.exists(file_h12_R):
             X_cnn=np.load(file_cnn)
             X_cnn = np.reshape(X_cnn,(1,max_bin,54))
             X_h12=np.load(file_h12)
             X_h12 = np.reshape(X_h12,(1,-1))
             Feature_cnn=np.concatenate((Feature_cnn,X_cnn),axis=0)
             Feature_h12=np.concatenate((Feature_h12,X_h12),axis=0)
             
#             X_cnn_R=np.load(file_cnn_R)
#             X_cnn_R = np.reshape(X_cnn_R,(1,max_bin,54))
#             X_h12_R=np.load(file_h12_R)
#             X_h12_R = np.reshape(X_h12_R,(1,-1))
#             Feature_cnn_R=np.concatenate((Feature_cnn_R,X_cnn_R),axis=0)
#             Feature_h12_R=np.concatenate((Feature_h12_R,X_h12_R),axis=0)
             
             
             
         else:
              wrong.append(file_cnn)
              #print(file_cnn)
   # delete zeros([48, 54])
    Feature_cnn=np.delete(Feature_cnn,0,axis=0)
    Feature_h12=np.delete(Feature_h12,0,axis=0)
    x_h0=Feature_cnn.reshape([len(Feature_cnn),12*54])
    np.save(outdir+'/X_h0.npy',x_h0)
    np.save(outdir+"/X_h12.npy", Feature_h12)
   

    
    return print('wrong filname:',wrong)
    
    
if __name__ == '__main__':
  main()

   