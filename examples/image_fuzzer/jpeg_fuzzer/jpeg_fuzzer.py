import frelatage 
from PIL import Image

def fuzz_jpeg(input_file):
    Image.open(input_file)

# Input file is a 1px*1px JPEG file
image_file = frelatage.Input(file=True)
f = frelatage.Fuzzer(fuzz_jpeg, [image_file])
f.fuzz()