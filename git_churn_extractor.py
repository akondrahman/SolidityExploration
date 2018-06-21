'''
June 21, 2018
Churn of files belonging to git repos
'''
import os, subprocess, numpy as np

def getRelativeChurnMetrics(param_file_path, repo_path):
  churn_str_for_file= ""

  churn_added_lines = getAddedChurnMetrics(param_file_path, repo_path)
  churn_delet_lines = getDeletedChurnMetrics(param_file_path, repo_path)
  churn_total_lines = churn_added_lines + churn_delet_lines
  #print "Churn:add={}, churn:del={}, churn:total={}".format(churn_added_lines, churn_delet_lines, churn_total_lines)
  
  lines_for_file      = sum(1 for line in open(param_file_path))

  churn_total_days    = getDaysOfChurn(param_file_path, repo_path)
  churn_count_of_file = getCountOfChurn(param_file_path, repo_path)

  if(lines_for_file > 0):
    rel_churn_1 = float(churn_total_lines) / float(lines_for_file)
  else:
      rel_churn_1 = float(0)
  rel_churn_1 = round(rel_churn_1, 5)

  if(lines_for_file > 0 ):
    rel_churn_2 = float(churn_delet_lines) / float(lines_for_file)
  else:
      rel_churn_2 = float(0)
  rel_churn_2 = round(rel_churn_2, 5)

  if (churn_delet_lines > 0):
    rel_churn_3 = float(churn_total_lines) / float(churn_delet_lines)
    rel_churn_3 = round(rel_churn_3, 5)
  else:
    rel_churn_3 = float(0)

  if(lines_for_file > 0 ):
    rel_churn_4 = float(churn_total_days) / float(lines_for_file)
  else:
      rel_churn_4 = float(0)
  rel_churn_4 = round(rel_churn_4, 5)

  #churn_str_for_file = str(churn_total_lines) + "," + str(rel_churn_1) + "," + str(rel_churn_2) + "," + str(rel_churn_3) + "," + str(rel_churn_4) + "," + str(churn_count_of_file) + ","
  churn_str_for_file = str(churn_total_lines) + "," + str(rel_churn_1) + "," + str(rel_churn_2)  + "," + str(churn_count_of_file) + ","
  return churn_str_for_file




def getAddedChurnMetrics(param_file_path, repo_path):
   totalAddedLinesForChurn = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   #print "full path: {}, repo path:{}, theFile:{}".format(param_file_path, repo_path, theFile)
   churnAddedCommand = "git log --numstat --oneline " + theFile + " | grep -F '"+ theFile +"' |  awk '{ print $1 }' | sed -e  's/ /,/g'"
   command2Run = cdCommand + churnAddedCommand

   add_churn_output = subprocess.check_output(['bash','-c', command2Run])
   add_churn_output = add_churn_output.split('\n')
   add_churn_output = [x_ for x_ in add_churn_output if x_!='']
   #add_churn_output = [int(y_) for y_ in add_churn_output ]
   add_churn_output = [int(y_) for y_ in add_churn_output if y_.isdigit()]
   #print add_churn_output
   totalAddedLinesForChurn = sum(add_churn_output)
   #print totalAddedLinesForChurn
   return totalAddedLinesForChurn



def getDeletedChurnMetrics(param_file_path, repo_path):
   totalDeletedLinesForChurn = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   #print "full path: {}, repo path:{}, theFile:{}".format(param_file_path, repo_path, theFile)
   churnDeletedCommand = "git log --numstat --oneline " + theFile + " | grep -F '"+ theFile +"' |  awk '{ print $2 }' | sed -e  's/ /,/g'"
   command2Run = cdCommand + churnDeletedCommand

   del_churn_output = subprocess.check_output(['bash','-c', command2Run])
   del_churn_output = del_churn_output.split('\n')
   del_churn_output = [x_ for x_ in del_churn_output if x_!='']
   #del_churn_output = [int(y_) for y_ in del_churn_output]
   del_churn_output = [int(y_) for y_ in del_churn_output if y_.isdigit()]
   #print del_churn_output
   totalDeletedLinesForChurn = sum(del_churn_output)
   #print totalDeletedLinesForChurn
   return totalDeletedLinesForChurn




def getDaysOfChurn(param_file_path, repo_path):
   totalDaysForChurn = 0

   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   churnDateTimeCommand = "git log  --format=%cd " + theFile + " | awk '{ print $2 $3 $5}' | sed -e 's/ /,/g'"
   command2Run          = cdCommand + churnDateTimeCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   dt_churn_output = [x_ for x_ in dt_churn_output if x_!='']
   dt_churn_output = np.unique(dt_churn_output)
   #print dt_churn_output
   totalDaysForChurn = len(dt_churn_output)
   #print totalDaysForChurn
   return totalDaysForChurn




def getCountOfChurn(param_file_path, repo_path):
   totalCountForChurn = 0

   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   churnDateTimeCommand = "git log  --format=%cd " + theFile + " | awk '{ print $2 $3 $5}' | sed -e 's/ /,/g'"
   command2Run          = cdCommand + churnDateTimeCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   dt_churn_output = [x_ for x_ in dt_churn_output if x_!='']
   totalCountForChurn = len(dt_churn_output)
   #print totalCountForChurn
   return totalCountForChurn
