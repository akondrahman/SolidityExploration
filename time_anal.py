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
    print uni_months


if __name__=='__main__':
   the_fil = ''
   generateCSV(the_fil)