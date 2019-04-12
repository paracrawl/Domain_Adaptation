import numpy as np 
import xml.etree.ElementTree as ET
from lxml import etree
import kenlm
import sys
import time
import os
import logging
import subprocess

print('Omniscien Domain Detector P2')
print('==========================')

#Arguments List Description
"""
InputFile = Path+name of input File that run throught LM 
OutputFile = Path+name of output file of LadderXMLfile that have Indomain scores for all sentences
ModelPath = Path to LM 
moses = Path to mosesdecoder
langID = Language ID to use for Domain Detection
log_path = Path to store all System Logs
"""

#Arguments List
try : 
	InputFile = sys.argv[1]
	OutputFile = sys.argv[2]
	ModelPath = sys.argv[3]
	moses = sys.argv[4]
	langID = sys.argv[5]
	log_path = sys.argv[6]

except :
	print('Not the right syntax---  \n'\
          'usage: P2_DD_LMScoring.py {Input_File} {Output_File} {Model_Path} {moses_Path} {lang_ID} {log_path}')
	sys.exit(1)

#logger Settings
log_path = log_path + 'P2_DD_Log_LMScoring.txt'
logger = logging.getLogger('P2_DD_Log_LMScoring.txt')
hdlr = logging.FileHandler(log_path)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

#Settings
print("Loding the model ======> ")
model = kenlm.LanguageModel(str(ModelPath))
list_Sentences = []
list_Scores = []
list_Soft_Scores_w = []
#Transformation Scores for Lm 
def transform_func(x):
	return (1 / (1 + np.exp((np.log(float(-x))))))
#Ladder File creation 2 functions
def create_xml():
	sentences = ET.Element("sentences")
	sentences = ET.SubElement(sentences,"sentences")
	for sent_nb in range(len(all_sentences)):
		sent_i = ET.SubElement(sentences,"sent")
		score_s = ET.SubElement(sent_i,"s_s")
		score_s.text =str(sent_nb + 1)+"\t"+str(all_scores[sent_nb])+"\t"+str(list_Soft_Scores_w[sent_nb])
	tree = ET.ElementTree(sentences)
	tree.write(str(OutputFile),encoding='utf-8', xml_declaration=True)

def prettyPrintXml(xmlFilePathToPrettyPrint):
	assert xmlFilePathToPrettyPrint is not None
	parser = etree.XMLParser(resolve_entities=False, strip_cdata=False)
	document = etree.parse(xmlFilePathToPrettyPrint, parser)
	document.write(xmlFilePathToPrettyPrint, pretty_print=True, encoding='utf-8')

#Prepare the new input files
subprocess.call(str(moses)+"scripts/tokenizer/tokenizer.perl -l "+str(langID)+" -threads 4 <"+str(InputFile)+ ">  " + str(InputFile).replace('.txt',str(langID.upper())+'.Tok.txt'), shell=True)
print("moses " +str(moses)+"scripts/tokenizer/tokenizer.perl -l "+str(langID)+" -threads 4 <"+str(InputFile)+ ">  " + str(InputFile).replace('.txt',str(langID.upper())+'.Tok.txt'))
InputFile2 = str(InputFile).replace('.txt',str(langID.upper())+'.Tok.txt')
#fill in list Sentences
with open(str(InputFile2),mode = "r" , encoding = 'utf-8') as my_matcher :
	logger.info("Start- Prepare Input")
	for item1 in my_matcher:
		list_Sentences.append(item1.replace('\n',''))
	logger.info("End- Prepare Input")
#fill in List scores
with open(str(InputFile2),mode = "r" , encoding = 'utf-8') as my_matcher :
	logger.info("Start- Scoring Input")
	for item2 in my_matcher:
		list_Scores.append(float(model.score(str(item2))))
	logger.info("Start- Scoring Input")

all_sentences = list_Sentences
all_scores = list_Scores
logger.info("Start- Transform Scores")
for w in (all_scores):
	list_Soft_Scores_w.append(transform_func(float(w))*10)
logger.info("End- Transform Score")

#Run the main Process
if __name__== "__main__":
	start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
	print ("=== Start at:\t"+str(start_time))
	logger.info("Start- Prepare XML")
	print("LSS-w",list_Soft_Scores_w)
	create_xml()
	prettyPrintXml(str(OutputFile))
	print("Ladder File IsReady !")
	logger.info("End- Prepare XML")

	end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
	print ("=== End at:\t"+str(end_time))
