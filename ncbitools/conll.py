import os
import re

import requests

PARAMS = {"annotators": "tokenize,ssplit,pos", "outputFormat": "json"}


def convert_to_conll(input_corpus_file, output_conll_file, corenlp_url):

    regex_title = re.compile("^(\d+)\|t\|(.*)$")
    regex_abstract = re.compile("^(\d+)\|a\|(.*)$")
    regex_annotation = re.compile("^(\d+)\t(\d+)\t(\d+)\t([^\t]+)\t([^\t]+)\t([^\t]+)$")

    instances = dict()

    with open(os.path.abspath(input_corpus_file), "r", encoding="UTF-8") as input_file:
        for line in input_file:

            if re.match("^$", line):
                continue

            match_title = regex_title.match(line)
            if match_title:
                instances[int(match_title.group(1))] = {
                    "title": match_title.group(2),
                    "annotations": list()
                }

            match_abstract = regex_abstract.match(line)
            if match_abstract:
                instances[int(match_abstract.group(1))]["abstract"] = match_abstract.group(2)

            match_annotation = regex_annotation.match(line)
            if match_annotation:
                instances[int(match_annotation.group(1))]["annotations"].append({
                    "begin": int(match_annotation.group(2)),
                    "end": int(match_annotation.group(3)),
                    "text": match_annotation.group(4),
                    "entity": match_annotation.group(5),
                    "tokens": list()
                })

    with open(os.path.abspath(output_conll_file), "w", encoding="UTF-8") as output_file:
        for pmid, content in instances.items():

            r = requests.post(corenlp_url, params=PARAMS, data="{} {}".format(
                content["title"],
                content["abstract"]
            ))
            r_content = r.json()

            annotations_sorted = sorted(content["annotations"], key=lambda tup: tup["begin"])

            for sentence in r_content["sentences"]:
                for token in sentence["tokens"]:
                    for annotation in annotations_sorted:

                        if annotation["begin"] == token["characterOffsetBegin"] and \
                                        token["characterOffsetEnd"] <= annotation["end"]:

                            annotation["tokens"].append((sentence["index"], token["index"]))

                        elif annotation["end"] == token["characterOffsetEnd"] and \
                                        annotation["begin"] <= token["characterOffsetBegin"]:

                            annotation["tokens"].append((sentence["index"], token["index"]))

                        elif annotation["begin"] <= token["characterOffsetBegin"] < token["characterOffsetEnd"] \
                                <= annotation["end"]:

                            annotation["tokens"].append((sentence["index"], token["index"]))

                for token in sentence["tokens"]:

                    label = "O"

                    for annotation in annotations_sorted:

                        if (sentence["index"], token["index"]) in annotation["tokens"]:
                            if annotation["tokens"].index((sentence["index"], token["index"])) == 0:
                                label = "B-Disease"
                            else:
                                label = "I-Disease"

                    line_str = "{}\t{}\t{}\n".format(
                        token["originalText"],
                        token["pos"],
                        label
                    )
                    output_file.write(line_str)

                output_file.write("\n")
