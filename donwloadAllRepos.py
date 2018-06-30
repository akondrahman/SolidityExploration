'''
Akond Rahman 
June 29, 2018
Download solidity repos from Github 
'''
from itertools import izip_longest
import os 
import csv 
import subprocess
import numpy as np
import shutil

def getRepos(file_name):
    list_ = []
    with open(file_name, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
          the_repo_name = row_[0]
          repo_dload_url = 'https://github.com/' + the_repo_name + '.git'
          list_.append(repo_dload_url)
          #https://github.com/akondrahman/SolidityExploration.git    
    return list_



def makeChunks(the_list, size_):
    for i in range(0, len(the_list), size_):
        yield the_list[i:i+size_]

def cloneRepo(repo_name):
    cmd_ = "git clone " + repo_name
    try:
       subprocess.check_output(['bash','-c', cmd_])    
    except subprocess.CalledProcessError:
       print 'Skipping this repo ... trouble cloning repo', repo_name 

def getSolidityFiles(directory):
    pp_list = []
    for root_, dirnames, filenames in os.walk(directory):
        for file_ in filenames:
            if (file_.endswith('sol')):
               pp_list.append(os.path.join(root_, file_))
    return pp_list        

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP )
    fileToWrite.close()
    return str(os.stat(fileP).st_size)

def cloneRepos(repo_list):
    counter = 0     
    for repo_batch in repo_list:
        repo_cnt = 0 
        str_ = ''
        for repo_ in repo_batch:
            repo_cnt += 1
            counter += 1 
            print 'Cloning ', repo_
            cloneRepo(repo_)
            dirName = repo_.split('/')[-1].split('.')[0]
            # print dirName
            ### get file count 
            all_fil_cnt = sum([len(files) for r_, d_, files in os.walk(dirName)])
            sol_fil_cnt  = len(getSolidityFiles(dirName))
            if (all_fil_cnt <= 0):
                print 'Deleting ', repo_
                try:
                   if os.path.exists(dirName):
                      shutil.rmtree(dirName)
                except OSError:
                   print 'Failed deleting, will try manually'
                sol_perc     = float(0)
            else:
                sol_perc     = float(sol_fil_cnt)/float(all_fil_cnt)
            print '*'*50
            # print dirName, all_fil_cnt, pp_perc
            print '*'*50
            if (sol_perc < 0.05):
                print 'Deleting ', repo_
                try:
                   if os.path.exists(dirName):
                      shutil.rmtree(dirName)
                except OSError:
                   print 'Failed deleting, will try manually'
            else:
                print 'Keeping ', repo_
            print '*'*50
            str_ = str_ + dirName + ',' + str(sol_perc) + ',' + '\n'
            print "So far we have processed {} repos".format(counter)
            print str_
            print '*'*50
        dumpContentIntoFile(str_, str(repo_cnt) + '_tracker_completed_repos.csv')
               

if __name__=='__main__':
   srcFile1='/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V5/gh-solidity-batch1.csv'
   srcFile2='/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V5/gh-solidity-batch2.csv'
   list1=getRepos(srcFile1)    
   list2=getRepos(srcFile2)      
   list_ = list1 + list2 
   list_ = np.unique(list_)
   print 'Repos to download:', len(list_)
   ## need to create chunks as too many repos 
   chunked_list = list(makeChunks(list_, 1000))  ### list of lists, at each batch download 1000 repos 
   #print chunked_list
   cloneRepos(chunked_list)
