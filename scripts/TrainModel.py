#!/usr/bin/env python

"""
Arguments

-data_path The Data Path is the path to the folder comtaining the Data. The tokenized files found in the path {data_path} will be used to train the model.
This folder must contain one or more files.
-model_path The path to where the Model and other relevant files will be written. See Output Files below for more details.
-l The language that will be used for analysis. This should be lower case. For example en, fr, de.
-c (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.
"""

import os
import subprocess
import sys 
import json
import argparse

#check Python version
if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")
	sys.exit(1)

sys.stderr.write('=====================\n')
sys.stderr.write('Process : Train Model\n')
sys.stderr.write('=====================\n')

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
def train_lm(InputDir,OutputDir,kenLM,nGram):
	if not os.path.exists(str(OutputDir)):
		os.makedirs(str(OutputDir))
	subprocess.call("cat "+str(InputDir)+"/* > " + str(OutputDir)+"/lm_data.txt", shell=True)
	sys.stderr.write('Prepare for Training LM========>'+"\n")
	os.system(str(kenLM)+"/lmplz -o " + str(nGram) + " -S 50% --skip_symbols < " + str(OutputDir)+"/lm_data.txt" +" > "+ str(OutputDir)+str("/lm.arpa"))
	os.system(str(kenLM)+"/build_binary "+str(OutputDir)+"/lm.arpa "+str(OutputDir)+"/lm.bin")

if __name__ == '__main__':
	# setting arguments
	curr_path = (os.path.dirname(os.path.realpath(__file__)))+"/"
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-data_path', help='Data Path.', required=True)
	parser.add_argument('-model_path', help='Model Path.')
	parser.add_argument('-c', default=curr_path+'Config.json', help='Config File for tokenizer.')
	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	#set the principal paths 
	data_path = str(args.data_path)
	model_path = str(args.model_path)
	#check the working environment
	if len(get_file_list(data_path)) == 0:
		raise Exception("No Tokenized Data")
		sys.exit(1)
	if not os.path.exists(model_path):
		os.makedirs(model_path)
	if os.path.exists(model_path + "/lm.bin"):
		sys.stderr.write("Already trained model " + model_path + "/lm.bin")
	else:
		train_lm(data_path,model_path,str(parse_config(args.c)["KenLM"]),str(parse_config(args.c)["nGram"]))
	sys.stderr.write('Done'+"\n")

