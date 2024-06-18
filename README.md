# FP

A tool to generate file fingerprints

## Installation

Git clone this repository and run the following command:

```bash
pip install .
```

## Usage

```bash
python -m FP <file>
```

This will output the fingerprint of the file in JSON

```
usage: __main__.py [-h] [-o OUTPUT] [-v] [-n NOTE] [-f FORMAT] [-bo] file

Fingerprinter

positional arguments:
  file                  The file to fingerprint

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        The output file to write the fingerprint to
  -v, --verbose         Verbose output
  -n NOTE, --note NOTE  A note to add to the fingerprint
  -f FORMAT, --format FORMAT
                        The output format (json, yaml, etc.)
  -bo, --base64_output  Output the fingerprint in base64
```

## Licence

This project is licensed under the GNU General Public License v3.0 - see the [LICENCE](LICENCE) file for details