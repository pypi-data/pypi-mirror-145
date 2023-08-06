import pandas as pd
from bs4 import BeautifulSoup


def html_to_df(page_source):
    """

    :param page_source:
    """
    soup = BeautifulSoup(page_source, features="lxml")

    tot_val = soup.findAll("div", {"class": ["iImxPQ"]})[0]
    tot_val = tot_val.text.replace("SEK", "").replace(u"\xa0", "")
    tot_val = float(tot_val)

    # Table
    els = soup.findAll("div", {"role": "row"})
    header = els[0].findAll(text=True, recursive=True)
    header = [col.replace("\xa0", " ") for col in header]
    df = pd.DataFrame(columns=header)  # Header

    for el in els[1:-1]:
        row = el.findAll(text=True, recursive=True)[3:]
        row = [col.replace("\xa0", " ") for col in row]
        row = [col.replace("%", "") for col in row]
        row = [col.replace(",", ".") for col in row]
        df.loc[len(df)] = row

    for col in df.columns[2:]:
        try:
            # df[col] = df[col].str.replace("", "-")
            df[col] = df[col].str.replace("\xa0", "")
            df[col] = df[col].str.replace(" ", "")
            df[col] = df[col].astype(float)
        except Exception as e:
            print(e)

    return df, tot_val
