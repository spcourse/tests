import typing
from checkpy import *


text_to_unique_words = (declarative
    .function("text_to_unique_words")
    .returnType(typing.List[str])
    .params("text")
)   

correctEmpty = test()(text_to_unique_words
    .call("")
    .returns([])
)

correctOneWord = test()(text_to_unique_words
    .call("StickBoy")
    .returns(["StickBoy".lower()])
)


@passed(correctOneWord, hide=False)
def correctOneSentence():
    """works for multiple words with punctuation"""
    state = text_to_unique_words.call("Stick Boy's Festive, Season.")()
    output = sorted(state.returned)
    
    assert "boy's" in output, "make sure to deal with punctuation"
    
    assert "festive," not in output and "season." not in output,\
            "make sure there are no periods and/or commas"
    
    expected = sorted(['stick', "boy's", 'festive', 'season'])
    assert output == expected


@passed(correctOneSentence, hide=False)
def correctComplexSentence():
    """works for multiple words with double spaces"""
    testText = "Stick  Boy noticed that his  Christmas tree, looked  healtier than he did"
    state = text_to_unique_words.call(testText)()
    output = sorted(state.returned)

    assert "" not in output, "make sure there are no empty strings in the returned list"
    
    expected = sorted(['stick', 'boy', 'noticed', 'that', 'his', 'christmas', 'tree', 'looked', 'healtier', 'than', 'he', 'did'])
    assert output == expected


@passed(correctOneSentence, hide=False)
def Alphabetically():
    """the words are returned in alphabetical order"""
    testText = "Unwisely Santa offered a teddy bear to James unaware that he had been mauled by a grizzly earlier that year"
    state = text_to_unique_words.call(testText)()
    output = state.returned
    
    assert sorted(set(output)) == sorted(output), "make sure there are no duplicate words"

    expected = sorted(['a', 'bear', 'been', 'by', 'earlier', 'grizzly', 'had', 'he', 'james', 'mauled', 'offered', 'santa', 'teddy', 'that', 'to', 'unaware', 'unwisely', 'year'])
    assert output == expected
