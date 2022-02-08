import math
import random
import itertools
import data_loader
import copy

# c1: characters in right location; [(Index, Character)]
# c2: characters in wrong location; map [(Index, Character)]
# c3: characters not in word; [Characters]

class Scorer:
    def __init__(self, use_all_words=False):
        self.all_words = data_loader.load_data("data/words.csv")
        self.words = copy.copy(self.all_words)
        self.c1 = set([])
        self.c2 = set([])
        self.c3 = set([])
        self.use_all_words = use_all_words
        self.first_word = None

    def score_word(self, word):
        pass

    def update(self, words, c1, c2, c3):
        self.words = words
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3

    def greedy_word_choice(self):
        if len(self.words) == len(self.all_words) and first_word is not None:
            return first_word
        words = self.all_words if self.use_all_words else self.words
        word, max_score = "", -10e10 # very small number
        for w in words:
            score = self.score_word(w)
            if score > max_score:
                word = w
                max_score = score
        return word

    def words_ranked_by_score(self):
        words = self.all_words if self.use_all_words else self.words
        return sorted(words, key=self.score_word, reverse=True)

class FrequencyHeuristicScorer(Scorer):
    def __init__(self):
        super().__init__()
        self.char_freqs = {}

    def score_word(self, word):
        score = 0
        for i, c in enumerate(word):
            if all([c not in x for x in [self.c1, self.c2, self.c3]]) and \
                c not in word[:i]:
                score += self.char_freqs[c]
        return score

    def update(self, words, c1, c2, c3):
        super().update(words, c1, c2, c3)
        self.char_freqs = {}
        for word in words:
            for i, c in enumerate(word):
                if c not in self.char_freqs:
                    self.char_freqs[c] = 0
                if c not in word[:i]:
                    self.char_freqs[c] += 1

class WordReachScorer(Scorer):
    def __init__(self):
        super().__init__()
        self.explored_chars = set([])
        self.reachable_words = set([])
        self.new_chars = []

    def score_word(self, word):
        self.new_chars = list(filter(lambda c: c not in self.explored_chars, word))
        self.reachable_words = set([])
        for w in self.words:
            for c in self.new_chars:
                if c in w:
                    self.reachable_words.add(w)
                    break
        return len(self.reachable_words)

    def update(self, words, c1, c2, c3):
        super().update(words, c1, c2, c3)
        self.explored_chars = {}
        l1 = set(map(lambda x: x[0], self.c1))
        l2 = set(map(lambda x: x[0], self.c2))
        self.explored_chars = l1.union(l2)

class WeightedWordReachScorer(WordReachScorer):
    def score_word(self, word):
        super().score_word(word)
        return sum(map(lambda w: self.word_weight(word, w), self.reachable_words))

    # weight of word w given query word word
    def word_weight(self, word, w):
        weight = 1
        for i, c in enumerate(w):
            if c in self.new_chars and c not in w[:i]:
                weight += 1
            if c == word[i] and (i, c) not in self.c1:
                weight += 1
        return weight


class EntropyScorer(Scorer):
    def __init__(self):
        super().__init__()
        self.use_all_words = True
        self.first_word = "tares"

    def score_word(self, word):
        N = len(self.words)
        if N == 1:
            return 1 if word == self.words[0] else 0

        entropy = 0
        perm_dist = {}

        for ans in self.words:
            perm = induced_permutation(word, ans)
            if perm not in perm_dist:
                perm_dist[perm] = 0
            perm_dist[perm] += 1

        for perm in perm_dist:
            p = perm_dist[perm] / N
            if p > 0:
                entropy -= p * math.log(p, 2)
        return entropy


# 0: black, 1: yellow, 2: green
def induced_permutation(guess, answer):
    perm = [0, 0, 0, 0, 0]
    c1, c2, c3 = get_constraints_given_word(answer, guess)
    for i, c in c1:
        perm[i] = 2
    for i, c in c2:
        perm[i] = 1
    return tuple(perm)


# returns if word is plausible given constraints
def is_plausible(word, c1, c2, c3):
    c1_holds = all([word[i] == c for i, c in c1])
    c2_holds = all([word[i] != c and c in word for i, c in c2])
    c3_holds = all([c not in word for c in c3])
    return c1_holds and c2_holds and c3_holds

def get_constrained_list(words, c1, c2, c3):
    return list(filter(lambda w: is_plausible(w, c1, c2, c3), words))

# get constraints for input guess supposing word is the answer
def get_constraints_given_word(word, guess):
    c1, c2, c3 = set([]), set([]), set([])
    for i, c in enumerate(guess):
        if c == word[i]:
            c1.add((i, c))
        elif c in word:
            c2.add((i, c))
        else:
            c3.add(c)
    return c1, c2, c3
    