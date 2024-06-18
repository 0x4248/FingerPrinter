# FingerPrinter
# A tool to generate file fingerprints
# Github://www.github.com/0x4248/FingerPrinter
# Licence: GNU General Public License v3.0
# By: 0x4248

import argparse
import hashlib
import json
import os
import sys
import datetime
import base64
import yaml
import xml.etree.ElementTree as ET

verbose = False

def log(message):
    if verbose:
        print(message)

def generate_fingerprint(file_name, note=""):
    with open(file_name, "rb") as file:
        file_contents = file.read()
        file_size = os.path.getsize(file_name)
        file_mime = os.popen(f"file --mime-type -b {file_name}").read().strip()
        file_magic = os.popen(f"file --mime-type -b {file_name}").read().strip()
        file_base64 = base64.b64encode(file_contents).decode("utf-8")

        md5 = hashlib.md5(file_contents).hexdigest()
        sha1 = hashlib.sha1(file_contents).hexdigest()
        sha256 = hashlib.sha256(file_contents).hexdigest()
        sha512 = hashlib.sha512(file_contents).hexdigest()

        sha256_lines = []
        md5_lines = []
        lines = file_contents.splitlines()
        for line in lines:
            sha256_lines.append(hashlib.sha256(line).hexdigest())
            md5_lines.append(hashlib.md5(line).hexdigest())

        date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if note == None:
            note = ""

        fingerprint = {
            "Meta": {
                "FileName": file_name,
                "FileMagic": file_magic,
                "FileMime": file_mime,
                "FileSize": file_size,
                "FileBase64": file_base64,
                "Note": note,
                "DateCreated": date_created,
            },
            "Hashes": {
                "MD5": md5,
                "SHA1": sha1,
                "SHA256": sha256,
                "SHA512": sha512
            },
            "Lines": {
                "Total": len(lines),
                "SHA256": sha256_lines,
                "MD5": md5_lines
            }
        }

        return fingerprint

def write_fingerprint(fingerprint, output_file):
    with open(output_file, "w") as file:
        json.dump(fingerprint, file, indent=4)


def export_fingerprint(fingerprint, format):
    if format == "json":
        output = json.dumps(fingerprint, indent=4)
        return output
    elif format == "yaml":
        output = yaml.dump(fingerprint)
        return output
    elif format == "xml":
        root = ET.Element("Fingerprint")
        meta = ET.SubElement(root, "Meta")
        hashes = ET.SubElement(root, "Hashes")
        lines = ET.SubElement(root, "Lines")

        for key, value in fingerprint["Meta"].items():
            ET.SubElement(meta, key).text = str(value)
        for key, value in fingerprint["Hashes"].items():
            ET.SubElement(hashes, key).text = str(value)
        for key, value in fingerprint["Lines"].items():
            ET.SubElement(lines, key).text = str(value)

        output = ET.tostring(root, encoding="unicode")
        return output
    elif format == "txt":
        output = ""
        for key, value in fingerprint["Meta"].items():
            output += f"{key}: {value}\n"
        output += "\n"
        for key, value in fingerprint["Hashes"].items():
            output += f"{key}: {value}\n"
        output += "\n"
        for key, value in fingerprint["Lines"].items():
            output += f"{key}: {value}\n"
        return output

    else:
        print(f"Unsupported format: {format}")
        sys.exit(1)



def main():
    parser = argparse.ArgumentParser(description="Fingerprinter")
    parser.add_argument("file", help="The file to fingerprint")
    parser.add_argument("-o", "--output", help="The output file to write the fingerprint to")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-n", "--note", help="A note to add to the fingerprint")
    parser.add_argument("-f", "--format", help="The output format (json, yaml, etc.)")
    parser.add_argument("-bo", "--base64_output", action="store_true", help="Output the fingerprint in base64")
    args = parser.parse_args()

    global verbose
    verbose = args.verbose

    fingerprint = generate_fingerprint(args.file, args.note)
    supported_formats = ["json", "yaml", "xml", "txt"]
    format = "json"
    if args.format:
        if args.format not in supported_formats:
            print(f"Unsupported format: {args.format}")
            sys.exit(1)
        else:
            format = args.format
    output = export_fingerprint(fingerprint, format)
    if args.output:
        if args.base64_output:
            output = base64.b64encode(output.encode("utf-8")).decode("utf-8")
            with open(args.output, "w") as file:
                file.write(output)
        else:
            with open(args.output, "w") as file:
                file.write(output)
    else:
        if args.base64_output:
            output = base64.b64encode(output.encode("utf-8")).decode("utf-8")
            print(output)
        else:
            print(output)
            sys.exit(0)

if __name__ == "__main__":
    main()
