'''
Akond Rahman
Feb 04, 2018
Meenely's Dev Network
'''
import os
import csv
import itertools
import subprocess
import numpy as np
import cPickle as pickle

def getRepoFromFileName(file_param, org_par):
    start_path = os.path.relpath(file_param, org_par)
    repo_name  = start_path.split('/')[0]
    repo_path  = org_par  + repo_name + '/'
    # print 'Start path:{}, repo name:{}, repo path:{}'.format(start_path, repo_name, repo_path)
    return repo_path

def getGitProgrammerInfo(param_file_path, repo_path):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   commitCountCmd    = " git blame "+ theFile +"  | awk '{print $2}' | cut -d'(' -f2 "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   author_count_output = [x_ for x_ in author_count_output if x_!='']
   node_cnt            = len(np.unique(author_count_output)) ## get node count
   ## create edges using combinations
   ## get unique author names
   uni_aut_names = np.unique(author_count_output)
   temp_edge_list = list(itertools.permutations(uni_aut_names, 2))
   edge_list = [(x_[0], x_[1]) for x_ in temp_edge_list if x_[0] != x_[1]] ## used list comprehension to egenrate valid edges
   return (edge_list, node_cnt)

def getHgProgrammerInfo(param_file_path, repo_path):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   commitCountCmd    = "hg churn --diffstat  " + theFile + " | awk '{print $1}'  "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   author_count_output = [x_ for x_ in author_count_output if x_!='']
   node_cnt            = len(np.unique(author_count_output)) ## get node count

   ## create edges using combinations
   ## get unique author names
   uni_aut_names = np.unique(author_count_output)
   temp_edge_list = list(itertools.permutations(uni_aut_names, 2))
   edge_list = [(x_[0], x_[1]) for x_ in temp_edge_list if x_[0] != x_[1]] ## used list comprehension to egenrate valid edges
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

def getGraphForFiles(file_path_p, org_par):
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

    # org_nam = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V3/'
    # org_nam = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V4/'

    ### OUTPUT
    # datasetFile2Save='/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_V3_DEV.PKL'
    # datasetFile2Save='/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_V4_DEV.PKL'

    # final_dict = getGraphForFiles(theCompleteCategFile, org_nam)
    # pickle.dump(final_dict, open(datasetFile2Save, 'wb'))

    '''
    Merge Meenely Collab and Dev Network Metrics
    '''
    import pandas as pd

    # dev_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/dev_network_output/OUT.GITHUB.V3.DEV.csv'
    # col_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/col_network_output/OUT.GITHUB.V3.COLLA.csv'
    # out_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_V3_MEENELY.csv'

    # # dev_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/dev_network_output/OUT.GITHUB.V4.DEV.csv'
    # # col_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/col_network_output/OUT.GITHUB.V4.COLLA.csv'
    # # out_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_V4_MEENELY.csv'
    #
    # dev_df_ = pd.read_csv(dev_fil)
    # col_df_ = pd.read_csv(col_fil)
    # dev_col_df = dev_df_.merge(col_df_, on=['FILE'])
    # print dev_col_df.head()
    # dev_col_df.to_csv(out_fil)

    # mee_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_ALL_MEENELY.csv'
    # pro_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_ALL_PROCESS.csv'
    # out_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_ALL_FINAL.csv'
    #
    # mee_df_ = pd.read_csv(mee_fil)
    # pro_df_ = pd.read_csv(pro_fil)
    # mee_pro_df = mee_df_.merge(pro_df_, on=['FILE'])
    # print mee_pro_df.head()
    # mee_pro_df.to_csv(out_fil)

    # '''
    # Merge lint and process metric 
    # '''
    # lint_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_ALL_LINTER_FINAL.csv'
    # metr_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_ALL_METRICS_FINAL.csv'
    # outp_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_ALL_FINAL_LOCKED.csv'
    
    # lint_df_ = pd.read_csv(lint_fil)
    # metr_df_ = pd.read_csv(metr_fil)
    # final_df = lint_df_.merge(metr_df_, on=['FILE'])
    # print final_df.head()
    # final_df.to_csv(outp_fil)