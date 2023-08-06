import pandas as pd


def json_response_to_df(data: dict) -> dict:
    dfs = {}
    for key, val in data.items():
        dfs[key] = pd.json_normalize(val)

    return dfs