from checkpy import *
from unittest.mock import patch, Mock
from copy import deepcopy

only("monopoly_dicts.py")

monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

# shared tests
from contains_main import *

# Test design notes::
# - Most simulation tests use fixed dice rolls so the expected result is reproducible.
# - Small changes to board_config are used to isolate one configuration value at a time.
# - limited_roller() prevents a wrong stopping condition from becoming an unhelpful timeout.
# - Checks that board_config stayed unchanged are deliberately placed last, so a more
#   specific functional error is shown first.

# property prices per board position
PROPERTIES = {
  1: 60, 3: 60, 5: 200, 6: 100, 8: 100, 9: 120,
  11: 140, 12: 150, 13: 140, 14: 160, 15: 200,
  16: 180, 18: 180, 19: 200, 21: 220, 23: 220,
  24: 240, 25: 200, 26: 260, 27: 260, 28: 150,
  29: 280, 31: 300, 32: 300, 34: 320, 35: 200,
  37: 350, 39: 400
}


def create_config(board_size=40, lap_money=200, starting_money=None, properties=None):
    """Small helper function to create configs."""
    if starting_money is None:
        starting_money = [1500, 1500]
    if properties is None:
        properties = PROPERTIES

    return {
        "board_size": board_size,
        "lap_money": lap_money,
        "starting_money": list(starting_money),
        "properties": dict(properties),
    }


def default_config():
    return create_config()


def assert_config_unchanged(config, original):
    """Check this last, so more specific functional errors are shown first."""
    changed_keys = sorted(
        key for key in set(config) | set(original)
        if config.get(key) != original.get(key)
    )

    assert config == original, (
        "The simulation changed board_config. Treat board_config as read-only. "
        f"Changed keys: {changed_keys}"
    )


class RollLimitReached(Exception):
    """Raised when a test requests more dice rolls than expected."""
    pass


def limited_roller(rolls):
    """Return a finite sequence of dice rolls.

    If student code keeps asking for rolls, the simulation probably did not stop when
    expected. RollLimitReached is caught outside the student function so Checkpy can
    show a short, useful error message instead of a wrapped exception.
    """
    rolls = iter(rolls)

    def roller():
        try:
            return next(rolls)
        except StopIteration:
            raise RollLimitReached()

    return roller


def caused_by(error, exception_type):
    """Return True if an exception in the chain has the requested type."""
    while error is not None:
        if isinstance(error, exception_type):
            return True

        error = error.__cause__ or error.__context__

    return False


def run_with_limited_roller(function_name, args, rolls, message):
    """Run a student function with fixed dice and a readable roll-limit error.

    Checkpy wraps exceptions raised while student functions are running, but keeps
    the original exception in the exception chain. If the roller is exhausted, find
    RollLimitReached in that chain and replace it with the test-specific message.
    Other student exceptions are left untouched.
    """
    roller = Mock(side_effect=limited_roller(rolls))

    try:
        with patch.object(getModule(), "throw_two_dice", roller):
            outcome = getFunction(function_name)(*args)
    except Exception as error:
        if caused_by(error, RollLimitReached):
            raise AssertionError(message) from None
        raise

    return outcome, roller


# ============================================================
# Step 0 tests
# ============================================================

@passed(codeShieldedByMain, timeout=30, hide=False)
def noEquilibrium():
    """equilibrium() has been removed"""
    assert not hasattr(getModule(), "equilibrium"), \
        "Remove the legacy function equilibrium() — it's not part of this assignment."


@passed(codeShieldedByMain, timeout=30, hide=False)
def hasThrowTwoDice():
    """throw_two_dice() is present"""
    assert hasattr(getModule(), "throw_two_dice"), \
        "Define a throw_two_dice() function so we can set dice rolls in tests to a specific value."


@passed(codeShieldedByMain, timeout=30, hide=False)
def hasSimulateFunctions():
    """Simulation functions have the required parameters"""
    simulate_one_game = getFunction("simulate_monopoly")
    simulate_multiple_games = getFunction("simulate_monopoly_games")

    assert simulate_one_game is not None, "simulate_monopoly(board_config) must be defined."
    assert simulate_multiple_games is not None, "simulate_monopoly_games(games, board_config) must be defined."
    assert len(simulate_one_game.parameters) == 1, "simulate_monopoly must accept exactly one parameter: board_config."
    assert len(simulate_multiple_games.parameters) == 2, "simulate_monopoly_games must accept two parameters: games, board_config."


@passed(hasSimulateFunctions, timeout=30, hide=False)
def usesNumberOfGames():
    """simulate_monopoly_games simulates and averages the requested number of games"""
    config = default_config()
    original = deepcopy(config)

    # Instead of running three full games, make simulate_monopoly return three known
    # results. This isolates the looping and averaging done by simulate_monopoly_games.
    simulated_game = Mock(side_effect=[3, -1, 1])

    with patch.object(getModule(), "simulate_monopoly", simulated_game):
        outcome = getFunction("simulate_monopoly_games")(3, config)

    assert simulated_game.call_count == 3, \
        "simulate_monopoly_games(3, board_config) should simulate exactly 3 games."

    assert Type(float) == outcome, \
        "simulate_monopoly_games should return the average difference as a float."

    assert outcome == 1.0, \
        "For game results 3, -1 and 1, simulate_monopoly_games should return their average: 1.0."

    for args, kwargs in simulated_game.call_args_list:
        assert args == (config,) and kwargs == {}, \
            "Pass board_config to simulate_monopoly for every simulated game."

    assert_config_unchanged(config, original)


@passed(usesNumberOfGames, timeout=30, hide=False)
def correctAverageDiff1():
    """The simulation gives the expected result with the default settings"""
    cfg = default_config()
    original = deepcopy(cfg)

    finish_message = (
        "The simulation did not finish with fixed dice rolls. "
        "Check the game loop, property ownership and stopping condition."
    )
    outcome, roller = run_with_limited_roller(
        "simulate_monopoly_games", (1, cfg), [3] * 1000, finish_message
    )

    assert Type(float) == outcome, \
        "Make sure that simulate_monopoly_games only returns the difference in the number of streets owned."

    assert 0 < outcome, \
        "Are you sure you are subtracting player 2's values from player 1's and not the other way around?"

    assert outcome == 6.0, \
        "With the default config and dice=3, the expected difference is 6.0."
    assert_config_unchanged(cfg, original)


# ============================================================
# Step 1 tests: Config dictionary is actually used
# ============================================================

@passed(correctAverageDiff1, timeout=60, hide=False)
def usesLapMoney():
    """lap_money from board_config is used"""
    # These configs are identical except for lap_money. A different result therefore
    # shows that the simulation actually reads this value from board_config.
    cfg_90 = create_config(lap_money=90)
    cfg_100 = create_config(lap_money=100)
    original_90 = deepcopy(cfg_90)
    original_100 = deepcopy(cfg_100)

    finish_message = (
        "The simulation did not finish with fixed dice rolls. "
        "Check the game loop, property ownership and stopping condition."
    )

    outcome_90, _ = run_with_limited_roller(
        "simulate_monopoly_games", (1, cfg_90), [3] * 1000, finish_message
    )
    outcome_100, _ = run_with_limited_roller(
        "simulate_monopoly_games", (1, cfg_100), [3] * 1000, finish_message
    )

    assert Type(float) == outcome_90 and Type(float) == outcome_100, \
        "simulate_monopoly_games should return the average difference as a float."

    assert outcome_90 == 4.0 and outcome_100 == 6.0, (
        "This test uses lap_money=90 and lap_money=100. "
        "Check that lap money is read from board_config and is not hardcoded."
    )

    assert_config_unchanged(cfg_90, original_90)
    assert_config_unchanged(cfg_100, original_100)


@passed(usesLapMoney, timeout=60, hide=False)
def usesStartingMoney():
    """starting_money from board_config is used"""
    # These configs are identical except for Player 2's starting money.
    equal_cfg = create_config(starting_money=[1500, 1500])
    richer_cfg = create_config(starting_money=[1500, 1600])
    equal_original = deepcopy(equal_cfg)
    richer_original = deepcopy(richer_cfg)

    finish_message = (
        "The simulation did not finish with fixed dice rolls. "
        "Check the game loop, property ownership and stopping condition."
    )

    equal, _ = run_with_limited_roller(
        "simulate_monopoly_games", (1, equal_cfg), [3] * 1000, finish_message
    )
    p2_richer, _ = run_with_limited_roller(
        "simulate_monopoly_games", (1, richer_cfg), [3] * 1000, finish_message
    )

    assert Type(float) == equal and Type(float) == p2_richer, \
        "simulate_monopoly_games should return the average difference as a float."

    assert equal == 6.0 and p2_richer == 4.0, (
        "This test uses starting_money=[1500, 1500] and [1500, 1600]. "
        "Check that each player's starting money is read from board_config and is not hardcoded."
    )

    assert_config_unchanged(equal_cfg, equal_original)
    assert_config_unchanged(richer_cfg, richer_original)


@passed(usesStartingMoney, timeout=60, hide=False)
def doesntChangeConfig():
    """board_config is not changed during a simulation"""
    cfg = default_config()
    original = deepcopy(cfg)

    finish_message = (
        "The simulation did not finish with fixed dice rolls. "
        "Check the game loop, property ownership and stopping condition."
    )
    _, roller = run_with_limited_roller(
        "simulate_monopoly", (cfg,), [3] * 1000, finish_message
    )

    assert_config_unchanged(cfg, original)


@passed(doesntChangeConfig, timeout=30, hide=False)
def correctResultsDifferentSettings():
    """The simulation gives the expected results for different game settings"""
    scenarios = [
        (3, [1500, 1700], 4.0),
        (3, [1500, 2500], 0.0),
        (7, [1500, 2500], 4.0)
    ]

    for dice, starting_money, expected in scenarios:
        cfg = create_config(starting_money=starting_money)
        original = deepcopy(cfg)

        finish_message = (
            "The simulation did not finish with fixed dice rolls. "
            "Check the game loop, property ownership and stopping condition."
        )
        outcome, roller = run_with_limited_roller(
            "simulate_monopoly_games", (1, cfg), [dice] * 1000, finish_message
        )

        message = (
            f"This test uses dice={dice} and starting_money={starting_money}. "
            f"The expected average difference is {expected}."
        )

        assert Type(float) == outcome, \
            "simulate_monopoly_games should return the average difference as a float."

        assert outcome == expected, message
        assert_config_unchanged(cfg, original)


# ============================================================
# Step 2: Properties dict and nested lookup
# ============================================================

@passed(correctResultsDifferentSettings, timeout=30, hide=False)
def step2_usesPropertyPrices():
    """Property prices are read from board_config['properties']"""
    # Change exactly one price on the otherwise standard board. This catches solutions
    # that still use the old hardcoded board values for prices.
    properties = dict(PROPERTIES)
    properties[1] = 100
    cfg = create_config(properties=properties)
    original = deepcopy(cfg)

    message = (
        "This test changes properties[1] from 60 to 100. "
        "Check that property prices are read from board_config['properties'] and are not hardcoded."
    )
    outcome, roller = run_with_limited_roller(
        "simulate_monopoly_games", (1, cfg), [3] * 400, message
    )

    assert Type(float) == outcome, \
        "simulate_monopoly_games should return the average difference as a float."

    assert outcome == 4.0, message
    assert_config_unchanged(cfg, original)


@passed(step2_usesPropertyPrices, timeout=30, hide=False)
def step2_usesPropertyPositions():
    """Property positions are read from board_config['properties']"""
    # Move one property without changing its price. This isolates whether the set of
    # buyable board positions comes from board_config['properties'].
    properties = dict(PROPERTIES)
    price = properties.pop(23)
    properties[22] = price
    cfg = create_config(properties=properties)
    original = deepcopy(cfg)

    message = (
        "This test moves one property from position 23 to position 22. "
        "Check that buyable positions are taken from board_config['properties'] and are not hardcoded."
    )
    outcome, roller = run_with_limited_roller(
        "simulate_monopoly_games", (1, cfg), [3] * 400, message
    )

    assert Type(float) == outcome, \
        "simulate_monopoly_games should return the average difference as a float."

    assert outcome == 4.0, message
    assert_config_unchanged(cfg, original)


@passed(step2_usesPropertyPositions, timeout=30, hide=False)
def step2_usesBoardSize():
    """board_size from board_config is used when moving around the board"""
    # Only the board size differs from the default config.
    cfg = create_config(board_size=41)
    original = deepcopy(cfg)

    message = (
        "This test uses board_size=41. "
        "Check that the board size is not hardcoded in your simulation."
    )
    outcome, roller = run_with_limited_roller(
        "simulate_monopoly_games", (1, cfg), [11, 7] * 100, message
    )

    assert Type(float) == outcome, \
        "simulate_monopoly_games should return the average difference as a float."

    assert outcome == 2.0, message
    assert_config_unchanged(cfg, original)


@passed(step2_usesBoardSize, timeout=30, hide=False)
def step2_usesNumberOfProperties():
    """The game stops after all properties in board_config have been bought"""
    # A one-property board makes a hardcoded "28 properties" stopping condition fail
    # immediately. limited_roller() turns that mistake into the message below.
    cfg = create_config(properties={3: 60})
    original = deepcopy(cfg)

    message = (
        "This test uses properties={3: 60}, so there is only 1 buyable property. "
        "Check that the number of properties needed to finish the game is based on "
        "board_config['properties'] and is not hardcoded."
    )
    outcome, roller = run_with_limited_roller(
        "simulate_monopoly_games", (1, cfg), [3] * 6, message
    )

    assert Type(float) == outcome, \
        "simulate_monopoly_games should return the average difference as a float."

    assert outcome == 1.0, message
    assert_config_unchanged(cfg, original)


# ============================================================
# Step 3.1: is_unowned helper
# ============================================================

@passed(step2_usesNumberOfProperties, timeout=30, hide=False)
def hasIsUnowned():
    """is_unowned works for owned and unowned positions"""
    is_unowned = getFunction("is_unowned")

    assert is_unowned is not None, \
        "Define is_unowned(position, owned_sets) as described in Step 3.1."

    assert len(is_unowned.parameters) == 2, \
        "is_unowned should accept exactly two parameters: position and owned_sets."

    assert is_unowned(14, [{12, 16}, {18}]) is True, \
        "is_unowned should return True when neither player owns the position."

    assert is_unowned(12, [{12, 16}, {18}]) is False, \
        "is_unowned should return False when Player 1 owns the position."

    assert is_unowned(18, [{12, 16}, {18}]) is False, \
        "is_unowned should return False when Player 2 owns the position."

    assert is_unowned(14, [set(), set()]) is True, \
        "is_unowned should also work when both ownership sets are empty."


@passed(hasIsUnowned, timeout=30, hide=False)
def canBuyWithExactMoney():
    """A property can be bought with exactly enough money"""
    cfg = create_config(
        lap_money=0,
        starting_money=[100, 0],
        properties={3: 100},
    )
    original = deepcopy(cfg)

    # Player 1 has exactly the property price; Player 2 cannot buy it.
    # With a strict '>' check nobody can ever buy the property, so the roll limit
    # gives a direct hint about the affordability check.
    message = (
        "This test uses lap_money=0, starting_money=[100, 0] and properties={3: 100}. "
        "A player should be able to buy a property when their money is equal to its price."
    )

    outcome, _ = run_with_limited_roller(
        "simulate_monopoly_games", (1, cfg), [3] * 6, message
    )

    assert Type(float) == outcome, \
        "simulate_monopoly_games should return a float."

    assert outcome == 1.0, message
    assert_config_unchanged(cfg, original)


# ============================================================
# Step 3.2: ownership via sets
# ============================================================

@passed(canBuyWithExactMoney, timeout=30, hide=False)
def player1_buys_first():
    """Player 1 buys an affordable unowned property first"""
    cfg = create_config(
        lap_money=0,
        starting_money=[101, 101],
        properties={3: 100},
    )
    original = deepcopy(cfg)

    # Both players land on position 3, but Player 1 gets there first and buys it.
    message = (
        "This test uses lap_money=0, starting_money=[101, 101] and properties={3: 100}. "
        "With dice=3, Player 1 should be the first player to buy the property."
    )
    outcome, roller = run_with_limited_roller(
        "simulate_monopoly_games", (1, cfg), [3] * 6, message
    )

    assert Type(float) == outcome, \
        "simulate_monopoly_games should return a float."

    assert outcome == 1.0, message
    assert_config_unchanged(cfg, original)


@passed(player1_buys_first, timeout=30, hide=False)
def player2_buys_when_player1_cannot_afford():
    """Player 2 can buy a property Player 1 cannot afford"""
    cfg = create_config(
        lap_money=0,
        starting_money=[0, 101],
        properties={3: 100},
    )
    original = deepcopy(cfg)

    # Player 1 reaches position 3 first but has no money. The property must remain
    # available so Player 2 can buy it on the next turn.
    message = (
        "This test uses lap_money=0, starting_money=[0, 101] and properties={3: 100}. "
        "A player who cannot afford a property should leave it available for the other player."
    )
    outcome, roller = run_with_limited_roller(
        "simulate_monopoly_games", (1, cfg), [3] * 6, message
    )

    assert Type(float) == outcome, \
        "simulate_monopoly_games should return a float."

    assert outcome == -1.0, message
    assert_config_unchanged(cfg, original)


@passed(player2_buys_when_player1_cannot_afford, timeout=30, hide=False)
def owned_property_cannot_be_bought_again():
    """An owned property cannot be bought again"""
    cfg = create_config(
        lap_money=0,
        starting_money=[200, 200],
        properties={2: 100, 4: 100},
    )
    original = deepcopy(cfg)

    # With dice=2: Player 1 buys position 2, Player 2 then lands on the already-owned
    # position 2, and Player 1 later buys position 4. Final difference: 2 properties.
    message = (
        "This test uses lap_money=0, starting_money=[200, 200] and "
        "properties={2: 100, 4: 100}. With dice=2, both players land on position 2, "
        "but it must only be bought once."
    )
    outcome, roller = run_with_limited_roller(
        "simulate_monopoly_games", (1, cfg), [2] * 8, message
    )

    assert Type(float) == outcome, \
        "simulate_monopoly_games should return a float."

    assert outcome == 2.0, message
    assert_config_unchanged(cfg, original)


@passed(owned_property_cannot_be_bought_again, timeout=30, hide=False)
def changed_board_configuration():
    """Buying and ownership work with a changed board configuration"""
    cfg = create_config(
        board_size=10,
        lap_money=100,
        starting_money=[101, 101],
        properties={2: 100, 4: 100, 6: 100},
    )
    original = deepcopy(cfg)

    # Turn sequence with alternating rolls 2, 4:
    # Player 1 buys position 2, Player 2 buys position 4, and Player 2 later buys 6.
    # The expected final difference is therefore -1.
    message = (
        "This test uses board_size=10, lap_money=100, starting_money=[101, 101], "
        "properties={2: 100, 4: 100, 6: 100} and alternating dice rolls 2, 4. "
        "Check that movement, buying and ownership all use the current configuration."
    )
    outcome, roller = run_with_limited_roller(
        "simulate_monopoly_games", (1, cfg), [2, 4] * 10, message
    )

    assert Type(float) == outcome, \
        "simulate_monopoly_games should return a float."

    assert outcome == -1.0, message
    assert_config_unchanged(cfg, original)


@passed(changed_board_configuration, timeout=30, hide=False)
def multiple_games_start_fresh():
    """Each game starts with new positions, money and ownership"""
    cfg = default_config()
    original = deepcopy(cfg)

    # First measure how many rolls one correct deterministic game needs. This gives us
    # a clean baseline for the two-game run below.
    single_message = (
        "A game with the default config and dice=3 should finish normally. "
        "Check the game loop and its stopping condition."
    )
    single_outcome, single_roller = run_with_limited_roller(
        "simulate_monopoly", (cfg,), [3] * 300, single_message
    )

    single_rolls = single_roller.call_count

    assert single_outcome == 6, \
        "With the default config and dice=3, one game should end with a difference of 6 properties."

    assert single_rolls > 0, \
        "simulate_monopoly should actually simulate the game."

    assert_config_unchanged(cfg, original)

    # Now run two identical games. Fresh state means the result should be identical in
    # both games and exactly twice as many dice rolls should be requested.
    multi_message = (
        "This test calls simulate_monopoly_games(2, board_config). "
        "Each game should start with fresh positions, money and ownership; state from one game "
        "must not affect the next game."
    )
    outcome, multi_roller = run_with_limited_roller(
        "simulate_monopoly_games",
        (2, cfg),
        [3] * (2 * single_rolls + 20),
        multi_message
    )

    assert Type(float) == outcome, \
        "simulate_monopoly_games should return the average difference as a float."

    assert outcome == float(single_outcome), \
        "With deterministic dice, two fresh identical games should have the same average result as one game."

    assert multi_roller.call_count == 2 * single_rolls, multi_message
    assert_config_unchanged(cfg, original)
