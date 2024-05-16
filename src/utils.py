from pathlib import Path

import pandas as pd
from pandasql import sqldf


def load_all_restaurants(data_path):
    all_data_paths = list(Path(data_path).glob("*.csv"))

    df_raw = pd.DataFrame()
    for street_path in all_data_paths:
        new_df = pd.read_csv(street_path)
        df_raw = pd.concat([df_raw, new_df])

    df_raw["unique_id"] = [f"{row['title']} | {row['street']}" for _, row in df_raw.iterrows()]
    return df_raw.drop_duplicates(subset=["unique_id"])


def load_parsed_queries(data_path, df_data: pd.DataFrame):
    if df_data is None:
        raise ValueError("No data provided to load_parsed_queries")

    df_queries = pd.read_csv(data_path)
    query_dict = {}
    for _, row in df_queries.iterrows():
        query = f"SELECT * FROM df_data {row['sql_query']}, muchas_resenas DESC, medio_resenas DESC, pocas_resenas DESC"
        entry = row["search_query"]
        query_dict[entry] = sqldf(query, locals())

    return query_dict
