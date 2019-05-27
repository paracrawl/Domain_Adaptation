# Domain Adaptation Tools Installation

## Table of Contents
- [Introduction](#introduction)
- [Configuration File – config.json](#configuration-file--configjson)
  - [Pool Data Folder Structure](#pool-data-folder-structure)
- [Dependencies](#dependencies)
  - [KenLM](#kenlm)
  - [Tokenizer](#tokenizer)

----
## Introduction
### Installation Steps
### Configuration File
### Pool Data Folder Structure


InDomain detection is a tool designed to extract in-domain data from a large collections of data.

# Requirements 
# KenLM:
	Dowlnload from here: https://kheafield.com/code/kenlm/
# Moses :
	Download from here : https://github.com/moses-smt/mosesdecoder.git
# Python Libraries
	run: pip install -r requirements.txt

## Configuration File – config.json
------------
The configuration file determines constant elements within the processing such as paths and dependency tools for tokenizing and model training.
```json
{
	"TokenizerCMD" : "/opt/mosesdecoder/scripts/tokenizer/tokenizer.perl -l %lang  -threads 4 < %input_file_path >  %output_file_path ",
	"KenLM" : "/opt/send2/Data_Sentences/kenlm/",
	"nGram" : "5",
	"PoolDataRootPath" : "/domainadaptation/data/pool/",
	"LogPath" : "/domainadaptation/logs/"
}
```

*Parameters*
- `-TokenizerCMD` The full path to the tokenizer to be used. The variable names that can be passed through the tools to the tokenizer are as follows:
  - `%lang` - The tokenization language.
  - `%input_file_path` - The path to the input file that is to be tokenized.
  - `%output_file_path` - The path to the tokenized output file.
- `KenKM` - The path to the KenLM Installation.
- `PoolDataRootPath` - The path to where the *Pool Data* is stored. 
- `LogPath` - The path to write log files when processes are run.

>**Note:**
>
>The default configuration file will be loaded automatically by the tools. This file resides in the same folder as the scripts are running. The default configuration file can be overridden by specifing the `-c` argument on any of the tools and providing a path to an alternate configuration file.

## Pool Data Folder Structure
The *Pool Data* follows a simple structure. Files are stored grouped by language pair and then split into each individual language. This is the same format that ParaCrawl is published in. Each file has 1 sentence per line.

* `{pool_data_path}/{source_language}_{target_language}/` - The root folder for the language pair for the overall pool
* `{pool_data_path}/{source_language}_{target_language}/{source_language}` - The pool files in the source language.
* `{pool_data_path}/{source_language}_{target_language}/{target_language}` - The pool files in the target language. The file names should be identical to the source language file name.

**Example:**

```sh
/data/pool/en_de/en/myfile.txt
/data/pool/en_de/de/myfile.txt
```

>**Note:**
>
>*Pool Data* can be very large. When the *Pool Data* is tokenized, the tokenized data will be at a little bigger than the non-tokenized data due to the spaces added. Ensure that there is enough storage capacity available for this large set of data.

----
## Dependencies
### KenLM
https://kheafield.com/code/kenlm/

### Tokenizer
The default tokenizer is from the Moses toolkit. Any tokenizer can be used, so long as it is the same tokenizer used for processing both the *Pool Data* and the *Domain Sample Data*.
