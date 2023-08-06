import pandas as pd
from aiv_api.convert_df import convert_df

def html_to_df(page_source):
    """Convert the html with the table to the correct dataframe

    """
    tables = pd.read_html(page_source, decimal=",", thousands=".")

    df = convert_df(tables[2][:-1])  # Aktier

    try:
        df = df.append(convert_df(tables[10][:-1]), ignore_index=True)  # Fonder
    except Exception as e:
        print(e)

    #print("")
    #print(df.head())
    #print(df.dtypes)

    return df

