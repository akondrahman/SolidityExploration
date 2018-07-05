'''
Akond Rahman 
July 02, 2018 
final list of repos 
'''
import os 
import shutil
import csv 

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP )
    fileToWrite.close()
    return str(os.stat(fileP).st_size)


def getOutputLines(file_name):
    file_lines = []
    with open(file_name, 'rU') as fil:
         file_str = fil.read()
         file_lines = file_str.split('\n')
    file_lines = [x_.split('.')[0] for x_ in file_lines if x_ != '\n']
    return file_lines

def finalizeDirs(dir_name_p, valid_list, out_dir_nam):
    for dir_name in os.listdir(dir_name_p):
            full_dir_name = dir_name_p + dir_name + '/'
            dest_folder   = out_dir_nam + dir_name
            try:
               shutil.copytree(full_dir_name, dest_folder)
            except shutil.Error as err_:
               print 'Directory not copied, error:', err_

if __name__=='__main__':
   root_dir = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V5/gh-sol-repos/'
   final_list_file = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V5/sol.file.list.txt'
   final_list = getOutputLines(final_list_file)
   output_dir = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V5/final_repos/'
   finalizeDirs(root_dir, final_list, output_dir)