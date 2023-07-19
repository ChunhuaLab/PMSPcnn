import os
import sys 
import struct
import numpy as np

  
def input_para():
#    pdbid = sys.argv[1]
#    chainid = sys.argv[2]
#    resid = sys.argv[3]
#    wildname = sys.argv[4]
#    mutname = sys.argv[5]
    cutoff = sys.argv[1]
    data_name=sys.argv[2]
    return cutoff,data_name

   
def judge_residue(workpath,pdbid,chainid,resid,wild):
    dit = {'GLY':'G','ALA':'A','VAL':'V','LEU':'L',
      'ILE':'I','SER':'S','THR':'T','PRO':'P',
        'ASP':'D','ASN':'N','GLU':'E','GLN':'Q',
          'LYS':'K','ARG':'R','CYS':'C','MET':'M',
            'HIS':'H','TRP':'W','PHE':'F','TYR':'Y'}
    pdb_format = '17s3s2s4s49s'  
    w = []
    for line in open('./'+workpath+'/'+pdbid+'.pdb'):
        if line[0:4] == "ATOM":
          col = struct.unpack(pdb_format,line.encode())
          resid_num = col[3].decode("utf-8").strip()
          Chain = col[2].decode("utf-8").strip()
          wild_name = col[1].decode("utf-8")
          if resid_num == resid and dit[wild_name] == wild and Chain==chainid:
            w.append(resid)
          else:
            continue
    if len(w):
      return True
    else:
      return False
      
def Gen_mut(workdir,pdbid,chainid,resid,wildname,mutname):
    scapfile = open('./tmp_scap.list', 'w')
    scapfile.write(chainid+','+resid+','+mutname)
    scapfile.close()
    filename = workdir+'/'+ pdbid+'.pdb'
    mutfilename= pdbid[0:4]+'_'+resid+'_'+wildname+'_'+mutname+'_mut.pdb'
    #resultdir='Results'
    os.system('./scap -ini 20 -min 4 '+ filename +' ./tmp_scap.list')
    os.system('mv '+pdbid+'_scap.pdb '+ workdir+'/'+mutfilename)
    os.system('rm ./tmp_scap.list')
    return
    
def def_site(filepath,name,chainid,resid,cutoff,outfile):
    tclname = filepath +'/def_site.tcl'
    filename = filepath +'/'+ name +'.pdb'
    #b_name = name +'_b.pdb'
    m_name = outfile +'_m.pdb'
    tclfile = open(tclname,'w')
    tclfile.write("mol new {" + filename +"} type {pdb} first 0 last 0 step 1 waitfor 1\n")
#    tclfile.write('set prot [atomselect top "within '+ str(cutoff) + ' of chain '+chainid+'"]\n')
#    tclfile.write('$prot writepdb '+ b_name +'\n')
    tclfile.write('set prot2 [atomselect top "within '+ str(cutoff) + ' of resid '+resid+' and chain '+chainid+'"]\n')
    tclfile.write('$prot2 writepdb '+ m_name +'\n')
    tclfile.write('exit')
    tclfile.close()
    os.system('vmd -dispdev text -e '+ tclname)
    os.system('mv *.pdb '+ filepath)
    return    
    
def main():
    workdir = 'pdbfile'
    cutoff,data_name=input_para()
    #cutoff=12
    nofile=[]
    wrong=[]
    for line in open(data_name):
        line=line.strip('\n').split(',')
        pdbid=line[0]
        #pdbid=pdbid
        chain=line[1]
        resid=line[2]
        wildname=line[3]
        mutname=line[4]
        filename=workdir+'/'+pdbid+'.pdb'
        pri_filename = pdbid+'_'+resid+'_'+wildname+'_'+mutname
        mut_filename= pdbid+'_'+resid+'_'+wildname+'_'+mutname+'_mut'
        if os.path.exists(filename):
            if judge_residue(workdir,pdbid,chain,resid,wildname):
               Gen_mut(workdir,pdbid,chain,resid,wildname,mutname)
               def_site(workdir,pdbid,chain,resid,cutoff,pri_filename)
               def_site(workdir,mut_filename,chain,resid,cutoff,mut_filename)
            else:
               wrong.append(pri_filename)
        else:
          nofile.append(filename)
    #np.savetxt('wrong_residue.txt',wrong,delimiter=' ')
    #np.savetxt('no_exists_file.txt',nofile,delimiter=' ')
    return print('wrong residue or wild:',wrong),print('no exists file in pdbfile:',nofile)
    
if __name__ == "__main__":
    main()
