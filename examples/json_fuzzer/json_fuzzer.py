#!/usr/bin/env python3

import frelatage
import zipfile
import json

def fuzz_json(json_file):
    with open(json_file, "rb") as f:
        json_content = f.read()
    json.loads(json_content)

# Load corpus
json_files = frelatage.load_corpus("./")
# Initialize the fuzzer
f = frelatage.Fuzzer(fuzz_json, [json_files])
# Fuzz
f.fuzz()