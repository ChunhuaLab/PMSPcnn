import os,sys
import numpy as np

np.set_printoptions(threshold=sys.maxsize)


  
# Constant Settings
elelist = ['C','N','O']
eleid ={'C':0,'N':1,'O':2}
small = 0.01


# Set filtration
def set_filtration(cut,interval):
  bin_max = int(cut/interval)
  Bins = []
  for i in range(0,bin_max+1):
      Bins.append(i*interval)
  return Bins

# Count bars for Rips Complex from javaplex (betti0)
def BinID(x,B):
  for i in range(0,len(B)-1):
   if x>= B[i] and x <= B[i+1]:
      y = i
  return y


# Count bars for Complex (betti0)

def feature_jplex_mut(max_bin,Cut,Bins):
  dt = np.dtype([('dim', int), ('birth', float), ('death', float)])
  Feature_dth = np.zeros([max_bin,27])
  Feature_per = np.zeros([max_bin,27])
#  Feature_dth_R = np.zeros([max_bin,27])
#  Feature_per_R = np.zeros([max_bin,27])
  for e1 in elelist:
    for e2 in elelist:
      wildname = 'wild_mutation_'+e1+'_'+e2+'.PH'
      mutname ='mut_mutation_'+e1+'_'+e2+'.PH'
      for j in range(0,2):
        if j == 0: PHFile = open('./'+wildname)
        if j == 1: PHFile = open('./'+mutname)
        lines = PHFile.read().splitlines()
        tmpbars = np.zeros(len(lines),dtype = dt)
        count = 0

                # Exclude the bars with persistence less than small, death > cut
        for line in lines:
          dim, b, d = line.split()
          if float(d) - float(b) < small: continue
          if float(b) > Cut: continue
          tmpbars[count]['dim'] = int(dim)
          tmpbars[count]['birth'] = float(b)
          tmpbars[count]['death'] = float(d)
          count += 1
        
        bars = tmpbars[0:count]
        print(e1,e2,j)
        print(bars.shape)
        
        Ip = eleid[e1]
        Is = eleid[e2]
        
        for bar in bars:
          death = bar['death']
          if death >= Cut: continue
          bid = BinID(death,Bins)
          fid = Ip*3 + Is + j*9
          Feature_dth[bid,fid] += 1.0
          Feature_per[:bid,fid] += 1.0

  Feature_dth[:,18:27] = Feature_dth[:,0:9] - Feature_dth[:,9:18]
  Feature_per[:,18:27] = Feature_per[:,0:9] - Feature_per[:,9:18]

  
  return Feature_dth,Feature_per
  
def input_param():
  cut=sys.argv[1]
  Bin=sys.argv[2]
  return float(cut),float(Bin)
  
# Generate persistent homology feature vector
def main():
  Cut,Bin = input_param()
  interval = Bin
  max_bin = int(Cut/interval)
  
  Bins = set_filtration(Cut,interval)
  Feature_b0_dth,Feature_b0_per= feature_jplex_mut(max_bin,Cut,Bins)
  Feature_cnn = np.concatenate((Feature_b0_dth,Feature_b0_per),axis=1)
  
  np.save('X_h0',Feature_cnn)
 
  

  return

main()
