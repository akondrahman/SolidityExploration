'''
Akond Rahman 
June 21, 2018 
Placeholder for all metric extraction: chrun
'''

import git_churn_extractor 
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


def getChurnForSingleFile(full_path_param, repo_path_param):
  print full_path_param
  print "-"*50
  ### SLOC 
  sloc_for_file      = sum(1 for line in open(full_path_param))
  
  all_metric_as_str_for_file = str(sloc_for_file) + ',' + git_churn_extractor.getRelativeChurnMetrics(full_path_param, repo_path_param)
  return all_metric_as_str_for_file

def getChurnForAllFile(in_fi, or_di):
   str2ret=''
   fileCount = 0
   with open(in_fi, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
          file_name_ = row_[1]
          defect_status = row_[-1]
          ### checking loc as not all sol files are valid 
          if (os.path.exists(file_name_)):
             sloc_for_file      = sum(1 for line in open(file_name_))
             if sloc_for_file > 1:
                repo_ = getRepoFromFileName(file_name_, or_di)   
                fileCount = fileCount + 1
                print "The file:", file_name_
                all_metric_for_this_file = getChurnForSingleFile(file_name_, repo_)
                print all_metric_for_this_file
                str2ret = str2ret + file_name_ + ',' + all_metric_for_this_file + defect_status + '\n'
                print "="*10
   
   str2ret = 'FILE,SLOC,TOT_CHN_LOC,NOR_TOT_CHN,NOR_DEL_CHN,NOR_CHN_DAY,PER_DEL_CHN,PER_ADD_CHN,TOT_CHN_CNT,defect_status' + '\n' + str2ret
   return str2ret


if __name__=='__main__':
   print "-"*100

   input_ = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/FINAL_PROCESS_GITHUB.csv'
   output_ = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/FINAL_LOC_CHURN_GITHUB.csv'    
   org_dir = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V5/final_repos/'   

#    input_ = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/prior/GITHUB_V3_MEENELY.csv'
#    output_ = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/CHURN.GITHUB.V3.csv'    
#    org_dir = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V3/'   

   data_dump  = getChurnForAllFile(input_, org_dir)
   dumpContentIntoFile(data_dump, output_)