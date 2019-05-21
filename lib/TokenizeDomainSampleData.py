"""
Arguments

-dsd The Domain Sample Data Path is the path to the folder comtaining the Domain Sample Data that will be used as a reference set of data for analysis and model training.
This folder must contain one or more files.
Each file in the folder will be checked. If {domain_sample_path}/{original file name} does not have a matching file {domain_sample_path}/tok/{original file name} then the file will be tokenized and written to {domain_sample_path}/tok/{original file name}.
-sl The source language that will be used for domain analysis. This should be lower case. For example en, fr, de.
-c (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.
"""
#import lib
import os
import subprocess
import sys 
import logging
import json
import argparse
#check Python version

if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")
	sys.exit(1)
print('Domain Adaptation')
print('==========================\n')
print('Process : Tokenize Domain Sample Data')
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
	return (list_args)
#get the difference between two lists
def diff(first, second):
	second = set(second)
	return [item for item in first if item not in second]
#get the difference of files between two folders to check if data tokenized already or not
def diff_data(path1,path2):
	list_item1 = []
	list_item2 = []
	diff_data = []
	list_item1 = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
	list_item2 = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
	diff_data = diff(list_item1, list_item2)
	return (diff_data)

if __name__ == '__main__':
	# setting arguments
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-dsd', help='DomainSampleData.')
	parser.add_argument('-sl', help='LangID tsource.')
	parser.add_argument('-tl', help='LangID target.')
	parser.add_argument('-c', default='Config.json',help='Config File for tokenizer.')
	try:
		args = parser.parse_args()
		if parse_config(args.c)[4] is not None :
			log_path = str(parse_config(args.c)[4])+ 'Tokenize_Domain_Sample_Data_log.txt'
		else:
			log_path = str(os.getcwd())+"/"+ 'Tokenize_Domain_Sample_Data_log.txt'
	except:
		parser.print_help()
		sys.exit(0)

	logger = logging.getLogger('Tokenize_Domain_Sample_Data_log.txt')
	hdlr = logging.FileHandler(log_path)
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 
	logger.setLevel(logging.DEBUG)
	#set the principal paths 
	domain_data_path = str(args.dsd)
	#check the working environment
	if not os.path.exists(str(domain_data_path)):
		raise Exception("No path for Domain_data ")
		sys.exit(1)
	if len(get_file_list(str(domain_data_path))) == 0:
		raise Exception("No data to Tokenize")
		sys.exit(1)
	#tokenize domain sample data
	if not os.path.exists(str(domain_data_path)+"tok/"):
		os.makedirs(str(domain_data_path)+"tok/")
		for item_to_tok in get_file_list(str(domain_data_path)):
			logger.info("Start :\t"+str(item_to_tok))
			print('processing item :' , item_to_tok)
			full_item_to_tok = str(domain_data_path)+item_to_tok
			full_item_tok = str(domain_data_path)+"tok/"+item_to_tok
			#prepare the tokenize command based on user settings on config file
			tok_cmd = parse_config(args.c)[0].replace("%lang",args.sl).replace("%input_file_path",full_item_to_tok).replace("%output_file_path",full_item_tok)
			subprocess.call(str(tok_cmd), shell=True)
			logger.info("End :\t"+str(item_to_tok))

	else :
		if len(diff_data(str(domain_data_path),str(domain_data_path)+"tok/")) !=0 :
			for item_to_tok in diff_data(str(domain_data_path),str(domain_data_path)+"tok/"):
				logger.info("Start :\t"+str(item_to_tok))
				print('processing item :' , item_to_tok)
				full_item_to_tok = str(domain_data_path)+item_to_tok
				full_item_tok = str(domain_data_path)+"tok/"+item_to_tok
				#prepare the tokenize command based on user settings on config file
				tok_cmd = parse_config(args.c)[0].replace("%lang",args.sl).replace("%input_file_path",full_item_to_tok).replace("%output_file_path",full_item_tok)
				subprocess.call(str(tok_cmd), shell=True)
				logger.info("End :\t"+str(item_to_tok))
		else:
			print("No Data left to tokenize")
