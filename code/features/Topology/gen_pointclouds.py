# Gen_pointclouds.py
# Use cut off to generate pointclouds for Persistant Homology Calculation

import os
import sys
import numpy as np
import scipy as sp

pro_ele_list = ['C','N','O']

def input_para():
    data_name=sys.argv[1]
    return data_name

def readpdb(name):
    pdbname = open(name)
    lines = pdbname.read().splitlines()
    PRO = []
    for i in range(0,len(lines)):
        line = lines[i]
        if line[0:4] == 'ATOM':
            AtomType = line[13:14]
            chain = line[21:22]
            resid = line[22:26]
            if AtomType in pro_ele_list:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                PRO.append([chain,resid.strip(),AtomType,x,y,z])
                continue
            else:
                continue
        else:
            continue 
    return PRO

#Function to generate point cloud of mutation interaction
def cutoff_mut(pro,chain,resid):
    p1cloud = []
    p2cloud = []
    length = len(pro)
    for i in range(0,length):
        #mut_site
        if pro[i][0]==chain and pro[i][1].strip()==resid:
            p1cloud.append(pro[i])
        else:
            p2cloud.append(pro[i])
    return p1cloud,p2cloud

#Generate point clouds files for javaplex (H0) calculation: 
#e1,e2: element for component1 and component2
#p1cloud, p2cloud: atom postion for component1 and component2

def write_h0_points(e1,e2,p1cloud,p2cloud,prefix):
    Name = prefix+'_'+e1+'_'+e2+'.pts'
    OutFile = open(Name,'w')
    for i in range(0,len(p1cloud)):
        if p1cloud[i][2] == e1:
            OutFile.write(('1 '+str(p1cloud[i][3])+' '+str(p1cloud[i][4])+' '+str(p1cloud[i][5])+'\n'))
    for i in range(0,len(p2cloud)):
        if p2cloud[i][2] == e2:
            OutFile.write(('0 '+str(p2cloud[i][3])+' '+str(p2cloud[i][4])+' '+str(p2cloud[i][5])+'\n'))
    OutFile.close()
    return

#Generate point clouds file for TDA (H1,H2) calculation in csv format:

def write_h12_points(e1,e2,p1cloud,p2cloud,prefix):
    Name = prefix + '_' + e1 + '_' + e2 + '.csv'
    OutFile = open(Name,'w')
    OutFile.write("x1,x2,x3\n")
    for i in range(0,len(p1cloud)):
        if p1cloud[i][2] == e1:
            OutFile.write((str(p1cloud[i][3])+' ,'+str(p1cloud[i][4])+' ,'+str(p1cloud[i][5])+'\n'))
    for i in range(0,len(p2cloud)):
        if p2cloud[i][2] == e2:
            OutFile.write((str(p2cloud[i][3])+' ,'+str(p2cloud[i][4])+' ,'+str(p2cloud[i][5])+'\n'))
    OutFile.close()
    return

def main():
    workdir='pdbfile'
    out_dir='pdbfile/mutation_PH'
    data_name=input_para()
    
    os.system('mkdir '+ out_dir)
    #os.system('cp ./data_name/'+data_name+' ../e/')
    
    for line in open(data_name):
       line=line.strip('\n').split(',')
       pdbid=line[0]
       pdbid=pdbid[0:4]
       chain=line[1]
       resid=line[2]
       wildname=line[3]
       mutname=line[4]
       pdbid_wild = pdbid+'_'+resid+'_'+wildname+'_'+mutname
       pdbid_mut = pdbid+'_'+resid+'_'+wildname+'_'+mutname+'_mut'
       #judge whether the file exists
       file_mut='./'+workdir+'/' + pdbid_mut + '.pdb'
       if os.path.exists(file_mut):
           file_name= out_dir+'/'+pdbid_wild
           os.system('mkdir '+file_name)
           #Set up point clouds generation for mutation interaction PH calculation
           wild_mutation = './'+workdir+'/' + pdbid_wild + '_m.pdb'
           mut_mutation  = './'+workdir+'/' + pdbid_mut + '_m.pdb'
           pro_wild_m = readpdb(wild_mutation)
           pro_mut_m = readpdb(mut_mutation)

           p1cloud,p2cloud = cutoff_mut(pro_wild_m,chain,resid)
           p1cloud_m,p2cloud_m = cutoff_mut(pro_mut_m,chain,resid)
            
           for e1 in pro_ele_list:
               for e2 in pro_ele_list:
                    write_h0_points(e1,e2,p1cloud,p2cloud,'wild_mutation')
                    write_h0_points(e1,e2,p1cloud_m,p2cloud_m,'mut_mutation')
                    write_h12_points(e1,e2,p1cloud,p2cloud,'wild_mutation')
                    write_h12_points(e1,e2,p1cloud_m,p2cloud_m,'mut_mutation')
           os.system('mv *.pts '+file_name)
           os.system('mv *.csv '+file_name)
       else:
           print(file_mut)

if __name__ == '__main__':
  main()
