import re

import pandas as pd


# Función para asignar la categoría.
def _categorize_price(price_range):
    # Verificar si el valor es un string
    if not isinstance(price_range, str):
        return "precio_medio"

    # Dividir el rango de precios y obtener el último fragmento
    last_fragment = price_range.split("-")[-1]

    # Buscar números en el último fragmento
    numbers = re.findall(r"\d+", last_fragment)

    # Verificar si hay números encontrados
    if not numbers:
        return "precio_medio"

    # Obtener el precio máximo del rango
    price_max = int(numbers[0])

    # Asignar categoría
    if price_max <= 10:
        return "precio_barato"
    elif price_max <= 20:
        return "precio_medio"
    else:
        return "precio_caro"


def add_price_range(df):
    new_df = df.copy()

    new_df["price_range"] = new_df["price_range"].replace(
        {"Más de 100€": "+100€", "€": "10-40€", "€€": "40-80€", "€€€": "+100€"}
    )
    new_df["price_range"] = new_df["price_range"].apply(_categorize_price)
    dummies_price_range = pd.get_dummies(new_df["price_range"], dtype=int)

    return pd.concat([new_df, dummies_price_range], axis=1)
