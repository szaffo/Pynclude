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
RE_GUARD = re.compile(r"^\s*# ?pyncludeGuard\s*(?P<key>[A-z\./aáoóöőuúüű0-9]+(/)?)\s*$")
# RE_DEFINE = re.compile(r"^\s*# ?define\s*(?P<key>[A-zaáoóöőuúüű0-9]+)\s*$")
# RE_IFDEFINED = re.compile(r"^\s*# ?ifdef\s*(?P<key>[A-zaáoóöőuúüű0-9]+)\s*$")
# RE_IFNDEFINED = re.compile(r"^\s*# ?ifndef\s*(?P<key>[A-zaáoóöőuúüű0-9]+)\s*$")
# RE_ELSE = re.compile(r"^\s*# ?else\s*$")
RE_COMMENT = re.compile(r"^\s*#.*$")
RE_KEEP_COMMENTS = re.compile(r"^\s*# ?keepComments (?P<key>False|True)\s*$")
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
    # "original_include_directory": CWD, # No need to declare it here
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


class OutputLayer(object):

    def __init__(self):
        # self.lines = []
        self.collector = Collector(str)

    def add(self, lines):
        lines = [lines]

        [self.collector.add(x) for x in lines]

    def getLines(self):
        return self.collector.getAll()

    def _save(self):
        filename = CWD + SETTINGS["output_file"]
        log(filename, "Saving builded code")
        with open(filename, "w") as file:
            file.write("\n".join(list(self.collector.getAll())))

        log(filename, "Saved")
# ===================================================


class Output(OutputLayer):

    def addLayer(self, layer):
        lines = layer.getLines()
        [self.add(line) for line in lines]

    def save(self):
        super(Output, self)._save()
# ===================================================


class Collector(object):

    def __init__(self, type):
        self.type = type
        self.items = []

    def add(self, item):
        if (not isinstance(item, self.type)):
            raise TypeError("Can't collect {} with Collector[{}]".format(type(item), self.type))
            return False
        else:
            self.items = self.items + [item]
            return True

    def has(self, item):
        return (item in self.items)

    def getAll(self):
        return self.items.copy()
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

    if (checkFile(CWD + "settings.pynclude")):
        with open(CWD + "settings.pynclude", "r") as file:
            data = json.load(file)

        settingsFilename = CWD + "settings.pynclude"

    elif (checkFile("settings.pynclude")):
        log(CWD + "settings.pynclude", "Not found")
        with open("settings.pynclude", "r") as file:
            data = json.load(file)

        settingsFilename = "settings.pynclude"

    else:
        log(CWD + "settings.pynclude", "Not found")
        log("./settings.pynclude", "Not found")

    if (not data is None):
        for key in data.keys():
            settings[key] = data[key]

        log(settingsFilename, "Applied")
# ===================================================


def compile(filename, settings):
    log(filename, "Starting compiling...")

    settings = settings.copy()
    settings["original_include_directory"] = settings["include_directory"]

    file = Input(filename)
    layer = OutputLayer()
    includeAble = True

    while ((not file.end()) and includeAble):
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
            settings["include_directory"] += value
            addLine = False

        # clearIncludeDir
        elif RE_CLEAR_INCLUDE.match(line):
            settings["include_directory"] = settings["original_include_directory"]
            addLine = False

        # keepComments
        elif RE_KEEP_COMMENTS.match(line):
            settings["keep_comments"] = (RE_KEEP_COMMENTS.match(line).group("key") == "True")
            addLine = False

        # pyncludeGuard XXX
        elif RE_GUARD.match(line):
            guard = RE_GUARD.match(line).group("key")
            addLine = False

            # Check if was included
            if guards.has(guard):
                includeAble = False
                log(filename, "File was included once and it's protected by a guard (" + guard + ")", unlockVerbose=True)
            else:
                guards.add(guard)

        # comment
        # This should be after all command
        elif RE_COMMENT.match(line):
            addLine = settings["keep_comments"]

        if addLine:
            layer.add(line)

        file.next()

    if includeAble:
        output.addLayer(layer)

    log(filename, "Compiled")
# ===================================================

if __name__ == '__main__':
    log("Pynclude v2.2.3", "")
    applySettings(SETTINGS)

    output = Output()
    guards = Collector(str)

    if checkFile(FILEPATH):
        compile(FILEPATH, SETTINGS)
        output.save()
    else:
        log(FILEPATH, "Not found")
