from operator import ne
from dag import *

def main():
    positive, negative, banned = {}, {}, {}
    dag = DAG()
    print("Try adieu")
    word = "adieu"
    while True:
        done = input("Done? ")
        if done == "y": break
        in1 = input("Indices of characters in right location: ")
        in2 = input("Indices of characters in wrong location: ")
        idxs1 = [] if in1 == "" else [int(x) for x in in1.split(" ")]
        idxs2 = [] if in2 == "" else [int(x) for x in in2.split(" ")]
        for i in idxs1:
            if word[i] not in positive:
                positive[word[i]] = []
            positive[word[i]].append(i)
        for i in idxs2:
            if word[i] not in negative:
                negative[word[i]] = []
            negative[word[i]].append(i)
        for i in range(len(word)):
            if i not in idxs1 and i not in idxs2:
                if word[i] not in positive and word[i] not in negative:
                    banned[word[i]] = []
                else:
                    negative[word[i]].append(i)
        l = dag.get_constrained_word_list(positive, negative, banned)
        print("Possible words:")
        print(l)
        word = input("Input chosen word: ")

if __name__ == "__main__":
    main()