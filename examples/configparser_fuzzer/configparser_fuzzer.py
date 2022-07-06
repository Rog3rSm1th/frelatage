import frelatage
import configparser
from configparser import ConfigParser, ExtendedInterpolation

parser = ConfigParser(interpolation=ExtendedInterpolation())


def fuzz_configparser(config_file):
    with open(config_file, "r") as f:
        string = f.read()
    parser.read_string(string)


# Load Corpus
toml_corpus = frelatage.load_corpus(directory="./")
# Initialize the fuzzer
f = frelatage.Fuzzer(
    fuzz_configparser,
    [toml_corpus],
    exceptions_blacklist=(
        configparser.NoSectionError,
        configparser.DuplicateSectionError,
        configparser.DuplicateOptionError,
        configparser.NoOptionError,
        configparser.InterpolationError,
        configparser.InterpolationDepthError,
        configparser.InterpolationMissingOptionError,
        configparser.InterpolationSyntaxError,
        configparser.MissingSectionHeaderError,
        configparser.ParsingError,
    ),
)
# Fuzz
f.fuzz()
