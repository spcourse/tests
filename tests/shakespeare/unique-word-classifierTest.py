from checkpy import *
from pathlib import Path
import ast

only("unique-word-classifier.py")

download("shakespeare-words.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/shakespeare-words.txt")
download("words.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/words.txt")
download("shakespeare.0379.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/shakespeare.0379.txt")
download("shakespeare.0318.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/shakespeare.0318.txt")
download("jonson.0183.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/jonson.0183.txt")
download("jonson.0223.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/jonson.0223.txt")
download("marlowe.0198.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/marlowe.0198.txt")
download("marlowe.0068.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/marlowe.0068.txt")

def defines_function(name: str) -> bool:
    check = name in static.getFunctionDefinitions()
    if not check:
        raise AssertionError(f"`{name}` is not defined")
    return check

data = [
    Path("shakespeare.0379.txt"),
    Path("shakespeare.0318.txt"),
    Path("jonson.0183.txt"),
    Path("jonson.0223.txt"),
    Path("marlowe.0198.txt"),
    Path("marlowe.0068.txt")
]

@test()
def no_timeit():
    """Does not include timeit"""
    calls = \
        [node.func.id for node in static.getAstNodes(ast.Call) if
        type(node.func) == ast.Name] + \
        [node.func.value.id for node in static.getAstNodes(ast.Call) if
        type(node.func) == ast.Attribute and type(node.func.value) == ast.Name]

    assert "timeit" not in calls, "remove timeit from your code before sumbitting"

@passed(no_timeit)
def has_basic_functions():
    """Functions calculate_shakespeare_score and load_shakespeare_words defined"""

    assert defines_function("load_shakespeare_words")
    assert defines_function("calculate_shakespeare_score")

@passed(has_basic_functions, timeout=8)
def test1():
    """Testing speed calculate_shakespeare_score()
    (calculating the score 100 times using a text of 800 lines and a file
    containing 466550 words)."""
    shakespeare_words = getFunction("load_shakespeare_words")("words.txt")
    text = """_Ham._ (C.) Heaven make thee free of it! I follow thee.
You that look pale and tremble at this chance,
That are but mutes or audience to this act,
Had I but time (as this fell sergeant, death,[79]
Is strict in his arrest), O, I could tell you,--
But let it be. Horatio,
Report me and my cause aright
To the unsatisfied."""*100
    for i in range(100): # 6000 - 35
        score = getFunction("calculate_shakespeare_score")(text, shakespeare_words)



@passed(has_basic_functions)
def has_compute_all_accuracies():
    """Function compute_all_accuracies defined"""
    assert defines_function("compute_all_accuracies")

@passed(has_compute_all_accuracies, timeout=10)
def test2():
    """Testing accuracies using files: shakespeare.0379.txt, shakespeare.0318.txt,
    jonson.0183.txt, jonson.0223.txt, marlowe.0198.txt, marlowe.0068.txt
    and thresholds: [0.0, 0.02, 0.04, 0.06, 0.08]
    """
    shakespeare_words = getFunction("load_shakespeare_words")("shakespeare-words.txt")

    # for file_name in data:
    #     print(getFunction("is_written_by_shakespeare")(file_name))
    #     with open(file_name, "r") as file:
    #         print(getFunction("calculate_shakespeare_score")(file.read(), shakespeare_words))
    compute_all_accuracies = getFunction("compute_all_accuracies")
    accs = compute_all_accuracies(
        [0.0, 0.02, 0.04, 0.06, 0.08],
        data,
        shakespeare_words)

    assert accs == [approx(0.33, abs=0.1), approx(0.83, abs=0.1),
        approx(0.83, abs=0.1), approx(0.83, abs=0.1), approx(0.67, abs=0.1)]
