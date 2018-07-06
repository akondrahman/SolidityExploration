'''
Akond Rahman
April 01, 2017
utility file for process metric
'''
import ctypes
from collections import Counter
import os, csv, numpy as np, time, datetime
import os, subprocess, numpy as np, operator
from  collections import Counter
from scipy.stats import entropy
import math
import pandas as pd


def getRepoFromFileName(file_param, org_par):
    start_path = os.path.relpath(file_param, org_par)
    repo_name  = start_path.split('/')[0]
    repo_path  = org_par  + repo_name + '/'
    # print 'Start path:{}, repo name:{}, repo path:{}'.format(start_path, repo_name, repo_path)
    return repo_path

def getPuppetFileDetails(theCompleteCategFile, org_dir):
    dict2Ret={}
    with open(theCompleteCategFile, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
          file_name_ = row_[0]
          repo_ = getRepoFromFileName(file_name_, org_dir)
          tot_smell_count = int(row_[-1])
          if tot_smell_count > 0:
              smell_status = '1'
          else:
              smell_status = '0'
          if file_name_ not in dict2Ret:
             dict2Ret[file_name_] = (repo_, smell_status)
    return dict2Ret




def dumpContentIntoFile(strP, fileP):
  fileToWrite = open( fileP, 'w')
  fileToWrite.write(strP )
  fileToWrite.close()
  return str(os.stat(fileP).st_size)


def giveTimeStamp():
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

def createDataset(str2Dump, datasetNameParam):
   headerOfFile0='org,file_,'
   #headerOfFile1='COMM,AGE,DEV,AVGTIMEOFEDITS,ADDPERLOC,'
   headerOfFile1='COMM,AGE,DEV,ADDPERLOC,'
   #headerOfFile2='DELPERLOC,ADDNORM,DELNORM,AVGCHNG,MINOR,OWN,SCTR,'
   headerOfFile2='DELPERLOC,SUMCHNG,TOTCHNGPERLOC,AVGCHNG,MINOR,SCTR,'
   #headerOfFile3='COMM_SIZE,MT_PP, MT_NON_PP,'
   headerOfFile3='NON_SOL_PER,'
   headerOfFile4='defect_status'

   headerStr = headerOfFile0 + headerOfFile1 + headerOfFile2  +  headerOfFile3 + headerOfFile4

   str2Write = headerStr + '\n' + str2Dump
   return dumpContentIntoFile(str2Write, datasetNameParam)

def getDatasetFromCSV(fileParam, dataTypeFlag=True):
  if dataTypeFlag:
    data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1, dtype='float')
  else:
        data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1,  dtype='str')
  return data_set_to_return



def createOutputDirectory(dirParam):
  if not os.path.exists(dirParam):
     os.makedirs(dirParam)
  if os.path.exists(dirParam):
     print "Output directory created ..."

def getMercurialProgrammerList(file_with_rel_path, repo_path):
   prog_output = []
   if (('student' not in file_with_rel_path) and ('.csv' not in file_with_rel_path) and ('.txt' not in file_with_rel_path) and ('EXTRA_AST' not in file_with_rel_path)):
      cdCommand         = "cd " + repo_path + " ; "
      commitCountCmd    = "hg churn --diffstat  " + file_with_rel_path + " | awk '{print $1}'  "
      command2Run = cdCommand + commitCountCmd
      _output = subprocess.check_output(['bash','-c', command2Run])
      prog_output = _output.split('\n')
      prog_output = [x_ for x_ in prog_output if x_!='']
   return prog_output

def getRepoList(org_name_p):
    repoList2Ret = []
    repoList2Ret = os.listdir(org_name_p)
    
    return repoList2Ret

def getMercurialProgToFileMapping(org_name_p):
   dict2ret = {}
   repo_list = getRepoList(org_name_p)
   for repo_path_param in repo_list:
       cdCommand         = "cd " + repo_path_param + " ; "
       progToFileCommand = "hg status --all | cut -d' ' -f2 "
       command2Run = cdCommand + progToFileCommand

       all_file_in_repo_output = subprocess.check_output(['bash','-c', command2Run])
       all_file_in_repo_output = all_file_in_repo_output.split('\n')
       all_file_in_repo_output = [x_ for x_ in all_file_in_repo_output if x_!='']
       for file_ in all_file_in_repo_output:
           prog_list = getMercurialProgrammerList(file_, repo_path_param)
           for programmer_ in prog_list:
               if programmer_ not in dict2ret:
                  dict2ret[programmer_] =  [file_]
               else:
                  dict2ret[programmer_] = dict2ret[programmer_] + [file_]
   return dict2ret

def getGitProgrammerList(file_with_rel_path, repo_path):
   prog_output = []
   #print file_with_rel_path, repo_path
   if (('student' not in file_with_rel_path) and ('.csv' not in file_with_rel_path) and ('.txt' not in file_with_rel_path) and ('EXTRA_AST' not in file_with_rel_path)):
      cdCommand         = "cd " + repo_path + " ; "
      commitCountCmd    = " git blame "+ file_with_rel_path +"  | awk '{print $2}' | cut -d'(' -f2 "
      command2Run = cdCommand + commitCountCmd
      _output = subprocess.check_output(['bash','-c', command2Run])
      prog_output = _output.split('\n')
      prog_output = [x_ for x_ in prog_output if x_!='']
   return prog_output


def getGitProgToFileMapping(org_name_p):
   dict2ret = {}
   repo_list = getRepoList(org_name_p)
   repo_cnt = 0
   print '[PROGRAMMER TO FILE MAPPING]:::Repos to analyze:', len( repo_list )
   print '%'*25
   for repo_path_param in repo_list:
       #print repo_path_param
        repo_cnt += 1
       # cdCommand         = "cd " + repo_path_param + " ; "
       # progToFileCommand = "git ls-files "
       # command2Run = cdCommand + progToFileCommand
       #
       # all_file_in_repo_output = subprocess.check_output(['bash','-c', command2Run])
       # all_file_in_repo_output = all_file_in_repo_output.split('\n')
       # all_file_in_repo_output = [x_ for x_ in all_file_in_repo_output if x_!='']
       # #print all_file_in_repo_output

        for root_, dirs, files_ in os.walk(repo_path_param):
           for file_ in files_:
              full_p_file = os.path.join(root_, file_)
              if not ( full_p_file.startswith('.') or has_hidden_attribute(full_p_file) ):
                 prog_list = getGitProgrammerList(full_p_file, repo_path_param)
                 for programmer_ in prog_list:
                   if programmer_ not in dict2ret:
                      dict2ret[programmer_] =  [full_p_file]
                   else:
                      dict2ret[programmer_] = dict2ret[programmer_] + [full_p_file]
        print '[PROGRAMMER TO FILE MAPPING]:::{} analyzed, {} more to go'.format(repo_cnt, len(repo_list) - repo_cnt)
        print '!'*10
   return dict2ret


def createLogTransformedFeatures(allFeatureParam):
  log_transformed_feature_dataset_to_ret = []
  dataset_rows = len(allFeatureParam)
  print "-"*50
  print "Dataset rows:",dataset_rows
  print "-"*50
  for ind_ in xrange(dataset_rows):
    features_for_this_index = allFeatureParam[ind_, :]
    log_transformed_features_for_index = [math.log1p(x_) for x_ in features_for_this_index]
    log_transformed_feature_dataset_to_ret.append(log_transformed_features_for_index)

  log_transformed_feature_dataset_to_ret = np.array(log_transformed_feature_dataset_to_ret)
  return log_transformed_feature_dataset_to_ret

def has_hidden_attribute(filepath):
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(filepath))
        assert attrs != -1
        result = bool(attrs & 2)
    except (AttributeError, AssertionError):
        result = False
    return result
