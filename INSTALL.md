# Domain Adaptation Tools Installation

## Table of Contents
- [Introduction](#introduction)
- [Installation Steps](#installation-steps)
- [Configuration File](#configuration-file)
- [Storage Considerations](#storage-considerations)
- [Pool Data Folder Structure](#pool-data-folder-structure)
- [Example Folder Structures](#example-folder-structures)
- [Testing Installation](#testing-installation)
- [Dependencies](#dependencies)
  - [KenLM](#kenlm)
  - [Tokenizer](#tokenizer)

----
## Introduction
This document provides step by step installation instructions and guides you through the configuration options, storage considerations and optimization settings that can be adjusted to meet the requrements of different systems and users.

### Installation Steps

### KenLM
https://kheafield.com/code/kenlm/

### Tokenizer
Any tokenizer can be used, so long as it is the same tokenizer used for processing both the *Pool Data* and the *Domain Sample Data*.
If you already have the Moses toolkit installed, then this is a good option. You can also use the XXXXX tokenizer from KEN EMAIL
* Moses Toolkit Tokenizer
* KENS EMAIL TOKENIZER


# Requirements 
 
# KenLM:
	Download from here: https://kheafield.com/code/kenlm/

# Moses :
	Download from here : https://github.com/moses-smt/mosesdecoder.git
# Python Libraries
	run: pip install -r requirements.txt


## Configuration File
------------
The configuration file determines constant elements within the processing such as paths and dependency tools for tokenizing and model training. The default `config.json` configuration file is loaded from the same folder location as the running script. If you wish to use different *Pool Data* or different tokenizers at different times, you can override the default config file using the `-c` argument. 

**Default config.json**
```json
{
	"TokenizerCMD" : "/tools/mosesdecoder/scripts/tokenizer/tokenizer.perl -l %lang  -threads 4 < %input_file_path >  %output_file_path ",
	"KenLM" : "/tools/kenlm/",
	"nGram" : "5",
}
```

*Parameters*
- `-TokenizerCMD` The full path to the tokenizer to be used. The variable names that can be passed through the tools to the tokenizer are as follows:
  - `%lang` - The tokenization language.
  - `%input_file_path` - The path to the input file that is to be tokenized.
  - `%output_file_path` - The path to the tokenized output file.
- `KenLM` - The path to the KenLM Installation.
- `nGram` - The number of nGrams to train the language models with.

>**Note:**
>
>The default configuration file will be loaded automatically by the tools. This file resides in the same folder as the scripts are running. The default configuration file can be overridden by specifing the `-c` argument on any of the tools and providing a path to an alternate configuration file.

## Storage Considerations

Data used in this process can become very large. The initial files, especially the *Pool Data* files can be large from the outset.
* All source data when tokenzied will more than double in size.
* Depending on the size of your *Pool Data*, the working files and generated models can be many gigabytes.
* The extracted domain data can be very large. Depending on the amount of matching data, it can be up to total size of the combined source language and target language pool data. 

