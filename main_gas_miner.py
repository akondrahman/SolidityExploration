'''
Mine gas cost estimate 
Akond Rahman 
June 21, 2018 
'''
import os 
import subprocess
import csv 

def getRepoFromFileName(file_param, org_par):
    start_path = os.path.relpath(file_param, org_par)
    repo_name  = start_path.split('/')[0]
    repo_path  = org_par  + repo_name + '/'
    # print 'File:{}, start path:{}, repo name:{}, repo path:{}'.format(file_param, start_path, repo_name, repo_path)
    return repo_path

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP )
    fileToWrite.close()
    return str(os.stat(fileP).st_size)

def getGasForSingleFile(full_file_path):

def getGasForAllFiles(in_, org_, out_):
    str_dump = ''
    with open(in_, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
          file_name_ = row_[0]
          if os.path.exists(file_name_):
             repo_ = getRepoFromFileName(file_name_, org_)
             tot_gas_est = getGasForSingleFile(file_name_)
             str_dump = str_dump + file_name_ + ',' + tot_gas_est + ',' + repo_ + ',' + '\n'
             print '-'*50
    str_dump = 'FILE,GAS_ESTIMATE,REPO,' + '\n' + str_dump 
    out_byt=dumpContentIntoFile(str_dump, out_)
    print 'We dumped a file of {} bytes'.format(out_byt)    



if __name__=='__main__':
   the_file = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/prior/GITHUB_V4_MEENELY.csv'
   dt_out_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/DATE.GITHUB.V4.csv'    
   org = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V4/'   

   getGasForAllFiles(the_file, org, dt_out_fil)