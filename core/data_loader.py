import pandas as pd
import ast
from pathlib import Path


class WardrobeDataLoader:
    def __init__(self):
        self.csv_path = Path("data/wadrobe.csv")
        self.raw_df = None
        self.processed_df = None

    def load(self) -> pd.DataFrame:
        raw_df = pd.read_csv(self.csv_path, quotechar='"', skipinitialspace=True)
        self.raw_df = raw_df.copy()
        df = raw_df.copy()

        df = self._parse_vibes_column(df)
        df = self._create_color_vectors(df)
        df = self._create_watch_vectors(df)
        df = self._clean_types(df)
        df["formality"] = pd.to_numeric(df["formality"], errors="coerce")

        self.processed_df = df
        return df

    def get_items(self):
        df = self.processed_df.copy()
        records = df.to_dict("records")

        def clean(obj):
            if isinstance(obj, float) and pd.isna(obj):
                return None
            if isinstance(obj, list):
                return [clean(x) for x in obj]
            if isinstance(obj, dict):
                return {k: clean(v) for k, v in obj.items()}
            return obj

        records = [clean(r) for r in records]
        records = sorted(records, key=lambda x: (x["type"], x["item_name"]))
        return records

    def get_items_by_type(self, item_type):
        all_items = self.get_items()
        return [i for i in all_items if i["type"] == item_type]

    def _parse_vibes(self, x):
        if not isinstance(x, str):
            return []
        try:
            return ast.literal_eval(x)
        except Exception:
            x = x.replace("[", "").replace("]", "")
            return [v.strip().strip("'\"") for v in x.split(",") if v.strip()]

    def _parse_vibes_column(self, df):
        if "vibe" in df.columns:
            df["vibe"] = df["vibe"].apply(self._parse_vibes)
        return df

    def _create_color_vectors(self, df):
        if {"reds", "green", "blue"}.issubset(df.columns):
            df["color_vec"] = df.apply(
                lambda row: [row["reds"], row["green"], row["blue"]], axis=1
            )
        return df

    def _create_watch_vectors(self, df):
        def strap_vec(row):
            if row["type"] == "watch" and pd.notna(row.get("strap_reds")):
                return [row["strap_reds"], row["strap_green"], row["strap_blue"]]
            return None

        def dial_vec(row):
            if row["type"] == "watch" and pd.notna(row.get("dial_reds")):
                return [row["dial_reds"], row["dial_green"], row["dial_blue"]]
            return None

        df["strap_color_vec"] = df.apply(strap_vec, axis=1)
        df["dial_color_vec"] = df.apply(dial_vec, axis=1)
        return df

    def _clean_types(self, df):
        if "type" in df.columns:
            df["type"] = df["type"].str.lower().str.strip()
        return df