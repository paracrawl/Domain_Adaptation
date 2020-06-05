#!/usr/bin/env python

"""
Arguments

-data_path Directory that contains pool text files
-score_path Directory in which score files are stored
-model_path Model used for storing
-c (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.

The score data will be written to {score_path}. One file will be output for each file with a matching name to each pool data file. All previous score files will be deleted before the new scores start processing.
pool data files will be processed from {data_path}.
The domain model used will be loaded from {model_path}/lm.binlm
"""

import numpy as np 
import xml.etree.ElementTree as ET
from lxml import etree
import kenlm
import sys
import os
import json
import argparse
import re

#check Python version
if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")
	sys.exit(1)

sys.stderr.write('====================\n')
sys.stderr.write('Process : Score Data\n')
sys.stderr.write('====================\n')

#get list of files on a folder
def get_file_list(dirpath):
	files = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
	return (files)

#parse the config file
def parse_config(json_file):
	list_args = []
	with open(json_file,encoding='utf-8', errors='ignore') as json_data:
		data = json.load(json_data, strict=False)
		for x in data:
			list_args.append(data[x])
	return (data)

#count the number of words in a line
def get_word_count(line):
	count = len(re.findall(r'\w+', line))
	return (count)

#get_score of setence based on Domain LM
def compute_scores(InputFile,OutputFile,model):
	out = open(str(OutputFile), mode = "w")
	with open(str(InputFile), mode = "r", encoding = 'utf-8') as corpus:
		for line in corpus:
			length = int(get_word_count(str(line)))
			if length == 0: 
				out.write("0\n")
			else:
				raw_score = model.score(str(line))
				score = raw_score / length
				out.write(str(score)+"\n")

#run the main Process
if __name__== "__main__":
	# setting arguments
	curr_path = (os.path.dirname(os.path.realpath(__file__)))+"/"
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-data_path', help='Directory that contains text files', required=True)
	parser.add_argument('-score_path', help='Directory in which score files are stored', required=True)
	parser.add_argument('-model_path', help='Input DomainSample.', required=True)
	parser.add_argument('-c', default='Config.json',help='Config File for tokenizer.')
	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	model_path = str(args.model_path)
	data_path = str(args.data_path)
	score_path = str(args.score_path)

	if not os.path.exists(str(data_path)):
		raise Exception("Data path does not exist "+data_path)
		sys.exit(1)
	if not os.path.exists(model_path):
		raise Exception("No lm mode in "+model_path)
		sys.exit(1)
	if not os.path.exists(score_path):
		os.makedirs(score_path)

	file_list = get_file_list(data_path)
	# if empty, complain

	model = kenlm.LanguageModel(model_path)
	for text_file in file_list:
		in_file = data_path+"/"+text_file
		out_file = score_path+"/"+text_file
		if os.path.exists(out_file):
			sys.stderr.write("already processed " + in_file + "\n")
		else:
			sys.stderr.write("scoring " + in_file + ", score in " + out_file + "\n")
			compute_scores(in_file, out_file, model)
		
	sys.stdout.write("End :\t No Data left to Score \n")
