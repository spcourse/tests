from checkpy import *
from unittest.mock import patch, Mock


only("monopoly.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

# shared test
from contains_main import *

@passed(codeShieldedByMain, hide=False)
def hasthrow_two_dice():
	"""defines the function throw_two_dice"""
	assert "throw_two_dice" in static.getFunctionDefinitions()


@passed(hasthrow_two_dice, hide=False)
def correctDice():
	"""returns a correct value for a throw with two dice"""
	# https://xkcd.com/221/
	assert approx(7, abs=5) == getFunction("throw_two_dice")()


@passed(correctDice, hide=False)
def hassimulate_monopolyAndsimulate_monopoly_games():
	"""defines the functions simulate_monopoly and simulate_monopoly_games"""
	defs = static.getFunctionDefinitions()
	assert "simulate_monopoly" in defs and "simulate_monopoly_games" in defs


@passed(hassimulate_monopolyAndsimulate_monopoly_games, timeout=120, hide=False)
def correctAverageTrump(test):
	"""Monopoly works for Trump-mode (assuming player always throws 7)"""
	monopoly = getModule()
	nArguments = len(monopoly.simulate_monopoly_games.arguments)

	assert nArguments in [1, 2],\
		"Make sure that the function simulate_monopoly_games with Trumpmode accepts 1 argument and with starting_money 2 arguments"

	with patch.object(monopoly, "throw_two_dice", Mock(return_value=7)):
		# Trump
		if nArguments == 1:
			result = monopoly.simulate_monopoly_games(1)
			test.success = "The code works without starting_money, you can now proceed with adding starting_money!"
		# starting money, 1 player
		else:
			result = monopoly.simulate_monopoly_games(1, 1000000)

		assert result is not None,\
			"Make sure that the function simulate_monopoly_games returns the average required number of throws and nothing else"
		assert approx(38, abs=1) == result 


@passed(hassimulate_monopolyAndsimulate_monopoly_games, timeout=120, hide=False)
def correctAverageStartingMoney():
	"""Monopoly works with 1500 euro starting_money (assuming player always throws 7)"""
	monopoly = getModule()

	assert len(monopoly.simulate_monopoly_games.arguments) == 2,\
		"Did you implement starting money yet? If not, ignore this frowny."

	with patch.object(monopoly, "throw_two_dice", Mock(return_value=7)):
		result = monopoly.simulate_monopoly_games(1, 1500)
		assert result is not None,\
			"Make sure that the function simulate_monopoly_games returns the average required number of throws and nothing else"

		assert approx(142, abs=1) == result
