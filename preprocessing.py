import csv
import pickle
import solver
import os
from tqdm import tqdm

WORDS_PATH = "data/words.csv"
ANSWERS_PATH = "data/answers.csv"
TABLE_PATH = "data/table.pkl"

def load_words(path):
    with open(path) as f:
        words = list(csv.reader(f))[0]
    return words

def save_data(path, data):
    with open(path, "wb") as f:
        pickle.dump(data, f)

def load_data(path):
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data

# build a lookup table of permutations for all possible word-answer combinations
def build_lookup_table():
    words = load_words(WORDS_PATH)
    answers = load_words(ANSWERS_PATH)
    table = {}
    print("Building lookup table...")
    for word in tqdm(words):
        for answer in answers:
            perm = solver.induced_permutation(word, answer)
            table[(word, answer)] = perm
    return table
    
def get_lookup_table():
    if not os.path.isfile(TABLE_PATH):
        print("Lookup table does not exist.")
        table = build_lookup_table()
        print(f"Saving lookup table to {TABLE_PATH}")
        save_data(TABLE_PATH, table)
        return table
    print(f"Loading lookup table from {TABLE_PATH}")
    return load_data(TABLE_PATH)