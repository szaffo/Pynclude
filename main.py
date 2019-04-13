#!/usr/bin/python3
import re
import os

# ===================================================
# You can edit this section
CWD = os.getcwd() + "/"
FILENAME = "main.py"
FILEPATH = CWD + FILENAME
INCLUDE_DIR = CWD
# ===================================================
RE_INCLUDE = re.compile(r"^\s*# ?pynclude\s*(?P<key>[A-z\./aáoóöőuúüű0-9]+\.py)\s*$")
RE_SETDIR = re.compile(r"^\s*# ?setdir\s*(?P<key>[A-z\./aáoóöőuúüű0-9]+(/)?)\s*$")
# RE_DEFINE = re.compile(r"^\s*# ?define\s*(?P<key>[A-zaáoóöőuúüű0-9]+)\s*$")
# RE_IFDEFINED = re.compile(r"^\s*# ?ifdef\s*(?P<key>[A-zaáoóöőuúüű0-9]+)\s*$")
# RE_IFNDEFINED = re.compile(r"^\s*# ?ifndef\s*(?P<key>[A-zaáoóöőuúüű0-9]+)\s*$")
# RE_ELSE = re.compile(r"^\s*# ?else\s*$")
# RE_COMMENT = re.compile(r"^\s*#.*$")
# ===================================================
# Do not edit settings here
SETTINGS = {
    "recursive": True,
    "keep_comments": True,
    "output_file": "builded.py",
    "input_file": FILENAME,
    "input_file_path": FILEPATH,
    "cwd": CWD,
    "include_directory": CWD,
    "verbose": True
}
# ===================================================


class Input(object):

    def __init__(self, filename):
        log(filename, "Reading to buffer")

        with open(filename, "r") as file:
            self.lines = file.read().split("\n")
            # self.lines = file.read().strip().split("\n")

        self.currentIndex = 0
        log(filename, "Ready to process")

    def first(self):
        self.currentIndex = 0

    def next(self):
        self.currentIndex += 1

    def current(self):
        return self.lines[self.currentIndex]

    def end(self):
        return (self.currentIndex == (len(self.lines)))

# ===================================================


class Output(object):

    def __init__(self):
        self.lines = []

    def add(self, lines):
        if isinstance(lines, str):
            lines = [lines]

        [self.lines.append(x) for x in lines]

    def save(self):
        filename = CWD + SETTINGS["output_file"]
        log(filename, "Saving builded code")
        with open(filename, "w") as file:
            file.write("\n".join(list(self.lines)))

        log(filename, "Saved")

# ===================================================


def checkFile(filename):
    try:
        open(filename, "r")
        return True
    except Exception:
        return False

# ===================================================


def log(file, text):
    if SETTINGS["verbose"]:
        print("[{}] {}".format(file, text))
# ===================================================


def compile(filename, settings):
    log(filename, "Starting compiling...")
    settings = settings.copy()
    file = Input(filename)

    while (not file.end()):
        addLine = True
        line = file.current()

        # pyclude
        if RE_INCLUDE.match(line):
            data = settings["include_directory"] + RE_INCLUDE.match(line).group("key")

            if settings["recursive"]:
                compile(data, settings)

            addLine = False

        # setdir
        elif RE_SETDIR.match(line):
            value = RE_SETDIR.match(line).group("value")
            settings["include_directory"] += value

            addLine = False

        if addLine:
            output.add(line)
        file.next()

    log(filename, "Compiled")

# ===================================================

if __name__ == '__main__':
    log("Pynclude v2.0", "")
    output = Output()

    if checkFile(FILEPATH):
        compile(FILEPATH, SETTINGS)
        output.save()
    else:
        log(FILEPATH, "Not found")
