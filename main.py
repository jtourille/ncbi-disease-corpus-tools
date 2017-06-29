import argparse
import logging
import os

from ncbitools.conll import convert_to_conll

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="Sub-commands", description="Valid sub-commands",
                                       help="Valid sub-commands", dest="subparser_name")

    # Convert to conll
    parser_conll = subparsers.add_parser('CONVERT', help="Convert one corpus part to CONLL format")
    parser_conll.add_argument("--input_file", help="Input corpus part file", dest="input_file", type=str,
                              required=True)
    parser_conll.add_argument("--output_file", help="Output conll file", dest="output_file", type=str,
                              required=True)
    parser_conll.add_argument("--corenlp_url", help="CoreNLP server url", dest="corenlp_url", type=str,
                              required=True)

    args = parser.parse_args()

    if args.subparser_name == "CONVERT":

        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

        logging.info("Converting file: {}".format(os.path.abspath(args.input_file)))
        logging.info("* Target file: {}".format(os.path.abspath(args.output_file)))
        logging.info("* CoreNLP server address: {}".format(args.corenlp_url))

        convert_to_conll(args.input_file, args.output_file, args.corenlp_url)
