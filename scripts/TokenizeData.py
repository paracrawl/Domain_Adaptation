#!/usr/bin/env python

"""
Arguments

-raw_data The data path is the path to the folder containing the data that will be tokenized
This folder must contain one or more files.
Each file in the folder will be checked. If {raw_data}/{original file name} does not have a matching file {out}/tok/{original file name} then the file will be tokenized and written to {out}/tok/{original file name}.
-out Directory where the output will be stored.
-l The language of the text. This should be lower case ISO code. For example en, fr, de.
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

sys.stderr.write('=======================\n')
sys.stderr.write('Process : Tokenize Data\n')
sys.stderr.write('=======================\n')

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

if __name__ == '__main__':
	# setting arguments
	curr_path = (os.path.dirname(os.path.realpath(__file__)))
	default_json = os.path.join( curr_path , 'Config.json')
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-raw_data', help='Raw data.', required=True)
	parser.add_argument('-out', help='Output tokenized data.', required=True)
	parser.add_argument('-l', help='Language ID.', required=True)
	parser.add_argument('-c', default=curr_path+'Config.json',help='Config File for tokenizer.')
	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)
	if not os.path.exists(str(args.c)):
		raise Exception("Config does not exist: " + args.c)
		sys.exit(1)

	raw_data_path = str(args.raw_data)
	if not os.path.exists(str(raw_data_path)):
		raise Exception("Directory for data does not exist: " + raw_data_path)
		sys.exit(1)

	sys.stderr.write("tokenize data in " + raw_data_path + "\n")
	if len(get_file_list(str(raw_data_path))) == 0:
		raise Exception("No data to Tokenize")
		sys.exit(1)
	out_tok = (os.path.join( args.out , args.l ))
	sys.stderr.write("Storing tokenized data in " + out_tok + "\n")

	#tokenize data
	if not os.path.exists(str(out_tok)):
		os.makedirs(str(out_tok))
	for item_to_tok in get_file_list(str(raw_data_path)):
		full_item_to_tok = os.path.join( raw_data_path,item_to_tok)
		full_item_tok =  os.path.join(out_tok,item_to_tok)
		if os.path.exists(full_item_tok):
			sys.stderr.write("Already processed:\t"+str(full_item_tok)+"\n")
		else:
			sys.stderr.write("Start :\t"+str(item_to_tok)+"\n")
			sys.stderr.write('processing item :' +str(item_to_tok)+"\n")
			#prepare the tokenize command based on user settings on config file
			tok_cmd = parse_config(args.c)["TokenizerCMD"].replace("%lang",args.l).replace("%input_file_path",full_item_to_tok).replace("%output_file_path",full_item_tok)
			subprocess.call(str(tok_cmd), shell=True)
			sys.stderr.write("End :\t"+str(item_to_tok)+"\n")
