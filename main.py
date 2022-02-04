import assistant
import data_loader

def main():
    words = data_loader.load_data("data/words.csv")
    c1, c2, c3 = [], [], []
    scorer = assistant.FrequencyHeuristicScorer()
    
    while True:
        print("Top 10 words sorted by rank: ")
        print(assistant.words_ranked_by_score(words, scorer, c1, c2, c3)[:10])
        word = input("Input chosen word: ")
        done = input("Done? ")
        if done == "y": break
        in1 = input("Indices of characters in right location: ")
        in2 = input("Indices of characters in wrong location: ")
        idxs1 = [] if in1 == "" else [int(x) for x in in1.split(" ")]
        idxs2 = [] if in2 == "" else [int(x) for x in in2.split(" ")]
        for i in idxs1:
            x = (i, word[i])
            if x not in c1:
                c1.append(x)
        for i in idxs2:
            x = (i, word[i])
            if x not in c2:
                c2.append(x)
        for x in enumerate(word):
            i, c = x
            if i not in idxs1 and i not in idxs2:
                if x not in c1 and x not in c2:
                    c3.append(c)
                elif x not in c2:
                    c2.append(x)
        

if __name__ == "__main__":
    main()