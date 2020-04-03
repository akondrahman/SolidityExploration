'''
Akond Rahman 
Mar 29, 2020 
Solidity Stuff 
'''
import pandas as pd 
import numpy as np 
import os 

def pointCorrectly(file_):
    file_ = file_.replace('/Users/akond/Summers/IBM_Internship_materials/', '/Users/arahman/SOLIDITY_REPOS/')
    return file_ 

def doFSENIERWork():
    bio_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/SO-CATEG-BIO/FINAL_SO_BIOINFORMATICS.csv'
    bio_df   = pd.read_csv(bio_file)

    filtered_df = bio_df[bio_df['FINAL']!='X']
    # print(filtered_df.head()) 

    categs = np.unique( filtered_df['FINAL'].tolist() )
    questions = np.unique( filtered_df['ID'].tolist() )
    print('Total questions:', len(questions))
    for categ_ in categs:
        categ_df    = filtered_df[filtered_df['FINAL']==categ_]
        categ_ques  = np.unique( categ_df['ID'].tolist() ) 
        categ_views = np.unique( categ_df['VIEWS'].tolist()  ) 
        print('*'*50)
        print('CATEG:{}, COUNT:{}, PROP_QUES:{}, VIEW_PER_QUES:{}'.format(categ_, len(categ_ques) , float(len(categ_ques) ) / float( len(questions) )  , float(sum(categ_views) ) / float( len(categ_ques) )  ) )
        print('*'*50)


if __name__ == '__main__':
    # SOL_LABEL_FILE = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/ncsu_research/solidity-nier2018/results/V3/FINAL_PROCESS_GITHUB_PROCESSED.csv'
    # df_ = pd.read_csv(SOL_LABEL_FILE) 
    # df_['FILE_PATH'] = df_['file_'].apply(pointCorrectly) 
    # print(df_.head()) 
    # df_.to_csv('/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/ncsu_research/solidity-nier2018/results/V4/FINAL_CODE_METRICS.csv', index=False, encoding='utf-8')


    # doFSENIERWork()


