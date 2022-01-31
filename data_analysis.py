def char_freqs(word_list):
    char_freq = {}
    for word in list(word_list):
        for i, c in enumerate(word):
            if c not in char_freq:
                char_freq[c] = 0
            if c not in word[:i]:
                char_freq[c] += 1
    return char_freq

def word_ranks(word_list, pos, neg, ban):
    char_freq = char_freqs(word_list)
    scores = {}
    total = 0
    for c in char_freq:
        if c in [pos, neg, ban]:
            char_freq[c] = 0
            total += char_freq[c]
    for w in list(word_list):
        score = 0
        for i, c in enumerate(w):
            if c not in w[:i]:
                score += char_freq[c]
        scores[w] = score
    return sorted(list(word_list), key=lambda w: scores[w], reverse=True)
    