import os
import subprocess
import csv 

def dumpContentIntoFile(strP, fileP):
  fileToWrite = open( fileP, 'w')
  fileToWrite.write(strP)
  fileToWrite.close()
  return str(os.stat(fileP).st_size)

def getOutputLines(dir_):
    file_lines = []
    with open(dir_ + 'ANA_SOL_TMP.LOG', 'rU') as log_fil:
         file_str = log_fil.read()
         file_lines = file_str.split('\n')
    return file_lines

def getSecuIssueCount(file_lines, the_str):
    cnt2ret = sum(the_str in s_ for s_ in file_lines)
    return cnt2ret

def getOyenteData(inp_fil):
    oyente_dict ={}
    getVal = lambda x: 1 if (x=='TRUE') else 0
    with open(inp_fil, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
          callst, concurr, time, reent = 0, 0, 0, 0
          file_name_ = row_[0]
          full_file_path = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources' + file_name_ 
          if os.path.exists(full_file_path):             
             CALLSTACK	 = row_[1]
             CONCURRENCY = row_[2]	
             TIME        = row_[3]
             REENTRANCY  = row_[4]
             callst, concurr, time, reent = getVal(CALLSTACK), getVal(CONCURRENCY), getVal(TIME), getVal(REENTRANCY)
             if full_file_path not in oyente_dict:
                oyente_dict[full_file_path] = (callst, concurr, time, reent)
    return oyente_dict



def getSolFiles(the_dir, out_f, oyente_param):
    str_ = ''
    for root_, dirnames, filenames in os.walk(the_dir):
        for file_ in filenames:
            full_file_path = os.path.join(root_, file_)
            if full_file_path.endswith('.sol'):        
                avoid_throw, reentrancy, avoid_sha, avoid_sui, func_visi, state_vis, check_send, avoid_call, comp_fix = 0, 0, 0, 0, 0, 0, 0, 0, 0
                comp_gt, comp_fall, call_contr, mult_send, simp_even, tx_orig, inli_asse, block_hash, low_level = 0, 0, 0, 0, 0, 0, 0, 0, 0
                if os.path.exists(full_file_path):
                   sloc_for_file      = sum(1 for line in open(full_file_path))
                   if sloc_for_file > 1:
                     print full_file_path
                     cmd_of_interrest = "solhint -f unix " + full_file_path + " > " + the_dir + "ANA_SOL_TMP.LOG"
                     try:
                        subprocess.check_output(['bash','-c', cmd_of_interrest])
                     except subprocess.CalledProcessError as e_:
                        print 'Interesting ...' + str(e_)
                     file_lines = getOutputLines(the_dir)
                     # print file_lines
                     callst, concurr, time, reent = 0, 0, 0, 0
                     if full_file_path in oyente_param:
                        callst, concurr, time, reent = oyente_param[full_file_path]

                     avoid_throw = getSecuIssueCount(file_lines, 'Error/avoid-throw')
                     reentrancy  = getSecuIssueCount(file_lines, 'Error/reentrancy')
                     avoid_sha   =  getSecuIssueCount(file_lines, 'Error/avoid-sha3')
                     avoid_sui   = getSecuIssueCount(file_lines, 'Error/avoid-suicide')
                     func_visi   =  getSecuIssueCount(file_lines, 'Error/func-visibility')
                     state_vis   =  getSecuIssueCount(file_lines, 'Error/state-visibility')
                     check_send  =  getSecuIssueCount(file_lines, 'Error/check-send-result')
                     avoid_call  =  getSecuIssueCount(file_lines, 'Error/avoid-call-value')
                     comp_fix    = getSecuIssueCount(file_lines, 'Error/compiler-fixed')
                     comp_gt     =  getSecuIssueCount(file_lines, 'Error/compiler-gt-0_4')
                     comp_fall   = getSecuIssueCount(file_lines, 'Error/no-complex-fallback')
                     call_contr  =  getSecuIssueCount(file_lines, 'Error/mark-callable-contracts')
                     mult_send   =  getSecuIssueCount(file_lines, 'Error/multiple-sends')
                     simp_even   = getSecuIssueCount(file_lines, 'Error/no-simple-event-func-name')
                     tx_orig     = getSecuIssueCount(file_lines, 'Error/avoid-tx-origin')
                     inli_asse   = getSecuIssueCount(file_lines, 'Error/no-inline-assembly')
                     block_hash  = getSecuIssueCount(file_lines, 'Error/not-rely-on-block-hash')
                     low_level   = getSecuIssueCount(file_lines, 'Error/avoid-low-level-calls')

                     total1      = avoid_throw + reentrancy + avoid_sha +  avoid_sui + func_visi +  state_vis + check_send + avoid_call + comp_fix
                     total2      = comp_gt + comp_fall + call_contr + mult_send + simp_even + tx_orig + inli_asse + block_hash + low_level
                     # total       = total1 + total2
                     # print avoid_throw, reentrancy, avoid_sha, avoid_sui, func_visi, state_vis, check_send, avoid_call, comp_fix
                     # print comp_gt, comp_fall, call_contr, mult_send, simp_even, tx_orig, inli_asse, block_hash, low_level
                     # print total
                     # str1_ = full_file_path + ',' + str(avoid_throw) + ',' + str(reentrancy) + ',' + str(avoid_sha) + ',' + str(avoid_sui) + ',' + str(func_visi) + ',' + str(state_vis) + ',' + str(check_send) + ',' + str(avoid_call) + ',' + str(comp_fix) + ','
                     # str2_ = str(comp_gt) + ',' + str(comp_fall) + ',' + str(call_contr) + ',' + str(mult_send) + ',' + str(simp_even) + ',' + str(tx_orig) + ',' + str(inli_asse) + ',' + str(block_hash) + ',' + str(low_level) + ',' + str(total)
                     # str_ =  str_ + str1_ + str2_ + '\n'
                     total = reentrancy + check_send + tx_orig + time  ## only using time time dependence for oeynte results 
                     '''
                     not all smells  are threats so not considering all
                     '''
                     str1_ = full_file_path + ',' + str(reentrancy) + ',' + str(check_send) + ','
                     str2_ = str(tx_orig) + ',' + str(time) + ',' + str(total)
                     str_ =  str_ + str1_ + str2_ + '\n'                    
                     # print str_
                     print '='*50

    # str_ = 'FILE,AVOID_THROW,REENTRANCY,AVOID_SHA,AVOID_SUI,FUNC_VISI,STATE_VIS,CHECK_SEND,AVOID_CALL,COMP_FIX,COMP_GT,COMP_FALL,CALL_CONTR,MULT_SEND,SIMP_EVEN,TX_ORIG,INLIASS,BLOCK_HASH,LOW_LEVEL,TOTAL' + '\n' + str_
    str_ = 'FILE,REENTRANCY,CHECK_SEND,TX_ORIG,TIME_DEPE,TOTAL' + '\n' + str_    
    out_sta = dumpContentIntoFile(str_, out_f)
    print 'Dumped a file of {} bytes'.format(out_sta)

if __name__=='__main__':
   ### first get oyente values 
   oyente_file = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/FINAL_OYENTE.csv'
   oyente_dict = getOyenteData(oyente_file)
   

   inp_dir = '/Users/akond.rahman/Documents/Personal/smart_contracts_research/data_sources/V5/final_repos/'
   out_file = '/Users/akond.rahman/Documents/Personal/misc/solidity_output/FINAL_SECU_SOLHINT.csv'
   getSolFiles(inp_dir, out_file, oyente_dict)
