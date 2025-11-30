import pandas as pd


def get_top_k_players(
    df: pd.DataFrame,
    stat_col: str,
    k: int,
) -> pd.DataFrame:
    filtered_df = df.nlargest(k, stat_col)

    return filtered_df[["Player", stat_col]]
