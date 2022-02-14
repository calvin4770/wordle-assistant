import numpy as np
import solver as sl
import preprocessing
import matplotlib.pyplot as plt
from tqdm import tqdm

def evaluate_solver(solver):
    answers = preprocessing.load_words(preprocessing.ANSWERS_PATH)
    lengths = []

    first_word = "soare"
    for answer in tqdm(answers):
        lengths.append(guess_length_given_first_word(solver, first_word, answer))

    lengths = np.array(lengths)
    print(f"Mean length: {np.mean(lengths)}, Standard deviation:{np.std(lengths)}")
    plt.hist(lengths)
    plt.show()
    return np.mean(lengths), np.std(lengths)

def guess_length_given_first_word(solver, first_word, answer):
    word = first_word
    length = 1
    while word != answer:
        perm = solver.table[(word, answer)]
        solver.update_possible_answers(word, perm)
        word = solver.get_ranked_words()[0]
        length += 1
    solver.reset()
    return length


if __name__ == "__main__":
    evaluate_solver(sl.GreedyEntropySolver())