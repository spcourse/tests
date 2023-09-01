from checkpy import *

import ast
import typing

only("list_words.py")

@test()
def noBreakAndImport():
    """the program does not use break or import statements"""
    assert ast.Import not in static.AbstractSyntaxTree(), "you cannot use import statements"
    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"


correct_def_cleanup = test()(declarative
    .function("cleanup")
    .returnType(str)
    .params("word")
    .call("ClEaN!")
    .returns("clean")
    .description("correctly defines the cleanup() function")
)


correct_def_text_to_unique_words = test()(declarative
    .function("text_to_unique_words")
    .returnType(typing.List[str])
    .params("text")
    .call("Test sentence")
    .description("correctly defines the text_to_unique_words() function")
)


text_to_unique_words = (declarative
    .function("text_to_unique_words")
)


cleanup = (declarative
    .function("cleanup")
)


@passed(correct_def_text_to_unique_words, hide=False)
def correctEmpty():
    """function works correctly for empty strings"""
    text_to_unique_words.call("").returns([])()


@passed(correct_def_text_to_unique_words, hide=False)
def correctOneWord():
    """function works correctly for one word"""
    text_to_unique_words.call("StickBoy").returns(["StickBoy".lower()])()


@passed(correctOneWord, hide=False)
def correctOneSentence():
    """function works correctly for multiple words with punctuation"""
    state = text_to_unique_words.call("Stick Boy's Festive, Season.")()
    output = sorted(state.returned)
    
    assert "boy's" in output, "make sure to deal with punctuation"
    
    assert "festive," not in output and "season." not in output,\
            "make sure there are no periods and/or commas"
    
    expected = sorted(['stick', "boy's", 'festive', 'season'])
    assert output == expected


@passed(correctOneSentence, hide=False)
def correctComplexSentence():
    """function works correctly for multiple words with double spaces"""
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