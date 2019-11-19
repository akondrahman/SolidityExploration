'''
get summary stats from datasets
Akond Rahman
Nov 19, 2018 
'''
from scipy import stats
import pandas as pd
import numpy as np
import cliffsDelta


# all_file  = '/Users/akond/Documents/AkondOneDrive/OneDrive/solidity-nier2018/results/V2/FINAL_PROCESS_GITHUB_PROCESSED.csv'
all_file  = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/ncsu_research/solidity-nier2018/results/V3/FINAL_DENSITY_METRICS.csv'


def giveTimeStamp():
  import time, datetime
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

dataset_files = [all_file]

print("Started at:", giveTimeStamp())
for dataset_file in dataset_files:
    name = dataset_file.split('/')[-1]
    print("Dataset:", name )
    df2read = pd.read_csv(dataset_file)
    features = df2read.columns
    #  dropcols = ['defect_status', 'org', 'FILE', 'file_', 'CREATION_DATE']
    dropcols = ['file_', 'REENTRANCY',	'CHECK_SEND',	'AVOID_CALL',	'COMP_GT',	'TX_ORIG',	'BLOCK_HASH',	'LOW_LEVEL',	'TOTAL',	'org',	
                'COMM',	'defect_status', 'MODI_COMM',	'LINT_DENSITY', 'DEFECT_DENSITY']
    features2see = [x_ for x_ in features if x_ not in dropcols]
    for feature_ in features2see:
          #  print feature_
           '''
           all data summary
           '''
           data_for_feature = df2read[feature_]
           median_, mean_, total_ = np.median(data_for_feature), np.mean(data_for_feature), sum(data_for_feature)
           print("Feature:{}, [ALL DATA] median:{}, mean:{}, sum:{}".format(feature_, median_, mean_, total_  ) )
           print('='*50 )
           defective_vals_for_feature     = df2read[df2read['DEFECT_DENSITY']==1][feature_]
           non_defective_vals_for_feature = df2read[df2read['DEFECT_DENSITY']==0][feature_]
           '''
           summary time
           '''
           print('THE FEATURE IS:', feature_ )
           print('='*25 )
           print("Defective values [MEDIAN]:{}, [MEAN]:{}, [COUNT]:{}".format(np.median(list(defective_vals_for_feature)), np.mean(list(defective_vals_for_feature)), len(defective_vals_for_feature)) )
           print("Non Defective values [MEDIAN]:{}, [MEAN]:{}, [COUNT]:{}".format(np.median(list(non_defective_vals_for_feature)), np.mean(list(non_defective_vals_for_feature)), len(non_defective_vals_for_feature)) )
           try:
              TS, p = stats.mannwhitneyu(list(defective_vals_for_feature), list(non_defective_vals_for_feature), alternative='greater')
           except ValueError:
              TS, p = 0.0, 1.0
           cliffs_delta = cliffsDelta.cliffsDelta(list(defective_vals_for_feature), list(non_defective_vals_for_feature))
           print('*'*25 )
           print('Feature:{}, pee value:{}, cliffs:{}'.format(feature_, p, cliffs_delta) )
           print('*'*25 )
           print('='*50 )
print("Ended at:", giveTimeStamp() )
