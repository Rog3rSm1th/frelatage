#!/usr/bin/bash

# Set up the env variables
export FRELATAGE_DICTIONARY_ENABLE=1 &&
export FRELATAGE_TIMEOUT_DELAY=2 &&
export FRELATAGE_INPUT_FILE_TMP_DIR="/tmp/frelatage" &&
export FRELATAGE_INPUT_MAX_LEN=4096 &&
export FRELATAGE_MAX_THREADS=8 &&
export FRELATAGE_MAX_CYCLES_WITHOUT_NEW_PATHS=5000 &&
export FRELATAGE_INPUT_DIR="./in" &&
export FRELATAGE_DICTIONARY_DIR="./dict" &&

if [ $# -eq 0 ]
  then
    # Help message
    echo "Usage: ./run.sh <fuzzing harness file>"
    echo "Example: ./run.sh my_fuzzer.py"
    # Exit the program
    exit
fi

# Run the fuzzer
python3 $1