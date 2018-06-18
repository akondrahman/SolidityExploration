'''
Akond Rahman
Process extractor from git repositories
April 01, 2017
Need to modify to handle appropraite number
of metrics to be generated
'''
import math
import os, subprocess, numpy as np, operator
from  collections import Counter
from  scipy.stats import entropy
monthDict            = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
                         'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}


def getCommitCount(param_file_path, repo_path):
   totalCountForChurn = 0

   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   commitCommand        = "git log  --format=%cd " + theFile + " | awk '{ print $2 $3 $5}' | sed -e 's/ /,/g'"
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   dt_churn_output = [x_ for x_ in dt_churn_output if x_!='']
   totalCountForChurn = len(dt_churn_output)
   #print totalCountForChurn
   return totalCountForChurn

def calculateMonthDiffFromTwoDates(early, latest):
    from datetime import datetime
    early_year   = early.split('-')[0]
    latest_year  = latest.split('-')[0]
    early_month  = early.split('-')[-1]
    latest_month = latest.split('-')[-1]
    early_dt     = datetime(int(early_year), int(early_month), 1)
    latest_dt    = datetime(int(latest_year), int(latest_month), 1)

    return (latest_dt.year - early_dt.year)*12 + latest_dt.month - early_dt.month
def getAge(param_file_path, repo_path):
   totalCountForChurn   = 0

   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   commitCommand        = "git log  --format=%cd " + theFile + " | awk '{ print $2 $3 $5}' | sed -e 's/ /,/g'"
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   dt_churn_output = [x_ for x_ in dt_churn_output if x_!='']
   #print dt_churn_output
   monthList = [dob[0:3] for dob in  dt_churn_output]
   yearist = [dob[-4:] for dob in  dt_churn_output]
   monthAndYeatList = [dob[-4:] + '-' + monthDict[dob[0:3]] for dob in dt_churn_output]
   monthAndYeatList.sort()
   #print monthAndYeatList
   earliesttMonth  = monthAndYeatList[0]
   latesttMonth    = monthAndYeatList[-1]
   age = str(calculateMonthDiffFromTwoDates(earliesttMonth, latesttMonth))
   #print age
   return age



def getUniqueDevCount(param_file_path, repo_path):

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   #print "full path: {}, repo path:{}, theFile:{}".format(param_file_path, repo_path, theFile)
   commitCountCmd    = " git blame "+ theFile +"  | awk '{print $2}' | cut -d'(' -f2 "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   author_count_output = [x_ for x_ in author_count_output if x_!='']
   author_count        = len(np.unique(author_count_output))
   #print author_count
   return author_count

def getProgrammerMultiTasking(param_file_path, repo_path, dict_):
   '''
    first get all the programmers
   '''
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   commitCountCmd    = " git blame "+ theFile +"  | awk '{print $2}' | cut -d'(' -f2 "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   progr_name_output   = commit_count_output.split('\n')
   progr_name_output   = [x_ for x_ in progr_name_output if x_!='']

   sol_mt_prog_list, non_sol_mt_prog_list = [], []
   for progr_ in progr_name_output:
       if progr_ in dict_:
          all_files_worked          = dict_[progr_] # this is a list of files tocuhed by the programmer
          sol_files_worked          = [x_ for x_ in all_files_worked if '.sol' in x_]
          non_sol_files_worked      = [x_ for x_ in all_files_worked if '.sol' not in x_]
          uni_sol_files_worked      = np.unique(sol_files_worked)
          uni_non_sol_files_worked  = np.unique(non_sol_files_worked)
          # if each programmer worked on more solidity files, then the programmer is multi tasking for Puppet files
          # if each programmer worked on more non solidity files, then the programmer is multi tasking for non-Puppet files
          if (len(uni_sol_files_worked) > 1):
              sol_mt_prog_list.append(progr_)
          if (len(uni_non_sol_files_worked) > 1):
              non_sol_mt_prog_list.append(progr_)
   return len(np.unique(sol_mt_prog_list)), len(np.unique(non_sol_mt_prog_list))



def getAvgConsecutiveTimeDiff(month_year_list_param):
    counter = 0
    consecList = []
    len_    = len(month_year_list_param)
    for index_ in xrange(len_):
        first_  = month_year_list_param[index_]
        if((index_+1) < len_):
          second_ = month_year_list_param[index_+1]
          month_diff = calculateMonthDiffFromTwoDates(first_, second_)
          consecList.append(month_diff)
    #print consecList
    avg_month_diff = round(np.mean(consecList), 5)
    return avg_month_diff


def getAverageTimeBetweenEdits(param_file_path, repo_path):

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   commitCommand     = "git log  --format=%cd " + theFile + " | awk '{ print $2 $3 $5}' | sed -e 's/ /,/g'"
   command2Run       = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   dt_churn_output = [x_ for x_ in dt_churn_output if x_!='']
   #print dt_churn_output
   monthList = [dob[0:3] for dob in  dt_churn_output]
   yearist = [dob[-4:] for dob in  dt_churn_output]
   monthAndYeatList = [dob[-4:] + '-' + monthDict[dob[0:3]] for dob in dt_churn_output]
   monthAndYeatList.sort()
   #print monthAndYeatList
   avgConsecutiveTimeDiff = getAvgConsecutiveTimeDiff(monthAndYeatList)
   if((avgConsecutiveTimeDiff == float("NaN")) or (avgConsecutiveTimeDiff == float("NaN"))):
        avgConsecutiveTimeDiff = float(0)
   #print avgConsecutiveTimeDiff
   return avgConsecutiveTimeDiff

def getAddedChurnMetrics(param_file_path, repo_path):
   totalAddedLinesForChurn = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnAddedCommand = " git log --numstat --oneline "+ theFile +" | grep '" + theFile + "' | awk '{ print $1 }' "
   command2Run = cdCommand + churnAddedCommand

   add_churn_output = subprocess.check_output(['bash','-c', command2Run])
   add_churn_output = add_churn_output.split('\n')
   add_churn_output = [x_ for x_ in add_churn_output if x_!='']
   #print add_churn_output
   add_churn_output = [int(y_) for y_ in add_churn_output if y_.isdigit()]
   #print add_churn_output
   totalAddedLinesForChurn = sum(add_churn_output)
   #print totalAddedLinesForChurn
   return totalAddedLinesForChurn




def getDeletedChurnMetrics(param_file_path, repo_path):
   totalDeletedLinesForChurn = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnDeletedCommand = " git log --numstat --oneline "+ theFile +" | grep '" + theFile + "' | awk '{ print $2 }' "
   command2Run = cdCommand + churnDeletedCommand

   del_churn_output = subprocess.check_output(['bash','-c', command2Run])
   del_churn_output = del_churn_output.split('\n')
   del_churn_output = [x_ for x_ in del_churn_output if x_!='']
   del_churn_output = [int(y_) for y_ in del_churn_output if y_.isdigit()]
   #print del_churn_output
   totalDeletedLinesForChurn = sum(del_churn_output)
   #print totalDeletedLinesForChurn
   return totalDeletedLinesForChurn




def getAverageAndTotalChangedLines(param_file_path, repo_path):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnDeletedCommand = " git log --numstat --oneline "+ theFile +" | grep '" + theFile + "' | awk '{ print $2 }' "
   command2Run = cdCommand + churnDeletedCommand

   del_churn_output = subprocess.check_output(['bash','-c', command2Run])
   del_churn_output = del_churn_output.split('\n')
   del_churn_output = [x_ for x_ in del_churn_output if x_!='']
   del_churn_output = [int(y_) for y_ in del_churn_output if y_.isdigit()]

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnAddedCommand = " git log --numstat --oneline "+ theFile +" | grep '" + theFile + "' | awk '{ print $1 }' "
   command2Run = cdCommand + churnAddedCommand

   add_churn_output = subprocess.check_output(['bash','-c', command2Run])
   add_churn_output = add_churn_output.split('\n')
   add_churn_output = [x_ for x_ in add_churn_output if x_!='']
   add_churn_output = [int(y_) for y_ in add_churn_output if y_.isdigit()]

   chanegHolder     = add_churn_output + del_churn_output
   #print chanegHolder
   avgChangeLOC     = np.mean(chanegHolder)
   sumChangeLOC     = sum(chanegHolder)
   #print avgChangeLOC
   return avgChangeLOC, sumChangeLOC

def getMinorContribCount(param_file_path, repo_path, sloc):
   minorList = []
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame " + theFile + "  | awk '{print $2}'  | cut -d'(' -f2"
   command2Run       = cdCommand + blameCommand

   blame_output   = subprocess.check_output(['bash','-c', command2Run])
   blame_output   = blame_output.split('\n')
   blame_output   = [x_ for x_ in blame_output if x_!='']
   author_contrib = dict(Counter(blame_output))
   #print author_contrib
   for author, contribs in author_contrib.items():
      if((float(contribs)/float(sloc)) < 0.05):
        minorList.append(author)
   return len(minorList)


# useful for task/responsibility switching as well

def getHighestContribsPerc(param_file_path, repo_path, sloc):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame " + theFile + "  | awk '{print $2}'  | cut -d'(' -f2"
   command2Run       = cdCommand + blameCommand

   blame_output     = subprocess.check_output(['bash','-c', command2Run])
   blame_output     = blame_output.split('\n')
   blame_output     = [x_ for x_ in blame_output if x_!='']
   author_contrib   = dict(Counter(blame_output))
   #print author_contrib
   if (len(author_contrib) > 0):
     highest_author   = max(author_contrib.iteritems(), key=operator.itemgetter(1))[0]
     highest_contr    = author_contrib[highest_author]
     #print "LOC:{}, A:{}, C:{}, dict:{}".format(sloc, highest_author, highest_contr, author_contrib)
   else:
     highest_contr = 0
   if sloc <= 0 :
       sloc += 1
   return (round(float(highest_contr)/float(sloc), 5))*100

def getDeveloperScatternessOfFile(param_file_path, repo_path, sloc):
   '''
   output list
   '''
   lineNoProb        = []
   lineNoCnt         = []
   '''
   '''
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame -n " + theFile + " | awk '{print $2}' "
   command2Run       = cdCommand + blameCommand
   lineNoProb        = []

   blame_output      = subprocess.check_output(['bash','-c', command2Run])
   blame_output      = blame_output.split('\n')
   blame_output      = [x_ for x_ in blame_output if x_!='']
   line_chng_dict    = dict(Counter(blame_output))
   #print line_chng_dict
   for lineNo in xrange(sloc):
       line_key  = str(lineNo + 1)
       if (line_key in line_chng_dict):
          line_cnt  = line_chng_dict[line_key]
       else:
          line_cnt  = 0
       line_prob = float(line_cnt)/float(sloc)
       lineNoProb.append(line_prob) ### Version 1
       lineNoCnt.append(line_cnt)   ### Version 2
   #print "len:{}, list:{}, loc:{}".format(len(lineNoProb), lineNoProb, sloc)
   scatterness_prob = round(entropy(lineNoProb), 5)  ##Version 1
   scatterness_cnt  = round(entropy(lineNoCnt), 5)  ##Version 2
   '''
   handling -inf, inf, nan
   '''
   if((scatterness_cnt == float("-inf")) or (scatterness_cnt == float("inf")) or (scatterness_cnt == float("nan")) or math.isnan(scatterness_cnt)):
     scatterness_cnt = float(0)
   #print "list:{} ...\n prob->entropy:{}".format(lineNoProb, scatterness_prob)
   #print "list:{} ...\n count->entropy:{} ...sloc:{}".format(lineNoCnt, scatterness_cnt, sloc)
   #return scatterness_prob, scatterness_cnt
   return scatterness_cnt



def getProcessMetrics(file_path_p, repo_path_p, prog_to_file_dict):
    #get commit count
    COMM = getCommitCount(file_path_p, repo_path_p)
    #get age
    AGE  = getAge(file_path_p, repo_path_p)
    #get DEV
    DEV = getUniqueDevCount(file_path_p, repo_path_p)
    #get AVERAGE TIME BETWEEN EDITS
    AVGTIMEOFEDITS = getAverageTimeBetweenEdits(file_path_p, repo_path_p)
    #get total lines added
    ADDTOTALLINES  = getAddedChurnMetrics(file_path_p, repo_path_p)
    # get SLOC
    LOC            = sum(1 for line in open(file_path_p))

    #get total lines deleted
    DELETETOTALLINES  = getDeletedChurnMetrics(file_path_p, repo_path_p)

    if (LOC > 0):
       ##Addition Per LOC
       ADDPERLOC      = round(float(ADDTOTALLINES)/float(LOC), 5)
       ##Deletion Per LOC
       DELPERLOC      = round(float(DELETETOTALLINES)/float(LOC), 5)
    else:
        ADDPERLOC = float(0)
        DELPERLOC = float(0)



    ### TOTAL LINES CHANGED
    TOT_LOC_CHNG = ADDTOTALLINES + DELETETOTALLINES
    if(TOT_LOC_CHNG > 0):
      ##Addition Normalized
      ADDNORM      = round(float(ADDTOTALLINES)/float(TOT_LOC_CHNG), 5)
      ##Deletion Normalized
      DELNORM      = round(float(DELETETOTALLINES)/float(TOT_LOC_CHNG), 5)
    else:
      ##Addition Normalized
      ADDNORM      = float(0)
      ##Deletion Normalized
      DELNORM      = float(0)

    ### AVG CHANGED LINES PER COMMIT
    AVGCHNG, SUMCHNG      = getAverageAndTotalChangedLines(file_path_p, repo_path_p)

    ### GET MINOR CONTRIBUTOR COUNT
    MINOR        = getMinorContribCount(file_path_p, repo_path_p, LOC)
    ### GET HIGHEST CONTRIBUTOR's Authored lines
    OWN          = getHighestContribsPerc(file_path_p, repo_path_p, LOC)
    ### GET Scatterness of a file
    SCTR         = getDeveloperScatternessOfFile(file_path_p, repo_path_p, LOC)
    if(LOC > 0):
      ### GET total lines of code changed per SLOC
      TOTCHNGPERLOC = round(float(TOT_LOC_CHNG)/float(LOC), 5)
    else:
        TOTCHNGPERLOC = float(0)

    '''
    added aug 06, 2017: three more metrics:
    1. programmers who work on other files
    2. programmers who work on other Puppet files
    3. size of commits
    '''

    #size of commits
    if COMM > 0:
        COMM_SIZE = round(float(TOT_LOC_CHNG)/float(COMM), 5)
    else:
        COMM_SIZE = float(0)

    #get programmer multi tasking within Puppet and non Puppet files
    prog_mt_pp_count, prog_mt_non_pp_count= getProgrammerMultiTasking(file_path_p, repo_path_p, prog_to_file_dict)
    if (DEV > 0):
       prog_mt_pp_perc,  prog_mt_non_pp_perc = round(float(prog_mt_pp_count)/float(DEV), 5), round(float(prog_mt_non_pp_count)/float(DEV), 5)
    else:
       prog_mt_pp_perc,  prog_mt_non_pp_perc = 0, 0

    ## all process metrics
    #all_process_metrics = str(COMM) + ',' + str(AGE) + ',' + str(DEV) + ',' + str(AVGTIMEOFEDITS) + ',' + str(ADDPERLOC) + ','
    all_process_metrics = str(COMM) + ',' + str(AGE) + ',' + str(DEV) + ',' + str(ADDPERLOC) + ','
    #all_process_metrics = all_process_metrics +  str(DELPERLOC) + ',' + str(ADDNORM) + ',' + str(DELNORM) + ','
    all_process_metrics = all_process_metrics +  str(DELPERLOC) + ',' + str(SUMCHNG) + ',' + str(TOTCHNGPERLOC) + ','
    # all_process_metrics = all_process_metrics + str(AVGCHNG) + ',' + str(MINOR) + ',' + str(OWN) + ',' + str(SCTR) + ','
    all_process_metrics = all_process_metrics + str(AVGCHNG) + ',' + str(MINOR) + ','  + str(SCTR) + ','

    #all_process_metrics = all_process_metrics + str(COMM_SIZE) + ',' + str(prog_mt_pp_perc) + ',' + str(prog_mt_non_pp_perc) + ','

    all_process_metrics = all_process_metrics + str(prog_mt_pp_perc) + ',' + str(prog_mt_non_pp_perc) + ','
    return all_process_metrics
