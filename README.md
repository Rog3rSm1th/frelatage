<p align=center>
  <img src="doc/frelatage_logo.gif" width="200" height="200" style="border-radius:4px"/>
  <br>
  <code>pip3 install frelatage</code></br>
  <i>Current release : <a href="https://github.com/Rog3rSm1th/Frelatage/releases">0.0.1</a></i></br></br>
  <a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg"></a>
  <a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.6-green.svg"></a>
  <a target="_blank" href="LICENSE" title="License: MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  <a target="_blank" title="Downloads"><img src="https://static.pepy.tech/badge/frelatage"></a>
  <a target="_blank" href="https://twitter.com/Rog3rSm1th" title="Python version"><img src="https://img.shields.io/badge/-@Rog3rSm1th-1ca0f1?style=flat-square&labelColor=1ca0f1&logo=twitter&logoColor=white&link=https://twitter.com/Rog3rSm1th"></a>
  <br>
  <span><i>The Python Fuzzer that the world deserves</i></span>
</p>

<p align="center">
  <a href="#installation">Installation</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#how-it-works">How it works</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#features">Features</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#use-frelatage">Use Frelatage</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#configuration">Configuration</a>
</p>

![](doc/frelatage_demo.gif)

**DISCLAIMER** : This project is at the alpha stage and can still cause many unexpected behaviors. Frelatage should not be used in a production environment at this time.



Frelatage is a coverage-based Python fuzzing library which can be used to fuzz python code. The development of Frelatage was inspired by various other fuzzers, including [AFL](https://github.com/google/AFL)/[AFL++](https://github.com/AFLplusplus/AFLplusplus), [Atheris](https://github.com/google/atheris) and [PyFuzzer](https://github.com/eerimoq/pyfuzzer).The main purpose of the project is to take advantage of the best features of these fuzzers and gather them together into a new tool in order to efficiently fuzz python applications.

## Requirements
[Python 3](https://www.python.org/)

## Installation

#### Install with pip (recommended)

```bash
pip3 install frelatage
```

#### Or build from source

Recommended for developers. It automatically clones the main branch from the frelatage repo, and installs from source.

```bash
# Automatically clone the Frelatage repository and install Frelatage from source
bash <(wget -q https://raw.githubusercontent.com/Rog3rSm1th/Frelatage/main/scripts/autoinstall.sh -O -)
```

## How it works

The idea behind the design of Frelatage is the usage of a genetic algorithm to generate mutations that will cover as much code as possible. The functioning of a fuzzing cycle can be roughly summarized with this diagram : 

```mermaid
graph TB

    m1(Mutation 1) --> |input| function(Fuzzed function)
    m2(Mutation 2) --> |input| function(Fuzzed function)
    mplus(Mutation ...) --> |input| function(Fuzzed function)
    mn(Mutation n) --> |input| function(Fuzzed function)
    
    function --> generate_reports(Generate reports)
    generate_reports --> rank_reports(Rank reports)  
    rank_reports --> select(Select n best reports)
    
    select --> |mutate| nm1(Mutation 1) & nm2(Mutation 2) & nmplus(Mutation ...) & nmn(Mutation n)
    
    subgraph Cycle mutations
    direction LR
    m1
    m2
    mplus
    mn
    end
    
    subgraph Next cycle mutations
    direction LR
    nm1
    nm2
    nmplus
    nmn
    end
     
    style function fill:#5388e8,stroke:white,stroke-width:4px
```
## Features

#### Fuzzing different argument types: 
  - String
  - Int
  - Float
  - List
  - Tuple
  - Dictionnary
  
#### File fuzzing
Frelatage allows to fuzz a function by passing a file as input. 

## Use Frelatage

#### Fuzz a classical parameter

```python
import frelatage
import my_vulnerable_library

def MyFunctionFuzz(data):
  my_vulnerable_library.parse(data)

input = frelatage.Input(value="initial_value")
f = frelatage.Fuzzer(MyFunctionFuzz, [input])
f.fuzz()
```

#### Fuzz a file parameter

Frelatage gives you the possibility to fuzz file type input parameters. To initialize the value of these files, you must create as many files in the input folder as there are arguments of type file. These files must be named as follows: the first file argument must be named ```0```, the second ```1```, and so on.

```bash
echo "initial value" > ./in/0
```

For example : 

```python
import frelatage
import my_vulnerable_library

def MyFunctionFuzz(data):
  my_vulnerable_library.load_file(data)

input = frelatage.Input(file=True)
f = frelatage.Fuzzer(MyFunctionFuzz, [input])
f.fuzz()
```

#### Fuzz with a dictionnary

You can copy one or more dictionaries located [here](https://github.com/Rog3rSm1th/Frelatage/tree/main/dictionnaries) in the directory dedicated to dictionaries (`./dict` by default).


## Reports

Each crash is saved in the output folder (```./out``` by default), in a folder named : ```id<crash ID>,err<error type>```.

The report directory is in the following form: 
```
    ├── out
    │   ├── id<crash ID>,err<error type>
    │       ├── input
    │       ├── 0
    │       └── ...
    │   ├── ...
```

#### Read a crash report

Inputs passed to a function are serialized using the [pickle](https://docs.python.org/3/library/pickle.html) module before being saved in the ```<report_folder>/input file```. It is therefore necessary to deserialize it to be able to read the contents of the file. This action can be performed with [this script](https://github.com/Rog3rSm1th/Frelatage/blob/main/scripts/read_report.py). 

```bash
./read_report.py input
```
  
## Configuration

There are two ways to set up Frelatage:

#### Using the environment variables

| ENV Variable                   | Description |
| -------------------------------| ----------- |
| FRELATAGE_TIMEOUT_DELAY        | Delay after which a function will return a timeoutError |
| FRELATAGE_INPUT_FILE_TMP_DIR   | Temporary folder where input files are stored. It needs to be an absolute path |
| FRELATAGE_INPUT_MAX_LEN        | Maximum size of an input variable in bytes |
| FRELATAGE_MAX_THREADS          | Maximum number of simultaneous threads |
| FRELATAGE_DICTIONNARY_DIR      | Default directory for dictionaries. It needs to be a relative path (to the path of the fuzzing file) |


A configuration example :

```bash
export FRELATAGE_TIMEOUT_DELAY=2 &&
export FRELATAGE_INPUT_FILE_TMP_DIR="/tmp/frelatage" &&
export FRELATAGE_INPUT_MAX_LEN=4096 &&
export FRELATAGE_MAX_THREADS=20 &&
export FRELATAGE_DICTIONNARY_DIR="./dict" &&
python3 fuzzer.py
```

#### Passing arguments to the fuzzer 

```python
import frelatage 

def myfunction(input1_string, input2_int):
    pass

input1 = frelatage.Input(value="initial_value")
input2 = frelatage.Input(value=2)

f = frelatage.Fuzzer(
    # The method you want to fuzz
    method=myfunction,
    # The initial arguments
    arguments=[input1, input2],
    # Number of threads
    threads_count=8,
    # Exceptions that will be taken into account
    exceptions_whitelist=(OSError),
    # Exceptions that will not be taken into account
    exceptions_blacklist=(),
    # Directory where the error reports will be stored
    output_directory="./out",
    # Directory containing the initial input files
    input_directory="./in"
)
f.fuzz()
```

## Risks 

Please keep in mind that, similarly to many other computationally-intensive
tasks, fuzzing may put strain on your hardware and on the OS. In particular:

  - Your CPU will run hot and will need adequate cooling. In most cases, if
    cooling is insufficient or stops working properly, CPU speeds will be
    automatically throttled. That said, especially when fuzzing on less
    suitable hardware (laptops, smartphones, etc), it's not entirely impossible
    for something to blow up.

  - Targeted programs may end up erratically grabbing gigabytes of memory or
    filling up disk space with junk files. Frelatage tries to enforce basic memory
    limits, but can't prevent each and every possible mishap. The bottom line
    is that you shouldn't be fuzzing on systems where the prospect of data loss
    is not an acceptable risk.

  - Fuzzing involves billions of reads and writes to the filesystem. On modern
    systems, this will be usually heavily cached, resulting in fairly modest
    "physical" I/O - but there are many factors that may alter this equation.
    It is your responsibility to monitor for potential trouble; with very heavy
    I/O, the lifespan of many HDDs and SSDs may be reduced.

    A good way to monitor disk I/O on Linux is the 'iostat' command:

```shell
    $ iostat -d 3 -x -k [...optional disk ID...]
```

## Contact 

for any remark, suggestion, bug report, or if you found a bug using Frelatage, you can contact me at r0g3r5@protonmail.com or on twitter [@Rog3rSm1th](https://twitter.com/Rog3rSm1th)
