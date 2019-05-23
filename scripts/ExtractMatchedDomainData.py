#!/usr/bin/python3

"""
Arguments

-dn The name of the domain that you are training the model for. This is used only for the purpose of labeling and identifying the data that is matched.
-sl The source language that will be used for domain analysis. This should be lower case. For example en, fr, de.
-tl The target language that will be paired with the source language to determine the path to the language pair in the Pool Data. This should be lower case.
-dmd The path to where the Domain Matched Data and other relevant files are written. See Output Files below for more details.
-est This value represents the minimum score for data to be extracted with. If the score is greater than or equal to this score, then the line will be extracted. Values are between 0 and 1.
-c (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.
"""
#import_lib
import json
import argparse
import os
import sys 
import logging 
#check Python version
if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")
	sys.exit(1)
print('Domain Adaptation')
print('==========================\n')
print('Process : Extract Matched Domain')
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
	curr_path = (os.path.dirname(os.path.realpath(__file__)))+"/"
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-dn', help='domain', required=True)
	parser.add_argument('-sl', help='LangID tsource.', required=True)
	parser.add_argument('-tl', help='LangID target.', required=True)
	parser.add_argument('-dmd', help='Input DomainSample.', required=True)
	parser.add_argument('-est', default=0.5, type=float, help='Threshold to extract.')
	parser.add_argument('-c', default=curr_path+'Config.json', help='Config File for tokenizer.')

	try:
		args = parser.parse_args()
		sys.stderr = open(str(curr_path)+'ExtractMatchedDomainData.log', 'w')
	except:
		parser.print_help()
		sys.exit(0)
	#set the principal paths 
	pool_data_path = str(parse_config(args.c)["PoolDataRootPath"])+str(args.sl)+"_"+str(args.tl)+"/"
	pool_data_path_source = str(pool_data_path)+str(args.sl)+"/"
	pool_data_path_target = str(pool_data_path)+str(args.tl)+"/"
	scoring_path = str(args.dmd)+str(args.dn)+"/"+str(args.sl)+"_"+str(args.tl)+"/scores/"
	result_path_source = str(args.dmd)+str(args.dn)+"/"+str(args.sl)+"_"+str(args.tl)+"/"+str(args.est)+"/"+str(args.sl)+"/"
	result_path_target = str(args.dmd)+str(args.dn)+"/"+str(args.sl)+"_"+str(args.tl)+"/"+str(args.est)+"/"+str(args.tl)+"/"
	#check the working environment
	if not os.path.exists(str(scoring_path)):
		raise Exception("No Scores to extract Data")
		sys.exit(1)
	if not os.path.exists(str(result_path_source)):
		os.makedirs(str(result_path_source))
	if not os.path.exists(str(result_path_target)):
		os.makedirs(str(result_path_target))

	if not os.path.exists(str(pool_data_path)):
		raise Exception("No Pool Data to extract From")
		sys.exit(1)
	else :
		sys.stdout.write("Selected Threshold: \t"+str(float(args.est))+"\n")
		for item_to_domain in get_file_list(scoring_path) :
			#Set the Extractor
			sys.stdout.write("\nStart -Extract for :\t"+str(item_to_domain)+"\n")
			list_Index = []
			O_file=open(str(scoring_path)+str(item_to_domain))
			i = 0
			s = 0
			#stream the score file line by line and mine it 
			for item in O_file:
				if "s_s" in item:
					s +=1
					my_score = (item.strip().split("\t")[2]).replace("</s_s>","")
					my_index = (item.strip().split("\t")[0]).replace("<s_s>","")
					if float(my_score) >= float(str(args.est)) :
						i +=1
						list_Index.append(my_index)
			#Get the the domain matching lines and write source and target
			with open(str(pool_data_path_source)+str(item_to_domain),mode ='r', encoding ='utf-8') as pool_data_source, open(str(pool_data_path_target)+str(item_to_domain),mode ='r', encoding ='utf-8') as pool_data_target:
				with open(str(result_path_source)+str(item_to_domain),mode ='a', encoding ='utf-8') as source_sentences , open(str(result_path_target)+str(item_to_domain),mode ='a', encoding ='utf-8') as target_sentences:
					x = pool_data_source.readlines()
					z = pool_data_target.readlines()
					for l in range(len(list_Index)):
						y = list_Index[l]
						print (x[int(y)-1].replace('\n',''), file= source_sentences)
						print (z[int(y)-1].replace('\n',''), file= target_sentences)
			#print how much lines we get from domain matching for each file
			sys.stdout.write(str(i) + " Items,  selected from " + str(s) + " in :  " + str(item_to_domain)+"\n")
