from pathlib import Path

import pandas as pd


def load_all_restaurants():
    data_path = Path() / "data" / "raw"
    all_data_paths = list(data_path.glob("*.csv"))

    df = pd.DataFrame()
    for street_path in all_data_paths:
        new_df = pd.read_csv(street_path)
        df = pd.concat([df, new_df])

    df["unique_id"] = [f"{row['title']} | {row['street']}" for _, row in df.iterrows()]
    return df.drop_duplicates(subset=["unique_id"])