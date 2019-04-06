#!/usr/bin/python3
import sys
import re
import os
from compiler import Compiler

# ===================================================

RE_INCLUDE = r"^\s*# ?pynclude\s*([A-z\./aáoóöőuúüű0-9]+\.py)\s*$"
RE_SETDIR = r"^\s*# ?setdir\s*([A-z\./aáoóöőuúüű0-9]+(/)?)\s*$"
RE_DEFINE = r"^\s*# ?define\s*([A-zaáoóöőuúüűÁŐÓÚŰÖ0-9]+)\s*$"
RE_IFDEFINED = r"^\s*# ?ifdef\s*([A-zaáoóöőuúüűÁŐÓÚŰÖ0-9]+)\s*$"
RE_IFNDEFINED = r"^\s*# ?ifndef\s*([A-zaáoóöőuúüűÁŐÓÚŰÖ0-9]+)\s*$"
RE_ELSE = r"^\s*# ?else\s*$"
RE_COMMENT = r"^\s*#.*$"

# ===================================================

def validateArgs():
	try:
		file = sys.argv[1]
		cwd = os.getcwd() + '/'

		open(cwd + file, "r")
	except IndexError:
		print("You have to specify what file you want to compile")
		exit(1)

	except FileNotFoundError:
		print("This file not exist.")
		print("[CWD]", cwd)
		print("[FILE]", file)
		exit(2)

	return cwd + file

# ===================================================

def isInclude(line):
	pass

# ===================================================

class Compiler(object):
	def __init__(self, filename, definitions = []):
		self.filename = filename
		self.defs = definitions
		self.logHead = "[" + self.filename + "]"

	def compile(self):
		print(self.logHead, "Compiling")


		self.readLines()

		while not self.eof():
			line = self.getLine()

			self.processLine(line)

			self.nextLine()

	def readLines(self):
		try:
			with open(self.filename, "r") as f:
				self.lines = f.read().strip().split("\n")

		except:
			print(self.logHead, "Error while reading from file")
			self.pointer = len(self.lines)
			return

		self.pointer = 0


	def eof(self):
		return self.pointer == len(self.lines)

	def getLine(self):
		return self.lines[self.pointer]

	def nextLine(self):
		self.pointer += 1

	def processLine(self, line):
		pass
		# if isInclude(line):
		# 	pass
		# elif isSetDir(line):
		# 	pass
		# elif isDefine(line):
		# 	pass
		# elif isIfDefined(line):
		# 	pass
		# elif isIfNotDefined(line):
		# 	pass
		# elif isElse(line):
		# 	pass
		# elif isComment(line):
		# 	pass
		# else:
		# 	pass
		# 	# CodeLine



if __name__ == '__main__':
	print("Pynclude v2.0")

	mainFile = validateArgs()
	mainComp = Compiler(mainFile)
	mainComp.compile()
	

