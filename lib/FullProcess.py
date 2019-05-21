"""
Arguments

-dn The name of the domain that you are extracting data for. This is used only for the purpose of labeling and identifying the data that is matched.
-sl The source language that will be used for domain analysis. This should be lower case. For example en, fr, de.
-tl The target language that will be paired with the source language when sentence pair data is extracted. This should be lower case.
This is used to detemine the path to the Pool Data.
-dsd The Domain Sample Data Path is the path to the folder comtaining the Domain Sample Data that will be used as a reference set of data for analysis and model training.
This folder must contain one or more files.
Each file in the folder will be checked. If {domain_sample_path}/{original file name} does not have a matching file {domain_sample_path}/tok/{original file name} then the file will be tokenized and written to {domain_sample_path}/tok/{original file name}.
-dmd The path to where the Domain Matched Data and other relevant files will be written. See Output Files below for more details.
-est (Optional) This value represents the minimum score for data to be extracted with. If the score is greater than or equal to this score, then the line will be extracted. Values are between 0 and 1. If this parameter is not specified, then the extract process will not be performed. The extract process can be run separately at a later time using ExtractMatchedDomainData.py.
-c (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.
"""
#import lib
import json
import argparse
import collections
import os
import time 
import subprocess
import sys 
import xml.etree.ElementTree as ET
import logging 
#check Python version
if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")
	sys.exit(1)
print('Domain Adaptation')
print('==========================\n')
print('Full Runining ')
#parse the config file
def parse_config(json_file):
	list_args = []
	with open(json_file,encoding='utf-8', errors='ignore') as json_data:
		data = json.load(json_data, strict=False)
		for x in data:
			list_args.append(data[x])
	return (list_args)
	
if __name__ == '__main__':
	# setting arguments
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-dn', help='domain')
	parser.add_argument('-sl', help='LangID tsource.')
	parser.add_argument('-tl', help='LangID target.')
	parser.add_argument('-dsd', help='Input DomainSample.')
	parser.add_argument('-dmd', help='Input DomainSample.')
	parser.add_argument('-est', default=0.5, type=float, help='Threshold to extract.')
	parser.add_argument('-c', default='Config.json', help='Config File for tokenizer.')
	try:
		args = parser.parse_args()
		if parse_config(args.c)[4] is not None :
			log_path = str(parse_config(args.c)[4])+ 'Full_Runining_log.txt'
		else:
			log_path = str(os.getcwd())+"/"+ 'Full_Runining_log.txt'
	except:
		parser.print_help()
		sys.exit(0)
	logger = logging.getLogger('Full_Runining_log.txt')
	hdlr = logging.FileHandler(log_path)
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 
	logger.setLevel(logging.DEBUG)

	if not os.path.exists(str(args.dmd)):
		raise Exception("No Domain Match Data Path")
		sys.exit(1)
	#set the principal paths 
	full_dmd_path = str(args.dmd)+str(args.dn)+"/"
	full_dmd_langpair_path = str(args.dmd)+str(args.dn)+"/"+str(args.sl)+"_"+str(args.tl)+"/"
	#check the working environment
	if not os.path.exists(str(full_dmd_path)):
		os.makedirs(str(full_dmd_path))
	if not os.path.exists(str(full_dmd_langpair_path)):
		os.makedirs(str(full_dmd_langpair_path))
	#Run all the process one by one
	subprocess.call("python3.6  TokenizeDomainSampleData.py -dsd "+str(args.dsd)+" -sl "+str(args.sl)+" -c "+str(args.c), shell=True)
	time.sleep(1)
	subprocess.call("python3.6  TrainDomainModel.py  -dn "+str(args.dn)+" -dsd "+str(args.dsd)+" -sl "+str(args.sl)+" -tl "+str(args.tl)+" -dmd "+str(args.dmd)+"  -c "+str(args.c), shell=True)
	time.sleep(1)
	subprocess.call("python3.6  TokenizePoolData.py -sl  "+str(args.sl)+" -tl "+str(args.tl)+" -c "+str(args.c), shell=True)
	time.sleep(1)
	subprocess.call("python3.6  ScorePoolData.py -dn "+str(args.dn)+" -sl "+str(args.sl)+" -tl "+str(args.tl)+" -dmd "+str(args.dmd)+" -c "+str(args.c), shell=True)
	time.sleep(1)
	subprocess.call("python3.6  ExtractMatchedDomainData.py -dn "+str(args.dn)+" -sl "+str(args.sl)+" -tl "+str(args.tl)+" -dmd "+str(args.dmd)+" -est "+str(args.est)+" -c "+str(args.c), shell=True)
	logger.info("End -Extract")
