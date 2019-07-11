import math


import pandas as pd
import numpy as np


def get_woe_iv(x, y):
    """compute variable of x for y woe and iv value. y is the response.
    return woes, ivs
    """
    df = pd.DataFrame(data={"x": x, "y": y})
    count = df.groupby(["x", "y"]).size().sort_index()
    index1 = count.index.levels[0]
    zero_total = sum(count.loc(axis=0)[:, [0]])
    one_total = sum(count.loc(axis=0)[:, [1]])
    woes = {}
    ivs = {}
    for i in index1:
        zero = count.loc[i, 0]
        try:
            one = count.loc[i, 1]
        except:
            one = 1
        woe = math.log((one / one_total) / (zero / zero_total))
        woes[i] = woe
        iv = (one / one_total - zero / zero_total) * woe
        ivs[i] = iv
    return woes, ivs


def woe_iv(df, y):
    """compute df variable iv value. y is the response variable,
    return dict type."""
    d = df.drop(columns=[y])
    y = df.loc[:, y]
    ivs_dict = {}
    for c in d.columns:
        x = df.loc[:, c]
        woes, ivs = get_woe_iv(x, y)
        ivs_dict[c] = sum([iv for iv in ivs.values()])
    ivs_dict = pd.Series(ivs_dict).sort_values()
    return ivs_dict


def woe_change(df, y):
    """exchange woe. y is the response, return data frame exchanged."""
    d = df.drop(columns=[y])
    dy = df.loc[:, y]
    for c in d.columns:
        woes, ivs = get_woe_iv(d.loc[:, c], dy)
        d[c] = d[c].map(woes)
    d[y] = dy
    return d


def score_table(df, y, coes, B):
    """compute every variable bin score."""
    d = df.drop(columns=[y])
    y = df.loc[:, y]
    results = {}
    for c in d.columns:
        x = d.loc[:, c]
        woes, ivs = get_woe_iv(x, y)
        results[c] = pd.Series(woes) * coes[c] * B
    return results


def compute_score(df, st, basescore):
    """st is the score table, df is the computed data frame.
    return df with score columns"""
    d = pd.DataFrame()
    for c in st.keys():
        d[c] = df.loc[:, c].map(st[c])
    df["score"] = np.round(basescore + np.sum(d, axis=1))
    return df
