# functions to analyze the stored articles' text

from nltk import word_tokenize, sent_tokenize
import re
import os


def syllable_count(word):
    # lowercase to avoid any problems for uppercase word
    word = word.lower()

    # alphabets that can give a vowel sound, this includes 'y' also
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']

    count = 0

    if word[0] in vowels:
        count += 1

    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1

    # end letter 'e' case
    if word.endswith("e"):
        count -= 1

    # if no count observed
    if count == 0:
        count += 1

    return count


def analyze_text(stopwords, words):
    # get the list of filenames of all .'txt' articles
    article_files = os.listdir(r".\Articles")

    # creating an empty dictionary
    total_values = dict()

    # do for all the files
    for i in range(len(article_files)):

        print("Trying to analyze Article URD_ID :-", article_files[i])

        # path of article file
        article_file = r".\Articles\\" + article_files[i]

        # name of file
        file_name = article_files[i]
        # remove the end file extension, note: file_name is of string type
        file_name = file_name.replace('.txt', '')

        # read the file in string format
        with open(article_file, "r", encoding="utf-8") as f:
            string = f.read()

        # conditional for taking care of strings with 0 length, in case of empty file
        if len(string) == 0:
            # add None with file_name as key
            total_values.update({file_name: None})

            print("Cannot be Analyzed. Empty Text File\n")
            # skip the remaining code
            continue

        # create tokens/words and sentences
        tokens = word_tokenize(string)
        sentences = sent_tokenize(string)

        # list of cleaned tokens
        clean_tokens = []

        # first cleaning by removing any punctuations
        punctuations = ['[', ']', '@', '#', '$', '%', '^', '&', '*', '|', '{', '}', '(', ')', '<', '>',
                        '?', '`', '~', "'", '"', '/', '\\', ',', '.', ':', ';', '!', '-', '_', '+', '=']

        # now, clean the tokens of both punctuations & stopwords using stopwords list
        for item in tokens:

            if item not in stopwords and item not in punctuations:
                # add the token
                clean_tokens.append(item)

        # check for positive & negative words
        positive, negative = words[0], words[1]

        # initial score
        positive_score = 0
        negative_score = 0

        # increment score(s)
        for item in clean_tokens:

            if item in positive:
                positive_score += 1

            if item in negative:
                negative_score += 1

        # set condition for polarity score and subjective score
        if positive_score or negative_score:

            # Range is from -1 to + 1
            polarity_score = (positive_score - negative_score) / (positive_score + negative_score) + 0.000001

            # subjective score, Range is from 0 to + 1
            sub_score = (positive_score + negative_score) / (len(clean_tokens) + 0.000001)

        else:
            polarity_score = 'NA'
            sub_score = 'NA'

        # average sentence length
        avg_sent_length = len(clean_tokens) / len(sentences)

        # average number of words per sentence
        avg_word_per_sent = len(clean_tokens) / len(sentences)

        # complex word count: words having more than 2 syllables
        complex = 0

        for item in clean_tokens:
            # invoke syllable count function with conditional of (> 2)
            if syllable_count(item) > 2:
                complex += 1

        # percentage of complex words
        percentage_complex = complex / len(clean_tokens) * 100

        # fog index
        fog_index = 0.4 * (avg_sent_length + percentage_complex)

        # word count
        word_count = len(clean_tokens)

        # total syllables = syllable count per word in all clean tokens
        total_syllables = 0

        # for each of the clean token
        for item in clean_tokens:
            # invoke function for each and add
            total_syllables += syllable_count(item)

        # personal pronouns count
        pronouns_Regex = re.compile(r'\b(I|we|my|ours|(?-i:us))\b', re.I)

        pronouns = pronouns_Regex.findall(string)

        num_pronouns = len(pronouns)

        # calculation for average word length
        total_characters = 0

        for item in clean_tokens:
            total_characters += len(item)

        avg_word_length = total_characters / len(clean_tokens)

        print("Successfully Analyzed\n")

        # finally return all the quantities
        values = [positive_score, negative_score, polarity_score, sub_score, avg_sent_length, percentage_complex,
                  fog_index, avg_word_per_sent, complex, word_count, total_syllables, num_pronouns, avg_word_length]

        # update the dict
        total_values.update({file_name: values})

    return total_values
