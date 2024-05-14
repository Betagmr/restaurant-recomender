import string
import unicodedata

import pandas as pd
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


def _find_confidence(text):
    frequent_terms = ["bar", "restaurante", "taberna", "cafe", "hamburguesa"]
    encontrados = [term for term in frequent_terms if term in text]

    return encontrados if encontrados else ["otros"]


def add_restaurant_types(df):
    new_df = df.copy()
    clean_text = (new_df["description"].fillna("") + " " + new_df["title"]).apply(_clean_text)
    restaurant_type = clean_text.apply(_find_confidence).apply(
        lambda x: "_".join([f.strip() for f in x])
    )

    new_df = pd.concat([new_df, new_df["direction"].str.get_dummies()], axis=1)
    new_df = pd.concat([new_df, restaurant_type.str.get_dummies(sep="_")], axis=1)

    return new_df.drop(columns=["direction"])


def add_extra_features(df):
    new_df = df.copy()

    # Separar las categorías y limpiar los espacios en blanco
    split_features = new_df["extra_features"].fillna("").str.split("·")
    join_features = split_features.apply(lambda x: "_".join([f.strip() for f in x]))

    # Convertir las características en variables ficticias (dummies)
    dummies = join_features.str.get_dummies(sep="_")

    # Agregar las variables ficticias al DataFrame original
    new_df = pd.concat([new_df, dummies], axis=1)

    # Eliminar la columna original "extra_features"
    return new_df.drop(["extra_features"], axis=1)
