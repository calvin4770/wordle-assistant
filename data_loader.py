import json

def load_data(path):
    with open(path) as f:
        data = list(json.load(f).keys())
    return data

def filter_data(data, n_chars):
    return list(filter(lambda x: len(x) == n_chars, data))

if __name__ == "__main__":
    data = load_data("words_dictionary.json")
    data = filter_data(data, 5)
    print(data[:1000])
    print(len(data))