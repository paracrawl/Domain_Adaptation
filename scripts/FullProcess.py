#!/usr/bin/python3
"""
Arguments

-dn The name of the domain that you are extracting data for. This is used only for the purpose of labeling and identifying the data that is matched. \n
-sl The source language that will be used for domain analysis. This should be lower case. For example en, fr, de. \n
-tl The target language that will be paired with the source language when sentence pair data is extracted. This should be lower case. \n
This is used to detemine the path to the Pool Data. \n
-dsd The Domain Sample Data Path is the path to the folder comtaining the Domain Sample Data that will be used as a reference set of data for analysis and model training. \n
This folder must contain one or more files.\n
Each file in the folder will be checked. If {domain_sample_path}/{original file name} does not have a matching file {domain_sample_path}/tok/{original file name} then the file will be tokenized and written to {domain_sample_path}/tok/{original file name}.\n
-dmd The path to where the Domain Matched Data and other relevant files will be written. See Output Files below for more details.\n
-est (Optional) This value represents the minimum score for data to be extracted with. If the score is greater than or equal to this score, then the line will be extracted. Values are between 0 and 1. If this parameter is not specified, then the extract process will not be performed. The extract process can be run separately at a later time using ExtractMatchedDomainData.py \n
-c (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used \n
"""
#import_lib
import json
import argparse
import os
import subprocess
import sys 
#check Python version
if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")
	sys.exit(1)
print('Domain Adaptation')
print('==========================\n')
print('Full Running')
#parse the config file
def parse_config(json_file):
	list_args = []
	with open(json_file,encoding='utf-8', errors='ignore') as json_data:
		data = json.load(json_data, strict=False)
	return (data)
if __name__ == '__main__':
	# setting arguments
	curr_path = (os.path.dirname(os.path.realpath(__file__)))+"/"
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-dn', help='domain', required=True)
	parser.add_argument('-sl', help='LangID tsource.', required=True)
	parser.add_argument('-tl', help='LangID target.', required=True)
	parser.add_argument('-dsd', help='Input DomainSample.', required=True)
	parser.add_argument('-dmd', help='Input DomainSample.', required=True)
	parser.add_argument('-est', default=0.5, type=float, help='Threshold to extract.')
	parser.add_argument('-c', default=curr_path+'Config.json', help='Config File for tokenizer.')

	try:
		args = parser.parse_args()
		sys.stderr = open(str(curr_path)+'FullProcess.log', 'w')

	except:
		parser.print_help()
		sys.exit(0)

	if not os.path.exists(str(args.dmd)):
		raise Exception("No Domain Match Data Path")
		print("No Domain Match Data Path")
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

	try:
		cmd_1 = subprocess.call("python3  "+str(curr_path)+"TokenizeDomainSampleData.py -dsd "+str(args.dsd)+" -sl "+str(args.sl)+" -tl "+str(args.tl)+" -c "+str(args.c), shell=True)
		if cmd_1 != 0:
			sys.stdout.write("There was a problem with TokenizeDomainSampleData.py")
			sys.exit(1)
		cmd_2 = subprocess.call("python3  "+str(curr_path)+"TrainDomainModel.py  -dn "+str(args.dn)+" -dsd "+str(args.dsd)+" -sl "+str(args.sl)+" -tl "+str(args.tl)+" -dmd "+str(args.dmd)+" -c "+str(args.c), shell=True)
		if cmd_2 != 0:
			sys.stdout.write("There was a problem with TrainDomainModel.py")
			sys.exit(1)
		cmd_3 = subprocess.call("python3  "+str(curr_path)+"TokenizePoolData.py -sl  "+str(args.sl)+" -tl "+str(args.tl)+" -c "+str(args.c), shell=True)
		if cmd_3 != 0:
			sys.stdout.write("There was a problem with TokenizePoolData.py")
			sys.exit(1)
		cmd_4 = subprocess.call("python3  "+str(curr_path)+"ScorePoolData.py -dn "+str(args.dn)+" -sl "+str(args.sl)+" -tl "+str(args.tl)+" -dmd "+str(args.dmd)+" -c "+str(args.c), shell=True)
		if cmd_4 != 0:
			sys.stdout.write("There was a problem with ScorePoolData.py")
			sys.exit(1)
		cmd_5 = subprocess.call("python3  "+str(curr_path)+"ExtractMatchedDomainData.py -dn "+str(args.dn)+" -sl "+str(args.sl)+" -tl "+str(args.tl)+" -dmd "+str(args.dmd)+" -est "+str(args.est)+" -c "+str(args.c), shell=True)
		if cmd_5 != 0:
			sys.stdout.write("There was a problem with ExtractMatchedDomainData.py")
			sys.exit(1)
	except:
		raise Exception("There was a problem with Full Running ")
		sys.exit(1)
