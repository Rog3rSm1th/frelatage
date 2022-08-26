import frelatage
from PyPDF2 import PdfFileReader, utils
import time


def fuzz_pypdf2(pdf_file):
    reader = PdfFileReader(pdf_file)
    return


# Load Corpus
pdf_file = frelatage.load_corpus("./")
# Initialize the fuzzer
f = frelatage.Fuzzer(fuzz_pypdf2, [pdf_file], exceptions_blacklist=(utils.PdfReadError))
# Fuzz
f.fuzz()
