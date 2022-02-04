# c1: characters in right location; [(Index, Character)]
# c2: characters in wrong location; map [(Index, Character)]
# c3: characters not in word; [Characters]

class Scorer:
    def __init__(self) -> None:
        self.words = []
        self.c1 = []
        self.c2 = []
        self.c3 = []

    def score_word(self, word):
        pass

    def update_scorer(self, words, c1, c2, c3):
        self.words = words
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3

class FrequencyHeuristicScorer(Scorer):
    def __init__(self) -> None:
        super().__init__()
        self.char_freqs = {}

    def score_word(self, word):
        score = 0
        for i, c in enumerate(word):
            if all([c not in x for x in [self.c1, self.c2, self.c3]]) and \
                c not in word[:i]:
                score += self.char_freqs[c]
        return score

    def update_scorer(self, words, c1, c2, c3):
        super().update_scorer(words, c1, c2, c3)
        self.char_freqs = {}
        for word in words:
            for i, c in enumerate(word):
                if c not in self.char_freqs:
                    self.char_freqs[c] = 0
                if c not in word[:i]:
                    self.char_freqs[c] += 1

class WordReachScorer(Scorer):
    def __init__(self) -> None:
        super().__init__()
        self.word_map = {}
        self.explored_chars = set([])

    def score_word(self, word):
        new_chars = list(filter(lambda c: c not in self.explored_chars, word))
        reachable_words = set([])
        for c in new_chars:
            reachable_words = reachable_words.union(self.word_map[c])
        return len(reachable_words)

    def update_scorer(self, words, c1, c2, c3):
        super().update_scorer(words, c1, c2, c3)
        self.word_map = {}
        self.explored_chars = {}
        for w in words:
            for c in w:
                if c not in self.word_map:
                    self.word_map[c] = set([])
                self.word_map[c].add(w)
        l1 = set(map(lambda x: x[0], self.c1))
        l2 = set(map(lambda x: x[0], self.c2))
        self.explored_chars = l1.union(l2)

# returns if word is plausible given constraints
def is_plausible(word, c1, c2, c3):
    c1_holds = all([word[i] == c for i, c in c1])
    c2_holds = all([word[i] != c and c in word for i, c in c2])
    c3_holds = all([c not in word for c in c3])
    return c1_holds and c2_holds and c3_holds

def get_constrained_list(words, c1, c2, c3):
    return list(filter(lambda w: is_plausible(w, c1, c2, c3), words))    

def words_ranked_by_score(words, scorer, c1, c2, c3):
    scorer.update_scorer(words, c1, c2, c3)
    return sorted(list(words), key=scorer.score_word, reverse=True)
    