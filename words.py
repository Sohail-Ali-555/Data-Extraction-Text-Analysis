# function to read the positive / negative words available in
# Master Dictionary folder and store them in a single list

from nltk import word_tokenize


def words_list():
    # positive words file
    pos_file = r".\MasterDictionary\positive-words.txt"
    # negative words file
    neg_file = r".\MasterDictionary\negative-words.txt"

    with open(pos_file, "r") as f:
        # read it temporarily as a string
        temp_string = f.read()

        # finally store as list
        positive = word_tokenize(temp_string)

    with open(neg_file, "r") as f:
        # read it temporarily as a string
        temp_string = f.read()

        # finally store as list
        negative = word_tokenize(temp_string)

    # return as a combined list
    return [positive, negative]
