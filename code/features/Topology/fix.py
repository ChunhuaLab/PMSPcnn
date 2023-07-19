# outfile ./fix
import os
import sys 

# fix pdb structure


def input_para():
    pdbid = sys.argv[1]
    return pdbid
    
def modifypdb(name1,name2):
        pdbname = open(name1)
        outfile = open(name2,"w")
        lines = pdbname.read().splitlines()
        PRO = []
        for line in lines:
            if line[0:4] == 'ATOM':
                 outfile.write(line+'\n')
        outfile.close()

def fix_structure(filepath,filename):
    os.system('./profix -fix 0 '+'/'+filepath+'/'+filename)
    os.system('mv '+filename[0:4]+'_fix.pdb '+filename)
    os.system('mv *.pdb '+ filepath)
    #os.system('mv '+filename+' '+filepath+'/'+filename)
    return
 
def main():
    #Datadir = './inpu/'
    workdir = 'pdbfile'
    pdbid = input_para()
    pdbid1=pdbid[0:4]+pdbid[-4:]
    #pdbid1=pdbid[3:7]+'.pdb'
    #pdbid = '1btaX.pdb'
    filename1=workdir + '/'+pdbid
    filename2=workdir + '/'+pdbid1
    # modifypdb and fix
    modifypdb(filename1,filename2)
    fix_structure(workdir,pdbid1)
    return
if __name__ == "__main__":
    main()
