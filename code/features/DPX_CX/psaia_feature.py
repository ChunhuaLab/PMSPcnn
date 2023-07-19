#
import os
import sys 
import struct
import numpy as np

def input_para():
    pdbid = sys.argv[1]
    type_ = sys.argv[2]
    
    return pdbid,type_
    
def extrat_feature(type_pdbfile,pdbid,residnum,residname):
    dit = {'GLY':'G','ALA':'A','VAL':'V','LEU':'L',
      'ILE':'I','SER':'S','THR':'T','PRO':'P',
        'ASP':'D','ASN':'N','GLU':'E','GLN':'Q',
          'LYS':'K','ARG':'R','CYS':'C','MET':'M',
            'HIS':'H','TRP':'W','PHE':'F','TYR':'Y'}
    w=[]
    tbl=open(type_pdbfile, 'r')             
    tbl_content=tbl.read()                  
    tbl.close                               
    tbl_line=tbl_content.strip().split("\n")

    for i in range(14,len(tbl_line)):
        num = tbl_line[i][96:104].strip()
        name= tbl_line[i][105:115].strip()
            
        if num == residnum and dit[name] == residname:
            
            ave_DPX   = tbl_line[i][196:210].strip()
            s_DPX     = tbl_line[i][211:225].strip()
            s_ch_DPX  = tbl_line[i][226:241].strip()
            s_ch_s_DPX= tbl_line[i][242:261].strip()
            
            ave_CX    = tbl_line[i][292:306].strip()
            s_CX      = tbl_line[i][307:320].strip()
            s_ch_CX   = tbl_line[i][321:338].strip()
            s_ch_s_CX = tbl_line[i][339:353].strip()
            w.append(residnum)
        else:
          continue
    if len(w):
      feature=[ave_DPX,s_DPX,s_ch_DPX,s_ch_s_DPX,ave_CX,s_CX,s_ch_CX,s_ch_s_CX]
      feature=np.array(feature).reshape([1,8])
      return feature
    else:
      return 0
    #filename.close()


def integrate_psaia(filename,mut_type):
 
    return wrong,nofile,psaia

    
    
    
def main():

    pdbid,type_pdb=input_para()
    data_name=pdbid+'.csv'
    
    psaia=np.zeros([1, 8])
    nofile=[]
    wrong=[]
    
    for line in open(data_name):
       line=line.strip('\n').split(',')
       pdbid=line[0]
       #chain=line[1]
       residnum=line[2]
       wildname=line[3]
       mutname=line[4]
       residue_type = pdbid+'_'+residnum+'_'+wildname+'_'+mutname
       alpha_pdb='./psaia/'+pdbid+'_202302132159_unbound.tbl'
       mutation_pdb='./psaia/'+pdbid+'_'+residnum+'_'+wildname+'_'+mutname+'_mut_202302132159_unbound.tbl'
       
       #wild
      
       if type_pdb == "w":
          if os.path.exists(alpha_pdb):
            feature_w = extrat_feature(alpha_pdb,pdbid,residnum,wildname)
            if len(feature_w) > 0:
                psaia=np.concatenate((psaia,feature_w),axis=0)
            else:
                wrong.append(residue_type)
          else:
            nofile.append(alpha_pdb)
       #mut
       else:
          if os.path.exists( mutation_pdb):
            feature_m = extrat_feature( mutation_pdb,pdbid,residnum,mutname)
            if len(feature_m) > 0:
                psaia=np.concatenate((psaia,feature_m),axis=0)
            else:
                wrong.append(residue_type)
          else:
            nofile.append( mutation_pdb)
         
    psaia_name= 'psaia_'+type_pdb
    
    psaia=np.delete(psaia,0,axis=0)
    print(psaia.shape)
    
    np.save(psaia_name+".npy", psaia)
    #np.savetxt(psaia_name+".csv", psaia,delimiter=",",fmt='%s')
    return print('no exists file in pdbfile:',nofile)


    
if __name__ == '__main__':
  main()
  
  
