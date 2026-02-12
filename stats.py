import pandas as pd

def calculate_stats(df):
    if df.empty:
        return None

    stats = {}
    stats["PPG"] = df["PTS"].mean()
    stats["RPG"] = df["TOT"].mean()
    stats["APG"] = df["AST"].mean()

    return stats
