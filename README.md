# NCBI Disease Corpus Tools

## 1. Description

This package provides several tools related to the [NCBI Disease Corpus](https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/):
1. Conversion of the corpus into tabulated format. Segmentation and tokenization are performed using [CoreNLP](https://stanfordnlp.github.io/CoreNLP/).
2. Conversion of the corpus into the [brat](http://brat.nlplab.org/) format (not yet implemented).

Characteristics of the tabulated files:
* Sentences are separated by empty lines
* One token per line
* Three columns per line separated by tabulations: *token*, *part-of-speech tag*, *label*
* Labels follow the IOB format: a token can be the beginning of a disease mention (B-Disease), inside a disease mention (I-Disease) or outside a disease mention (O)

## 2. Usage

General requirements:
* You must have a working [Python](https://www.python.org/) environment. Required libraries are mentioned in the `requirements.txt` file

### CoNLL format

Requirements:
* You must have a [CoreNLP server](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html) running somewhere on your network

To convert the files that are contained within the `original-data` directory, please follow the example below (adjust the CoreNLP server address to your settings).
```bash
python main.py CONVERT --input_file original-data/NCBItrainset_corpus.txt \
    --output_file ./train.conll \
    --corenlp_url http://localhost:9000

python main.py CONVERT --input_file original-data/NCBIdevelopset_corpus.txt \
    --output_file ./dev.conll \
    --corenlp_url http://localhost:9000
    
python main.py CONVERT --input_file original-data/NCBItestset_corpus.txt \
    --output_file ./test.conll \
    --corenlp_url http://localhost:9000
```