import frelatage
import bleach

input = frelatage.Input("aaaaaaaaaaaaaaa")


@frelatage.instrument(
    [[input]], output_directory="./linkify_errors", coverage_directory="./linkify_cov"
)
def fuzz_linkify(input):
    bleach.linkify(input)


@frelatage.instrument(
    [[input]], output_directory="./clean_errors", coverage_directory="./clean_cov"
)
def fuzz_clean(input):
    bleach.clean(input)


frelatage.Fuzzer.fuzz_all()
