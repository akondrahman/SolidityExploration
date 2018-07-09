'''
Akond Rahman 
July 08, 2018 
Script to prepapre data for temporal analysis
'''
import pandas as pd
import numpy as np

def generateCSV(file_para):
    full_df = pd.read_csv(file_para)
    all_months = full_df['CREATION_DATE'].tolist()
    uni_months = np.unique(all_months)
    #print uni_months
    for month in uni_months:
        sol_files = full_df[full_df['CREATION_DATE']==month]['file_'].tolist()
        uni_sol_files = np.unique(sol_files)
        print month
        print uni_sol_files 
        print '='*50


if __name__=='__main__':
   the_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/FINAL_PROCESS_GITHUB.csv'
   generateCSV(the_fil)