from checkpy import *
from shared import noBreakAndImport
import ast
import typing


only("alice.py")
download("alice.txt", "https://raw.githubusercontent.com/spcourse/shorts/refs/heads/main/longest_word_in_file/alice.txt")

fun = (declarative
    .function("longest_word_clean")
    .returnType(str)
    .params("text")
)


alice = "seen a rabbit with either a waistcoat-pocket, or a watch"

test1 = test()(fun
    .call(alice)
    .returns("waistcoat-pocket")
)

@test(timeout=90)
def opensFile():
	"""Opens a file using open()."""
	assert "open" in static.getFunctionCalls()

@test(timeout=90)
def closesFile():
    """Closes a file using file.close()."""
    methods = [f.split(".")[1] for f in list(static.getFunctionCalls()) if "." in f]
    assert "close" in methods

@test(timeout=90)
def readsFile():
    """Uses the file.read() to read the entire contents of a file."""
    methods = [f.split(".")[1] for f in list(static.getFunctionCalls()) if "." in f]
    assert "read" in methods
