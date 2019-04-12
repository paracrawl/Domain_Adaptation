import os
import time 
import subprocess
import sys 
import logging

print('Omniscien Domain Detector P1')
print('==========================')

#Arguments List Description
"""
InputDir = Path for the Data that will be used for Language Model Training
OutputDir = Path for LM after training
langID = Language ID to use for Domain Detection
nGram = NGram number to use in LM training
moses = Path to mosesdecoder
kenLM = path to kenLM
log_path = Path to store all System Logs
"""

#Arguments List
try : 
	InputDir = sys.argv[1]
	OutputDir = sys.argv[2]
	langID = sys.argv[3]
	nGram = sys.argv[4]
	moses = sys.argv[5]
	kenLM = sys.argv[6]
	log_path = sys.argv[7]
except :
	print('Not the right syntax---  \n'\
          'usage: P1_DD_TokandLM.py {Input_Folder} {Output_Folder} {langID} {nGram} {moses} {KenLm} {log_path}')
	sys.exit(1)

#logger Settings
log_path = log_path + 'P1_DD_Log_TOKandML.txt'
logger = logging.getLogger('P1_DD_Log_TOKandML.txt')
hdlr = logging.FileHandler(log_path)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

#Run Tokenizer and Prepare Data for LM training
for item_tmp in os.listdir(InputDir):
	logger.info("Start :\t"+str(item_tmp))
	print('processing item :' , item_tmp)
	subprocess.call("cp  "+str(InputDir)+str(item_tmp) + " " + str(OutputDir), shell=True)
	subprocess.call(str(moses)+"scripts/tokenizer/tokenizer.perl -l "+str(langID)+" -threads 4 <"+str(OutputDir)+str(item_tmp) + ">  " + str(OutputDir)+str(item_tmp).replace('.txt',str(langID.upper())+'.Tok.txt'), shell=True)
	subprocess.call("rm -rf  "+str(OutputDir)+str(item_tmp), shell=True)
	logger.info("End :\t"+str(item_tmp))

#LM Training
def main():
	subprocess.call("cat  "+str(OutputDir)+"*"+str(langID.upper())+".Tok.txt > " + str(OutputDir)+str(langID.upper())+"_Lm_data.txt", shell=True)
	subprocess.call("rm -rf "+str(OutputDir)+"*"+str(langID.upper())+".Tok.txt" , shell=True)
	print('Prepare for Training LM========>')
	os.system(str(kenLM)+"build/bin/lmplz -o " + str(nGram) + " -S 50% --skip_symbols < " + str(OutputDir)+str(langID.upper())+"_Lm_data.txt" +" > "+ str(OutputDir)+str("tmp.arpa"))
	os.system(str(kenLM)+"build/bin/build_binary "+str(OutputDir)+str("tmp.arpa")+" "+str(OutputDir)+str(langID.upper())+"_Lm.bin")

#Run Main Process
if __name__== "__main__":
	start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
	print ("=== Start at:\t"+str(start_time))
	logger.info("Start- Prepare LM")
	main()
	print('Done')
	logger.info("End- Prepare LM")
	end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
	print ("=== End at:\t"+str(end_time))