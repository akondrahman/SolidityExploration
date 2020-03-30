'''
Akond Rahman 
June 21, 2018 
Placeholder for all metric extraction: chrun
'''

import git_churn_extractor 
import os 
import subprocess
import pandas as pd 
import numpy as np 

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


def getChurnForSingleFile(full_path_param, repo_path_param):
  print(full_path_param)
  print("-"*50)
  ### SLOC 
  sloc_for_file      = sum(1 for line in open(full_path_param))
  
  all_metric_as_str_for_file = str(sloc_for_file) + ',' + git_churn_extractor.getRelativeChurnMetrics(full_path_param, repo_path_param)
  return all_metric_as_str_for_file

def getChurnForAllFile(in_fi, or_di):
    str2ret=''
    fileCount = 0
    df_ = pd.read_csv(in_fi) 
    files = np.unique( df_['FILE_PATH'].tolist() )
    for file_name_ in files: 
        if (os.path.exists(file_name_)):
            try:
                sloc_for_file      = sum(1 for line in open(file_name_)) 
            except UnicodeDecodeError:
                sloc_for_file      =  1    
            if sloc_for_file > 1:
                repo_ = getRepoFromFileName(file_name_, or_di)   
                fileCount = fileCount + 1
                print("The file:", file_name_)
                all_metric_for_this_file = getChurnForSingleFile(file_name_, repo_)
                print(all_metric_for_this_file)
                str2ret = str2ret + file_name_ + ',' + all_metric_for_this_file  + '\n'
                print("="*10)
   
    str2ret = 'FILE_PATH,SLOC,TOT_CHN_LOC,NOR_TOT_CHN,NOR_DEL_CHN,NOR_CHN_DAY,PER_DEL_CHN,PER_ADD_CHN,TOT_CHN_CNT,' + '\n' + str2ret
    return str2ret


if __name__=='__main__':
   print("-"*100)
   input_  = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/ncsu_research/solidity-nier2018/results/V4/FINAL_PROCESS_METRICS.csv'
   output_ = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/ncsu_research/solidity-nier2018/results/V4/FINAL_CODE_METRICS.csv'    
   org_dir = '/Users/arahman/SOLIDITY_REPOS/V5/final_repos/'   

   data_dump  = getChurnForAllFile(input_, org_dir)
   dumpContentIntoFile(data_dump, output_)

   print("-"*100)   