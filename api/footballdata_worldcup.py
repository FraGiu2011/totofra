import os
import requests
import pandas as pd

BASE_URL = "https://api.football-data.org/v4"
COMPETITION_CODE = "WC"  # World Cup


def _get_headers():
    api_key = os.getenv("FOOTBALL_DATA_API_KEY")
    if not api_key:
        raise ValueError("FOOTBALL_DATA_API_KEY non impostata nelle variabili d'ambiente.")
    return {"X-Auth-Token": api_key}


def fetch_matches():
    url = f"{BASE_URL}/competitions/{COMPETITION_CODE}/matches"
    r = requests.get(url, headers=_get_headers())
    r.raise_for_status()
    return r.json()["matches"]


def fetch_teams():
    url = f"{BASE_URL}/competitions/{COMPETITION_CODE}/teams"
    r = requests.get(url, headers=_get_headers())
    r.raise_for_status()
    return r.json()["teams"]


def fetch_standings():
    url = f"{BASE_URL}/competitions/{COMPETITION_CODE}/standings"
    r = requests.get(url, headers=_get_headers())
    r.raise_for_status()
    return r.json()["standings"]


def build_worldcup_results_csv(path):
    matches = fetch_matches()
    rows = []

    for m in matches:
        if m["status"] != "FINISHED":
            continue

        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]
        gh = m["score"]["fullTime"]["home"]
        ga = m["score"]["fullTime"]["away"]
        date = m["utcDate"]

        rows.append({
            "home": home,
            "away": away,
            "goals_home": gh,
            "goals_away": ga,
            "match_date": date,
        })

    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)


def build_worldcup_team_ids_csv(path):
    teams = fetch_teams()
    rows = []

    for t in teams:
        rows.append({
            "team": t["name"],
            "id": t["id"],
        })

    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)


def build_worldcup_standings_csv(path):
    standings = fetch_standings()
    rows = []

    for group in standings:
        group_name = group["group"] or group["stage"]
        for t in group["table"]:
            rows.append({
                "group": group_name,
                "team": t["team"]["name"],
                "pts": t["points"],
                "gf": t["goalsFor"],
                "ga": t["goalsAgainst"],
                "gd": t["goalDifference"],
                "mp": t["playedGames"],
            })

    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
