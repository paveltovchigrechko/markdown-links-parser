# markdown-parser

## What is it? 

This is an auxiliary Python script for parsing and checking text files. The main problem it solves is verifying Markdown links between text files. For example, the Docusaurus, a static site generator that we use for documentation, recognizes the link to a non-existing file like \[a link to a file\](non-existing-path-to-file). But it cannot recognize a link to a non-existing heading inside a file: \[link to a paragraph\](existing-file#non-existing-heading). So, when we change a heading we might break a link to it in other files. This script is intended to catch such situations. 

## Configuration

The script is configurable. You can define configuration parameters either in a `config.ini` file or pass them as arguments when running the script. 

### Config file

The configuration must have a section `[MAIN]` and the following parameters:
* `root` is the root directory where the files are scanned. Note that the script works with all files of the given extension in the root recursively. The root can be an absolute path or a relative path. 
* `file_extension` is the extension of files that are being parsed. Accepts only one value with a leading dot, for example `.md`. You can use any text extension that can be opened with the default Python `open` function.
* `action` is the intended action of the script. Accepts one of the following values: 
<!--  * `check_links` parses all files with a given extension in a given root and checks all Markdown links. If there are broken links, it outputs them in a stream specified in `output` parameter. -->
<!--  * `print_links` parses all files with a given extension in a given root and prints them in a stream specified in `output` parameter. -->
  * `search` asks for a non-empty string to search, parses all files with the given extension in the given root, and searches the string. Then outputs the result in a stream specified in `output` parameter.
<!-- * `output` defines the stream for outputting the action result. Accepts one of the following values: -->
<!--  * `console` outputs the result in the standard OS console stream -->
<!--  * `file` creates a `txt` file in the script directory with the result -->

If `config.ini` misses `[MAIN]` section, the default configuration is used.
If `config.ini` misses one or more obligatory parameters in `[MAIN]` section, the default values are used.
If a path specified in `root` parameter is not found or not a directory or empty string, the default value is used.
If `action` <!-- and / or `output` parameters have --> has a value that is not accepted, the default value is used.
All other sections and parameters are ignored.

Default configuration:
```commandline
[MAIN]
root: .
file_extension: .mdx
action: check_links
<!-- output: console -->
```

### Arguments

Note if you pass configuration arguments, the config file is ignored.

All arguments are optional, if you don't pass an argument the default value will be used.
You can use the following configuration arguments in command line:
* `-r` or `--root` to define the root directory
* `-f` or `--file` to define the file extension
<!-- * `-o` or `--output` to define the output format. The argument accepts `file` or `console` values only -->
* `-a` or `--action` to define the action. The argument accepts `check_links`<!-- , `print_links`, --> or `search` values only

Run `python3 main.py -h` to see the help in console.

Example of using arguments:
```commandline
python3 main.py -r ../../docs -f .md <!-- -o file --> -a print_links
```

## Script files and directories

TBD.

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
