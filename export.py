# function to write the data to an Excel file
# in a pre-defined order & format

import pandas as pd
from decimal import Decimal


def export_excel(total_values):
    # first read the format structure from template output file
    df = pd.read_excel("Output Data Structure.xlsx")

    # get the column headers
    keys = list(df.keys())

    # all the rows / records in dataframe
    total_rows = df.values

    # for each row
    for i in range(len(total_rows)):

        # get url_id,
        # plus deal with float type numbers from pandas dataframe
        url_id = str(Decimal(str(df['URL_ID'][i])).normalize())

        # fix for scientific notations in url_id
        if 'E' in url_id:
            url_id = str(int(float(url_id)))

        # get row value from dict with 'file_name as key'
        row_value = total_values[url_id]

        # if row doesn't carry any data in case of Page Not Found error (404)
        if row_value is None:
            # skip rest code, write nothing to data list
            continue

        # otherwise for each column, we have to fit in
        # 13 values from  column index (2-14) of a row of size 15
        for j in range(2, len(total_rows[i])):
            # fit/replace values
            total_rows[i][j] = row_value[j - 2]

    # now create a new dataframe, with the created 2D list
    new = pd.DataFrame(total_rows, columns=keys)

    # export to a new Excel file
    new.to_excel(r"Output.xlsx", index=False)

    print("\nSuccessful Data Export\n")
