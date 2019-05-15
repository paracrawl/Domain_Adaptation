# Domain Adaptation
## Introduction
---------------
Domain Adaptation in the context of machine translation is achieved by training machine translation engines using a set of domain specific data. The challenge in doing so is to identify domain specific bilingual data that is suitable for training an MT engine.

Bilingual datasets and corpus collections, such as ParaCrawl, have very large volumes of data that have many different domains mixed in together. Often the data has been collected from unknown sources with no associated metadata that could identify the content as belonging to any particular domain. For example, websites crawled could include information technology, life sciences, travel, shopping, automotive and much more. In the case of ParaCrawl, this can be as large as hundreds of millions of sentences or even several billion of sentences.

This set of tools is designed to extract domain specific data using an in-domain monolingual data source from a pool of existing bilingual data (i.e. ParaCrawl). A model is trained on in-domain monolingual data that is used to score the larger pool of bilingual data. Once scores have been produced, different extracts can be created using a user specified score threshold.

![alt text](https://github.com/paracrawl/Domain_Adaptation/blob/master/ConceptialDiagram2.jpg "Contextual Diagram")

**Definitions:**
* Domain Sample Data:
  * The source language data that represents the content that is in domain. 
  * Larger amount of data will provide better results.
  * This data will be used to train a model for use in domain analysis.
  * This data can be the source language side of existing bilingual data or could be monolingual data in the source language data that is in domain. 
* Pool Data: 
  * Bilingual data that is from mixed domains. 
  * ParaCrawl an example the kind of data that would be suitable to uses as Pool Data.
* Domain Matched Data: 
  * The subset of Pool Data that is determined to be similar to the Domain Sample Data.
  * This data is bilingual and suitable for training a domain specific engine.

## Process and Tools
---------
Each tool can be run independently to update data or to rerun a step if needed without rerunning the entire process. 

![alt text](https://github.com/paracrawl/Domain_Adaptation/blob/master/Process3.jpg "Process")

To run the full process use the following command line:
```bash
FullProcess.sh -dn {domain_name} -sl {source_language} -tl {target_language} -dsd {domain_sample_data_path} -dmd {domain_match_data_path} -est {extract_score_threshold} -c {config_path}
```

*Arguments*
- `-dn` The name of the domain that you are extracting data for. This is used only for the purpose of labeling and identifying the data that is matched.
- `-sl` The source language that will be used for domain analysis. This should be lower case. For example en, fr, de.
- `-tl` The target language that will be paired with the source language when sentence pair data is extracted. This should be lower case.
  - This is used to detemine the path to the *Pool Data*.
- `-dsd` The Domain Sample Data Path is the path to the folder comtaining the *Domain Sample Data* that will be used as a reference set of data for analysis and model training. 
  - This folder must contain one or more files. 
  - Each file in the folder will be checked. If `{domain_sample_path}/{original file name}` does not have a matching file `{domain_sample_path}/tok/{original file name}` then the file will be tokenized and written to `{domain_sample_path}/tok/{original file name}`.
- `-dmd` The path to where the Domain Matched Data and other relevant files will be written. See **Output Files** below for more details.
- `-est` (Optional) This value represents the minimum score for data to be extracted with. If the score is greater than or equal to this score, then the line will be extracted. Values are between 0 and 1. If this parameter is not specified, then the extract process will not be performed. The extract process can be run separately at a later time using `ExtractMatchedDomainData.py`.
- `-c` (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.

The *Pool Data* is usually quite large, so could take a long time to process depending on the size of the data in the pool for the language pair. 
If the *Pool Data* is already tokenized, then the data does not need to be tokenized again. The process has logic that will check files have been tokenized and only tokenize the file once. Deleting the tokenized file will cause it to be tokenized again on the next processing run.

**Example:**

The example below will process *Domain Sample Data* file found in  `/data/mysample/` and write the *Domain Matched Data* to `/data/domain/automotive/en_de/`. Matching data will only be extracted if it scores above the threshold of 0.5.

```sh
FullProcess.sh -dn automotive -s en -t de -dsd /data/mysample/ -dmd /data/domain/ -est 0.5
```

### Output Files
All output files (excluding tokenized data) will be output to the *Domain Match Data* path. This path is then appended with other parameters.

```bash
{domain_match_data_path}/{domain_name}/{source_language}_{target_language}/
```

**Example:**

In the example below, the full path is specified with the automotive domain and a source language of English (en) and a target langauge of German (de). 

```bash
/data/automotive/en_de/
```

Assuming a *Extract Score Threshold* of 0.5 was used, subfolders would be as follows:

```sh
/data/automotive/en_de/0.5/en/
/data/automotive/en_de/0.5/de/
/data/automotive/en_de/model/
/data/automotive/en_de/scores/
```

#### Extracted Domain Matched Data
When extracting, the *Threshold Score* is used to as part of the path so that different extracts can be performed with different scores on the same data.

```bash
{extract_score_threshold}/{source_language}/
{extract_score_threshold}/{target_language}/
```

**Example:**

In the below example the full path is specified, with the score and the source and target language in different folders.

```bash
/data/automotive/en_de/0.15/en
/data/automotive/en_de/0.15/de
```

#### Model
The trained model used for matching is stored in the `model` subfolder.

```bash
{domain_match_data_path}/{domain_name}/{source_language}_{target_language}/model/
```
**Example:**

```bash
/data/automotive/en_de/model/
```
This model will be updated each time the training is run for this language pair and domain.

### Scores
The *Pool Data* is processed and stored in the `scores` subfolder. 

```bash
{domain_match_data_path}/{domain_name}/{source_language}_{target_language}/model/
```
**Example:**

```bash
/data/automotive/en_de/scores/
```
The tool `ExtractDomainData.py` can be run multiple times with different score thresholds to generate different datasets without the need to reprocess the scores.

## Individual Tools
------
### TokenizeDomainSampleData.py
Tokenizes the *Domain Sample Data* using the tokenizer specified in the configuration file.

```sh
TokenizeDomainSampleData.py -dsd {domain_sample_data_path} -sl {source_language} -c {config_path}
```

*Arguments*
- `-dsd` The Domain Sample Data Path is the path to the folder comtaining the *Domain Sample Data* that will be used as a reference set of data for analysis and model training. 
  - This folder must contain one or more files. 
  - Each file in the folder will be checked. If `{domain_sample_path}/{original file name}` does not have a matching file `{domain_sample_path}/tok/{original file name}` then the file will be tokenized and written to `{domain_sample_path}/tok/{original file name}`.
- `-sl` The source language that will be used for domain analysis. This should be lower case. For example en, fr, de.
- `-c` (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.

**Example:**
The below example tokenizes any files not already tokenized in the path `/data/mysample/` and writes the to `/data/mysample/tok/{origninal_file_name}`. The language passed to the tokenizer is English (en).

```sh
TokenizeDomainSampleData.py -dsd /data/mysample/ -sl en
```

### TokenizePoolData.py
Tokenizes the *Pool Data* for a specified language pair using the tokenizer specified in the configuration file. The path to the *Pool Data* is specified in the configuration file.

```sh
TokenizePoolData.py -sl {source_language} -tl {target_language} -c {config_path}
```

*Arguments*
- `-dsd` The Domain Sample Data Path is the path to the folder comtaining the *Domain Sample Data* that will be used as a reference set of data for analysis and model training. 
  - This folder must contain one or more files. 
  - Each file in the folder will be checked. If `{pool_data_path}/{source_language}_{target_language}/{source_language}/{original file name}` does not have a matching file `{pool_data_path}/{source_language}_{target_language}/{source_language}/tok/{original file name}` then the file will be tokenized and written to `{pool_data_path}/{source_language}_{target_language}/{source_language}/tok/{original_file_name}`.
- `-sl` The source language that will be used for domain analysis. This should be lower case. For example en, fr, de.
- `-tl` The target language that will be paired with the source language to determine the path to the language pair in the *Pool Data*. This should be lower case.
- `-c` (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.

Data that is already tokenized in the *Pool Data* folder will not be retokenized. To tokenize again, delete the file in the folder `{pool_data_path}/{source_language}_{target_language}/{source_language}/tok/{file_name}`

**Example:**

The below example tokenizes any files the pool in the en-de language pair that are not already tokenized. The files will be writtern to `{pool_data_path}/en_de/en/tok/{original_file_name}`.

```sh
TokenizePoolData.py -sl en -tl de
```

### TrainDomainModel.py
Trains the domain model to be used when scoring the *Pool Data*.

```sh
TrainDomainModel.py -dn {domain_name} -dnd {domain_data_sample_path} -sl {source_language} -tl {target_language} -dmd {domain_match_data_path} -c {config_path}
```

*Arguments*
- `-dn` The name of the domain that you are training the model for. This is used only for the purpose of labeling and identifying the data that is matched.
- `-dsd` The *Domain Sample Data Path* is the path to the folder comtaining the *Domain Sample Data*. The tokenized files found in the path `{domain_data_sample_path}/tok/` will be used to train the model. 
  - This folder must contain one or more files. 
- `-sl` The source language that will be used for domain analysis. This should be lower case. For example en, fr, de.
- `-tl` The target language that will be paired with the source language to determine the path to the language pair in the *Pool Data*. This should be lower case.
- `-dmd` The path to where the *Domain Matched Data* and other relevant files will be written. See **Output Files** below for more details.
- `-c` (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.

The trained model will be written to `{domain_match_data_path}/{domain_name}/{source_language}_{target_language}/model/`. If the model is retrained, then it will be overwritten.

**Example:**

The below example trains a model and tokenizes any files found in `/data/mysample/tok/` and writes the model file to 
`/data/automotive/en_de/model/`.

```sh
TrainDomainModel.py -dn autotmotive -dnd /data/mysample/ -sl en -tl de -dmd /data/output/
```

### ScorePoolData.py
Scores the *Pool Data* for the specified langauge pair against a specified domain model.

```sh
ScorePoolData.py -dn {domain_name} -sl {source_language} -tl {target_language} -dmd {domain_match_data_path}  -c {config_path}
```

*Arguments*
- `-dn` The name of the domain that you are training the model for. This is used only for the purpose of labeling and identifying the data that is matched.
- `-sl` The source language that will be used for domain analysis. This should be lower case. For example en, fr, de.
- `-tl` The target language that will be paired with the source language to determine the path to the language pair in the *Pool Data*. This should be lower case.
- `-dmd` The path to where the *Domain Matched Data* and other relevant files are written. See **Output Files** below for more details.
- `-c` (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.

* The score data will be written to `{domain_match_data_path}/{domain_name}/{source_language}_{target_language}/scores/`. One file will be output for each file with a matching name to each *Pool Data* file. All previous score files will be deleted before the new scores start processing.
* Pool Data files will be processed from `{pool_data_path}/{source_language}_{target_language}/{source_language}/tok/`.
* The domain model used will be loaded from `{domain_match_data_path}/{domain_name}/{source_language}_{target_language}/model/`. 

**Example:**

In the below example, the model will be loaded from `/data/automotive/en_de/model/` and the scores written to `/data/automotive/en_de/scores/`.

```sh
ScorePoolData.py -dn automotive -sl en -tl de -dmd /data/
```

Once scores have been processed, data can be extracted with different extract score thresholds using `ExtractMatchedDomainData.py`.

### ExtractMatchedDomainData.py

ExtractMatchedDomainData.py -dn {domain_name} -sl {source_language} -tl {target_language} -dmd {domain_match_data_path} -est {extract_score_threshold} -c {config_path}

*Arguments*
- `-dn` The name of the domain that you are training the model for. This is used only for the purpose of labeling and identifying the data that is matched.
- `-sl` The source language that will be used for domain analysis. This should be lower case. For example en, fr, de.
- `-tl` The target language that will be paired with the source language to determine the path to the language pair in the *Pool Data*. This should be lower case.
- `-dmd` The path to where the *Domain Matched Data* and other relevant files are written. See **Output Files** below for more details.
- `-est` This value represents the minimum score for data to be extracted with. If the score is greater than or equal to this score, then the line will be extracted. Values are between 0 and 1. 
- `-c` (Optional) The path to a user specified configuration file. If not specified, then the default configuration file will be used.


* The score data will be loaded from `{domain_match_data_path}/{domain_name}/{source_language}_{target_language}/scores/`. 
* Bilingual *Pool Data* files processed, with the lines in the files that score greater than or equal to the Extract Score Threshold being written to the Matched Domain Data. 
* Source Language Pool Data files - `{pool_data_path}/{source_language}_{target_language}/{source_language}`
* Target Language Pool Data files - `{pool_data_path}/{source_language}_{target_language}/{target_language}`
* Source Language Matched Domain Data files - `{domain_match_data_path}/{domain_name}/{source_language}_{target_language}{extract_score_threshold}/{source_language}/`
et_language}`
* Target Language Matched Domain Data files - `{domain_match_data_path}/{domain_name}/{source_language}_{target_language}/{extract_score_threshold}/{source_language}/`
* The *Extract Score Threshold* is used in the output path to permit the extraction of different datasets at different threshold levels and storing them with a reference to the score that they were matched against.

**Example:**

In the below example, the scores will be loaded from `/data/automotive/en_de/scores/` and the source language domain data written to `/data/automotive/en_de/0.5/en/` and the target language domain data written to `/data/automotive/en_de/0.5/de/`.

```sh
ExtractMatchedDomainData.py -dn automotive -sl en -tl de -dmd /data/ -est 0.5
```

## Configuration File – config.json
------------
The configuration file determines constant elements within the processing such as paths and dependency tools for tokenizing and model training.
```json
{
	"TokenizerCMD" : "/opt/mosesdecoder/scripts/tokenizer/tokenizer.perl -l %langID  -threads 4 < %input_item >  %output_item ",
	"KenLM" : "/opt/send2/Data_Sentences/kenlm/",
	"nGram" : "5",
	"PoolDataRootPath" : "/xxxx/xxx/xx/",
	"LogPath" : "/xxx/"
}
```

## Dependancies
---------------
### KenLM
https://kheafield.com/code/kenlm/

### Tokenizer
The default tokenizer is from the Moses toolkit. Any tokenizer can be used, so long as it is the same tokenizer used for processing both the *Pool Data* and the *Domain Sample Data*.

## Pool Data Folder Structure
The pool data follows a simple structure. Files are stored grouped by language pair and then split into each individual language. Thsi is the same format that ParaCrawl is published in.

* `{pool_data_path}/{source_language}_{target_language}/` - The root folder for the language pair for the overall pool
* `{pool_data_path}/{source_language}_{target_language}/{source_language}` - The pool files in the source language.
* `{pool_data_path}/{source_language}_{target_language}/{target_language}` - The pool files in the target language. The file names should be identical to the source language file name.

**Example:**

```sh
/data/pool/en_de/en/myfile.txt
/data/pool/en_de/de/myfile.txt
```

## FAQ
------
#### What encoding is supported for data files?
All data files should be encoded in UTF-8.

#### What pre-processing of the the in-domain files are needed?
All files should be sentence segmented with 1 sentence per line.

#### What tokenizers can be used?
You can utilize any tokenization scheme that you wish so long as the tokenization is consistent for both the *Domain Sample Data* and the *Pool Data*.

#### Can each step be run manually?
Yes. See the Individual Tools section.

#### Can you run multiple instances at the same time?
Yes, there are no limits on the number of current instances beyond the capacity of the machine that the tools are running on. These processes are memory and disk intensive, as such, this should be taken into consideration when processing multiple concurrent jobs.

#### Datasets like ParaCrawl are very big. Do we need to tokenize them each time?
No. The files are tokenized the first time and then saved. When running the tokenize steps, a check is performed and only files that are not already tokenized are processed.

#### Can I add more files to the Pool Data over time?
Yes. You can copy the source and target langauge files into the source and target language folder under the specified language pair in the Pool Data folder. Next time tokenize is run, these files will be tokenized automatically and then available for scoring. You should run scoring again to include the files in the scores that will be extracted.

#### Can I add more files to the Domain Sample Data over time?
Yes. Copy the files to the Domain Sample Data folder and then run the tokenize process and train the language model. If you run the Full Process, it will tokenize, train the model and score the data with the new model.

