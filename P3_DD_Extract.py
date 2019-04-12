import os
import time 
import subprocess
import sys 
import xml.etree.ElementTree as ET
import logging 

print('\nOmniscien Domain Detector P3')
print('============================\n')

#Arguments List Description
"""
Inputfile = Path+name of input File that run throught LM 
LadderXMLfile = Path+name of output file .xml that have In domain score for all sentences
OutputScore  = Path+name of  output file that contain selected items by scores 
OutputFile = Path+name of output file that contain selected sentences 
log_path = Path to store all System Logs
"""

#Arguments List
try : 
	Input_File = sys.argv[1]
	LadderXMLfile = sys.argv[2]
	OutputScore = sys.argv[3]
	OutputFile = sys.argv[4]
	log_path = sys.argv[5]

except :
	print('Not the right format---  \n'\
          'usage: P3_DD_Extract.py {Input_File} {LadderXMLfile} {OutputScore} {Output_File} {log_path}  [threshold --default 0.5]')
	sys.exit(1)
try:
	threshold = sys.argv[6]
except :
	threshold = 0.5
	pass
#logger Settings
log_path = log_path + 'P3_DD_Log_Extract.txt'
logger = logging.getLogger('P1_DD_Log_TOKandML.txt')
hdlr = logging.FileHandler(log_path)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)
#Set the Extractor
i = 0
print("Selected Threshold: \t",float(threshold))
logger.info("Start -Extract")
list_Index = []
root =ET.parse(str(LadderXMLfile)).getroot()
all_items = root.findall("sent")
# Get Items by Threshold
for item in all_items:
		if float(item.find('s_s').text.strip().split("\t")[2]) >= float(threshold) :
			with open (str(OutputScore), mode = "a" , encoding = 'utf-8') as extract_result : 
				print(item.find('s_s').text.strip().split("\t")[0]+'\t'+item.find('s_s').text.strip().split("\t")[2] , file= extract_result)
				i +=1
				list_Index.append(item.find('s_s').text.strip().split("\t")[0])
#Get the correct Item
with open(str(Input_File),mode ='r', encoding ='utf-8') as original_data:
	with open(str(OutputFile),mode ='a', encoding ='utf-8') as output_sentences:
		x = original_data.readlines()
		for l in range(len(list_Index)):
			y = list_Index[l]
			print (x[int(y)-1].replace('\n',''), file= output_sentences)

print(str(i) + " Items selected from " + str(len(all_items)) )
logger.info("End -Extract")
