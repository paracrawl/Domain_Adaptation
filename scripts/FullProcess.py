#!/usr/bin/env python
"""
Arguments

-dn The name of the domain that you are extracting data for. This is used only for the purpose of labeling and identifying the data that is matched.
-sl The source language that will be used for domain analysis. This should be lower case. For example en, fr, de.
-tl The target language that will be paired with the source language when sentence pair data is extracted. This should be lower case.
-domain The Domain Sample Data Path is the path to the folder comtaining the Domain Sample Data that will be used as a reference set of data for analysis and model training. This folder must contain one or more files.
-pool Directory that contains the pool data (in two sub directories, one for each language)
-out Directory into which selected data is stored. 
-threshold This value represents the minimum score for data to be extracted with. If the score is greater than or equal to this score, then the line will be extracted.
-ratio Instead of specifying the threshold, compute it to select a specified ratio of the data
-c (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used
"""

import traceback
import json
import argparse
import os
import subprocess
import sys 
from pathlib import Path

#check Python version
if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")
	sys.exit(1)
sys.stderr.write('Domain Adaptation')
sys.stderr.write('=================\n')

#parse the config file
def parse_config(json_file):
	list_args = []
	with open(json_file,encoding='utf-8', errors='ignore') as json_data:
		data = json.load(json_data, strict=False)
	return (data)

if __name__ == '__main__':
	# setting arguments
	curr_path = (os.path.dirname(os.path.realpath(__file__)))
	config = os.path.join( curr_path , 'Config.json')

	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-dn', help='Domain name', required=True)
	parser.add_argument('-sl', help='LangID tsource.', required=True)
	parser.add_argument('-tl', help='LangID target.', required=True)
	parser.add_argument('-domain', help='Input domain data.', required=True)
	parser.add_argument('-pool', help='Input pool data.', required=True)
	parser.add_argument('-out', help='Selected data.', required=True)
	parser.add_argument('-working_dir', help='Working directory.', required=True)
	parser.add_argument('-threshold', type=float, help='Threshold for extraction.')
	parser.add_argument('-ratio', type=float, help='Ratio to extract.')
	parser.add_argument('-c', default=config, help='Config file for tokenizer.')

	try:
		args = parser.parse_args()
		print(sys.stderr)
	except:
		parser.print_help()
		sys.exit(0)

	if not os.path.exists(str(args.domain)):
		sys.stderr.write("No Domain Data Path " + str(args.domain))
		sys.exit(1)

	if args.threshold is not None and args.ratio is not None:
		sys.stderr.write("Either specify threshold or ratio, not both\n")
		sys.exit(1)

	if args.threshold is None and args.ratio is None:
		sys.stderr.write("Specify -threshold or -ratio\n")
		sys.exit(1)

	if args.ratio is not None and (args.ratio <= 0 or args.ratio >= 1):
		sys.stderr.write("Ratio should be between 0 and 1\n")
		sys.exit(1)
        
	#set the principal paths 
	sl = str(args.sl)
	tl = str(args.tl)
	wdir = str(args.working_dir)
	domain_name = str(args.dn)
	out = str(args.out)

	if args.c:
		config = str(args.c)

	#check the working environment
	if not os.path.exists(str(wdir)):
		os.makedirs(str(wdir))

	# Tokenize Data
	domain_data_path = wdir + "/" + domain_name + "-data/" + sl + "-" + tl + "/"
	pool_data_path = wdir + "/pool-data/" + sl + "-" + tl + "/"

	use_language = { sl: True, tl: True }

	data_sets = { str(args.domain): domain_data_path, str(args.pool): pool_data_path }
	for in_dir, out_dir in data_sets.items():
		for l in [sl, tl]:
			if in_dir == args.domain and not os.path.exists(in_dir + "/" + l): 
				use_language[l] = False
				continue
			tok_cmd = [ curr_path + "/TokenizeData.py", 
					"-c", config,
					"-l", l, 
					"-raw_data", in_dir + "/" + l, 
					"-out", out_dir ]
			sys.stderr.write( "=== Executing: " + (" ".join(tok_cmd)) + "\n" )
			subprocess.check_call( tok_cmd )


	if use_language[sl] is None and use_language[tl] is None:
		sys.stderr.write("No domain data for source or target language\n")
		sys.exit(1)

	# Train Models
	domain_model_path = wdir + "/" + domain_name + "-model/" + sl + "-" + tl + "/"
	pool_model_path = wdir + "/pool-model/" + sl + "-" + tl + "/"

	data_sets = { domain_data_path: domain_model_path, pool_data_path: pool_model_path }
	for in_dir, out_dir in data_sets.items():
		for l in [sl, tl]:
			if not use_language[l]:
				continue
			train_cmd = [ curr_path + "/TrainModel.py", 
					"-c", config,
					"-data_path", in_dir + l, 
					"-model_path", out_dir + l ]
			sys.stderr.write( "=== Executing: " + (" ".join(train_cmd)) + "\n" )
			subprocess.check_call( train_cmd )

	# Score Data
	domain_score_path = wdir + "/" + domain_name + "-score/" + sl + "-" + tl + "/"
	pool_score_path = wdir + "/pool-score/" + sl + "-" + tl + "/"

	data_sets = { domain_model_path: domain_score_path, pool_model_path: pool_score_path }
	for in_dir, out_dir in data_sets.items():
		for l in [sl, tl]:
			if not use_language[l]:
				continue
			score_cmd = [ curr_path + "/ScorePoolData.py", 
					"-c", config,
					"-model_path", in_dir + l + "/lm.bin", 
					"-data_path", pool_data_path + l, 
					"-score_path", out_dir + l ]
			sys.stderr.write( "=== Executing: " + (" ".join(score_cmd)) + "\n" )
			subprocess.check_call( score_cmd )


	# Select Data
	select_cmd = [ curr_path + "/SelectData.py",
			"-c", config,
			"-dn", domain_name,
			"-sl", sl,
			"-tl", tl,
			"-pool_path", wdir + "/pool-data/",
			"-score_path", wdir,
			"-out_path", out ]
	if args.threshold:
		select_cmd.append("-threshold")
		select_cmd.append(str(args.threshold))
	if args.ratio:
		select_cmd.append("-ratio")
		select_cmd.append(str(args.ratio))

	sys.stderr.write( "=== Executing: " + (" ".join(select_cmd)) + "\n" )
	subprocess.check_call( select_cmd )

