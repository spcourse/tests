from checkpy import *

only("unique-word-classifier.py")

download("shakespeare-words.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/shakespeare-words.txt")
download("words.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/words.txt")
download("shakespeare.1.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/shakespeare.1.txt")
download("shakespeare.2.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/shakespeare.2.txt")
download("jonson.1.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/jonson.1.txt")
download("jonson.2.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/jonson.2.txt")



@test(timeout=4)
def test1():
    """Testing speed calculate_shakespeare_score()
    (calculating the score 1000 times using a text of 800 lines and a file
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
    for i in range(1000): # 6000 - 35
        score = getFunction("calculate_shakespeare_score")(text, shakespeare_words)



# @test(timeout=10)
# def test2():
#     """Testing accuracies"""
#     shakespeare_words = getFunction("load_shakespeare_words")("words.txt")
#
#     accs = getFunction("compute_all_accuracies")(
#         [0.1, 0.2, 0.3, 0.4],
#         ["jonson.1.txt", "jonson.1.txt", "shakespeare.1.txt", "shakespeare.2.txt"],
#         shakespeare_words)
#
#     print(accs)
