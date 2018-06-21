'''
Akond , Feb 17, 2017
Placeholder for all metric extraction: static, process, chrun
'''
from SmellDetector import SmellDectector
import lint_metric_extractor, git_churn_extractor, hg_churn_extractor, static_metric_utility, bug_git_util
MOZFLAG='moz'
WIKIFLAG='wikimedia'

def getAllStaticMetricForSingleFile(full_path_param, repo_path_param):
  org_of_file                     = ''
  print full_path_param
  print "-"*50
  puppet_specific_metric_for_file =  SmellDectector.getQualGenratedMetricForFile(full_path_param)
  print puppet_specific_metric_for_file
  print "Generated the Puppet specific metrics, 14 will be used ... "
  print "-"*50
  #lint_specific_metric_for_file   =  lint_metric_extractor.getLintMetrics(full_path_param)
  #print lint_specific_metric_for_file
  print "Did not generated the Puppet lint metrics, as they will not be used ... "
  print "-"*50
  if(MOZFLAG in full_path_param):
   relative_churn_metrics         =  hg_churn_extractor.getRelativeChurnMetrics(full_path_param, repo_path_param)
   org_of_file                    =  'MOZILLA'
  elif(WIKIFLAG in full_path_param):
   relative_churn_metrics         =  git_churn_extractor.getRelativeChurnMetrics(full_path_param, repo_path_param)
   org_of_file                    =  'WIKIMEDIA'
  else:
   relative_churn_metrics         =  git_churn_extractor.getRelativeChurnMetrics(full_path_param, repo_path_param)
   org_of_file                    =  'OPENSTACK'
  #print relative_churn_metrics
  print "Generated the relative churn metrics, 4 will be used ... "
  print "-"*50
  #all_metric_as_str_for_file      = puppet_specific_metric_for_file + lint_specific_metric_for_file + relative_churn_metrics
  all_metric_as_str_for_file      = puppet_specific_metric_for_file  + relative_churn_metrics
  all_metric_as_str_for_file      = org_of_file + ',' + full_path_param + ',' + all_metric_as_str_for_file
  return all_metric_as_str_for_file




def getAllStaticMatricForAllFiles(pupp_map_dict_param):
   # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/MOZ_WIKI_FULL_DATASET.csv'
   # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/WITHOUT_BAD_BOYS_OPENSTACK_FULL_DATASET.csv'
   # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/MIRANTIS_FULL_DATASET.csv'
   # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/CISCO_FULL_DATASET.csv'
   # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/BASTION_FULL_DATASET.csv'
   str2ret=''
   fileCount = 0
   for file_, details_ in pupp_map_dict_param.items():
     fileCount = fileCount + 1
     repo_                    = details_[1]
     defect_status            = details_[0]
     print "Analyzing ... \nfile#{}\ndefect status:{}\nrepo:{}".format(fileCount, defect_status, repo_)
     print "The file:"
     all_metric_for_this_file = getAllStaticMetricForSingleFile(file_, repo_)
     str2ret = str2ret + all_metric_for_this_file + defect_status + '\n'
     print "="*100
   static_metric_utility.createDataset(str2ret, datasetFile2Save)
   return str2ret

print "Started at:", bug_git_util.giveTimeStamp()
print "-"*100
'''
FOR TEST STUFF
'''

test_hg_file  = '/Users/akond/PUPP_REPOS/mozilla-releng-downloads/relabs-puppet/manifests/site.pp'
#test_git_file = '/Users/akond/PUPP_REPOS/wikimedia-downloads/mariadb/manifests/heartbeat.pp'
test_git_file = '/Users/akond/PUPP_REPOS/openstack-downloads/puppet-nova/manifests/params.pp'
# git_repo_path = '/Users/akond/PUPP_REPOS/wikimedia-downloads/mariadb'
git_repo_path = '/Users/akond/PUPP_REPOS/openstack-downloads/puppet-nova'
hg_repo_path  = '/Users/akond/PUPP_REPOS/mozilla-releng-downloads/relabs-puppet/'
'''
FOR REAL STUFF
'''
fullPuppMap   = static_metric_utility.getPuppetFileDetails()
print "Loaded the mapping of files ... "
print "-"*100
'''
testing purpose
'''
###### getAllStaticMetricForSingleFile(test_hg_file, hg_repo_path)
# getAllStaticMetricForSingleFile(test_git_file, git_repo_path)
'''
for dataset generation
'''
getAllStaticMatricForAllFiles(fullPuppMap)
print "We analyzed {} Puppet files".format(len(fullPuppMap))
print "-"*100
print "Ended at:", bug_git_util.giveTimeStamp()
