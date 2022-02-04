import csv

def load_data(path):
    with open(path) as f:
        data = list(csv.reader(f))[0]
    return data

if __name__ == "__main__":
    data = load_data("data/words.csv")
    print(data[:100])
    print(len(data))