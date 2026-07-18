import pandas as pd
from worldcup.worldcup_phasefinals import (
    filter_matches, QUARTERS_TEAMS, SEMIFINALS_TEAMS, FINALS_TEAMS
)
from worldcup.worldcup_predictor import predict_match
from api.odds_worldcup import WorldCupOdds

def generate_schedina_phase(teams):
    df = filter_matches(teams)
    odds_api = WorldCupOdds()
    schedina = []

    for _, row in df.iterrows():
        home = row["team_home"]
        away = row["team_away"]

        pred = predict_match(home, away)
        odds = odds_api.get_odds(home, away) or {"1": 2.50, "X": 3.00, "2": 2.80}

        schedina.append({
            "home": home,
            "away": away,
            "prob_1": pred["prob_home_win"],
            "prob_x": pred["prob_draw"],
            "prob_2": pred["prob_away_win"],
            "value_1": pred["prob_home_win"] * odds["1"],
            "value_x": pred["prob_draw"] * odds["X"],
            "value_2": pred["prob_away_win"] * odds["2"],
        })

    return pd.DataFrame(schedina)

def generate_schedina_quarters():
    return generate_schedina_phase(QUARTERS_TEAMS)

def generate_schedina_semifinals():
    return generate_schedina_phase(SEMIFINALS_TEAMS)

def generate_schedina_finals():
    return generate_schedina_phase(FINALS_TEAMS)
