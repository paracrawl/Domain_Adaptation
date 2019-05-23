#!/usr/bin/python3
"""
Arguments

-dn The name of the domain that you are training the model for. This is used only for the purpose of labeling and identifying the data that is matched.
-dsd The Domain Sample Data Path is the path to the folder comtaining the Domain Sample Data. The tokenized files found in the path {domain_data_sample_path}/tok/ will be used to train the model.
This folder must contain one or more files.
-sl The source language that will be used for domain analysis. This should be lower case. For example en, fr, de.
-tl The target language that will be paired with the source language to determine the path to the language pair in the Pool Data. This should be lower case.
-dmd The path to where the Domain Matched Data and other relevant files will be written. See Output Files below for more details.
-c (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.
"""
#import_lib
import os
import subprocess
import sys 
import json
import argparse
#check Python version

if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")
	sys.exit(1)
print('Domain Adaptation')
print('==========================\n')
print('Process : Train Domain Data')
#get list of files on a folder
def get_file_list(dirpath):
	files = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
	return (files)
#parse the config file
def parse_config(json_file):
	list_args = []
	with open(json_file,encoding='utf-8', errors='ignore') as json_data:
		data = json.load(json_data, strict=False)
	return (data)
#train the language model with KenLM
def train_lm(InputDir,OutputDir,Domain,SlangID,TlangID,kenLM,nGram):
	subprocess.call("cat  "+str(InputDir)+"*.* > " + str(OutputDir)+str(SlangID.upper())+"_Lm_data.txt", shell=True)
	sys.stdout.write('Prepare for Training LM========>'+"\n")
	os.system(str(kenLM)+"build/bin/lmplz -o " + str(nGram) + " -S 50% --skip_symbols < " + str(OutputDir)+str(SlangID.upper())+"_Lm_data.txt" +" > "+ str(OutputDir)+str("tmp.arpa"))
	os.system(str(kenLM)+"build/bin/build_binary "+str(OutputDir)+str("tmp.arpa")+" "+str(OutputDir)+str(Domain)+"_"+str(SlangID)+"_"+str(TlangID)+"_Lm.bin")

if __name__ == '__main__':
	# setting arguments
	curr_path = (os.path.dirname(os.path.realpath(__file__)))+"/"
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-dn', help='domain', required=True)
	parser.add_argument('-dsd', help='DomainSampleData.', required=True)
	parser.add_argument('-sl', help='LangID tsource.', required=True)
	parser.add_argument('-tl', help='LangID target.', required=True)
	parser.add_argument('-dmd', help='Input DomainSample.')
	parser.add_argument('-c', default=curr_path+'Config.json', help='Config File for tokenizer.')
	try:
		args = parser.parse_args()
		sys.stderr = open(str(curr_path)+'Train_Domain_Data.log', 'w')
	except:
		parser.print_help()
		sys.exit(0)

	#set the principal paths 
	domain_data_path = str(args.dsd)+"tok/"
	model_path = str(args.dmd)+str(args.dn)+"/"+str(args.sl)+"_"+str(args.tl)+"/model/"
	#check the working environment
	if len(get_file_list(str(domain_data_path))) == 0:
		raise Exception("No Tokenized Data")
		sys.exit(1)
	if not os.path.exists(str(model_path)):
		os.makedirs(str(model_path))
	#Run the model training 
	train_lm(domain_data_path,model_path,str(args.dn),str(args.sl),str(args.tl),str(parse_config(args.c)["KenLM"]),str(parse_config(args.c)["nGram"]))
	sys.stdout.write('Done'+"\n")

