import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def load_worldcup_results():
    path = os.path.join(DATA_DIR, "worldcup_results.csv")
    df = pd.read_csv(path)
    df = df.rename(columns={
        "home": "team_home",
        "away": "team_away",
        "match_date": "date"
    })
    df["match_id"] = range(1, len(df) + 1)
    return df

def load_worldcup_team_ids():
    path = os.path.join(DATA_DIR, "worldcup_team_ids.csv")
    df = pd.read_csv(path)
    df = df.rename(columns={"id": "team_id"})
    return df

def load_worldcup_standings():
    path = os.path.join(DATA_DIR, "worldcup_standings.csv")
    return pd.read_csv(path)

def load_worldcup_team_stats():
    path = os.path.join(DATA_DIR, "worldcup_team_stats.csv")
    return pd.read_csv(path)

def load_worldcup_team_stats_extended():
    path = os.path.join(DATA_DIR, "worldcup_team_stats_extended.csv")
    return pd.read_csv(path)

def load_all_worldcup_data():
    return {
        "results": load_worldcup_results(),
        "team_ids": load_worldcup_team_ids(),
        "standings": load_worldcup_standings(),
        "team_stats": load_worldcup_team_stats(),
        "team_stats_extended": load_worldcup_team_stats_extended(),
    }
