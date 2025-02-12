from checkpy import *

only("unique-word-classifier.py")
download("shakespeare-words.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/shakespeare-words.txt")
# download("shakespeare.0350.txt", "https://raw.githubusercontent.com/spcourse/tests/refs/heads/master/data/shakespeare.0350.txt")



@test(timeout=2)
def test2():
    """Testing speed calculate_shakespeare_score()"""
    shakespeare_words = getFunction("load_shakespeare_words")("shakespeare-words.txt")
    text = """_Ham._ (C.) Heaven make thee free of it! I follow thee.
You that look pale and tremble at this chance,
That are but mutes or audience to this act,
Had I but time (as this fell sergeant, death,[79]
Is strict in his arrest), O, I could tell you,--
But let it be. Horatio,
Report me and my cause aright
To the unsatisfied."""*100
    for i in range(800): # 3100
        score = getFunction("calculate_shakespeare_score")(text, shakespeare_words)
    print(score)

    assert True
