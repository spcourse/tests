from checkpy import *
from pathlib import Path
import ast
import time
import shakespeare_fast
import shakespeare_slow
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

@passed(has_basic_functions, timeout=20)
def speed_test1(check):
    """Testing speed improvement calculate_shakespeare_score()
    - using a text of 40 lines
    - a shakespeare_words file containing 466550 words
    - repeated 20 times"""

    text = """_Ham._ (C.) Heaven make thee free of it! I follow thee.
You that look pale and tremble at this chance,
That are but mutes or audience to this act,
Had I but time (as this fell sergeant, death,[79]
Is strict in his arrest), O, I could tell you,--
But let it be. Horatio,
Report me and my cause aright
To the unsatisfied."""*5

    user_duration = test_performance(
        getFunction("load_shakespeare_words"),
        getFunction("calculate_shakespeare_score"),
        text
    )

    slow_duration = test_performance(
        shakespeare_slow.load_shakespeare_words,
        shakespeare_slow.calculate_shakespeare_score,
        text
    )

    optimal_duration = test_performance(
        shakespeare_fast.load_shakespeare_words,
        shakespeare_fast.calculate_shakespeare_score,
        text
    )

    msg =  f"\033[0mSpeedtest:\n - running time original solution: {slow_duration:.4f}\n"
    msg += f" - your running time             : {user_duration:.4f}\n"
    msg += f" - running time optimal solution : {optimal_duration:.4f}\033[0m\n"

    assert slow_duration/2 > user_duration, msg + "\033[91mYour code is not optimized enough.\033[0m"

    if optimal_duration*2 < user_duration:
        msg += "\033[93mYour code is sufficiently optimized, but could be optimized even more.\033[0m"
    else:
        msg += "\033[92mSolution fully optimized!\033[0m"
    check.success = msg

def test_performance(load_words, calculate_score, text):
    shakespeare_words = load_words("words.txt")
    start = time.time()
    for i in range(20): # 6000 - 35
        score = calculate_score(text, shakespeare_words)
    end = time.time()
    return end - start


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
