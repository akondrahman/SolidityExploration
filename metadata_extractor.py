'''
Parse Json to extract metadata 
Akond Rahman
July 02, 2018 
'''
import os 
import csv 
import requests
import json
import pandas as pd 

def getOutputLines(file_name):
    file_lines = []
    with open(file_name, 'rU') as fil:
         file_str = fil.read()
         file_lines = file_str.split('\n')
    return file_lines

def getMetaDataField(field_, str_list):
    val_to_ret = 0
    line = [ s_ for s_ in str_list if field_ in s_]
    if (len(line) > 0 ):
        if ':' in line[0]:
            val_to_ret =  line[0].split(':')[-1].split(',')[0].strip()
            if val_to_ret == 'false':
               val_to_ret = 0 
            if val_to_ret == 'true':
               val_to_ret = 1        
            # print 'asi mama:', val_to_ret
    return str(val_to_ret)

def getCreationDateField(str_list):
    val_to_ret = 0
    line = [ s_ for s_ in str_list if '"created_at":' in s_]
    if (len(line) > 0 ):
        if ':' in line[0]:
            val_to_ret =  line[0].split('"')[3].split('T')[0].strip()
    return str(val_to_ret)
        
def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP )
    fileToWrite.close()
    return str(os.stat(fileP).st_size)


def getMetaData(json_dir_name):
    str_ = ''
    for root_, dirnames, filenames in os.walk(json_dir_name):
        for file_ in filenames:
            if (file_.endswith('json')):
               names = file_.split('_')
               if len(names) > 1: 
                 repo_name = names[0] + '/' + names[1]
                 dir_name = names[1]
                 full_p_file = os.path.join(root_, file_)
                 if (os.path.exists(full_p_file)):
                    the_lines=getOutputLines(full_p_file)
                    fork_data    = getMetaDataField('"fork":', the_lines)
                    watcher_data = getMetaDataField('"watchers":', the_lines)
                    stars_data   = getMetaDataField('"stargazers_count":', the_lines)
                    start_ts     = getCreationDateField( the_lines)
                    start_data   = start_ts.split('T')[0]
                    the_str      = repo_name + ',' + dir_name + ',' + fork_data + ',' + watcher_data + ',' + stars_data + ',' + start_data  + '\n'
                    # print the_str
                    str_ = str_ + the_str
    str_ = 'repo,dir,fork,watcher,star,start_date' + '\n'  + str_
    return str_

def processRESTCall(url_param):
    header = {'Authorization': 'token TOKEN_GOES_HERE'}
    r_obj  = requests.get(url_param, headers=header)
    contributors = r_obj.json()
    return len(contributors), contributors
    


def getGithubURL(the_file, json_dump_dir_param, repo_name):
    all_lines = getOutputLines(the_file)
    line = [ s_ for s_ in all_lines if 'contributors_url' in s_]    
    if len(line) > 0 :
        if ':' in line[0]:
            # api_url =  line[0].split(':')[-1].split(',')[0].strip()        
            api_url =  line[0].split('"')[3].strip()                    
            dev_cnt , dev_dict_json = processRESTCall(api_url)
            contrib_json = json_dump_dir_param + repo_name + '.json'
            with open(contrib_json, 'w') as outfile:
                 json.dump(dev_dict_json, outfile)
            print api_url, dev_cnt
            return dev_cnt
            
       

 
def getDevCount(inp_fil, json_root, json_dump_dir_param):
    # print inp_fil
    contrib_str = ''
    with open(inp_fil, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
          repo_name_ = row_[0]                  
          dir_name_  = row_[1]
          forks_     = row_[2]      ### fork 0 means no fork, 1 means it's a fork             
          watchers_  = row_[3]
          stars      = row_[4]
          file_to_look = json_root + repo_name_.replace('/', '_')
          # print file_to_look
          if os.path.exists(file_to_look):
             devs=getGithubURL(file_to_look, json_dump_dir_param, dir_name_)
             the_str = repo_name_ + ',' + dir_name_ + ',' + forks_ + ',' + watchers_ + ',' + stars + ',' + str(devs)  + '\n'
             contrib_str = contrib_str + the_str
    contrib_str = 'repo,dir,fork,watcher,star,dev' + '\n' + contrib_str 
    return contrib_str


if __name__=='__main__':
    # json_dir = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V5/metadata/'
    # out_str = getMetaData(json_dir)
    # dumpContentIntoFile(out_str, 'metadata_forks_stars_watchers_starttime_output.csv')


    '''
    do not forget to provide the token 
    '''
    meta_data_input_file = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V5/metadata_filtered_list.csv'
    json_dir = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V5/metadata/'
    json_dump_dir = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V5/metadata/contrib_json/'
    dev_count_str = getDevCount(meta_data_input_file, json_dir, json_dump_dir)
    dumpContentIntoFile(dev_count_str, json_dir + 'metadata.devs.csv')


    
