#!/usr/bin/env python3
# usage : ./read_report input
import pickle
import sys

if len(sys.argv) > 1:
    report_file = sys.argv[1]
else:
    print("Usage : ./read_report.py <report file>")
    sys.exit(1)

with open(report_file, "rb") as f:
    report = pickle.load(f)
    print(report)
