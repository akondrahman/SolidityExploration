'''
Apri 01, 2017
Extracting process metrics
Akond Rahman
'''
import git_process_extractor, process_metric_utility
import cPickle as pickle
import os 

def getAllProcessMetricsForSingleFile(full_path_param, repo_path_param, prog_to_file_dict, org_of_file):
      process_metrics         =  git_process_extractor.getProcessMetrics(full_path_param, repo_path_param, prog_to_file_dict)
      print "-"*50
      print process_metrics
      print "Generated the process metrics ... "
      print "-"*50
      all_metric_as_str_for_file      = org_of_file + ',' + full_path_param + ',' + process_metrics
      return all_metric_as_str_for_file

def getAllProcessMetricForAllFiles(pupp_map_dict_param, datasetFile2Save, prog_to_file_dict, org_name):
   str2ret=''
   fileCount = 0
   '''
   LOAD the file to programmer dicts first
   '''
   for file_, details_ in pupp_map_dict_param.items():
     if (file_!= 'WTF') and (os.path.exists(file_)):
        fileCount = fileCount + 1
        repo_                    = details_[0]
        defect_status            = details_[1]
        print "Analyzing ... \nfile#{}\ndefect status:{}\nfile:{}\nrepo:{}".format(fileCount, defect_status, file_, repo_)
        all_metric_for_this_file = getAllProcessMetricsForSingleFile(file_, repo_, prog_to_file_dict, org_name)
        str2ret = str2ret + all_metric_for_this_file + defect_status + '\n'
        print "="*75
   dump_stats = process_metric_utility.createDataset(str2ret, datasetFile2Save)
   print "Dumped a file of {} bytes".format(dump_stats)
   return str2ret


'''
Solidity Mining
June 18, 2018
'''
org_name = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V5/final_repos/'
theCompleteCategFile='/Users/akond.rahman/Documents/Personal/misc/solidity_output/FINAL_SECU_SOLHINT.csv'
datasetFile2Save='/Users/akond.rahman/Documents/Personal/misc/solidity_output/FINAL_PROCESS_GITHUB.csv'
pkl_fil_nam='/Users/akond.rahman/Documents/Personal/misc/solidity_output/FINAL_GITHUB_PROG_DICT.p'
ORG   = 'GITHUB'

# org_name = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V4/'
# theCompleteCategFile='/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V4/FINAL_SECU_SOLHINT.csv'
# datasetFile2Save='/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_V4.csv'
# pkl_fil_nam='/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_V4_PROG_DICT.p'
# ORG   = 'GITHUB'

# org_name = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V3/'
# theCompleteCategFile='/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V3/FINAL_SECU_SOLHINT.csv'
# datasetFile2Save='/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_V3.csv'
# pkl_fil_nam='/Users/akond.rahman/Documents/Personal/misc/solidity_output/GITHUB_V3_PROG_DICT.p'
# ORG   = 'GITHUB'

print "Started at:", process_metric_utility.giveTimeStamp()
fullPuppMap   = process_metric_utility.getPuppetFileDetails(theCompleteCategFile, org_name)
print "Loaded the security smells mapping of files ... "
print "-"*100
prog_to_file_dict = process_metric_utility.getGitProgToFileMapping(org_name)
pickle.dump(prog_to_file_dict, open(pkl_fil_nam, "wb"))
print 'Done loading all file to programmer mapping ....'
print '-'*100
str_ = getAllProcessMetricForAllFiles(fullPuppMap, datasetFile2Save, prog_to_file_dict, ORG)
print "-"*100
print "We analyzed {} Solidity files".format(len(fullPuppMap))
print "-"*100
print "Ended at:", process_metric_utility.giveTimeStamp()
print "-"*100
