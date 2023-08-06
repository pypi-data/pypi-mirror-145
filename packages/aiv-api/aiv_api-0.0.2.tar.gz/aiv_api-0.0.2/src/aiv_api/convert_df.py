import pandas as pd
import numpy as np

def convert_df(df):
    columns = df.columns
    df_new = df.rename({columns[0]: "Värdepapper",
                        columns[1]: "Antal",
                        columns[2]: "Senast",
                        columns[3]: "1d",
                        columns[4]: "1d_",
                        columns[5]: "GAV",
                        columns[6]: "Inköp",
                        columns[7]: "Värde",
                        columns[8]: "Utv.",
                        columns[9]: "Avkastn.",
                        }, axis='columns')

    df_new = df_new.drop(["1d", "1d_", "Utv."], axis=1)
    df_new["Värdepapper"] = df_new["Värdepapper"].str.replace("Köp/sälj", "")

    df_new["Senast"] = df_new["Senast"].astype(str).str.replace(u"\xa0", "")
    df_new["Senast"] = df_new["Senast"].str.split().str[-1]
    df_new["Senast"] = df_new["Senast"].str.replace(",", ".")
    df_new["Värde"] = df_new["Värde"].astype(str).str.replace(u"\xa0", "")
    df_new["Värde"] = df_new["Värde"].str.replace(",", ".")
    df_new["Inköp"] = df_new["Inköp"].astype(str).str.replace(u"\xa0", "")
    df_new["Avkastn."] = df_new["Avkastn."].astype(str).str.replace(u"\xa0", "")
    df_new["GAV"] = df_new["GAV"].astype(str).str.replace(u"\xa0", "")
    df_new["GAV"] = df_new["GAV"].str.replace(",", ".")
    df_new["Senast"] = df_new["Senast"].astype(str).replace("\U00002013", "-")
    df_new["Värde"] = df_new["Värde"].astype(str).replace("\U00002013", "-")
    df_new["Avkastn."] = df_new["Avkastn."].astype(str).replace("\U00002013", "-")
    df_new["Avkastn."] = df_new["Avkastn."].str.replace(",", ".")

    df_new = df_new.replace('-', np.NaN)
    for column in df_new.columns[1:]:
        try:
            df_new[column] = df_new[column].astype(float)
        except Exception as e:
            print(e, column)
            print(df_new.loc[df_new[column] == "-"])

    return df_new
