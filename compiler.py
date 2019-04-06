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

	# def processLine(self, line):
		# if lin