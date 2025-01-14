from checkpy import *

only("hello.py")

@test()
def oneLine():
	"""prints exactly 1 line of output"""
	assert 1 == outputOf().count("\n")

@passed(oneLine, hide=False)
def exactHello():
	"""prints \"Hello, world!\""""
	assert "Hello, world!\n" == outputOf()
