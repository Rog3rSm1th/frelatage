import frelatage
from ruamel.yaml import YAML
import io

ruamel_yaml = YAML(typ='safe')

def fuzz_yaml_dump(data):
    string = io.StringIO()
    ruamel_yaml.dump(data, string)

# Load Corpus
dictionary = frelatage.Input(value={
    "key1": "value1",
    2: "value2",
    3: ["list_value1", "list_value2", 3, 4.999999, (1, [1, 2, 3], 3, 4), None]
})

# Initialize the fuzzer
f = frelatage.Fuzzer(fuzz_yaml_dump, [[dictionary]], infinite_fuzz=True)
# Fuzz
f.fuzz()