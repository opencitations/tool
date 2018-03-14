#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2016, Silvio Peroni <essepuntato@gmail.com>
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

# This script takes an input directory containing JSON files, an old key and
# the new one to use, and substitute all the occurences of the old key with
# the new key specified.

from argparse import ArgumentParser
from os import walk, sep
from json import load, dump


def change_key(d, o, n):
    if isinstance(d, dict):
        for k in d:
            change_key(d[k], o, n)
            if k == o:
                d[n] = d[k]
                del d[k]
    elif isinstance(d, list):
        for i in d:
            change_key(i, o, n)


arg_parser = ArgumentParser("jsonnoascii.py")
arg_parser.add_argument("-i", "--input_dir", dest="input_dir", required=True,
                        help="The directory containing JSON files to modify.")
arg_parser.add_argument("-o", "--old_key", dest="old_key", required=True,
                        help="The JSON key to change.")
arg_parser.add_argument("-n", "--new_key", dest="new_key", required=True,
                        help="The new JSON key to use instead of the old one.")

args = arg_parser.parse_args()
for cur_dir, cur_subdir, cur_files in walk(args.input_dir):
    for cur_file in cur_files:
        if cur_file.endswith(".json"):
            cur_path = cur_dir + sep + cur_file
            cur_json = None
            with open(cur_path) as f:
                cur_json = load(f)
            if cur_json is not None:
                change_key(cur_json, args.old_key, args.new_key)
                with open(cur_path, "w") as f:
                    dump(cur_json, f, indent=4, ensure_ascii=False)
