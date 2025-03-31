def tokenize_text(text):
    """
    Returns a list of words from string text.
    """
    words = []
    for word in text.split():
        clean = word.lower().strip(' ,;.:\'"[]()-_?!')
        if clean.isalpha():
            words.append(clean)
    return words
    
def load_shakespeare_words(filename):
    """
    Load the file containing words typicaly for Shakespearean language. Assumes
    that the input file does not contain any duplicate words.
    """
    words = []
    with open(filename, 'r', encoding='UTF-8') as file:
        for line in file:
            words.append(line.rstrip('\n'))
    return set(words)


def calculate_shakespeare_score(text, shakespeare_words):
    """
    Compute the score of a text fragment by checking the relative overlap of
    words in the text with the shakespeare word list.
    """
    unique_words = set(tokenize_text(text))

    shakespeare_words_in_text = shakespeare_words & unique_words

    shakespeare_score = len(shakespeare_words_in_text)/len(unique_words)
    return shakespeare_score
