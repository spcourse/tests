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
    return words


def calculate_shakespeare_score(text, shakespeare_words):
    """
    Compute the score of a text fragment by checking the relative overlap of
    words in the text with the shakespeare word list.
    """
    word_list = tokenize_text(text)

    # get all unique words in text
    unique_words = []
    for word in word_list:
        if word not in unique_words:
            unique_words.append(word)

    # get all unique shakespeare words in text
    shakespeare_words_in_text = []
    for word in unique_words:
        if word in shakespeare_words:
            shakespeare_words_in_text.append(word)

    shakespeare_score = len(shakespeare_words_in_text)/len(unique_words)
    return shakespeare_score
