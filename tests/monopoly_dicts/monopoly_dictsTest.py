from checkpy import *
from unittest.mock import patch, Mock


only("monopoly_dicts.py")

monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

# shared tests
from contains_main import *

# property prices per board position
PROPERTIES = {
  1: 60, 3: 60, 5: 200, 6: 100, 8: 100, 9: 120,
  11: 140, 12: 150, 13: 140, 14: 160, 15: 200,
  16: 180, 18: 180, 19: 200, 21: 220, 23: 220,
  24: 240, 25: 200, 26: 260, 27: 260, 28: 150,
  29: 280, 31: 300, 32: 300, 34: 320, 35: 200,
  37: 350, 39: 400,
}

def create_config(board_size=40, lap_money=200, starting_money=[1500,1500], properties=PROPERTIES):
    """ Small helper function to create configs"""

    return {
        "board_size": board_size,
        "lap_money": lap_money,
        "starting_money": starting_money,
        "properties": properties,
    }

def default_config():
    return {
        "board_size": 40,               # number of spaces on the board
        "lap_money": 200,               # money earned when passing start
        "starting_money": [1500, 1500], # starting money for player 1 and player 2
        "properties": {                 # property prices per board position
          1: 60, 3: 60, 5: 200, 6: 100, 8: 100, 9: 120,
          11: 140, 12: 150, 13: 140, 14: 160, 15: 200,
          16: 180, 18: 180, 19: 200, 21: 220, 23: 220,
          24: 240, 25: 200, 26: 260, 27: 260, 28: 150,
          29: 280, 31: 300, 32: 300, 34: 320, 35: 200,
          37: 350, 39: 400,
        }
    }

# ============================================================
# Step 0 tests
# ============================================================

@passed(codeShieldedByMain, timeout=30, hide=False)
def noEquilibrium():
    """No legacy 'equilibrium' function present"""
    assert not hasattr(getModule(), "equilibrium"), \
        "Remove the legacy function equilibrium() — it's not part of this assignment."

@passed(codeShieldedByMain, timeout=30, hide=False)
def hasThrowTwoDice():
    """throw_two_dice exists for deterministic tests"""
    assert hasattr(getModule(), "throw_two_dice"), \
        "Define a throw_two_dice() function so we can patch dice rolls in tests."

@passed(codeShieldedByMain, timeout=30, hide=False)
def hasSimulateFunctions():
    """Required functions exist with updated signatures"""
    sim1 = getFunction("simulate_monopoly")
    simN = getFunction("simulate_monopoly_games")
    assert sim1 is not None, "simulate_monopoly(board_config) must be defined."
    assert simN is not None, "simulate_monopoly_games(games, board_config) must be defined."
    assert len(sim1.parameters) == 1, "simulate_monopoly must accept exactly one parameter: board_config."
    assert len(simN.parameters) == 2, "simulate_monopoly_games must accept two parameters: games, board_config."


# # TODO: works as normal!? (this does test the board size issue later)

# ============================================================
# Step 1 tests: Config dictionary is actually used
# ============================================================


@passed(hasSimulateFunctions, timeout=60, hide=False)
def usesLapMoney():
    """Changing lap_money in config affects the outcome"""
    with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
        base = getFunction("simulate_monopoly_games")(1, create_config(lap_money=10),)
        rich = getFunction("simulate_monopoly_games")(1, create_config(lap_money=100))
        assert Type(float) == base and Type(float) == rich, \
            "simulate_monopoly_games should return a float (mean difference)."
        assert base != rich, \
            "Changing lap_money in the config should change the outcome. Are you using board_config['lap_money']?"

@passed(hasSimulateFunctions, timeout=60, hide=False)
def usesStartingMoney():
    """Changing starting_money in config affects the outcome """
    with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
        equal = getFunction("simulate_monopoly_games")(1, create_config(starting_money=[1500, 1500]))
        p2_richer = getFunction("simulate_monopoly_games")(1, create_config(starting_money=[1500, 2000]))
        assert Type(float) == equal and Type(float) == p2_richer
        # With player 2 richer, player 1's advantage should not increase
        assert p2_richer <= equal, \
            "When player 2 starts richer, the average (P0 - P1) should not increase."

# TODO: add a test that checks whether the student didnt directly copy starting_money by running twice

# BOARD SIZE CAN NOT BE TESTED AT THIS POINT




#
# # Test 2, still works with new method of giving player money
# @passed(hassimulate_monopoly_games, timeout=90, hide=False)
# def correctAverageDiff1():
# 	"""Simulate_monopoly_games gives the correct output
#    (dice always yield 3; start money: 1500, 1500)"""
# 	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
# 		outcome = getFunction("simulate_monopoly_games")(1, board_config, [1500, 1500])
#
# 		assert Type(float) == outcome,\
# 			"Make sure that the function simulate_monopoly_games only returns"\
# 			" the difference in the number of streets owned"
#
# 		assert 0 < outcome,\
# 			"Are you sure you are subtracting player 2s values from player 1"\
# 			" and not the other way around?"
#
# 		assert 6.0 == outcome
#
#
# @passed(hassimulate_monopoly_games, timeout=90, hide=False)
# def correctAverageDiff2():
# 	"""Simulate_monopoly_games gives the correct output
#    (dice always yield 3; start money: 1500, 1700)"""
# 	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
# 		outcome = getFunction("simulate_monopoly_games")(1, board_config, [1500, 1700])
#
# 		assert Type(float) == outcome,\
# 			"Make sure that the function simulate_monopoly_games only returns"\
# 			" the difference in the number of streets owned"
#
# 		assert 0 < outcome,\
# 			"Are you sure you are subtracting player 2s values from player 1"\
# 			" and not the other way around?"
#
# 		assert 4.0 == outcome
#
# @passed(hassimulate_monopoly_games, timeout=90, hide=False)
# def correctAverageDiff3():
# 	"""Simulate_monopoly_games gives the correct output
#    (dice always yield 3; start money: 1500, 2500)"""
# 	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
# 		outcome = getFunction("simulate_monopoly_games")(1, board_config, [1500, 2500])
#
# 		assert Type(float) == outcome,\
# 			"Make sure that the function simulate_monopoly_games only returns"\
# 			" the difference in the number of streets owned"
#
# 		assert 0.0 == outcome
#
#
# @passed(hassimulate_monopoly_games, timeout=90, hide=False)
# def correctAverageDiff4():
# 	"""Simulate_monopoly_games gives the correct output
#    (dice always yield 7; start money: 1500, 2500)"""
# 	with patch.object(getModule(), "throw_two_dice", Mock(return_value=7)):
# 		outcome = getFunction("simulate_monopoly_games")(1, board_config, [1500, 2500])
#
# 		assert Type(float) == outcome,\
# 			"Make sure that the function simulate_monopoly_games only returns"\
# 			" the difference in the number of streets owned"
#
# 		assert 0 < outcome,\
# 			"Are you sure you are subtracting player 2s values from player 1"\
# 			" and not the other way around?"
#
# 		assert 4.0 == outcome
#
# # Test 3; lap money test
# @passed(correctAverageDiff4, timeout=90, hide=False)
# def correctAverageDiff5():
# 	"""Simulate_monopoly_games gives the correct output
#    (dice always yield 3; start money: 0, 1500; lap_money 200)"""
# 	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
# 		board_config = board_config.copy()
# 		board_config['lap_money'] = 200
# 		outcome = getFunction("simulate_monopoly_games")(1, board_config, [0, 1500])
#
# 		assert Type(float) == outcome,\
# 			"Make sure that the function simulate_monopoly_games only returns"\
# 			" the difference in the number of streets owned"
#
# 		assert -8.0 == outcome
#
# @passed(correctAverageDiff4, timeout=90, hide=False)
# def correctAverageDiff6():
# 	"""Simulate_monopoly_games gives the correct output
#    (dice always yield 3; start money: 0, 1500; lap_money 500)"""
# 	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
# 		board_config = board_config.copy()
# 		board_config['lap_money'] = 500
# 		outcome = getFunction("simulate_monopoly_games")(1, board_config, [0, 1500])
#
# 		assert Type(float) == outcome,\
# 			"Make sure that the function simulate_monopoly_games only returns"\
# 			" the difference in the number of streets owned"
#
# 		assert -4.0 == outcome
#
# @passed(correctAverageDiff4, timeout=90, hide=False)
# def correctAverageDiff7():
# 	"""Simulate_monopoly_games gives the correct output
#    (dice always yield 3; start money: 0, 1500; lap_money 2000)"""
# 	with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
# 		board_config = board_config.copy()
# 		board_config['lap_money'] = 2000
# 		outcome = getFunction("simulate_monopoly_games")(1, board_config, [0, 1500])
#
# 		assert Type(float) == outcome,\
# 			"Make sure that the function simulate_monopoly_games only returns"\
# 			" the difference in the number of streets owned"
#
# 		assert -4.0 == outcome

# Test 4; get_buyable_properties
# fun_def = (declarative
# 	.function('get_buyable_properties')
# 	.params('board_properties', 'player_owned_properties')
# 	.returnType(set)
# )
#
# board = {"A": 100, "B": 150, "C": 200}
#
# test = passed(correctAverageDiff7)(fun_def
# 	.call({}, [set(), set()]).returns(set())
# 	.call(board, []).returns({"A", "B", "C"})
# 	.call(board, [set(), set()]).returns({"A", "B", "C"})
#     .call(board, [set(["A"])]).returns({"B", "C"})
# 	.call(board, [set(["A"]), set(["B", "C"])]).returns(set())
# 	.call(board, [set(["A"]), set(["B"]), set(["C"])]).returns(set())
# )

# Test 5; using properties from board config
