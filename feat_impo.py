
'''
Akond Rahman
June 25, 2017
Monday
Feature importance for Solidity Metrics using RF
'''
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os

def readDataset(fileParam, dataTypeFlag=True):
  if dataTypeFlag:
    data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1, dtype='float')
  else:
    data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1,  dtype='str')
  return data_set_to_return

def getColumnNames(file_name_param, start, end ):
    ds_   = pd.read_csv(file_name_param)
    temp_ = list(ds_.columns.values)
    temp_ = temp_[start:end]
    return temp_

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP)
    fileToWrite.close()
    return str(os.stat(fileP).st_size)

def calcFeatureImp(feature_vec, label_vec, feature_names_param, output_file, repeat=10):
    header_str, str2write= '', ''
    for name_ in feature_names_param:
        header_str = header_str + name_ + ','
    theRndForestModel = RandomForestClassifier()
    theRndForestModel.fit(feature_vec, label_vec)
    feat_imp_vector=theRndForestModel.feature_importances_
    #print feat_imp_vector

    for ind_ in xrange(repeat):
        for imp_vec_index in xrange(len(feat_imp_vector)):
            feat_imp_val = round(feat_imp_vector[imp_vec_index], 5)
            str2write = str2write +  str(feat_imp_val) + ','
            print 'Metric:{}, score:{}'.format(feature_names_param[imp_vec_index], feat_imp_val)
            print '-'*25
        str2write = str2write + '\n'
        print '='*50
    str2write = header_str + '\n' + str2write
    output_status= dumpContentIntoFile(str2write, output_file)
    print 'Dumped the RF FEATURE IMPORTANCE file of {} bytes'.format(output_status)


if __name__=='__main__':
#    ds_file_name       = '/Users/akond/Documents/AkondOneDrive/OneDrive/solidity-nier2018/results/V1/FINAL_PROCESS_GITHUB_FEAT_IMP.csv'
#    output_file_param  = '/Users/akond/Documents/AkondOneDrive/OneDrive/solidity-nier2018/results/V1/FEAT_IMP_LOCKED.csv'

   ds_file_name       = '/Users/akond/Documents/AkondOneDrive/OneDrive/solidity-nier2018/results/V2/FINAL_PROCESS_GITHUB_PROCESSED.csv'
   output_file_param  = '/Users/akond/Documents/AkondOneDrive/OneDrive/solidity-nier2018/results/V2/FEAT_IMP_LOCKED.csv'

   full_ds=readDataset(ds_file_name)
   full_rows, full_cols = np.shape(full_ds)
   feature_cols = full_cols - 1
   all_features = full_ds[:, 2:feature_cols]
   all_labels  =  full_ds[:, feature_cols]
   defected_file_count     = len([x_ for x_ in all_labels if x_==1.0])
   non_defected_file_count = len([x_ for x_ in all_labels if x_==0.0])
   feature_names = getColumnNames(ds_file_name, 2, feature_cols)
   calcFeatureImp(all_features, all_labels, feature_names, output_file_param)
   print '='*100
