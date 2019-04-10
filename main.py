#!/usr/bin/python3
import sys
import re
import os

# ===================================================
CWD = os.getcwd()
FILENAME = "main.py"
FILEPATH = CWD + "/" + FILENAME
# ===================================================
RE_INCLUDE = re.compile(r"^\s*# ?pynclude\s*(?P<data>[A-z\./aáoóöőuúüű0-9]+\.py)\s*$")
RE_SETDIR = re.compile(r"^\s*# ?setdir\s*(?P<data>[A-z\./aáoóöőuúüű0-9]+(/)?)\s*$")
RE_DEFINE = re.compile(r"^\s*# ?define\s*(?P<data>[A-zaáoóöőuúüű0-9]+)\s*$")
RE_IFDEFINED = re.compile(r"^\s*# ?ifdef\s*(?P<data>[A-zaáoóöőuúüű0-9]+)\s*$")
RE_IFNDEFINED = re.compile(r"^\s*# ?ifndef\s*(?P<data>[A-zaáoóöőuúüű0-9]+)\s*$")
RE_ELSE = re.compile(r"^\s*# ?else\s*$")
RE_COMMENT = re.compile(r"^\s*#.*$")
# ===================================================

def checkFile(filename):
	try:
		open(filename, "r")
		return True
	except Exception:
		return False

# ===================================================

if __name__ == '__main__':
	print("Pynclude v2.0")
	print(checkFile(FILEPATH))

