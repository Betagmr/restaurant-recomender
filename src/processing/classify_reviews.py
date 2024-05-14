import pandas as pd


def _classify_reviews(n_reviews):
    if n_reviews < 100:
        return "pocas_resenas"
    elif 100 <= n_reviews <= 800:
        return "medio_resenas"
    else:
        return "muchas_resenas"


def add_class_reviews(df):
    review_column = df["n_reviews"].apply(_classify_reviews)
    dummies_reviews = review_column.str.get_dummies()

    return pd.concat([df, dummies_reviews], axis=1)
