from checkpy import *
from unittest.mock import patch, Mock


only("monopoly_realistic.py")

monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

# shared tests
from contains_main import *

board_config = {
    "lap_money": 200,
    "board_size": 40,
    "properties": {
        1: 60,
        3: 60,
        5: 200,
        6: 100,
        8: 100,
        9: 120,
        11: 140,
        12: 150,
        13: 140,
        14: 160,
        15: 200,
        16: 180,
        18: 180,
        19: 200,
        21: 220,
        23: 220,
        24: 240,
        25: 200,
        26: 260,
        27: 260,
        28: 150,
        29: 280,
        31: 300,
        32: 300,
        34: 320,
        35: 200,
        37: 350,
        39: 400
    }
}

# Test 1; new header has been made and equilibrium removed
@passed(codeShieldedByMain, timeout=90, hide=False)
def hasno_equilibrium():
	"""file does not contain equilibrium() function"""

	assert "equilibrium" not in static.getFunctionDefinitions(),\
		"make sure to remove the equilibrium function from your file"

@passed(hasno_equilibrium, timeout=90, hide=False)
def hassimulate_monopoly_games():
	"""defines simulate_monopoly_games with the correct number of parameters"""
	assert "simulate_monopoly_games" in static.getFunctionDefinitions()

	assert len(getFunction("simulate_monopoly_games").parameters) == 3,\
		"make sure that the simulate_monopoly_games function has three parameters"\
		", the number of games, the board config dictionary,"\
		" and the starting_money list for both players"

# Test 2, still works with new method of giving player money
@passed(hassimulate_monopoly_games, timeout=90, hide=False)
def correctAverageDiff1():
	"""Simulate_monopoly_games gives the correct output
   (dice always yield 3; start money: 1500, 1500)"""
	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
		outcome = getFunction("simulate_monopoly_games")(1, board_config, [1500, 1500])

		assert Type(float) == outcome,\
			"Make sure that the function simulate_monopoly_games only returns"\
			" the difference in the number of streets owned"

		assert 0 < outcome,\
			"Are you sure you are subtracting player 2s values from player 1"\
			" and not the other way around?"

		assert 6.0 == outcome


@passed(hassimulate_monopoly_games, timeout=90, hide=False)
def correctAverageDiff2():
	"""Simulate_monopoly_games gives the correct output
   (dice always yield 3; start money: 1500, 1700)"""
	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
		outcome = getFunction("simulate_monopoly_games")(1, board_config, [1500, 1700])

		assert Type(float) == outcome,\
			"Make sure that the function simulate_monopoly_games only returns"\
			" the difference in the number of streets owned"

		assert 0 < outcome,\
			"Are you sure you are subtracting player 2s values from player 1"\
			" and not the other way around?"

		assert 4.0 == outcome

@passed(hassimulate_monopoly_games, timeout=90, hide=False)
def correctAverageDiff3():
	"""Simulate_monopoly_games gives the correct output
   (dice always yield 3; start money: 1500, 2500)"""
	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
		outcome = getFunction("simulate_monopoly_games")(1, board_config, [1500, 2500])

		assert Type(float) == outcome,\
			"Make sure that the function simulate_monopoly_games only returns"\
			" the difference in the number of streets owned"

		assert 0.0 == outcome


@passed(hassimulate_monopoly_games, timeout=90, hide=False)
def correctAverageDiff4():
	"""Simulate_monopoly_games gives the correct output
   (dice always yield 7; start money: 1500, 2500)"""
	with patch.object(getModule(), "throw_two_dice", Mock(return_value=7)):
		outcome = getFunction("simulate_monopoly_games")(1, board_config, [1500, 2500])

		assert Type(float) == outcome,\
			"Make sure that the function simulate_monopoly_games only returns"\
			" the difference in the number of streets owned"

		assert 0 < outcome,\
			"Are you sure you are subtracting player 2s values from player 1"\
			" and not the other way around?"

		assert 4.0 == outcome

# Test 3; lap money test
@passed(correctAverageDiff4, timeout=90, hide=False)
def correctAverageDiff5():
	"""Simulate_monopoly_games gives the correct output
   (dice always yield 3; start money: 0, 1500; lap_money 200)"""
	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
		board_config = board_config.copy()
		board_config['lap_money'] = 200
		outcome = getFunction("simulate_monopoly_games")(1, board_config, [0, 1500])

		assert Type(float) == outcome,\
			"Make sure that the function simulate_monopoly_games only returns"\
			" the difference in the number of streets owned"

		assert -8.0 == outcome

@passed(correctAverageDiff4, timeout=90, hide=False)
def correctAverageDiff6():
	"""Simulate_monopoly_games gives the correct output
   (dice always yield 3; start money: 0, 1500; lap_money 500)"""
	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
		board_config = board_config.copy()
		board_config['lap_money'] = 500
		outcome = getFunction("simulate_monopoly_games")(1, board_config, [0, 1500])

		assert Type(float) == outcome,\
			"Make sure that the function simulate_monopoly_games only returns"\
			" the difference in the number of streets owned"

		assert -4.0 == outcome

@passed(correctAverageDiff4, timeout=90, hide=False)
def correctAverageDiff7():
	"""Simulate_monopoly_games gives the correct output
   (dice always yield 3; start money: 0, 1500; lap_money 2000)"""
	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
		board_config = board_config.copy()
		board_config['lap_money'] = 2000
		outcome = getFunction("simulate_monopoly_games")(1, board_config, [0, 1500])

		assert Type(float) == outcome,\
			"Make sure that the function simulate_monopoly_games only returns"\
			" the difference in the number of streets owned"

		assert -4.0 == outcome

# Test 4; get_buyable_properties
fun_def = (declarative
	.function('get_buyable_properties')
	.params('board_properties', 'player_owned_properties')
	.returnType(set)
)

board = {"A": 100, "B": 150, "C": 200}

test = passed(correctAverageDiff7)(fun_def
	.call({}, [set(), set()]).returns(set())
	.call(board, []).returns({"A", "B", "C"})
	.call(board, [set(), set()]).returns({"A", "B", "C"})
    .call(board, [set(["A"])]).returns({"B", "C"})
	.call(board, [set(["A"]), set(["B", "C"])]).returns(set())
	.call(board, [set(["A"]), set(["B"]), set(["C"])]).returns(set())
)

# Test 5; using properties from board config
