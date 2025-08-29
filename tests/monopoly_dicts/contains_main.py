from checkpy import *
import ast

def contains_main():
	expressions = ['if __name__ == "__main__":', "if __name__ == '__main__':"]
	source = static.removeComments(static.getSource())
	for e in expressions:
		if e in source:
			return True
	return False

@test()
def codeShieldedByMain():
	"""if __name__ == "__main__" is present"""
	assert ast.Break not in static.AbstractSyntaxTree()
	assert contains_main(), "not found"
