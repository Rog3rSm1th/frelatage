import frelatage 
from PIL import Image

def fuzz_png(input_file):
    Image.open(input_file)

# Input file is a 1px*1px PNG file
image_file = frelatage.Input(file=True)
f = frelatage.Fuzzer(fuzz_png, [image_file])
f.fuzz()