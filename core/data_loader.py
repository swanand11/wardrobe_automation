import pandas as pd
import ast
from pathlib import Path


class WardrobeDataLoader:
    def __init__(self):
        self.csv_path = Path("data/wadrobe.csv")
        self.df = None

    def load(self) -> pd.DataFrame:
        df = pd.read_csv(self.csv_path)

        df = self._parse_vibes_column(df)
        df = self._create_color_vectors(df)
        df = self._clean_types(df)

        self.df = df
        return df

    def _parse_vibes(self, x):
        if not isinstance(x, str):
            return []

        try:
            return ast.literal_eval(x)
        except Exception:
            x = x.replace("[", "").replace("]", "")
            return [v.strip() for v in x.split(",") if v.strip()]

    def _parse_vibes_column(self, df: pd.DataFrame) -> pd.DataFrame:
        if "vibe" in df.columns:
            df["vibe"] = df["vibe"].apply(self._parse_vibes)
        return df

    def _create_color_vectors(self, df: pd.DataFrame) -> pd.DataFrame:
        if {"reds", "green", "blue"}.issubset(df.columns):

            df["color_vec"] = df.apply(
                lambda row: [
                    row["reds"],
                    row["green"],
                    row["blue"]
                ],
                axis=1
            )

        return df

    def _clean_types(self, df: pd.DataFrame) -> pd.DataFrame:
        if "type" in df.columns:
            df["type"] = df["type"].str.lower().str.strip()

        return df

    def get_items(self):
        return self.df.to_dict("records")

    def get_items_by_type(self, item_type: str):
        return self.df[self.df["type"] == item_type].to_dict("records")