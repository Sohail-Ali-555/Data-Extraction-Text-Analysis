# function to scrap html content from website and then extract text
# from it and save it as .txt document

import requests
from bs4 import BeautifulSoup
import pandas as pd
from decimal import Decimal
import os


def store_articles():
    # read input Excel file
    df = pd.read_excel(r".\input.xlsx")

    # html output folder
    html_folder = r".\HTMLs"

    if not os.path.exists(html_folder):
        os.mkdir(html_folder)

    # text article output folder
    txt_folder = r".\Articles"

    if not os.path.exists(txt_folder):
        os.mkdir(txt_folder)

    # do for all the website links in dataframe
    for i in range(len(df)):

        # get url_id,
        # plus deal with float type numbers from pandas dataframe
        url_id = str(Decimal(str(df['URL_ID'][i])).normalize())

        print("Trying to scrap Article URD ID :-", url_id)

        # fix for scientific notations in url_id
        if 'E' in url_id:
            url_id = str(int(float(url_id)))

        # .html file path
        txt_path = txt_folder + "\\" + url_id + ".txt"

        # .txt file path
        html_path = html_folder + "\\" + url_id + ".html"

        # url link
        url = str(df['URL'][i])

        # get/scrap the html doc
        r = requests.get(url)

        # prepare to write the .html doc, keep the utf-8 encoding
        with open(html_path, 'w', encoding="utf-8") as f:

            # write the html doc
            f.write(r.text)

        # now open those .html files
        with open(html_path, 'r', encoding="utf-8") as f:
            html_doc = f.read()

        # make the soup object for html tags parsing
        soup = BeautifulSoup(html_doc, 'html.parser')

        # create/write the final article title and article text
        with open(txt_path, 'a', encoding="utf-8") as f:

            # setting a conditional if in case page is not found (404)
            if soup.title.string[: 14] == "Page not found":
                print("###### Page not found (404) ######\n")
                # skip the remaining code portion
                continue

            # first write the article title
            f.write(soup.h1.string)
            f.write('\n')

            # multiple conditional for multiple div classes, further get text paragraphs
            if soup.find('div', class_="td-post-content tagdiv-type") is not None:

                results = soup.find('div', class_="td-post-content tagdiv-type").find_all('p')

            elif (soup.find('div', class_="td-post-content tagdiv-type") is None) and \
                    (soup.find('div', class_="tdb-block-inner td-fix-index") is not None):

                # first get all the new div tags only
                results = soup.find_all('div', class_="tdb-block-inner td-fix-index")

                # made a copy
                copied = results.copy()
                results.clear()

                for item in copied:

                    # get all p tags
                    element = item.find_all('p')

                    if element is not None:
                        for sub in element:
                            results.append(sub)

            # if any other tag case then skip
            else:
                print("******** Skipped (html tag error occurred) *********\n")
                continue

            # iterate the list
            for item in results:
                # get the text of the tags
                f.write(item.get_text())
                f.write('\n')

        print("Successfully Scrapped\n")
