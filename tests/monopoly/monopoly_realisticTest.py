import ast

from checkpy import *
from unittest.mock import patch, Mock


only("monopoly_realistic.py")
require("monopoly.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()


@test()
def codeShieldedByMain():
	"""if __name__ == "__main__" is present"""
	assert ast.Break not in static.AbstractSyntaxTree()
	assert 'if __name__ == "__main__":' in static.getSource()


@passed(codeShieldedByMain, timeout=90, hide=False)
def hassimulate_monopoly_games():
	"""defines simulate_monopoly_games with the correct number of parameters"""
	assert "simulate_monopoly_games" in static.getFunctionDefinitions()

	assert len(getFunction("simulate_monopoly_games").parameters) == 3,\
		"make sure that the simulate_monopoly_games function has three parameters"\
		", the number of games, the starting_money for player 1,"\
		" and the starting_money for player 2"


@passed(hassimulate_monopoly_games, timeout=90, hide=False)
def correctAverageDiff1():
	"""Players only throw the value 3; Player 1 and Player 2 both start with 1500; simulate_monopoly_games gives the correct output"""
	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
		outcome = getFunction("simulate_monopoly_games")(1, 1500, 1500)

		assert Type(float) == outcome,\
			"Make sure that the function simulate_monopoly_games only returns"\
			" the difference in the number of streets owned"

		assert 0 < outcome,\
			"Are you sure you are subtracting player 2s values from player 1"\
			" and not the other way around?"

		assert 6.0 == outcome


@passed(hassimulate_monopoly_games, timeout=90, hide=False)
def correctAverageDiff2():
	"""Players only throw the value 3; Player 1 starts with 1500 and Player 2 starts with 1700; simulate_monopoly_games gives the correct output"""
	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
		outcome = getFunction("simulate_monopoly_games")(1, 1500, 1700)

		assert Type(float) == outcome,\
			"Make sure that the function simulate_monopoly_games only returns"\
			" the difference in the number of streets owned"

		assert 0 < outcome,\
			"Are you sure you are subtracting player 2s values from player 1"\
			" and not the other way around?"

		assert 4.0 == outcome

@passed(hassimulate_monopoly_games, timeout=90, hide=False)
def correctAverageDiff2():
	"""Players only throw the value 3; Player 1 starts with 1500 and Player 2 starts with 1700; simulate_monopoly_games gives the correct output"""
	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
		outcome = getFunction("simulate_monopoly_games")(1, 1500, 1700)

		assert Type(float) == outcome,\
			"Make sure that the function simulate_monopoly_games only returns"\
			" the difference in the number of streets owned"

		assert 0 < outcome,\
			"Are you sure you are subtracting player 2s values from player 1"\
			" and not the other way around?"

		assert 4.0 == outcome


@passed(hassimulate_monopoly_games, timeout=90, hide=False)
def correctAverageDiff2():
	"""Players only throw the value 7; Player 1 starts with 1500 and Player 2 starts with 2200; simulate_monopoly_games gives the correct output"""
	with patch.object(getModule(), "throw_two_dice", Mock(return_value=7)):
		outcome = getFunction("simulate_monopoly_games")(1, 1500, 2200)

		assert Type(float) == outcome,\
			"Make sure that the function simulate_monopoly_games only returns"\
			" the difference in the number of streets owned"

		assert 0 < outcome,\
			"Are you sure you are subtracting player 2s values from player 1"\
			" and not the other way around?"

		assert 4.0 == outcome
