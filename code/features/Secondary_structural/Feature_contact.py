import os,sys
import shutil
import numpy as np



def main():
    #W=np.zeros([])
    
    Spot_w      =np.load('Spot_w.npy',allow_pickle=True)
    Spot_w =Spot_w.astype('float')
    Spot_m      =np.load('Spot_m.npy',allow_pickle=True)
    Spot_m =Spot_m.astype('float')
    Spot_diff   = Spot_w-Spot_m
    Spot_direct =np.concatenate((Spot_w,Spot_m,Spot_diff),axis=1)
   
    np.save("Spot_direct.npy", Spot_direct)
    
    #np.save("Spot_all.npy", Spot_feature)
    os.system('rm Spot_w.npy')
    os.system('rm Spot_m.npy')
if __name__ == '__main__':
  main()

   