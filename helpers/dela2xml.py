#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import logging
from logging.config import dictConfig

import xml.etree.ElementTree as ET
from xml.dom import minidom

import re

from zipfile import BadZipFile
import pandas as pd

###############################################################################
# global constants
###############################################################################
LEVEL = [logging.WARNING, logging.INFO, logging.DEBUG]

###############################################################################
# Functions
###############################################################################
def configure_logger(args) -> logging.Logger:
    """Setup the global logging configurations and instanciate a specific logger for the current script

    Parameters
    ----------
    args : dict
        The arguments given to the script

    Returns
    --------
    the logger: logger.Logger
    """
    # create logger and formatter
    logger = logging.getLogger()

    # Verbose level => logging level
    log_level = args.verbosity
    if args.verbosity >= len(LEVEL):
        log_level = len(LEVEL) - 1
        logging.warning(
            "verbosity level is too high, I'm gonna assume you're taking the highest (%d)"
            % log_level
        )

    # Define the default logger configuration
    logging_config = dict(
        version=1,
        disable_existing_logger=True,
        formatters={
            "f": {
                "format": "[%(asctime)s] [%(levelname)s] — [%(name)s — %(funcName)s:%(lineno)d] %(message)s",
                "datefmt": "%d/%b/%Y: %H:%M:%S ",
            }
        },
        handlers={
            "h": {
                "class": "logging.StreamHandler",
                "formatter": "f",
                "level": LEVEL[log_level],
            }
        },
        root={"handlers": ["h"], "level": LEVEL[log_level]},
    )

    # Add file handler if file logging required
    if args.log_file is not None:
        logging_config["handlers"]["f"] = {
            "class": "logging.FileHandler",
            "formatter": "f",
            "level": LEVEL[log_level],
            "filename": args.log_file,
        }
        logging_config["root"]["handlers"] = ["h", "f"]

    # Setup logging configuration
    dictConfig(logging_config)

    # Retrieve and return the logger dedicated to the script
    logger = logging.getLogger(__name__)
    return logger


def define_argument_parser() -> argparse.ArgumentParser:
    """Defines the argument parser

    Returns
    --------
    The argument parser: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description="")

    # Add logging options
    parser.add_argument("-l", "--log_file", default=None, help="Logger file")
    parser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        default=0,
        help="increase output verbosity",
    )

    # Add script options
    parser.add_argument(
        "-d",
        "--domain",
        required=False,
        type=str,
        default=None,
        help="The list of domain to select (if undefined, get all of them). The list is comma separated",
    )

    # Add arguments
    parser.add_argument(
        "input_spreadsheet", help="The spreadsheet containing the corpus"
    )
    parser.add_argument(
        "output_xml", help="The output XML file formatted following the WMT format"
    )

    # Return parser
    return parser


def spreadsheet2xml(spreadsheet, root_node, domain):
    i_doc = 0
    for i_row, row in spreadsheet.iterrows():
        if str(row["ID"]).startswith("<doc"):
            i_doc += 1
            id_val = str(row["text = source"])
            doc_id = f"{domain}-{i_doc}"

            if 'docid="' in id_val:
                doc_src = ""
                m = re.search(r'.*docid="([^"]*)".*', str(row["text = source"]))
                if not m:
                    raise Exception(f'The row doesn\'t seem to be formatted correctly: {str(row["text = source"])}')

                doc_id += f"_{m.group(1)}"
            else:
                # FIXME: it seems to not be consistent in the spreadsheet itself
                doc_src = str(row["text = source"]).replace(">", "").strip()

            doc_node = ET.SubElement(
                root_node,
                "doc",
                attrib={
                    "id": doc_id,
                    "src": doc_src,
                    "domain": domain,
                    "origlang": "en",
                },
            )
            src_node = ET.SubElement(doc_node, "src", attrib={"lang": "en"})
            src_node = ET.SubElement(src_node, "p")
            tgt_node = ET.SubElement(
                doc_node, "ref", attrib={"lang": "pt", "translator": "A"}  # FIXME: check this
            )
            tgt_node = ET.SubElement(tgt_node, "p")

        elif str(row["ID"]).startswith("<seg"):
            m = re.search(r'<seg id="([0-9]*)">', row["ID"])
            if m:
                seg_id = m.group(1)

                seg = ET.SubElement(src_node, "seg", attrib={"id": seg_id})
                seg.text = str(row["text = source"])

                seg = ET.SubElement(tgt_node, "seg", attrib={"id": seg_id})
                seg.text = str(row["PT-BR"])
            else:
                raise Exception(
                    f"It should be a segment with an ID, but got: {row['ID']}"
                )


###############################################################################
#  Envelopping
###############################################################################
if __name__ == "__main__":
    # Initialization
    arg_parser = define_argument_parser()
    args = arg_parser.parse_args()
    logger = configure_logger(args)

    # Loading the session file
    input_file = args.input_spreadsheet
    try:
        xlsx = pd.ExcelFile(input_file, engine="openpyxl")
        logger.info(f"Loaded {input_file} which contains sheets {xlsx.sheet_names}")
    except BadZipFile:
        logger.fatal(
            f"Cannot open Excel file ({input_file}): please either save or close it and try again"
        )
        sys.exit(1)

    # Convert each sheet to a dataframe
    output_dataset = ET.Element("dataset")
    for sheet_name in xlsx.sheet_names:
        spreadsheet_df = pd.read_excel(xlsx, sheet_name)

        output_dataset_collection = ET.SubElement(
            output_dataset, "collection", attrib={"id": sheet_name}
        )
        spreadsheet2xml(spreadsheet_df, output_dataset_collection, sheet_name)

    output_str = ET.tostring(output_dataset, encoding="unicode")
    xmlstr = minidom.parseString(output_str).toprettyxml(indent="  ")
    with open(args.output_xml, "w") as f_out:
        f_out.write(xmlstr)
