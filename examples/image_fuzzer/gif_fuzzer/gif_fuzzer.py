import frelatage 
from PIL import Image

def fuzz_gif(input_file):
    Image.open(input_file)

# Input file is a 1px*1px GIF file
image_file = frelatage.Input(file=True)
f = frelatage.Fuzzer(fuzz_gif, [image_file])
f.fuzz()