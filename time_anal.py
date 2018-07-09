'''
Akond Rahman 
July 08, 2018 
Script to prepapre data for temporal analysis
'''
import pandas as pd
import numpy as np
import os 

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP )
    fileToWrite.close()
    return str(os.stat(fileP).st_size) 

def generateCSV(file_para, out_file):
    full_df = pd.read_csv(file_para)
    all_months = full_df['CREATION_DATE'].tolist()
    uni_months = np.unique(all_months)
    #print uni_months
    mon_lis  = []
    str_ = ''
    for month in uni_months:
        sol_files = full_df[full_df['CREATION_DATE']==month]['file_'].tolist()
        uni_sol_files = np.unique(sol_files)
        mon_lis.append((month, len(uni_sol_files)))
    for val_ in mon_lis:
        str_ = str_ + str(val_[0]) + ',' + str(val_[1]) + '\n'
    str_ = 'MONTH,COUNT' + '\n' + str_
    dumpContentIntoFile(str_, out_file)

if __name__=='__main__':
   the_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/FINAL_PROCESS_GITHUB.csv'
   output  = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/FINAL_MONTH_WISE_COUNT.csv'
   generateCSV(the_fil, output)