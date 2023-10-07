# function to read stopwords from multiple text documents
# and store them in a single list

from nltk.tokenize import word_tokenize
import os


def get_stopwords():
    # read the stopwords folder for all stopwords files
    stopword_files = os.listdir(r".\StopWords")

    # avoid these specifics in stopwords
    specifics = [r'Surnames from 1990 census > .002%.  www.census.gov.genealogy/names/dist.all.last',
                 r'http://www.census.gov/genealogy/names/dist.male.first',
                 r'http://www.census.gov/genealogy/names/dist.female.first',
                 r'http://en.wikipedia.org/wiki/List_of_most_common_surnames#China',
                 r'|', r'.', r'(', r')']

    stop_string = ""

    # do for all the stopwords files
    for i in range(len(stopword_files)):

        stopword_file = r".\StopWords\\" + stopword_files[i]

        with open(stopword_file, "r") as f:
            # read the entire .txt doc in a string
            stop_string += f.read()

    # remove specifics
    for item in specifics:
        stop_string = stop_string.replace(item, "")

    # tokenize and store in a list
    stop_words = word_tokenize(stop_string)

    print("Successfully Generated Stopwords List")

    return stop_words
