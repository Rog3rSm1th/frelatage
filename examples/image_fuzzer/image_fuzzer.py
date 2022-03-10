import frelatage 
from PIL import Image

def fuzz_gif(input_file):
    Image.open(input_file)

# Corpus
# We use 1px*1px GIF, JPEG and PNG files
gif_file = frelatage.Input(file=True, value="image.gif")
jpeg_file = frelatage.Input(file=True, value="image.gif")
png_file = frelatage.Input(file=True, value="image.gif")

f = frelatage.Fuzzer(fuzz_gif, [[gif_file, jpeg_file, png_file, png_file]])
f.fuzz()