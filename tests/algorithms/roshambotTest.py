from checkpy import *
import ast
import builtins

only("roshambot.py")

MOVES = ("rock", "paper", "scissors")
BEATS = {"rock": "paper", "paper": "scissors", "scissors": "rock"}  # BEATS[x] beats x
OPPONENTS = {
    "dwayne": "Dwayne",
    "lance": "Lance",
    "bicyclist": "The Bicyclist",
    "winner": "The Winner",
    "winnerwinner": "The Winner Winner",
}


class StopGame(Exception):
    pass


def roundWinner(a, b):
    """the move that won the round; after a tie, the move both played"""
    if a == b or BEATS[b] == a:
        return a
    return b


def score(history):
    mine = sum(1 for t, m in history if t != m and roundWinner(t, m) == m)
    theirs = sum(1 for t, m in history if t != m and roundWinner(t, m) == t)
    return mine, theirs


def opponentMove(opponent, history):
    """history: (theirs, mine) for each round played so far"""
    n = len(history)
    if opponent == "dwayne":
        return "rock"
    if opponent == "lance":
        return MOVES[n % 3]
    if opponent == "bicyclist":
        return MOVES[(n // 2) % 3]
    if n == 0:
        return "rock"
    last = roundWinner(*history[-1])
    if opponent == "winner":
        return last
    return BEATS[last]


def play(opponent):
    """
    Run the student's program against an opponent. A fake print collects the
    student's moves, a fake input answers with the opponent's move, so the
    opponent can react to how the game is going, and only answers once the
    student's move for that round is printed.
    """
    history = []  # (theirs, mine)
    printed = []  # the student's moves
    problems = {}  # "order" or "tooLong": what went wrong

    def fakePrint(*args, **kwargs):
        line = kwargs.get("sep", " ").join(str(a) for a in args).strip()
        if line in MOVES:
            printed.append(line)
        builtins.print(*args, **kwargs)

    def fakeInput(prompt=None):
        mine, theirs = score(history)
        if mine == 5 or theirs == 5 or len(history) == 9:
            problems["tooLong"] = (
                f"after {len(history)} rounds it is {mine}-{theirs} and the game is over, "
                "but your program asks for the opponent's move again"
            )
            raise StopGame()
        if len(printed) != len(history) + 1:
            problems["order"] = (
                f"in round {len(history) + 1} your program should first print its move "
                "(just rock, paper or scissors, on a line of its own) and then ask for the opponent's move"
            )
            raise StopGame()
        move = opponentMove(opponent, history)
        history.append((move, printed[-1]))
        return move

    outputOf(
        overwriteAttributes=[("input", fakeInput), ("print", fakePrint)],
        ignoreExceptions=[StopGame],
    )

    mine, theirs = score(history)
    return history, mine, theirs, problems


def describe(opponent, history, mine, theirs):
    rounds = "\n".join(f"  round {i + 1}: you {m}, {OPPONENTS[opponent]} {t}" for i, (t, m) in enumerate(history))
    return f"against {OPPONENTS[opponent]} it was {mine}-{theirs} after {len(history)} rounds:\n{rounds}"


@test()
def noDataStructuresImportOrBreak():
    """the program does not use lists or other data structures, import or break"""
    tree = static.AbstractSyntaxTree()
    for node, name in [(ast.List, "lists"), (ast.ListComp, "lists"), (ast.Dict, "dicts"), (ast.DictComp, "dicts"),
                       (ast.Set, "sets"), (ast.SetComp, "sets"), (ast.Tuple, "tuples")]:
        assert node not in tree, f"you cannot use {name}"
    assert ast.Import not in tree and ast.ImportFrom not in tree, "you cannot use import statements"
    assert ast.Break not in tree, "you cannot use break statements"


@passed(noDataStructuresImportOrBreak, hide=False)
def printsThenAsks():
    """each round the program prints its move and then asks for the opponent's"""
    for opponent in OPPONENTS:
        history, mine, theirs, problems = play(opponent)
        if "order" in problems:
            raise AssertionError(problems["order"])
        assert history, "your program never asks for the opponent's move"


@passed(printsThenAsks, hide=False)
def gameEnds():
    """the game ends at 5 wins, or after 9 rounds"""
    for opponent in OPPONENTS:
        history, mine, theirs, problems = play(opponent)
        if "tooLong" in problems:
            raise AssertionError(problems["tooLong"] + ": " + describe(opponent, history, mine, theirs))
        assert mine == 5 or theirs == 5 or len(history) == 9, \
            "the game should go on until someone has 5 wins (or 9 rounds are played), but " + describe(opponent, history, mine, theirs)


def beats(opponent):
    history, mine, theirs, problems = play(opponent)
    assert mine == 5, "you need 5 wins to beat an opponent, and " + describe(opponent, history, mine, theirs)


@passed(gameEnds, hide=False)
def beatsDwayne():
    """beats Dwayne"""
    beats("dwayne")


@passed(gameEnds, hide=False)
def beatsLance():
    """beats Lance"""
    beats("lance")


@passed(gameEnds, hide=False)
def beatsTheBicyclist():
    """beats The Bicyclist"""
    beats("bicyclist")


@passed(gameEnds, hide=False)
def beatsTheWinner():
    """beats The Winner"""
    beats("winner")


@passed(gameEnds, hide=False)
def beatsTheWinnerWinner():
    """beats The Winner Winner"""
    beats("winnerwinner")
