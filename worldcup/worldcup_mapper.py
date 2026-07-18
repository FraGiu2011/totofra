import pandas as pd
from unidecode import unidecode
from worldcup.worldcup_loader import load_worldcup_team_ids

# Mappa nomi football-data.org → nomi TotoFra
SPECIAL_MAP = {
    "united states": "usa",
    "usa": "usa",
    "u.s.a": "usa",

    "korea republic": "south_korea",
    "south korea": "south_korea",

    "saudi arabia": "saudi_arabia",
    "saudi_arabia": "saudi_arabia",

    "costa rica": "costa_rica",
    "côte d’ivoire": "ivory_coast",
    "cote d'ivoire": "ivory_coast",
}

def normalize_team_name(name):
    if not isinstance(name, str):
        return ""

    name = unidecode(name).lower().strip()
    name = " ".join(name.split())

    if name in SPECIAL_MAP:
        return SPECIAL_MAP[name]

    return name


TEAM_IDS = load_worldcup_team_ids()
TEAM_IDS["team_normalized"] = TEAM_IDS["team"].apply(normalize_team_name)

def get_team_id(team_name):
    norm = normalize_team_name(team_name)
    row = TEAM_IDS[TEAM_IDS["team_normalized"] == norm]
    if row.empty:
        raise ValueError(f"Team ID non trovato per: {team_name}")
    return int(row.iloc[0]["team_id"])

def get_team_name(team_id):
    row = TEAM_IDS[TEAM_IDS["team_id"] == team_id]
    if row.empty:
        raise ValueError(f"Nome squadra non trovato per ID: {team_id}")
    return row.iloc[0]["team"]

def map_team_names(df):
    if "team_home" in df.columns:
        df["team_home_normalized"] = df["team_home"].apply(normalize_team_name)
    if "team_away" in df.columns:
        df["team_away_normalized"] = df["team_away"].apply(normalize_team_name)
    return df
