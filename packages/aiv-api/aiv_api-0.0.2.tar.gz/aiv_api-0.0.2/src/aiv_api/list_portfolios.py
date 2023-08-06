import pandas as pd

def list_portfolios(page_source):
    """ """
    df = pd.read_html(page_source)[0][:-1]
    portfolios = list(df["Depå"])

    df[df.columns[-1]] = df[df.columns[-1]].str.replace(",", ".")
    df[df.columns[-1]] = df[df.columns[-1]].str.replace(u"\xa0", "")
    df[df.columns[-1]] = df[df.columns[-1]].astype(float)

    tot_val = df[df.columns[-1]][:2].sum()

    return portfolios, tot_val

