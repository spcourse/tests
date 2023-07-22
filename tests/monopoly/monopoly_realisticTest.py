import pathlib
import sys

from checkpy import *

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from notAllowedCode import *


only("monopoly_realistic.py")
require("monopoly.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()


@test()
def codeShieldedByMain():
	"""if __name__ == "__main__" is present"""
	notAllowedCode({"break": "break"})
	assert 'if __name__ == "__main__":' in static.getSource()


@passed(codeShieldedByMain, timeout=90, hide=False)
def hassimulate_monopoly_games():
	"""defines simulate_monopoly_games with the correct number of parameters"""
	notAllowedCode({"break": "break"})

	assert "simulate_monopoly_games" in static.getFunctionDefinitions()

	assert len(getFunction("simulate_monopoly_games").parameters) == 3,\
		"make sure that the simulate_monopoly_games function has three parameters"\
		", the number of games, the starting_money for player 1,"\
		" and the starting_money for player 2"


@passed(hassimulate_monopoly_games, timeout=90, hide=False)
def correctAverageDiff():
	"""Monopoly with two players gives the correct average difference in owned streets"""
	outcome = getFunction("simulate_monopoly_games")(10000, 1500, 1500)

	assert Type(float) == outcome,\
		"Make sure that the function simulate_monopoly_games only returns"\
		" the difference in the number of streets owned"

	assert outcome > 0,\
		"Are you sure you are subtracting player 2s values from player 1"\
		" and not the other way around?"

	assert outcome == approx(.35, abs=0.2)


@passed(correctAverageDiff, timeout=90, hide=False)
def correctAverageDiff2():
	"""Monopoly with two players finds the correct amount of extra starting money for player 2"""
	def findline(text: str) -> str:
		tsts = ['starting', 'money', 'equal', 'number', 'streets']
		for line in text.split("\n"):
			if all(tst in line for tst in tsts):
				return line
		return ""

	output = outputOf(overwriteAttributes=[("__name__", "__main__")])
	line = findline(output)

	if not line:
		return False, "Check the assignment for the correct output format of the solution."

	numbers = static.getNumbersFrom(line)

	assert 0 in numbers or 50 in numbers or 100 in numbers or 150 in numbers or 200 in numbers,\
		"The found value was not rounded to the nearest value of 50 euros."

	assert 100 in numbers or 150 in numbers,\
		"Properly rounded to the nearest value, but the value returned was incorrect."
