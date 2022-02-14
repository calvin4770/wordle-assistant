import solver as sl

def main():
    solver = sl.GreedyEntropySolver()
    
    while True:
        print("Top 10 words sorted by rank: ")
        print(solver.get_ranked_words()[:10])
        word = input("Input chosen word: ")
        done = input("Done? ")
        if done == "y": break
        inp = input("Input observed permutation (black=0, yellow=1, green=2): ")
        perm = tuple([int(x) for x in inp])
        solver.update_possible_answers(word, perm)
        print("Possible answers:", solver.answers)
        
if __name__ == "__main__":
    main()