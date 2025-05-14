from itertools import permutations
from collections import Counter

word = "КОМБИНАТОРИКА"
letter_counts = Counter(word)


def count_unique_words(word, length):
    unique_words = set()
    for p in permutations(word, length):
        unique_words.add(p)
    return len(unique_words)


result = count_unique_words(word, 6)
print(f"Количество различных 6-буквенных слов: {result}")