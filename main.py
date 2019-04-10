#!/usr/bin/python3
import sys
import re
import os

# ===================================================

RE_INCLUDE = r"^\s*# ?pynclude\s*([A-z\./aáoóöőuúüű0-9]+\.py)\s*$"
RE_SETDIR = r"^\s*# ?setdir\s*([A-z\./aáoóöőuúüű0-9]+(/)?)\s*$"
RE_DEFINE = r"^\s*# ?define\s*([A-zaáoóöőuúüűÁŐÓÚŰÖ0-9]+)\s*$"
RE_IFDEFINED = r"^\s*# ?ifdef\s*([A-zaáoóöőuúüűÁŐÓÚŰÖ0-9]+)\s*$"
RE_IFNDEFINED = r"^\s*# ?ifndef\s*([A-zaáoóöőuúüűÁŐÓÚŰÖ0-9]+)\s*$"
RE_ELSE = r"^\s*# ?else\s*$"
RE_COMMENT = r"^\s*#.*$"

# ===================================================

if __name__ == '__main__':
	print("Pynclude v2.0")

