import numpy as np
import data_loader
import assistant
import copy
import tqdm
import random

def evaluate_scorer(scorer, sample=False, num_samples=50, output=False):
    if output:
        print(f"Scorer: {scorer}")
    all_words = words = data_loader.load_data("data/words.csv")
    if sample:
        words = random.sample(all_words, num_samples)
    lengths = []
    first_guess = first_word(all_words, scorer)
    if output:
        print(f"First guess: {first_guess}")
    for word in tqdm.tqdm(words):
        lengths.append(guess_length_given_first_word(all_words, word, scorer, first_guess))
    lengths = np.array(lengths)
    if output:
        print(f"Mean length: {np.mean(lengths)}, Standard deviation:{np.std(lengths)}")
    return np.mean(lengths), np.std(lengths)

def guess_length_given_first_word(words, word, scorer, first_word):
    length = 1
    guess = copy.copy(first_word)
    words_list = copy.copy(words)
    while guess != word:
        c1, c2, c3 = [], [], []
        for i, c in enumerate(guess):
            if c == word[i]:
                c1.append((i, c))
            elif c in word:
                c2.append((i, c))
            else:
                c3.append(c)
        words_list = assistant.get_constrained_list(words_list, c1, c2, c3)
        guess = assistant.greedy_word_choice(words_list, scorer, c1, c2, c3)
        length += 1
    return length

def first_word(words, scorer):
    return assistant.greedy_word_choice(words, scorer, [], [], [])

if __name__ == "__main__":
    #scorers = [assistant.FrequencyHeuristicScorer(), assistant.WordReachScorer(), assistant.WeightedWordReachScorer()]
    scorers = [assistant.WeightedWordReachScorer()]
    for scorer in scorers:
        evaluate_scorer(scorer, sample=True, num_samples=1000, output=True)