'''
Akond Rahman 
Script to get time wise repos 
June 22, 2018 
'''
import os 
import shutil
import pandas as pd 
import numpy as np

def generatePastData(file_inp):
    df_ = pd.read_csv(file_inp) 
    repo_names  = np.unique(df_['REPO'].tolist())    
    for repo_ in repo_names:
        start_month_list = df_[df_['REPO']==repo_]['START_MONTH'].tolist()  
        end_month_list   = df_[df_['REPO']==repo_]['END_MONTH'].tolist()
        start_month_list.sort()
        end_month_list.sort()
        print repo_, start_month_list, end_month_list 
        print '-'*25    
        sta_mon = start_month_list[0]  ## start month list is already sorted 
        end_mon = end_month_list[-1]  ## start month list is already sorted 

if __name__=='__main__':
   dt_fi = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/DATE.GITHUB.ALL.LOCKED.csv'
   generatePastData(dt_fi)   