import frelatage 
from PIL import Image

def fuzz_gif(input_file):
    Image.open(input_file)

# Load corpus
gif_file = frelatage.load_corpus("./gif")
jpeg_file = frelatage.load_corpus("./jpg")
png_file = frelatage.load_corpus("./png")
image_file = gif_file + jpeg_file + png_file

# Initialize the fuzzer
f = frelatage.Fuzzer(fuzz_gif, [image_file])
# Fuzz
f.fuzz()