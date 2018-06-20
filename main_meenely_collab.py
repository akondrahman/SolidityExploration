'''
Akond Rahman
Feb 01, 2018
Thursday
'''
import cPickle as pickle
import os
import csv
import subprocess
import numpy as np
from collections import Counter

def getRepoFromFileName(file_param, org_par):
    start_path = os.path.relpath(file_param, org_par)
    repo_name  = start_path.split('/')[0]
    repo_path  = org_par  + repo_name + '/'
    # print 'Start path:{}, repo name:{}, repo path:{}'.format(start_path, repo_name, repo_path)
    return repo_path

def createEdges(comm_auth_dict, file_p):
    list2ret = []
    devCnt   = 0
    for k_, v_ in comm_auth_dict.iteritems():
        devCnt    += 1
        name2save = 'Dev_' + str(devCnt)
        tup_ = (name2save, file_p, v_)
        list2ret.append(tup_)
    return list2ret

def getGitProgrammerInfo(param_file_path, repo_path):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   commitCountCmd    = " git blame "+ theFile +"  | awk '{print $2}' | cut -d'(' -f2 "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   author_count_output = [x_ for x_ in author_count_output if x_!='']
   node_cnt            = len(np.unique(author_count_output)) ## get node count
   ## get commit  count per author
   comm_per_auth       = dict(Counter(author_count_output))
   edge_list           = createEdges(comm_per_auth, param_file_path) # list of edges with weights
   # print param_file_path
   return (edge_list, node_cnt)

def getHgCommPerAuth(param_file_path, repo_path):
   '''
   Commit per author is different for Hg than Git
   '''
   dict2ret = {}
   tempDict = {}
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " hg annotate -uc " + theFile + " | cut -d':' -f1 | tr ' ' ',' "
   command2Run       = cdCommand + blameCommand

   blame_output   = subprocess.check_output(['bash','-c', command2Run])
   blame_output   = blame_output.split('\n')
   blame_output   = [x_ for x_ in blame_output if x_!='']  ## get the author and the commti ID by splitting using commas

   auth_per_comm  = [(x_.split(',')[-2], x_.split(',')[-1]) for x_ in blame_output]
   for tu_ in auth_per_comm:
       auth = tu_[0]
       comm = tu_[1]
       if auth not in tempDict:
           tempDict[auth] = [comm]
       else:
           tempDict[auth] = tempDict[auth] + [comm]
   for k_, v_ in tempDict.iteritems():
       if k_ not in dict2ret:
          dict2ret[k_] = len(np.unique(v_))
   # print param_file_path
   # print dict2ret
   return dict2ret

def getHgProgrammerInfo(param_file_path, repo_path):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   commitCountCmd    = "hg churn --diffstat  " + theFile + " | awk '{print $1}'  "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   author_count_output = [x_ for x_ in author_count_output if x_!='']
   node_cnt            = len(np.unique(author_count_output)) ## get node count

   ## get commit  count per author
   comm_per_auth       = getHgCommPerAuth(param_file_path, repo_path)
   edge_list           = createEdges(comm_per_auth, param_file_path) # list of edges with weights
   # print param_file_path
   return (edge_list, node_cnt)


def getGraphData(file_path_p, repo_path_p):
    if 'moz' in file_path_p:
        graph_per_file = getHgProgrammerInfo(file_path_p, repo_path_p)
    else:
        graph_per_file = getGitProgrammerInfo(file_path_p, repo_path_p)
    ### now return value
    print 'File:{}, Graph:{}'.format(file_path_p, graph_per_file)
    # print 'Processing {} ...'.format(file_path_p)
    return graph_per_file

def getEdgeForFiles(file_path_p, org_par):
    output_dict = {}
    with open(file_path_p, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
        categ_of_file      = row_[-1]
        full_path_of_file  = row_[1]
        repo_of_file       = getRepoFromFileName(full_path_of_file, org_par)
        if os.path.exists(full_path_of_file):
            if full_path_of_file not in output_dict:
                gr_for_file = getGraphData(full_path_of_file, repo_of_file)
                output_dict[full_path_of_file] = gr_for_file
    return output_dict


if __name__=='__main__':

    ### INPUT
    # theCompleteCategFile='/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_V3.csv'
    # theCompleteCategFile='/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_V4.csv'

    # org_name = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V3/'
    # org_name = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V4/'

    ### OUTPUT
    # datasetFile2Save='/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_V3_COLLA.PKL'
    # datasetFile2Save='/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_V4_COLLA.PKL'


    final_dict = getEdgeForFiles(theCompleteCategFile, org_name)
    pickle.dump(final_dict, open(datasetFile2Save, 'wb'))
