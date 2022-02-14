import numpy as np
import random
import copy
import preprocessing

BLACK = 0
YELLOW = 1
GREEN = 2

class GreedyEntropySolver:
    def __init__(self):
        self.words = preprocessing.load_words(preprocessing.WORDS_PATH)
        self.answers = preprocessing.load_words(preprocessing.ANSWERS_PATH)
        self.table = preprocessing.get_lookup_table()

    def get_ranked_words(self):
        return sorted(self.words, key=lambda w: get_word_entropy(self.table, w, self.answers), reverse=True)

    def update_possible_answers(self, chosen_word, perm):
        self.answers = get_possible_answers(self.table, chosen_word, perm, self.answers)

    def reset(self):
        self.answers = preprocessing.load_words(preprocessing.ANSWERS_PATH)

# return list of possible answers given a guess and observed permutation
def get_possible_answers(table, word, perm, answers):
    possible_answers = []
    for answer in answers:
        if table[(word, answer)] == perm:
            possible_answers.append(answer)
    return possible_answers

# entropy of a given word
def get_word_entropy(table, word, possible_answers):
    if len(possible_answers) == 1:
        return 1 if word == possible_answers[0] else 0
    total = len(possible_answers)
    perm_dist = {}
    entropy = 0
    for answer in possible_answers:
        perm = table[(word, answer)]
        if perm not in perm_dist:
            perm_dist[perm] = 0
        perm_dist[perm] += 1
    for perm in perm_dist:
        p = perm_dist[perm] / total
        entropy -= p * np.log2(p)
    return entropy


def induced_permutation(word, answer):
    perm = [0, 0, 0, 0, 0]
    char_total_counts = {}
    char_counts = {}

    # init counts
    for c in answer:
        char_total_counts[c] = 0
        char_counts[c] = 0

    # compute total counts
    for c in answer:
        char_total_counts[c] += 1

    # compute induced permutation
    for i, c in enumerate(word):
        if answer[i] == c:
            perm[i] = GREEN
            char_counts[c] += 1
    for i, c in enumerate(word):
        if c in char_total_counts and char_counts[c] < char_total_counts[c]:
            perm[i] = YELLOW
            char_counts[c] += 1
    return tuple(perm)

if __name__ == "__main__":
    print(induced_permutation("sssds", "iiiss"))