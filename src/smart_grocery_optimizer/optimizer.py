import pandas as pd
from .config import DISTANCE_WEIGHT, PRICE_WEIGHT, RATING_WEIGHT


def optimize_shops(results_df):
    def normalize(series):
        max_val = series.max()
        if max_val == 0:
            return series
        return series / max_val

    results_df["price_score"] = 1 - normalize(results_df["total_cost"])
    results_df["distance_score"] = 1 - normalize(results_df["distance"])
    results_df["rating_score"] = results_df["rating"] / 5

    results_df["final_score"] = (
        PRICE_WEIGHT * results_df["price_score"]
        + DISTANCE_WEIGHT * results_df["distance_score"]
        + RATING_WEIGHT * results_df["rating_score"]
    )

    return results_df.sort_values(by="final_score", ascending=False)