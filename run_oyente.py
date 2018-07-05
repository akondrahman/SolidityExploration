import os 
import subprocess 

def dumpContentIntoFile(strP, fileP):
  fileToWrite = open( fileP, 'w')
  fileToWrite.write(strP)
  fileToWrite.close()
  return str(os.stat(fileP).st_size)

def getOutputLines():
    file_lines = []
    with open('/V4/ANA_SOL_TMP.LOG', 'rU') as log_fil:
         file_str = log_fil.read()
         file_lines = file_str.split('\n')
    return file_lines


def getSolFiles(the_dir, out_f):
    str_ = ''
    for root_, dirnames, filenames in os.walk(the_dir):
        for file_ in filenames:
            full_file_path = os.path.join(root_, file_)
            if (full_file_path.endswith('.sol') and os.path.exists(full_file_path)):
                #print sol_file_full_path 
                cmd_of_interrest = " cd /home/oyente/oyente && source ../dependencies/venv/bin/activate && python oyente.py " + full_file_path + " > /V5/ANA_SOL_TMP.LOG "
                subprocess.check_output(['bash','-c', cmd_of_interrest])
                file_lines = getOutputLines()
                call_stac, concu_bug, time_depe, reent_bug = False, False, False, False 
                if len(file_lines) > 3: 
                    call_stac = [s_ for s_ in file_lines if 'CallStack' in s_][0].split(':')[1].strip()
                    concu_bug = [s_ for s_ in file_lines if 'Concurrency' in s_][0].split(':')[1].strip()
                    time_depe = [s_ for s_ in file_lines if 'Time' in s_][0].split(':')[1].strip()
                    reent_bug = [s_ for s_ in file_lines if 'Reentrancy' in s_][0].split(':')[1].strip() 
                
                    print "File:{}, CallstackError:{}, Concurrency:{}, TimeDependency:{}, ReentryBug:{}".format(full_file_path, call_stac, concu_bug, time_depe, reent_bug) 
                    str_ = str_ + full_file_path + ',' +  str(call_stac) + ',' + str(concu_bug) + ',' + str(time_depe) + ',' + str(reent_bug) + '\n'
                    print "*"*50  
    str_ = 'FILE,CALLSTACK,CONCURRENCY,TIME,REENTRY' + '\n' + str_
    out_sta = dumpContentIntoFile(str_, out_f)
    print 'Dumped a file of {} bytes'.format(out_sta) 

if __name__=='__main__': 
   inp_dir = '/V5/'
   out_file = '/V5/FINAL_SECU_BUG.csv' 
   getSolFiles(inp_dir, out_file)    
