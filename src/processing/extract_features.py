import string
import unicodedata

import pandas as pd
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize


def _clean_text(texto):
    texto = texto.lower()
    tokens = word_tokenize(texto, language="spanish")
    tabla = str.maketrans("", "", string.punctuation)
    tokens = [palabra.translate(tabla) for palabra in tokens]
    tokens = [
        unicodedata.normalize("NFKD", palabra).encode("ASCII", "ignore").decode("utf-8")
        for palabra in tokens
    ]

    return " ".join(tokens)


def find_confidence(text):
    frequent_terms = ["bar", "restaurante", "taberna", "cafe", "hamburguesa"]
    encontrados = [term for term in frequent_terms if term in text]

    return encontrados if encontrados else ["otros"]


def tipo_establecimiento_direccion(df):
    clean_text = (df["description"].fillna("") + " " + df["title"]).apply(_clean_text)
    restaurant_type = clean_text.apply(find_confidence).apply(
        lambda x: "_".join([f.strip() for f in x])
    )

    new_df = pd.concat([df, df["direction"].str.get_dummies()], axis=1)
    new_df = pd.concat([new_df, restaurant_type.str.get_dummies(sep="_")], axis=1)

    return new_df.drop(columns=["direction"])
