# main file for the program / project

import scrap_articles
import stopwords
import words
import analyze
import export
import time

if __name__ == '__main__':
    start = time.time()

    # invoke function to scrap websites for article's html
    # and then store the text as .txt file
    scrap_articles.store_articles()

    # get the stopwords list
    stop_words = stopwords.get_stopwords()

    # get the positive / negative words
    words = words.words_list()

    # invoke function to analyze the text
    total_values = analyze.analyze_text(stop_words, words)

    # invoke function to export final collected data
    export.export_excel(total_values)

    print("\nProgram Executed Successfully")
    print("Time taken :-", time.time() - start)
