# generate .tda fles

import sys,os
import numpy as np

elelist = ['C','N','O']

#Run tda pacakge for alpha complex

def run_tda():
#    dirname = sys.argv[1]
#    dir1 = './'+dirname+'/'
#   
#    prefix = dir1
    for e1 in elelist:
        for e2 in elelist:
            wildpts =  'wild_mutation_'+e1+'_'+e2+'.csv'
            wildout =  'wild_mutation_'+e1+'_'+e2+'.tda'
            os.system("Rscript PH_Alpha.R "+ wildpts + " tmp_output")
            os.system("sed '1d' tmp_output > "+wildout)
  
            mutpts =  'mut_mutation_'+e1+'_'+e2+'.csv'
            mutout =  'mut_mutation_'+e1+'_'+e2+'.tda'
            os.system("Rscript PH_Alpha.R "+ mutpts + " tmp_output")
            os.system("sed '1d' tmp_output > "+mutout)


run_tda()


