import frelatage
from ruamel.yaml import YAML
import yaml

ruamel_yaml = YAML(typ='safe')

class YamlParsingError(Exception):
    pass

def fuzz_yaml_load_differential(yaml_file):
    with open(yaml_file, "r") as f:
        data = f.read()

    yaml_load = yaml.load(data, Loader=yaml.FullLoader)
    ruamel_yaml_load = ruamel_yaml.load(data)

    print(yaml_load, ruamel_yaml_load)

    if yaml_load != ruamel_yaml_load:
        raise YamlParsingError

# Load Corpus
yaml_corpus = frelatage.load_corpus(directory="./")
# Initialize corpus
f = frelatage.Fuzzer(fuzz_yaml_load_differential, [yaml_corpus], exceptions_whitelist=(YamlParsingError))
# Fuzz
f.fuzz()