'''
Akond Rahman
Extra IEEE Software 
Nov 19, 2019 
'''
import pandas as pd 

def getDensityData(lint_file, metric_file, density_output_file):
    lint_df   = pd.read_csv(lint_file) 
    lint_df   = lint_df.set_index('file_')
    metric_df = pd.read_csv(metric_file) 
    metric_df = metric_df.set_index('file_')
    merged_df = lint_df.merge(metric_df, left_index=True, right_index=True)

    print(merged_df.head())

if __name__=='__main__':
    lint_output_file   = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/ncsu_research/solidity-nier2018/results/V2/FINAL_SECU_SOLHINT.csv'
    metric_output_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/ncsu_research/solidity-nier2018/results/V2/FINAL_PROCESS_GITHUB_PROCESSED.csv'
    lint_density_output_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/ncsu_research/solidity-nier2018/results/V3/FINAL_DENSITY_METRICS.csv'

    getDensityData(lint_output_file, metric_output_file, lint_density_output_file) 

    