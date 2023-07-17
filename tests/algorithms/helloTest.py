from checkpy import *

only("hello.py")

@test()
def exactHello():
	"""prints \"Hello, world!\""""
	assert outputOf() == "Hello, world!\n"

@failed(exactHello)
def oneLine():
	"""prints exactly 1 line of output"""
	assert outputOf().count("\n") == 1