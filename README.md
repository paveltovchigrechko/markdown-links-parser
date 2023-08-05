# markdown-parser

## What is it? 

This is an auxiliary Python script for parsing and checking text files. The main problem it solves is verifying Markdown links between text files. 

## Configuration

The script is configurable. You can define a `config.ini` file in a script directory to adjust the script action. The configuration must have a section `[MAIN]` and the following parameters:
* `root` is the root directory where the files are scanned. Note that script works with all files of given extension in the root recursively. Root can be an absolute path or a relative path. 
* `file_extension` is the extension of files that are being parsed. Accepts only one value with leading dot, for example `.md`. You can use any text extension that can be opened with default Python `open` function.
* `action` is intended action of the script. Accepts one of the following values: 
  * `check_links` parses all files with given extension in given root and checks all Markdown links in them. If there are broken links, outputs them in a stream specified in `output` parameter.
  * `print_links` parses all files with given extension in given root and prints them in a stream specified in `output` parameter.
  * `search` asks for a non-empty string to search, parses all files with given extension in given root and searches the string. Then outputs the result in a stream specified in `output` parameter.
* `output` defines the stream for outputting the action result. Accepts one of the following values:
  * `console` outputs the result in standard OS console stream
  * `file` creates a `txt` file in script directory with the result 

If `config.ini` misses `[MAIN]` section, the default configuration is used.
If `config.ini` misses one or more obligatory parameters in `[MAIN]` section, the default values are used.
If a path specified in `root` parameter is not found or not a directory or empty string, the default value is used.
If `action` and / or `output` parameters have the value that is not accepted, the default value is used.
All other sections and parameters are ignored.

Default configuration:
```commandline
[MAIN]
root: .
file_extension: .mdx
action: check_links
output: console
```

## Script files

* `main.py` is the main runner. Reads config and runs the corresponding methods
* `parser.py` contains the objects and methods for parsing directories, files, checking links, searching given line
* `config.py` contains the config object and methods
* `test_config.py` and `test_parser.py` contain tests for the corresponding files

## Using as Git action

You can run the script as a Github action, for example, when someone creates a new PR.

1. Create a `yaml` file in `.github/workflows` directory.
2. Copy the following snippet into `yaml` file:
```
name: Check Markdown links

on: 
  pull_request:    
    branches: [ "main", "test", "develop" ]

  workflow_dispatch:

jobs:
  links-checker:
    name: links-checker
    runs-on: ubuntu-latest
    steps:
    - name: Normal checkout
      uses: actions/checkout@v3
      
    - name: Check-out parser repository
      uses: actions/checkout@v2
      with:
        repository: paveltovchigrechko/markdown-parser
        path: "markdown-parser"
        
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11

    - name: Run parser
      run: python3 markdown-parser/main.py      
``` 
