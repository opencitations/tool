#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2018, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.

# This script takes an input directory, looks for all the brs that have more than one DOI,
# and returns a two-column table with the br local id plus a dash separated list of local id
# of the ids identified

from argparse import ArgumentParser
from os import walk, sep
from json import load, dump


def browse_dir(local_dir, f_to_call, *res):
    for cur_dir, cur_subdir, cur_files in walk(args.input_dir + sep + local_dir):
        for cur_file in cur_files:
            if cur_file.endswith(".json"):
                cur_path = cur_dir + sep + cur_file
                with open(cur_path) as f:
                    cur_json = load(f)
                    for cur_entity in cur_json["@graph"]:
                        f_to_call(cur_entity, *res)


def add_doi(entity, res):
    if "type" in entity and entity["type"] == "doi":
        id_string = ""
        if "id" in entity:
            id_string = entity["id"]
        res[entity["iri"]] = id_string


def duplicate_doi(entity, dois, res):
    cur_dois = []

    if "identifier" in entity:
        for cur_id in entity["identifier"]:
            if cur_id in dois:
                cur_dois.append({"r": cur_id, "t": dois[cur_id]})

        if len(cur_dois) > 1:
            res[entity["iri"]] = cur_dois


arg_parser = ArgumentParser("duplicateddoi.py")
arg_parser.add_argument("-i", "--input_dir", dest="input_dir", required=True,
                        help="The directory of the Corpus.")
arg_parser.add_argument("-o", "--out_file", dest="out_file", required=True,
                        help="The file where to store all the information.")

args = arg_parser.parse_args()

print("Start duplicateddoi")

# Find all DOIs
all_dois = {}
browse_dir("id", add_doi, all_dois)

# Get all duplicated DOIs
dup_doi = {}
browse_dir("br", duplicate_doi, all_dois, dup_doi)
with open(args.out_file, "w") as f:
    dump(dup_doi, f, ensure_ascii=False)

print("End")
