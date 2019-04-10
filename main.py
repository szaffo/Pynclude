#!/usr/bin/python3
import sys
import re
import os

# ===================================================
CWD = os.getcwd() + "/"
FILENAME = "main.py"
FILEPATH = CWD + FILENAME
INCLUDE_DIR = CWD
# ===================================================
RE_INCLUDE = re.compile(r"^\s*# ?pynclude\s*(?P<key>[A-z\./aáoóöőuúüű0-9]+\.py)\s*$")
RE_SETDIR = re.compile(r"^\s*# ?setdir\s*(?P<key>[A-z\./aáoóöőuúüű0-9]+(/)?)\s*$")
RE_DEFINE = re.compile(r"^\s*# ?define\s*(?P<key>[A-zaáoóöőuúüű0-9]+)\s*$")
RE_IFDEFINED = re.compile(r"^\s*# ?ifdef\s*(?P<key>[A-zaáoóöőuúüű0-9]+)\s*$")
RE_IFNDEFINED = re.compile(r"^\s*# ?ifndef\s*(?P<key>[A-zaáoóöőuúüű0-9]+)\s*$")
RE_ELSE = re.compile(r"^\s*# ?else\s*$")
RE_COMMENT = re.compile(r"^\s*#.*$")
# ===================================================
G_output = []
G_settings = {
    "recursive": True,
    "keep_comments": True
}
# ===================================================


class Input(object):

    def __init__(self, filename):
        log(filename, "Reading to buffer")

        with open(filename, "r")

# ===================================================


def checkFile(filename):
    try:
        open(filename, "r")
        return True
    except Exception:
        return False

# ===================================================


def log(file, text):
    print("[{}] {}".format(file, text))
# ===================================================


def compile(filename):
    log(filename, "Compiling...")
    inp = Input(filename)

# ===================================================

if __name__ == '__main__':
    print("Pynclude v2.0")
    if checkFile(FILEPATH):
        compile(FILEPATH)
    else:
        log(FILEPATH, "Not found")
