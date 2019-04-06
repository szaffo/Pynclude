#!/usr/bin/python3
import sys
import re
import os
from compiler import Compiler

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



if __name__ == '__main__':
	print("Pynclude v2.0")

	mainFile = validateArgs()
	mainComp = Compiler(mainFile)
	

