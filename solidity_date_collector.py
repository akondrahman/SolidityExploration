'''
Akond Rahman 
Collect Start and End Dates from Solidity files 
June 20, 2018 
'''
import os 
import csv  
import subprocess


def getRepoFromFileName(file_param, org_par):
    start_path = os.path.relpath(file_param, org_par)
    repo_name  = start_path.split('/')[0]
    repo_path  = org_par  + repo_name + '/'
    # print 'File:{}, start path:{}, repo name:{}, repo path:{}'.format(file_param, start_path, repo_name, repo_path)
    return repo_path

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP )
    fileToWrite.close()
    return str(os.stat(fileP).st_size)

def extractDateAllFiles(in_, out_, org_):
    str_dump = ''
    with open(in_, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
          file_name_ = row_[0]
          repo_ = getRepoFromFileName(file_name_, org_)
          start, end = extractDateSingleFile(file_name_, repo_)
          print file_name_, start, end 
          str_dump = str_dump + file_name_ + ',' + start + ',' + end + ',' + '\n'
          print '-'*50
    str_dump = 'FILE,START_MONTH,END_MONTH,' + '\n' + str_dump 
    out_byt=dumpContentIntoFile(str_dump, out_)
    print 'We dumped a file of {} bytes'.format(out_byt)


def extractDateSingleFile(param_file_path, repo_path):
   monthDict            = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
                         'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}    

   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   commitCommand        = "git log  --format=%cd " + theFile + " | awk '{ print $2 $3 $5}' | sed -e 's/ /,/g'"
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   dt_churn_output = [x_ for x_ in dt_churn_output if x_!='']

   monthAndYeatList = [dob[-4:] + '-' + monthDict[dob[0:3]] for dob in dt_churn_output]
   monthAndYeatList.sort()

   earliesttMonth  = monthAndYeatList[0]
   latesttMonth    = monthAndYeatList[-1]

   return str(earliesttMonth), str(latesttMonth)


if __name__=='__main__':
#    the_file = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/prior/GITHUB_V4_MEENELY.csv'
#    dt_out_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/DATE.GITHUB.V4.csv'    
#    org = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V4/'

#    the_file = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/prior/GITHUB_V3_MEENELY.csv'
#    dt_out_fil = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/DATE.GITHUB.V3.csv'    
#    org = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V3/'

   extractDateAllFiles(the_file, dt_out_fil, org)
   print '='*100