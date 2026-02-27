from checkpy import *

only("datastructures1.py")

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


### 3 Incrementing values
fun3_def = (declarative
    .function("increment_counts")
    .params("counts", "words")
    .returnType(dict)
)

# Test 3.1: basic example
counts1 = {'apple': 2, 'banana': 1}
words1 = ['banana', 'apple', 'orange']
expected1 = {'apple': 3, 'banana': 2, 'orange': 1}
test3_1 = test()(fun3_def.call(counts1, words1).returns(expected1))

# Test 3.2: empty input list should leave dict unchanged
counts2 = {'x': 5}
words2 = []
expected2 = {'x': 5}
test3_2 = test()(fun3_def.call(counts2, words2).returns(expected2))

# Test 3.3: starting from empty dict
counts3 = {}
words3 = ['a', 'b', 'a', 'a']
expected3 = {'a': 3, 'b': 1}
test3_3 = test()(fun3_def.call(counts3, words3).returns(expected3))


### 4 Library
fun4_def = (declarative
    .function("group_titles_by_genre")
    .params("library")
    .returnType(dict)
)

library1 = {"Life of Pi": "Adventure",
            "One World The Water Dancer": "Fantasy",
            "The Three Musketeers": "Adventure",
            "To Kill a Mockingbird": "Classics",
            "Circe": "Fantasy",
            "The Call of the Wild": "Adventure",
            "Little Women": "Classics"}

grouped1 = {'Adventure': ['Life of Pi', 'The Three Musketeers', 'The Call of the Wild'],
            'Fantasy': ['One World The Water Dancer', 'Circe'],
            'Classics': ['To Kill a Mockingbird', 'Little Women']}

test4_1 = test()(fun4_def.call(library1).returns(grouped1))

# Extra: different library, to prevent hardcoding
library2 = {"A": "X", "B": "Y", "C": "X"}
grouped2 = {"X": ["A", "C"], "Y": ["B"]}
test4_2 = test()(fun4_def.call(library2).returns(grouped2))
