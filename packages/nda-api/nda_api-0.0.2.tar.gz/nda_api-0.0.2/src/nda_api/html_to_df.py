import pandas as pd
import numpy as np

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

def html_to_df(page_source):
    """
    """
    tables = pd.read_html(page_source, flavor="bs4",
                          decimal=",", thousands=".")


    cols = ["Namn", "Kurs", "Anskaffningskurs", "Värdeförändring", "Antal", "Värde"]
    df = tables[0][:-1]
    df.columns = df.columns.droplevel()
    df = df[cols]

    df1 = tables[1]
    df1.columns = df1.columns.droplevel()
    df1 = df1[cols]

    df = pd.concat([df, df1], ignore_index=True)

    df["Kurs"] = df["Kurs"].astype(float)
    df["Anskaffningskurs"] = df["Anskaffningskurs"].str.replace("-", "NaN")
    for col in df.columns[2:]:
        try:
            df[col] = df[col].str.replace(u"\xa0SEK", "")
            df[col] = df[col].str.replace(u"\xa0st", "")
            df[col] = df[col].str.replace(",", ".")
            df[col] = df[col].str.replace(u"\xa0", "")
            df[col] = df[col].apply(pd.to_numeric, errors='coerce')
        except Exception as e:
            print(e)

        try:
            df[col] = df[col].astype(float)
        except Exception as e:
            print(e)

    df = df[df['Namn'].notna()]

    return df
