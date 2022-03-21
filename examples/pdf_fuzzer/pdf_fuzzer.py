import frelatage 
import PyPDF2

def fuzz_pdf(input_file):
    # creating a pdf file object
    pdfFileObj = open(input_file, 'rb')
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pdfFileObj.close()

# Load Corpus
pdf_file = frelatage.load_corpus("./")
# Initialize the fuzzer
f = frelatage.Fuzzer(fuzz_pdf, [pdf_file])
# Fuzz
f.fuzz()