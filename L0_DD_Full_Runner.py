import os
import time 
import subprocess
import sys 
import logging 

print('\nOmniscien Domain Detector - Launcher')
print('============================\n')

#Arguments List Description
"""
libPATH = Path for lib which include all Domain Detection scripts
InputDir = Path for the Data that will be used for Language Model Training
OutputDir = Path for LM after training
langID = Language ID to use for Domain Detection
nGram = NGram number to use in LM training
moses = Path to mosesdecoder
kenLM = path to kenLM
log_path = Path to store all System Logs
P2_Path_to_Input_files = Path to input file that need to check if its In-Domain
P2_Path_to_output_files = Output folder in which the Indomain files will be stored 
Deactivate_LM_Training = 0/1 required field to run all the process including Lm training or run only domain Detection on new files
"""

#Arguments List
try : 
	libPATH = sys.argv[1]
	InputDir = sys.argv[2]
	OutputDir = sys.argv[3]
	langID = sys.argv[4]
	nGram = sys.argv[5]
	moses = sys.argv[6]
	kenLM = sys.argv[7]
	log_path = sys.argv[8]
	P2_Path_to_Input_files = sys.argv[9]
	P2_Path_to_output_files = sys.argv[10]
	Deactivate_LM_Training = int(sys.argv[11])

except :
	print('Not the right format---  \n'\
          'usage: L0_DD_Full_Runner.py {libPATH} {Input_Folder} {Output_Folder} {langID} {nGram} {moses_path} {KenLm_path} {log_path} {Input_Indomain_test_file} {Output_Indomain_test_file} {Deactivate LM Training 0/1 }')
	sys.exit(1)

#logger Settings
log_path_L0 = log_path + 'L0_DD_Log_Full_Runner.txt'
logger = logging.getLogger('L0_DD_Log_Full_Runner.txt')
hdlr = logging.FileHandler(log_path_L0)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)
#Set LM
P2_model_file=str(OutputDir)+str(langID.upper())+"_Lm.bin"

if int(Deactivate_LM_Training) == 1:	#Run Full Mode
	print("Running All steps")
	proc1 = "python3.6 "+str(libPATH)+"P1_DD_TokandLM.py"+" "+str(InputDir)+" "+str(OutputDir) +" "+str(langID)+" "+str(nGram)+" "+str(moses)+" "+str(kenLM)+" "+str(log_path)
	subprocess.call(proc1, shell=True) 
	print(proc1)
	print("*********")
	for item_tmp in os.listdir(P2_Path_to_Input_files):
		logger.info("Start :\t"+str(item_tmp))
		print('processing item :' , item_tmp)
		P2_output_file = item_tmp.replace('txt','scoring.xml')
		print("python3.6 "+str(libPATH)+"P2_DD_LMScoring.py"+" "+str(P2_Path_to_Input_files)+str(item_tmp) + " " +str(P2_Path_to_output_files)+str(P2_output_file)+" "+str(P2_model_file)+" "+str(moses)+" "+str(langID)+" "+str(log_path))
		subprocess.call("python3.6 "+str(libPATH)+"P2_DD_LMScoring.py"+" "+str(P2_Path_to_Input_files)+str(item_tmp) + " " +str(P2_Path_to_output_files)+str(P2_output_file)+" "+str(P2_model_file)+" "+str(moses)+" "+str(langID)+" "+str(log_path), shell=True)
		P3_input_file = str(P2_Path_to_Input_files)+str(item_tmp)
		P3_xml_file = str(P2_Path_to_output_files)+str(P2_output_file)
		P3_outputscore_file=str(P2_Path_to_output_files)+P2_output_file.replace('scoring.xml','extracted-score.txt')
		P3_outputsentences_file=str(P2_Path_to_output_files)+P2_output_file.replace('scoring.xml','InDomain-Sentences.txt')
		subprocess.call("python3.6 "+str(libPATH)+"P3_DD_Extract.py"+" "+str(P3_input_file)+" "+str(P3_xml_file)+" "+str(P3_outputscore_file)+" "+str(P3_outputsentences_file)+" "+str(log_path), shell=True)
		logger.info("End :\t"+str(item_tmp))
else :	#Run LM scoring and Extract
	print("Running Step 2 & 3")
	for item_tmp in os.listdir(P2_Path_to_Input_files):
		logger.info("Start :\t"+str(item_tmp))
		print('processing item :' , item_tmp)
		P2_output_file = item_tmp.replace('txt','scoring.xml')
		print("python3.6 "+str(libPATH)+"P2_DD_LMScoring.py"+" "+str(P2_Path_to_Input_files)+str(item_tmp) + " " +str(P2_Path_to_output_files)+str(P2_output_file)+" "+str(P2_model_file)+" "+str(moses)+" "+str(langID)+" "+str(log_path))
		subprocess.call("python3.6 "+str(libPATH)+"P2_DD_LMScoring.py"+" "+str(P2_Path_to_Input_files)+str(item_tmp) + " " +str(P2_Path_to_output_files)+str(P2_output_file)+" "+str(P2_model_file)+" "+str(moses)+" "+str(langID)+" "+str(log_path), shell=True)
		P3_input_file = str(P2_Path_to_Input_files)+str(item_tmp)
		P3_xml_file = str(P2_Path_to_output_files)+str(P2_output_file)
		P3_outputscore_file=str(P2_Path_to_output_files)+P2_output_file.replace('scoring.xml','extracted-score.txt')
		P3_outputsentences_file=str(P2_Path_to_output_files)+P2_output_file.replace('scoring.xml','InDomain-Sentences.txt')
		subprocess.call("python3.6 "+str(libPATH)+"P3_DD_Extract.py"+" "+str(P3_input_file)+" "+str(P3_xml_file)+" "+str(P3_outputscore_file)+" "+str(P3_outputsentences_file)+" "+str(log_path), shell=True)
		logger.info("End :\t"+str(item_tmp))
subprocess.call("mv "+ str(P2_Path_to_Input_files)+"*.Tok.txt "+str(P2_Path_to_output_files), shell=True)