import sys,os
import numpy as np
import pandas as pd

def standardization(data,name):
    mean = np.load('../model/'+name+'_mean.npy')
    std = np.load('../model/'+name+'_std.npy')
    data_nor= (data - mean) / std
#    np.save(name+'_mean.npy',mean)
#    np.save(name+'_std.npy',std)
    return data_nor

def main():
    
    
    
    index_path='../index/'
    Idx = np.load(index_path+"/index.npy")
    cut = Idx[:300]
    #print('cut',cut)
    idx = cut.ravel()

    X = np.load('./Topology/Results/X_h0.npy')
    x_h0 = X[:, idx]
    #pssm = np.load('./pssm/PSSM.npy',allow_pickle=True)
    x_h12 = np.load('./Topology/Results/X_h12.npy')
    pssm= np.load('./PSSM/PSSM_direct.npy')
    pssm_cut= np.load('./PSSM/PSSM_cut_direct.npy')
    phy_che = np.load('./Physicochemical_characteristics/AA_direct.npy')
    dpx_cx = np.load('./DPX_CX/psaia_direct.npy')
    spot= np.load('./Secondary_structural/Spot_rever.npy')
    X_aux = np.concatenate((pssm,pssm_cut,phy_che,dpx_cx,spot), axis=1)
    #X_aux_R = np.concatenate((pssm_R,pssm_cut_R,phy_che_R,dpx_cx_R,spot_R), axis=1)
    #print('X_aux.shape', X_aux.shape)
    
    X_aux_nor=standardization(X_aux,'X_aux')
    #X_aux_R_nor=standardization(X_aux_R,'X_aux_R')
    
    X_all_nor=np.concatenate((x_h0,x_h12,X_aux_nor), axis=1)
    

    np.save('X_test_nor.npy', X_all_nor)
    
    
main()

