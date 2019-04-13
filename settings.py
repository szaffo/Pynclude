#!/usr/bin/python3
import os
import json

cwd = os.getcwd() + "/"

settings = {
    "recursive": True,
    "keep_comments": True,
    "input_file": "main.py",
    "output_file": "builded.py",
    "include_directory": cwd,
    "verbose": True
}

with open('settings.pynclude', 'w') as outfile:
    json.dump(settings, outfile, indent=4)
