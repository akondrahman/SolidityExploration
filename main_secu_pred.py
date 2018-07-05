'''
Akond Rahman
July 04, 2018
'''

from sklearn.ensemble import ExtraTreesClassifier
from sklearn import decomposition
import process_metric_utility , numpy as np , pandas as pd, sklearn_utility


print "Started at:", process_metric_utility.giveTimeStamp()
print "-"*50

dataset_file= '/Users/akond.rahman/Documents/Personal/misc/solidity_output/LOCKED_FINAL_GITHUB.csv'

print "The dataset is:", dataset_file
print "-"*50
full_dataset_from_csv = process_metric_utility.getDatasetFromCSV(dataset_file)
full_rows, full_cols = np.shape(full_dataset_from_csv)
print "Total number of columns", full_cols

feature_cols = full_cols - 1  ## the last column is defect status, so one column to skip
all_features = full_dataset_from_csv[:, 2:feature_cols]

dataset_for_labels = process_metric_utility.getDatasetFromCSV(dataset_file) 
label_cols = full_cols - 1 ### FOR FIEL LEVEL

all_labels  =  dataset_for_labels[:, label_cols]

defected_file_count     = len([x_ for x_ in all_labels if x_==1.0])
non_defected_file_count = len([x_ for x_ in all_labels if x_==0.0])
print "No of. defects={}, non-defects={}".format(defected_file_count, non_defected_file_count)
print "-"*50

'''
lets transform all the features via log transformation
'''
log_transformed_features = process_metric_utility.createLogTransformedFeatures(all_features)
feature_input_for_pca = log_transformed_features
'''
PCA ZONE
'''
pca_comp = 7 ###  must be less than or equal to no of features
pcaObj = decomposition.PCA(n_components=pca_comp)
pcaObj.fit(feature_input_for_pca)
# variance of features
variance_of_features = pcaObj.explained_variance_
# how much variance is explained each component
variance_ratio_of_features = pcaObj.explained_variance_ratio_
print "Explained varaince ratio"
for index_ in xrange(len(variance_ratio_of_features)):
    print "Principal component#{}, explained variance:{}".format(index_+1, variance_ratio_of_features[index_])
print "-"*50
no_features_to_use = 4 #using one PCA you get lesser accuracy
pcaObj.n_components=no_features_to_use
selected_features = pcaObj.fit_transform(feature_input_for_pca)
print "Selected feature dataset size:", np.shape(selected_features)
print "-"*50

outputDir = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/PRED-NODE-OUTPUT-' +   dataset_file.split('/')[-1] + '/'
process_metric_utility.createOutputDirectory(outputDir)
print 'Output directory created ...'
sklearn_utility.performIterativeModeling(selected_features, all_labels, 10, 10, outputDir)
print "-"*50
print "The dataset was:", dataset_file
print "-"*50
print "Ended at:", process_metric_utility.giveTimeStamp()
