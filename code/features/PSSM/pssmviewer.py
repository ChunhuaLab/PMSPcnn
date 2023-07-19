import sys

import time
import pandas as pd
import numpy as np
import os


#os.system('cp ../../example/*.asn ./ASN')


def sequenceComment(line):

    t = 0
    comment = ''
    for j in line:
        if j == '"':
            t += 1
        if t == 1:
            comment = comment + j
        else:
            if t == 2:
                return comment



def sequenceCode(sequence):
    change_str = ''
    for i in sequence:
        i.strip()
        change_str = change_str + i
    t = 0
    outSequence = ''
    for j in change_str:
        if j == '"':
            t += 1
        if t == 1:
            outSequence = outSequence + j
        else:
            if t == 2:
                return outSequence[1:]



def PSSM_matrix(d,x, pssmBox):
    num = d[x + 3:x + 23]
    num1 = d[x+1]#add
    outLine = ''
    count =0
    for j in num:
        count=count+1

        if count == 19:
            line = num1.replace(',\n', '')
            outLine = outLine + line
        else:
            line = j.replace(',\n', '')
            outLine = outLine + line

    pssmBox.append(outLine)
    if x + 28 <= len(d) - 30:
        call = PSSM_matrix(d,x + 28, pssmBox)
    return pssmBox



def singlePSSM(rowName):
    midBox = []
    pssmLine = ''
    pssmRow = pssmBox[rowName].strip()
    midPSSM = pssmRow.replace('        ', ' ')
    midBox = midPSSM.split(' ')
    for j in midBox:
        if len(str(j)) == 1:
            newNumber = ' ' + j
            pssmLine = pssmLine + '  ' + newNumber
        else:
            newNumber = j
            pssmLine = pssmLine + '  ' + newNumber
    return pssmLine



def help_Pro(d):
    teq = ['1', ]
    for i in range(len(d)):
        if 'seq-data' in d[i]:
            teq.clear()
        if len(teq) == 0:
            if '}' in d[i]:
                d[i] = '}12345'
                return d
            else:
                continue
    return d
def pssm_chuli(formerName):
    with open(formerName, 'r') as u:
        d = u.readlines()
        u.close()
    
    
    d = help_Pro(d)
    print(len(d))
    
    seq = ['1', ]
    sequence = ''
    yourwant = []
    pssmBox = []
    time.sleep(0.2)
    for line in range(len(d)):
        i = d[line]
        i.strip()

        if 'seq-data' in i:
            seq.clear()
            seq.append(i)
            yourwant.extend(seq)
            seq.clear()
        if '}12345' in i:
            sequence = yourwant[1:]
            seq = ['1', ]
            sequence = sequenceCode(sequence)  
            sequence = sequence.replace('\n', '')
        else:
            if len(seq) == 0:
                yourwant.append(i)
        if 'finalData' in i:
            pssmBox = PSSM_matrix(d,line + 2, pssmBox)  
   

   
    return pssmBox,sequence

def pssm_zhengli(sequence):
    Result = ''
    for rowName in range(len(sequence)):
        pssmLine = singlePSSM(rowName)  
        trueName = rowName + 1
        if len(str(trueName)) == 1:
            rowLine = '  ' + str(trueName)
        else:
            if len(str(trueName)) == 2:
                rowLine = ' ' + str(trueName)
            else:
                rowLine = str(trueName)
        outRow = rowLine + ' ' + sequence[rowName] + '  ' + pssmLine
        # print(outRow)
        Result = Result + '\n' + outRow
    title = ['NUM', 'RES', 'C', 'D', 'E ', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W',
             'A ', 'Y ']
    dataxlsx = []
    for name_i in title:
        dataxlsx.append(name_i)
    for i in range(len(Result.split('\n')) - 1):

        for j in range(len(Result.split('\n')[i + 1].split())):
            dataxlsx.append(Result.split('\n')[i + 1].split()[j])
    dataxlsx = np.array(dataxlsx).reshape(len(Result.split('\n')), 22)
    dataxlsx = pd.DataFrame(dataxlsx)
    return dataxlsx



path = './ASN'

ansfile =  os.listdir(path)
for ans_name in ansfile:
    ans_path = path +'/'+ans_name
    formerName = str(ans_path)
    mdia = ans_name.split('.')[0]
    finalName = str(path +'/'+mdia+'_pssm.txt')
   
   
    pssmBox,sequence = pssm_chuli(formerName)
    data = pssm_zhengli(sequence)
    #data.to_csv(finalName, sep=',', index=False, header=None)
    np.savetxt(finalName,data,delimiter=',',fmt ='%s') 
  

os.system('mkdir PSSM')
os.system('mv ./ASN/*.txt ./PSSM')