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
        "properties": PROPERTIES
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
        "Define a throw_two_dice() function so we can set dice rolls in tests to a specific value."

@passed(codeShieldedByMain, timeout=30, hide=False)
def hasSimulateFunctions():
    """Required functions exist with updated signatures"""
    sim1 = getFunction("simulate_monopoly")
    simN = getFunction("simulate_monopoly_games")
    assert sim1 is not None, "simulate_monopoly(board_config) must be defined."
    assert simN is not None, "simulate_monopoly_games(games, board_config) must be defined."
    assert len(sim1.parameters) == 1, "simulate_monopoly must accept exactly one parameter: board_config."
    assert len(simN.parameters) == 2, "simulate_monopoly_games must accept two parameters: games, board_config."

@passed(hasSimulateFunctions, timeout=30, hide=False)
def correctAverageDiff1():
    """Simulate_monopoly_games gives the correct output
    (dice always yield 3; start money: 1500, 1500)"""
    with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
        outcome = getFunction("simulate_monopoly_games")(1, default_config())

        assert Type(float) == outcome,\
            "Make sure that the function simulate_monopoly_games only returns"\
            " the difference in the number of streets owned"

        assert 0 < outcome,\
            "Are you sure you are subtracting player 2s values from player 1"\
            " and not the other way around?"

        assert 6.0 == outcome


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
    """Changing starting_money in config affects the outcome"""
    with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
        equal = getFunction("simulate_monopoly_games")(1, create_config(starting_money=[1500, 1500]))

        p2_richer = getFunction("simulate_monopoly_games")(1, create_config(starting_money=[1500, 2000]))
        assert Type(float) == equal and Type(float) == p2_richer

        # With player 2 richer, player 1's advantage should not increase
        assert p2_richer <= equal, \
            "When player 2 starts richer, the average (P0 - P1) should not increase."

@passed(hasSimulateFunctions, timeout=60, hide=False)
def doesntChangeStartingMoney():
    """Starting_money doesn't get changed by simulate_monopoly"""
    with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
        board_config = create_config(starting_money=[1500, 1500])

        result = getFunction("simulate_monopoly")(board_config)

        assert board_config['starting_money'] == [1500, 1500], \
            "Make sure the original starting_money list is not changed!"


@passed(hasSimulateFunctions, timeout=30, hide=False)
def correctAverageDiff2():
    """Simulate_monopoly_games gives the correct output
    (dice always yield 3; start money: 1500, 1700)"""
    with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
        outcome = getFunction("simulate_monopoly_games")(1, create_config(starting_money=[1500, 1700]))

        assert Type(float) == outcome,\
        "Make sure that the function simulate_monopoly_games only returns"\
        " the difference in the number of streets owned"

        assert 0 < outcome,\
        "Are you sure you are subtracting player 2s values from player 1"\
        " and not the other way around?"

        assert 4.0 == outcome

@passed(hasSimulateFunctions, timeout=30, hide=False)
def correctAverageDiff3():
    """Simulate_monopoly_games gives the correct output
    (dice always yield 3; start money: 1500, 2500)"""
    with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
        outcome = getFunction("simulate_monopoly_games")(1, create_config(starting_money=[1500, 2500]))

        assert Type(float) == outcome,\
        "Make sure that the function simulate_monopoly_games only returns"\
        " the difference in the number of streets owned"

        assert 0.0 == outcome


@passed(hasSimulateFunctions, timeout=30, hide=False)
def correctAverageDiff4():
    """Simulate_monopoly_games gives the correct output
    (dice always yield 7; start money: 1500, 2500)"""
    with patch.object(getModule(), "throw_two_dice", Mock(return_value=7)):
        outcome = getFunction("simulate_monopoly_games")(1, create_config(starting_money=[1500, 2500]))

        assert Type(float) == outcome,\
        "Make sure that the function simulate_monopoly_games only returns"\
        " the difference in the number of streets owned"

        assert 0 < outcome,\
        "Are you sure you are subtracting player 2s values from player 1"\
        " and not the other way around?"

        assert 4.0 == outcome

# ============================================================
# Step 2: Properties dict and nested lookup
# ============================================================

# Not setting the properties dict results in an error
@passed(correctAverageDiff4, timeout=30, hide=False)
def step2_missingProperties():
    """Code uses the properties key from the board_config"""
    cfg = default_config()
    del cfg["properties"]

    with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
        threw = False
        try:
            _ = getFunction("simulate_monopoly_games")(1, cfg)
        except:
            threw = True

        assert threw, "Did you implement step 2 yet?"


# ============================================================
# Step 3.1: is_unowned helper exists and works on tody data
# ============================================================

@test()
def hasIsUnowned():
    """is_unowned helper exists and works on toy data"""
    f = getFunction("is_unowned")
    assert f is not None, "Define is_unowned(position, owned_sets) as described in Step 3.1."
    assert f(14, [{12,16}, {18}]) is True, "is_unowned should return True when nobody owns the tile."
    assert f(18, [{12,16}, {18}]) is False, "is_unowned should return False when a player owns the tile."

# ============================================================
# Step 3.2: ownership via sets
# ============================================================

@passed(hasIsUnowned, timeout=30, hide=False)
def p0_buys_first():
    """Property ownership is tracked for a single property
    (dice always yield 3; starting_money: varies; board_size 12; single property at pos 3)"""
    cfg = create_config(
        board_size=12,
        lap_money=0,
        starting_money=[100, 0],
        properties={3: 100},
    )

    with patch.object(getModule(), "throw_two_dice", Mock(return_value=3)):
        outcome = getFunction("simulate_monopoly_games")(1, cfg)
        assert Type(float) == outcome, "simulate_monopoly_games should return a float."
        assert outcome == 1.0, "With a single property at 3 and dice=3, Player 0 should buy it first → difference 1.0"

        cfg['starting_money'] = [0, 100]

        outcome = getFunction("simulate_monopoly_games")(1, cfg)
        assert Type(float) == outcome, "simulate_monopoly_games should return a float."
        assert outcome == -1.0, "With a single property at 3 and dice=3, where player 0 has no money, Player 1 should buy it first → difference 1.0"

        cfg['starting_money'] = [100, 100]

        outcome = getFunction("simulate_monopoly_games")(1, cfg)
        assert Type(float) == outcome, "simulate_monopoly_games should return a float."
        assert outcome == 1.0, "Make sure that a single property cannot be bought twice!"


@passed(hasIsUnowned, timeout=60, hide=False)
def p1_buys_first():
    """Property ownership is tracked properly in more complex cases
    (dice yield 2 for Player 0, 4 for Player 1; starting_money: varies; board_size 10)"""

    cfg = create_config(
        board_size=10,
        lap_money=100,
        starting_money=[100, 100],
        properties={2: 100, 4: 100, 6: 100},
    )

    # P0 hits 2 (buy), P1 hits 4 (buy), 6 is bought on second round by P1
    def roller():
        seq = [2, 4]
        while True:
            for r in seq:
                yield r
    gen = roller()

    def fixed_seq():
        return next(gen)

    with patch.object(getModule(), "throw_two_dice", Mock(side_effect=fixed_seq)):
        outcome = getFunction("simulate_monopoly_games")(1, cfg)
        assert Type(float) == outcome, "simulate_monopoly_games should return a float."
        assert outcome == -1.0, (
            "With a single property at 4 and alternating rolls 2,4, Player 1 should buy it first → difference -1.0"
        )
