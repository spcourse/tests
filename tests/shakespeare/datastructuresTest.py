from checkpy import *


### 1 Lemmas
fun1_def = (declarative
    .function("count_lemmas")
    .params("text", "lemmas")
    .returnType(dict)
)

text1 = "He is, was and will be a runner. And runners ran, run and will always run. This is their nature."

lemmas = {
    "runners": "runner",
    "ran": "run",
    "was": "be",
    "is": "be"
}

dict1 = {'he': 1, 'be': 4, 'and': 3, 'will': 2, 'a': 1, 'runner': 2, 'run': 3, 'always': 1, 'this': 1, 'their': 1, 'nature': 1}

test1_1 = test()(fun1_def.call(text1, lemmas).returns(dict1))


### 2 Grammatical categories
fun2_def = (declarative
    .function("count_category")
    .params("lemma_counts", "category")
    .returnType(int)
)

lemma_counts = {'he': 1, 'be': 4, 'and': 3, 'will': 2, 'a': 1, 'runner': 2, 'run': 3, 'always': 1, 'this': 1, 'their': 1, 'nature': 1}
nouns = {'runner', 'nature', 'building'}
verbs = {'walk', 'run', 'be'}
determiners = {'the', 'a', 'this', 'their'}

test2_1 = test()(fun2_def.call(lemma_counts, nouns).returns(3))
test2_2 = test()(fun2_def.call(lemma_counts, verbs).returns(7))
test2_3 = test()(fun2_def.call(lemma_counts, determiners).returns(3))


### 3 Library
fun3_def = (declarative
    .function("group_titles_by_genre")
    .params("library")
    .returnType(dict)
)

library = {"Life of Pi": "Adventure",
         "One World The Water Dancer": "Fantasy",
         "The Three Musketeers": "Adventure",
         "To Kill a Mockingbird": "Classics",
         "Circe": "Fantasy",
         "The Call of the Wild": "Adventure",
         "Little Women": "Classics"}
grouped =  {'Adventure': ['Life of Pi', 'The Three Musketeers', 'The Call of the Wild'],
          'Fantasy': ['One World The Water Dancer', 'Circe'],
          'Classics': ['To Kill a Mockingbird', 'Little Women']}

test3_1 = test()(fun3_def.call(library).returns(grouped))


### 4 Unify
fun4_def = (declarative
    .function("unify")
    .params("dict1", "dict2")
    .returnType(dict)
)

dict2 = {"a": [1, 2, 3], "c": [4, 5, 6], "d": [6]}
dict3 = {"a": [1, 3, 4], "b": [9], "c": [2, 4]}

test4_1 = test()(fun4_def.call(dict2, dict3).returns({'b': [9], 'c': [2, 4, 5, 6], 'd': [6], 'a': [1, 2, 3, 4]}))


### 5 Melt
fun5_def = (declarative
    .function("melt")
    .params("dict")
    .returnType(list)
)

dict4 = {"a": [1, 2, 3], "c": [4, 5, 6], "d": [6]}

test5_2 = test()(fun5_def.call(dict4).returns([('a', 1), ('a', 2), ('a', 3), ('c', 4), ('c', 5), ('c', 6), ('d', 6)]))


### 6 N-intersection
fun6_def = (declarative
    .function("n_intersection")
    .params("sets")
    .returnType(set)
)

test6_1 = test()(fun6_def.call([{5, 9, 6}, {9, 2, 6}, {6, 5, 9}]).returns({9, 6}))
test6_2 = test()(fun6_def.call([
                      {"kerfuffle", "hullaballoo", "ragamuffin", "flummox"},
                      {"kerfuffle", "ragamuffin", "gobbledygook", "flummox"},
                      {"hullaballoo", "ragamuffin", "gobbledygook", "flummox"},
                      {"hullaballoo", "ragamuffin", "ragamuffin", "gobbledygook", "flummox"}]).returns({'ragamuffin', 'flummox'}))
test6_3 = test()(fun6_def.call([]).returns(set()))


### 7 Sentiment
fun7_def = (declarative
    .function("sentiment_of_text")
    .params("text", "sentiment_of_word")
    .returnType(int)
)

sentiment_of_word = {
    "abysmal": -5, "dreadful": -5, "miserable": -4, "terrible": -5, "upset": -3,
    "amazing": 5, "fantastic": 4, "great": 3, "superb": 4, "fantabulous": 5
}

text11 = "Wow, what an amazing day it has been! The weather is fantastic!"

text12 = "Today has been abysmal. The weather is dreadful, and I feel miserably upset."

test7_1 = test()(fun7_def.call(text11, sentiment_of_word).returns(9))
test7_2 = test()(fun7_def.call(text12, sentiment_of_word).returns(-13))
