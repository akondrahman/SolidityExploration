'''
Sklearn items for prediction model
Akond Rahman
July 04, 2018
'''

from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np, pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation, svm
from sklearn.linear_model import RandomizedLogisticRegression, LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, mean_absolute_error, accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
import process_metric_utility




def dumpPredPerfValuesToFile(iterations, predPerfVector, fileName):
   str2write=''
   headerStr='AUC,FMEASURE,PRECISION,RECALL,'
   for cnt in xrange(iterations):
     auc_   = predPerfVector[0][cnt]
     fmeasure_   = predPerfVector[1][cnt]
     prec_  = predPerfVector[2][cnt]
     recal  = predPerfVector[3][cnt]
     str2write = str2write + str(auc_) + ',' + str(fmeasure_) + ',' + str(prec_) + ',' + str(recal) + ',' + '\n'
   str2write = headerStr + '\n' + str2write
   bytes_ = process_metric_utility.dumpContentIntoFile(str2write, fileName)
   print "Created {} of {} bytes".format(fileName, bytes_)




def evalClassifier(actualLabels, predictedLabels):
  '''
    the way skelarn treats is the following: first index -> lower index -> 0 -> 'Low'
                                             next index after first  -> next lower index -> 1 -> 'high'
  '''
  target_labels =  ['N', 'Y']
  '''
    peeking into the labels of the dataset
  '''
  #print "Glimpse at  actual:{}, and predicted:{} labels(10th entry in label list)".format(actualLabels[10], predictedLabels[10])
  print classification_report(actualLabels, predictedLabels, target_names=target_labels)
  print">"*25
  '''
  getting the confusion matrix
  '''
  #conf_matr_output = confusion_matrix(actualLabels, predictedLabels)
  print "Confusion matrix start"
  #print conf_matr_output
  conf_matr_output = pd.crosstab(actualLabels, predictedLabels, rownames=['True'], colnames=['Predicted'], margins=True)
  print conf_matr_output
  print "Confusion matrix end"
  # preserve the order first test(real values from dataset), then predcited (from the classifier )

  prec_ = precision_score(actualLabels, predictedLabels, average='binary')


  recall_ = recall_score(actualLabels, predictedLabels, average='binary')
  '''
    are under the curve values .... reff: http://gim.unmc.edu/dxtests/roc3.htm
    0.80~0.90 -> good, any thing less than 0.70 bad , 0.90~1.00 -> excellent
  '''

  area_roc_output = roc_auc_score(actualLabels, predictedLabels)
  # preserve the order first test(real values from dataset), then predcited (from the classifier )

  '''
  getting f score .... f score might get hugher values than AUC
  '''
  f1_score_output = f1_score(actualLabels, predictedLabels, average='binary')

  return area_roc_output, prec_, recall_, f1_score_output


def perform_cross_validation(classiferP, featuresP, labelsP, cross_vali_param, infoP):

  predicted_labels = cross_validation.cross_val_predict(classiferP, featuresP , labelsP, cv=cross_vali_param)
  area_roc_to_ret = evalClassifier(labelsP, predicted_labels)
  return area_roc_to_ret


def performCART(featureParam, labelParam, foldParam, infoP):
  theCARTModel = DecisionTreeClassifier()


  cart_area_under_roc = perform_cross_validation(theCARTModel, featureParam, labelParam, foldParam, infoP)
  print "For {}, area under ROC is: {}, f-measure is:{}".format(infoP, cart_area_under_roc[0], cart_area_under_roc[-1])
  return cart_area_under_roc

def performRF(featureParam, labelParam, foldParam, infoP):
  theRndForestModel = RandomForestClassifier()
  rf_area_under_roc = perform_cross_validation(theRndForestModel, featureParam, labelParam, foldParam, infoP)
  print "For {}, area under ROC is: {}, f-measure is:{}".format(infoP, rf_area_under_roc[0], rf_area_under_roc[-1])
  return rf_area_under_roc

def performSVC(featureParam, labelParam, foldParam, infoP):
  theSVMModel = svm.SVC(kernel='rbf').fit(featureParam, labelParam)
  svc_area_under_roc = perform_cross_validation(theSVMModel, featureParam, labelParam, foldParam, infoP)
  print "For {}, area under ROC is: {}, f-measure is:{}".format(infoP, svc_area_under_roc[0], svc_area_under_roc[-1])
  return svc_area_under_roc


def performLogiReg(featureParam, labelParam, foldParam, infoP):
  theLogisticModel = LogisticRegression()
  theLogisticModel.fit(featureParam, labelParam)
  logireg_area_under_roc = perform_cross_validation(theLogisticModel, featureParam, labelParam, foldParam, infoP)
  print "For {}, area under ROC is: {}, f-measure is:{}".format(infoP, logireg_area_under_roc[0], logireg_area_under_roc[-1])
  return logireg_area_under_roc



def performNaiveBayes(featureParam, labelParam, foldParam, infoP):
  theNBModel = GaussianNB()
  # theNBModel = BernoulliNB()  ### for parameter tuning
  theNBModel.fit(featureParam, labelParam)
  gnb_area_under_roc = perform_cross_validation(theNBModel, featureParam, labelParam, foldParam, infoP)
  print "For {}, area under ROC is: {}, f-measure is:{}".format(infoP, gnb_area_under_roc[0], gnb_area_under_roc[-1])
  return gnb_area_under_roc


def performIterativeModeling(featureParam, labelParam, foldParam, iterationP, outputDirParam):
  cart_prec_holder, cart_recall_holder, holder_cart, cart_fmeasure_holder = [], [], [], []
  rf_prec_holder,   rf_recall_holder,   holder_rf, rf_fmeasure_holder   = [], [], [], []
  svc_prec_holder,  svc_recall_holder,  holder_svc, svc_fmeasure_holder  = [], [], [], []
  logi_prec_holder, logi_recall_holder, holder_logi, logi_fmeasure_holder = [], [], [], []
  nb_prec_holder,   nb_recall_holder,   holder_nb, nb_fmeasure_holder   = [], [], [], []
  for ind_ in xrange(iterationP):
    ## iterative modeling for CART
    cart_area_roc, cart_prec_, cart_recall_, cart_fmeasure_ = performCART(featureParam, labelParam, foldParam, "CART")
    holder_cart.append(cart_area_roc)
    cart_prec_holder.append(cart_prec_)
    cart_recall_holder.append(cart_recall_)
    cart_fmeasure_holder.append(cart_fmeasure_)
    cart_area_roc = float(0)
    cart_prec_    = float(0)
    cart_recall_  = float(0)
    cart_fmeasure_ = float(0)

    ## iterative modeling for RF
    rf_area_roc, rf_prec_, rf_recall_, rf_fmeasure_ = performRF(featureParam, labelParam, foldParam, "Rand. Forest")
    holder_rf.append(rf_area_roc)
    rf_prec_holder.append(rf_prec_)
    rf_recall_holder.append(rf_recall_)
    rf_fmeasure_holder.append(rf_fmeasure_)
    rf_area_roc = float(0)
    rf_prec_    = float(0)
    rf_recall_  = float(0)
    rf_fmeasure_ = float(0)

    ## iterative modeling for SVC
    svc_area_roc, svc_prec_, svc_recall_, svc_fmeasure_ = performSVC(featureParam, labelParam, foldParam, "Supp. Vector Classi.")

    holder_svc.append(svc_area_roc)
    svc_prec_holder.append(svc_prec_)
    svc_recall_holder.append(svc_recall_)
    svc_fmeasure_holder.append(svc_fmeasure_)
    svc_area_roc = float(0)
    svc_prec_    = float(0)
    svc_recall_  = float(0)
    svc_fmeasure_ = float(0)


    ## iterative modeling for logistic regression
    logi_reg_area_roc, logi_reg_preci_, logi_reg_recall, logi_reg_fmeasure = performLogiReg(featureParam, labelParam, foldParam, "Logi. Regression Classi.")

    holder_logi.append(logi_reg_area_roc)
    logi_prec_holder.append(logi_reg_preci_)
    logi_recall_holder.append(logi_reg_recall)
    logi_fmeasure_holder.append(logi_reg_fmeasure)
    logi_reg_area_roc = float(0)
    logi_reg_preci_   = float(0)
    logi_reg_recall   = float(0)
    logi_reg_fmeasure = float(0)

    ## iterative modeling for naiev bayes
    nb_area_roc, nb_preci_, nb_recall, nb_fmeasure = performNaiveBayes(featureParam, labelParam, foldParam, "Naive Bayes")
    holder_nb.append(nb_area_roc)
    nb_prec_holder.append(nb_preci_)
    nb_recall_holder.append(nb_recall)
    nb_fmeasure_holder.append(nb_fmeasure)
    nb_area_roc = float(0)
    nb_preci_   = float(0)
    nb_recall   = float(0)
    nb_fmeasure = float(0)

  print "-"*50
  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("CART", np.mean(holder_cart),
                                                                          np.median(holder_cart), max(holder_cart),
                                                                          min(holder_cart))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("CART", np.mean(cart_prec_holder),
                                                                          np.median(cart_prec_holder), max(cart_prec_holder),
                                                                          min(cart_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("CART", np.mean(cart_recall_holder),
                                                                          np.median(cart_recall_holder), max(cart_recall_holder),
                                                                          min(cart_recall_holder))
  print "*"*25
  print "Summary: F-Measure, for:{}, mean:{}, median:{}, max:{}, min:{}".format("CART", np.mean(cart_fmeasure_holder),
                                                                          np.median(cart_fmeasure_holder), max(cart_fmeasure_holder),
                                                                          min(cart_fmeasure_holder))
  print "*"*25
  cart_all_pred_perf_values = (holder_cart, cart_fmeasure_holder, cart_prec_holder, cart_recall_holder)
  dumpPredPerfValuesToFile(iterationP, cart_all_pred_perf_values, outputDirParam +  'PRED_PERF_CART.csv')
  print "-"*50

  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Logi. Regression", np.mean(holder_logi),
                                                                          np.median(holder_logi), max(holder_logi),
                                                                          min(holder_logi))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Logi. Regression", np.mean(logi_prec_holder),
                                                                            np.median(logi_prec_holder), max(logi_prec_holder),
                                                                            min(logi_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Logi. Regression", np.mean(logi_recall_holder),
                                                                            np.median(logi_recall_holder), max(logi_recall_holder),
                                                                            min(logi_recall_holder))
  print "*"*25

  print "Summary: F-Measure, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Logi. Regression", np.mean(logi_fmeasure_holder),
                                                                            np.median(logi_fmeasure_holder), max(logi_fmeasure_holder),
                                                                            min(logi_fmeasure_holder))
  print "*"*25
  logireg_all_pred_perf_values = (holder_logi, logi_fmeasure_holder, logi_prec_holder, logi_recall_holder)
  dumpPredPerfValuesToFile(iterationP, logireg_all_pred_perf_values, outputDirParam + 'PRED_PERF_LOGIREG.csv')
  print "-"*50

  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Rand. Forest", np.mean(holder_rf),
                                                                          np.median(holder_rf), max(holder_rf),
                                                                          min(holder_rf))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Rand. Forest", np.mean(rf_prec_holder),
                                                                          np.median(rf_prec_holder), max(rf_prec_holder),
                                                                          min(rf_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Rand. Forest", np.mean(rf_recall_holder),
                                                                          np.median(rf_recall_holder), max(rf_recall_holder),
                                                                          min(rf_recall_holder))
  print "*"*25
  print "Summary: F-Measure, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Rand. Forest", np.mean(rf_fmeasure_holder),
                                                                          np.median(rf_fmeasure_holder), max(rf_fmeasure_holder),
                                                                          min(rf_fmeasure_holder))
  print "*"*25
  rf_all_pred_perf_values = (holder_rf, rf_fmeasure_holder, rf_prec_holder, rf_recall_holder)
  dumpPredPerfValuesToFile(iterationP, rf_all_pred_perf_values, outputDirParam +  'PRED_PERF_RF.csv')
  print "-"*50

  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("S. Vec. Class.", np.mean(holder_svc),
                                                                          np.median(holder_svc), max(holder_svc),
                                                                          min(holder_svc))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("S. Vec. Class.", np.mean(svc_prec_holder),
                                                                            np.median(svc_prec_holder), max(svc_prec_holder),
                                                                            min(svc_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("S. Vec. Class.", np.mean(svc_recall_holder),
                                                                            np.median(svc_recall_holder), max(svc_recall_holder),
                                                                            min(svc_recall_holder))
  print "*"*25
  print "Summary: F-Measure, for:{}, mean:{}, median:{}, max:{}, min:{}".format("S. Vec. Class", np.mean(svc_fmeasure_holder),
                                                                          np.median(svc_fmeasure_holder), max(svc_fmeasure_holder),
                                                                          min(svc_fmeasure_holder))
  print "*"*25

  svc_all_pred_perf_values = (holder_svc, svc_fmeasure_holder, svc_prec_holder, svc_recall_holder)
  dumpPredPerfValuesToFile(iterationP, svc_all_pred_perf_values, outputDirParam +  'PRED_PERF_SVC.csv')
  print "-"*50

  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Naive Bayes", np.mean(holder_nb),
                                                                          np.median(holder_nb), max(holder_nb),
                                                                          min(holder_nb))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Naive Bayes", np.mean(nb_prec_holder),
                                                                            np.median(nb_prec_holder), max(nb_prec_holder),
                                                                            min(nb_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Naive Bayes", np.mean(nb_recall_holder),
                                                                            np.median(nb_recall_holder), max(nb_recall_holder),
                                                                            min(nb_recall_holder))
  print "*"*25
  print "Summary: F-Measure, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Naive Bayes", np.mean(nb_fmeasure_holder),
                                                                            np.median(nb_fmeasure_holder), max(nb_fmeasure_holder),
                                                                            min(nb_fmeasure_holder))
  print "*"*25
  nb_all_pred_perf_values = (holder_nb, nb_fmeasure_holder, nb_prec_holder, nb_recall_holder)
  dumpPredPerfValuesToFile(iterationP, nb_all_pred_perf_values, outputDirParam + 'PRED_PERF_NB.csv')
  print "-"*50
