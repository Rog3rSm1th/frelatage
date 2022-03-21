#!/usr/bin/env python3
# Inspired by the Atheris JSON differential fuzzer: https://github.com/google/atheris/blob/master/example_fuzzers/json_fuzzer/json_differential_fuzzer.py

import frelatage
import json
import ujson

class JsonParsingException(Exception):
    pass

def ClearAllIntegers(data):
    """
    Used to prevent known bug; sets all integers in data recursively to 0.
    """
    if type(data) == int:
        return 0
    if type(data) == list:
        for i in range(0, len(data)):
            data[i] = ClearAllIntegers(data[i])
    if type(data) == dict:
        for k, v in data:
             data[k] = ClearAllIntegers(v)
    return data   

def fuzz_json(json_file):
    with open(json_file, "rb") as f:
        json_content = f.read()

    try:
        json_data = json.loads(json_content)
        ujson_data = ujson.loads(json_content)
    except Exception as e:
        return

    json_data = ClearAllIntegers(json_data)
    ujson_data = ClearAllIntegers(ujson_data)
   
    json_dumped = json.dumps(json_data)
    ujson_dumped = ujson.dumps(ujson_data)

    if json_dumped != ujson_dumped:
        raise JsonParsingException
    return

# Load corpus
json_files = frelatage.load_corpus(directory="./")
# Initialize the fuzzer
f = frelatage.Fuzzer(fuzz_json, [json_files], exceptions_whitelist=(JsonParsingException))
# Fuzz
f.fuzz()