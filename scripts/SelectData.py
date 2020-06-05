#!/usr/bin/env python

"""
Arguments

-dn The name of the domain that you are training the model for. This is used only for the purpose of labeling and identifying the data that is matched.
-sl The source language that will be used for domain analysis. This should be lower case. For example en, fr, de.
-tl The target language that will be paired with the source language to determine the path to the language pair in the Pool Data. This should be lower case.
-score_path Directory that contains scores.
-out_path Directory into which selected data is stored. 
-threshold This value represents the minimum score for data to be extracted with. If the score is greater than or equal to this score, then the line will be extracted.
-ratio Instead of specifying the threshold, compute it to select a specified ratio of the data
-c (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.
"""

import json
import argparse
import os
import sys
import heapq

#check Python version
if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")
	sys.exit(1)

sys.stderr.write('================================\n')
sys.stderr.write('Process : Extract Matched Domain\n')
sys.stderr.write('================================\n')

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
	
def process(pool_data_path, pool_score_path, domain_score_path, out_path, sl, tl, threshold, ratio):
	pool_data_path_source = pool_data_path + str(sl)
	pool_data_path_target = pool_data_path + str(tl)
	pool_score_path_source = pool_score_path + str(sl)
	pool_score_path_target = pool_score_path + str(tl)
	domain_score_path_source = domain_score_path + str(sl)
	domain_score_path_target = domain_score_path + str(tl)
	out_path_source = out_path + str(sl)
	out_path_target = out_path + str(tl)

	# configure or detect from dir
	compute_threshold = ratio is not None

	use_source_score = True
	use_target_score = True
	if not os.path.exists(domain_score_path_source):
		use_source_score= False
	if not os.path.exists(domain_score_path_target):
		use_target_score= False
	if not use_source_score and not use_target_score:
		sys.stderr.write("ERROR: Either source or target scores need to exist")
		sys.exit(1)

	# checks
	if not os.path.exists(str(out_path_source)):
		os.makedirs(str(out_path_source))
	if not os.path.exists(str(out_path_target)):
		os.makedirs(str(out_path_target))

	# let's go
	file_list = get_file_list(pool_data_path_source)
	for file_name in file_list:
		sys.stderr.write("processing file " + file_name + "...")
		# check if all files exist
		try:
			pool_data_source = open(pool_data_path_source + "/" + file_name, mode ='r', encoding ='utf-8')
		except:
			sys.stderr.write("could not open pool data source file " + pool_data_path_source + "/" + file_name + "\n")
			sys.exit(1)
		try:
			pool_data_target = open(pool_data_path_target + "/" + file_name, mode ='r', encoding ='utf-8')
		except:
			sys.stderr.write("could not open pool data target file " + pool_data_path_target + "/" + file_name + "\n")
			sys.exit(1)
		try:
			out_source = open(out_path_source + "/" + file_name, mode ='w', encoding ='utf-8')
		except:
			sys.stderr.write("could not open selected data source file " + out_path_source + "/" + file_name + "\n")
			sys.exit(1)
		try:
			out_target = open(out_path_target + "/" + file_name, mode ='w', encoding ='utf-8')
		except:
			sys.stderr.write("could not open selected data target file " + out_path_target + "/" + file_name + "\n")
			sys.exit(1)

		if use_source_score:
			try:
				pool_score_source = open(pool_score_path_source + "/" + file_name, mode ='r')
			except:
				sys.stderr.write("could not open pool score source file " + pool_score_path_source + "/" + file_name + "\n")
				sys.exit(1)
			try:
				domain_score_source = open(domain_score_path_source + "/" + file_name, mode ='r')
			except:
				sys.stderr.write("could not open domain score source file " + domain_score_path_source + "/" + file_name + "\n")
				sys.exit(1)
		if use_target_score:
			try:
				pool_score_target = open(pool_score_path_target + "/" + file_name, mode ='r')
			except:
				sys.stderr.write("could not open pool score target file " + pool_score_path_target + "/" + file_name + "\n")
				sys.exit(1)
			try:
				domain_score_target = open(domain_score_path_target + "/" + file_name, mode ='r')
			except:
				sys.stderr.write("could not open domain score target file " + domain_score_path_target + "/" + file_name + "\n")
				sys.exit(1)
		total_count = 0
		selected_count = 0
		score_list = []
		for pool_data_source_line in pool_data_source:
			score = 0
			if use_source_score:
				pool = float(pool_score_source.readline())
				domain = float(domain_score_source.readline())
				score = domain - pool
			if use_target_score:
				pool = float(pool_score_target.readline())
				domain = float(domain_score_target.readline())
				score += domain - pool
			# have threshold -> write out file
			pool_data_target_line = pool_data_target.readline()
			if compute_threshold:
				score_list.append(score)
			else:
				if score > threshold:
					selected_count += 1
					out_source.write( pool_data_source_line )
					out_target.write( pool_data_target_line )
				total_count += 1
		
		#print how much lines we get from domain matching for each file
		if compute_threshold:
			return heapq.nlargest(1+int(float(len(score_list))*ratio), score_list)[-1]
		else:
			sys.stderr.write(str(selected_count) + " lines selected from " + str(total_count) + "\n")

if __name__ == '__main__':
	# setting arguments
	curr_path = (os.path.dirname(os.path.realpath(__file__)))+"/"
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-dn', help='domain name', required=True)
	parser.add_argument('-sl', help='LangID source.', required=True)
	parser.add_argument('-tl', help='LangID target.', required=True)
	parser.add_argument('-score_path', help='Working directory with score files.', required=True)
	parser.add_argument('-pool_path', help='Pool data directory.', required=True)
	parser.add_argument('-out_path', help='Directory into which extracted data is written.', required=True)
	parser.add_argument('-threshold', type=float, help='Threshold to extract.')
	parser.add_argument('-ratio', type=float, help='Ratio of data to extract.')
	parser.add_argument('-c', default=curr_path+'Config.json', help='Config File for tokenizer.')

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	sl = str(args.sl)
	tl = str(args.tl)
	lp = sl+"-"+tl

	threshold = args.threshold
	ratio = args.ratio

	if threshold is not None and ratio is not None:
		sys.stderr.write("Either specify threshold or ratio, not both\n")
		sys.exit(1)

	if threshold is None and ratio is None:
		sys.stderr.write("Specify -threshold or -ratio\n")
		sys.exit(1)

	if ratio is not None and (ratio <= 0 or ratio >= 1):
		sys.stderr.write("Ratio should be between 0 and 1\n")
		sys.exit(1)

	#set the principal paths 
	pool_data_path = str(args.pool_path)+"/"+lp+"/"
	pool_score_path = str(args.score_path)+"/pool-score/"+lp+"/"
	domain_score_path = str(args.score_path)+"/"+args.dn+"-score/"+lp+"/"
	out_path = str(args.out_path)+"/"

	if ratio is None:
		process(pool_data_path, pool_score_path, domain_score_path, out_path, sl, tl, threshold, None)
	else:
		threshold = process(pool_data_path, pool_score_path, domain_score_path, out_path, sl, tl, None, ratio)
		process(pool_data_path, pool_score_path, domain_score_path, out_path, sl, tl, threshold, None)

