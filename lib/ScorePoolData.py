"""
Arguments

-dn The name of the domain that you are training the model for. This is used only for the purpose of labeling and identifying the data that is matched.
-sl The source language that will be used for domain analysis. This should be lower case. For example en, fr, de.
-tl The target language that will be paired with the source language to determine the path to the language pair in the Pool Data. This should be lower case.
-dmd The path to where the Domain Matched Data and other relevant files are written. See Output Files below for more details.
-c (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.
The score data will be written to {domain_match_data_path}/{domain_name}/{source_language}_{target_language}/scores/. One file will be output for each file with a matching name to each Pool Data file. All previous score files will be deleted before the new scores start processing.
Pool Data files will be processed from {pool_data_path}/{source_language}_{target_language}/{source_language}/tok/.
The domain model used will be loaded from {domain_match_data_path}/{domain_name}/{source_language}_{target_language}/model/.
"""
#import lib
import numpy as np 
import xml.etree.ElementTree as ET
from lxml import etree
import kenlm
import sys
import os
import logging
import json
import argparse
import re
#check Python version
if sys.version_info[0] < 3:
	raise Exception("Must be using Python 3")
	sys.exit(1)

print('Domain Adaptation')
print('==========================')
print('Process : Score Pool Data')
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
#count the number of words in a line
def get_word_count(line):
	count = len(re.findall(r'\w+', line))
	return (count)
#get the difference of files between two folders to check if data tokenized already or not
def diff_data(path1,path2):
	list_item1 = []
	list_item2 = []
	diff_data = []
	list_item1 = [f for f in os.listdir(path1) if os.path.isfile(os.path.join(path1, f))]
	list_item2 = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
	diff_data = diff(list_item1, list_item2)
	return (diff_data)
#get_score of setence based on Domain LM
def get_list_of_scores(InputFile,model):
	list_Scores = []
	with open(str(InputFile),mode = "r" , encoding = 'utf-8') as my_matcher :
		for item2 in my_matcher:
			#list_Scores.append(float(model.score(str(item2))))
			list_Scores.append(float(model.score(str(item2)))/int(get_word_count(str(item2))))

	return(list_Scores)

#Transformation Scores for Lm 
def transform_func(x):
	return (1 / (1 + np.exp((np.log(float(-x))))))
#Get scores of all lines in a file
def get_Soft_scores(InputFile):
	list_Soft_Scores_w = []
	scores = get_list_of_scores(InputFile,model)
	for w in (scores):
		list_Soft_Scores_w.append(transform_func(float(w))*10)
	return(list_Soft_Scores_w)
#Get lines from a file
def get_list_of_sent(InputFile):
	list_Sentences = []
	with open(str(InputFile),mode = "r" , encoding = 'utf-8') as my_matcher :
		for item1 in my_matcher:
			list_Sentences.append(item1.replace('\n',''))
	return(list_Sentences)
#create score file in xml format
def create_xml(all_sentences,all_scores,list_Soft_Scores_w,OutputFile):
	sentences = ET.Element("sentences")
	sentences = ET.SubElement(sentences,"sentences")
	for sent_nb in range(len(all_sentences)):
		sent_i = ET.SubElement(sentences,"sent")
		score_s = ET.SubElement(sent_i,"s_s")
		score_s.text =str(sent_nb + 1)+"\t"+str(all_scores[sent_nb])+"\t"+str(list_Soft_Scores_w[sent_nb])
	tree = ET.ElementTree(sentences)
	tree.write(str(OutputFile),encoding='utf-8', xml_declaration=True)
	assert str(OutputFile) is not None
	parser = etree.XMLParser(resolve_entities=False, strip_cdata=False)
	document = etree.parse(str(OutputFile), parser)
	document.write(str(OutputFile), pretty_print=True, encoding='utf-8')


#Run the main Process
if __name__== "__main__":
	# setting arguments
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-dn', help='domain')
	parser.add_argument('-sl', help='LangID tsource.')
	parser.add_argument('-tl', help='LangID target.')
	parser.add_argument('-dmd', help='Input DomainSample.')
	parser.add_argument('-c', default='Config.json',help='Config File for tokenizer.')
	try:
		args = parser.parse_args()
		if parse_config(args.c)[4] is not None :
			log_path = str(parse_config(args.c)[4])+ 'Score_Pool_Data_log.txt'
		else:
			log_path = str(os.getcwd())+"/"+ 'Score_Pool_Data_log.txt'
	except:
		parser.print_help()
		sys.exit(0)
	logger = logging.getLogger('Score_Pool_Data_log.txt')
	hdlr = logging.FileHandler(log_path)
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 
	logger.setLevel(logging.DEBUG)
	#set the principal paths 
	pool_data_path = str(parse_config(args.c)[3])+str(args.sl)+"_"+str(args.tl)+"/"
	pool_data_path_source = str(pool_data_path)+str(args.sl)+"/"
	pool_data_path_target = str(pool_data_path)+str(args.tl)+"/"
	scoring_path = str(args.dmd)+str(args.dn)+"/"+str(args.sl)+"_"+str(args.tl)+"/scores/"
	lm_model_path = str(args.dmd)+str(args.dn)+"/"+str(args.sl)+"_"+str(args.tl)+"/model/"
	kenlm_model = lm_model_path+str(args.dn)+"_"+str(args.sl)+"_"+str(args.tl)+"_Lm.bin"
	#check the working environment
	if not os.path.exists(str(pool_data_path)):
		raise Exception("No Pool Data to extract From")
		sys.exit(1)
	if not os.path.exists(str(lm_model_path)):
		raise Exception("No lm model")
		sys.exit(1)
	print("Loding the model ======> ")
	model = kenlm.LanguageModel(kenlm_model)
	#check if all data scored or not 
	if not os.path.exists(str(scoring_path)):
		os.makedirs(str(scoring_path))
		#start scoring data
		for item_to_score in get_file_list(str(pool_data_path_source)+"tok/"):
			logger.info("Start- Prepare XML")
			full_item_to_score = str(pool_data_path_source)+"tok/"+item_to_score
			full_item_score = str(scoring_path)+item_to_score
			create_xml(get_list_of_sent(full_item_to_score),get_list_of_scores(full_item_to_score,model),get_Soft_scores(full_item_to_score),full_item_score)
			print("Ladder File IsReady !")
			logger.info("End- Prepare XML")
	else :
		for item_to_score in diff_data(str(pool_data_path_source)+"tok/",str(scoring_path)):
			logger.info("Start- Prepare XML")
			full_item_to_score = str(pool_data_path_source)+"tok/"+item_to_score
			full_item_score = str(scoring_path)+item_to_score
			create_xml(get_list_of_sent(full_item_to_score),get_list_of_scores(full_item_to_score,model),get_Soft_scores(full_item_to_score),full_item_score)
			print("Ladder File IsReady !")
			logger.info("End- Prepare XML")
