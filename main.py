#!/usr/bin/python3
import re
import os
import json

# ===================================================
# You can edit this section
CWD = os.getcwd() + "/"
FILENAME = "main.py"
FILEPATH = CWD + FILENAME
INCLUDE_DIR = CWD
# ===================================================
RE_INCLUDE = re.compile(r"^\s*# ?pynclude\s*(?P<key>[A-z\./aáoóöőuúüű0-9]+\.py)\s*$")
RE_SETDIR = re.compile(r"^\s*# ?setdir\s*(?P<key>[A-z\./aáoóöőuúüű0-9]+(/)?)\s*$")
RE_CLEAR_INCLUDE = re.compile(r"^\s*# ?clearIncludeDir\s*$")
# RE_DEFINE = re.compile(r"^\s*# ?define\s*(?P<key>[A-zaáoóöőuúüű0-9]+)\s*$")
# RE_IFDEFINED = re.compile(r"^\s*# ?ifdef\s*(?P<key>[A-zaáoóöőuúüű0-9]+)\s*$")
# RE_IFNDEFINED = re.compile(r"^\s*# ?ifndef\s*(?P<key>[A-zaáoóöőuúüű0-9]+)\s*$")
# RE_ELSE = re.compile(r"^\s*# ?else\s*$")
RE_COMMENT = re.compile(r"^\s*#.*$")
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
    "previous_include_directory": CWD,
    "verbose": True
}
# ===================================================


class Input(object):

    def __init__(self, filename):
        log(filename, "Reading to buffer")
        self.currentIndex = 0

        try:
            with open(filename, "r") as file:
                self.lines = file.read().split("\n")
        except:
            log(filename, "Can't open file", unlockVerbose=True)
            self.lines = []
            return
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


def log(file, text, unlockVerbose=False):
    if SETTINGS["verbose"] or unlockVerbose:
        print("[{}] {}".format(file, text))
# ===================================================


def applySettings(settings):
    data = None
    settingsFilename = None
    try:
        with open(CWD + "settings.pynclude", "r") as file:
            data = json.load(file)
            settingsFilename = CWD + "settings.pynclude"
    except:
        log(CWD + "settings.pynclude", "Not found")
        try:
            with open("settings.pynclude", "r") as file:
                data = json.load(file)
                settingsFilename = "settings.pynclude"
        except:
            log("settings.pynclude", "Not found")

    if (not data is None):
        for key in data.keys():
            settings[key] = data[key]

        log(settingsFilename, "Applied")


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
            value = RE_SETDIR.match(line).group("key")
            settings["previous_include_directory"] = settings["include_directory"]
            settings["include_directory"] += value
            addLine = False

        # clearIncludeDir
        elif RE_CLEAR_INCLUDE.match(line):
            settings["include_directory"] = settings["previous_include_directory"]
            addLine = False

        # comment
        elif RE_COMMENT.match(line):
            addLine = settings["keep_comments"]

        if addLine:
            output.add(line)
        file.next()

    log(filename, "Compiled")
# ===================================================

if __name__ == '__main__':
    log("Pynclude v2.0", "")
    applySettings(SETTINGS)
    output = Output()

    if checkFile(FILEPATH):
        compile(FILEPATH, SETTINGS)
        output.save()
    else:
        log(FILEPATH, "Not found")
