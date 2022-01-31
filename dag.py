from data_loader import *
from itertools import permutations
from copy import copy

def get_new_key(old_key, char, idx):
    l = list(old_key)
    l[idx] = char
    return tuple(l)

class Node:
    def __init__(self, key) -> None:
        self.key = key
        self.children = {}
        self.count = 0

class DAG:
    def __init__(self, length=5) -> None:
        self.length = length
        self.root = Node(tuple(['' for _ in range(length)]))
        self.node_dict = {}
        self.node_dict[self.root.key] = self.root

        data = load_data("words_dictionary.json")
        data = filter_data(data, length)
        self.build_dag(data)

    def build_dag(self, data):
        for word in data:
            updated = {}
            for p in list(permutations(range(len(word)))):
                node = self.root
                for i in list(p):
                    key = node.key
                    if key not in updated:
                        node.count += 1
                        updated[key] = 1
                    new_key = get_new_key(key, word[i], i)
                    if new_key not in self.node_dict:
                        new_node = Node(new_key)
                        self.node_dict[new_key] = new_node
                    if new_key not in node.children:
                        node.children[new_key] = self.node_dict[new_key]
                    node = node.children[new_key]
                node.count = 1
    
    def get_word_list(self, key, banned={}):
        if key not in self.node_dict:
            return set([])
        if self.is_terminal(key):
            for k in list(key):
                if k in banned:
                    return set([])
            return set([''.join(key)])
        node = self.node_dict[key]
        word_list = set([])
        for k in node.children:
            if k not in banned:
                word_list = word_list.union(self.get_word_list(k, banned=banned))
        return word_list

    def get_constrained_word_list(self, positive, negative, banned):
        base = ['' for _ in range(self.length)]
        for c in positive:
            for i in positive[c]:
                base[i] = c

        bases = [base]
        for c in negative:
            if c not in positive:
                new_bases = []
                for base in bases:
                    for j, d in enumerate(base):
                        if d == '' and j not in negative[c]:
                            b = copy(base)
                            b[j] = c
                            new_bases.append(b)
                bases = new_bases
        bases = [tuple(b) for b in bases]
        word_list = set([])
        for b in bases:
            word_list = word_list.union(self.get_word_list(b, banned))
        pos_neg = {}
        for c in positive:
            if c in negative:
                pos_neg[c] = negative[c]
        new_list = []
        for w in list(word_list):
            sat = True
            for i, c in enumerate(w):
                if c in pos_neg and any([c == w[j] for j in pos_neg[c]]):
                    sat = False
                    break
            if sat:
                new_list.append(w)
        return set(new_list)

    def is_terminal(self, key):
        return all([c != '' for c in list(key)])
