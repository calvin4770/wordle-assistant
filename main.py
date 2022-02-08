import assistant
import data_loader

def main():
    words = data_loader.load_data("data/words.csv")
    c1, c2, c3 = set([]), set([]), set([])
    scorer = assistant.EntropyScorer()
    letters = set([])
    
    while True:
        print("Top 10 words sorted by rank: ")
        print(scorer.words_ranked_by_score()[:10])
        word = input("Input chosen word: ")
        done = input("Done? ")
        if done == "y": break
        in1 = input("Indices of characters in right location: ")
        in2 = input("Indices of characters in wrong location: ")
        idxs1 = [] if in1 == "" else [int(x) for x in in1.split(" ")]
        idxs2 = [] if in2 == "" else [int(x) for x in in2.split(" ")]
        for i in idxs1:
            c1.add((i, word[i]))
            letters.add(word[i])
        for i in idxs2:
            c2.add((i, word[i]))
            letters.add(word[i])
        for x in enumerate(word):
            i, c = x
            if i not in idxs1 and i not in idxs2:
                if c not in letters:
                    c3.add(c)
                else: c2.add(x)
        words = assistant.get_constrained_list(words, c1, c2, c3)
        scorer.update(words, c1, c2, c3)
        
if __name__ == "__main__":
    main()