import frelatage 
from ruamel.yaml import YAML
import yaml
import io

ruamel_yaml = YAML(typ='safe')

def fuzz_yaml_load(yaml_file):
    with open(yaml_file, "r") as f:
        data = f.read()
    a = ruamel_yaml.load(data)

# Load Corpus
yaml_corpus = frelatage.load_corpus(directory="./")
# Initialize the fuzzer
f = frelatage.Fuzzer(fuzz_yaml_load, [yaml_corpus])
# Fuzz
f.fuzz()