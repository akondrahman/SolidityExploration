'''
Akond Rahman 
Script to get time wise repos 
June 22, 2018 
'''
import os 
import shutil
import pandas as pd 
import numpy as np
import itertools
from datetime import datetime
import subprocess

def genValidMonths(s_mon, e_mon, y_l, m_l):
    valid_months = []

    s_year = int(s_mon.split('-')[0])
    s_mont = int(s_mon.split('-')[-1])

    e_year = int(e_mon.split('-')[0])
    e_mont = int(e_mon.split('-')[-1])

    sta_ = datetime(s_year, s_mont, 1)
    end_ = datetime(e_year, e_mont, 1)

    all_mon = list(itertools.product(y_l, m_l)) 
    for mont_ in all_mon:
        cand_mont = datetime(mont_[0], mont_[1], 1)
        # print cand_mont, sta_, end_
        if ( (cand_mont >= sta_) and (cand_mont <= end_) ):
           valid_months.append(cand_mont)
        #    print 'asi mama'
        #    print '*'*50
    return valid_months


def resetTheDir(src, des, val_mon):
    repo_name = src.split('/')[-2]

    year_ = val_mon.year
    mont_ = val_mon.month
 
    folder2create = des + repo_name + '-' + str(year_) + '-' + str(mont_) + '/'
 
    print '='*50
    print folder2create
    print '-'*25
    if((os.path.exists(folder2create))==False):
        print src, folder2create, year_, mont_
        try:
          shutil.copytree(src, folder2create)
          '''
          now  do a reset
          '''
          cdCommand            = "cd " + folder2create + " ; "
          date2reset           = year_ + '-' + mont_ + '-' + '28'  ## 28 th of the month
          commitCommand        = "git checkout -f `git rev-list -n 1 --before='"+ date2reset +"' master`"
          command2Run          = cdCommand + commitCommand
          try:
            subprocess.check_output(['bash','-c', command2Run])
          except subprocess.CalledProcessError as subpro_err:
            print 'Subprocess error:', subpro_err
        except shutil.Error as err_:
            print 'Directory not copied, error:', err_
    print '='*50


def generatePastData(file_inp, y_l, m_l):
    df_ = pd.read_csv(file_inp) 
    repo_names  = np.unique(df_['REPO'].tolist())    
    for repo_ in repo_names:
        start_month_list = df_[df_['REPO']==repo_]['START_MONTH'].tolist()  
        end_month_list   = df_[df_['REPO']==repo_]['END_MONTH'].tolist()
        start_month_list.sort()
        end_month_list.sort()
        # print repo_, start_month_list, end_month_list 
        # print '-'*25    
        sta_mon = start_month_list[0]  ## start month list is already sorted 
        end_mon = end_month_list[-1]  ## start month list is already sorted 
        val_mon_lis = genValidMonths(sta_mon, end_mon, y_l, m_l)
        for val_mon in val_mon_lis:
            srcDir = repo_
            desDir = '/Users/akond.rahman/Documents/Personal/misc/sol_time_data/'
            resetTheDir(srcDir, desDir, val_mon)
           

if __name__=='__main__':
   dt_fi = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/DATE.GITHUB.ALL.LOCKED.csv'
   year_list, mont_list = [2015, 2016, 2017, 2018], [x_+1 for x_ in xrange(12)]
   generatePastData(dt_fi, year_list, mont_list)   