import pandas as pd
from worldcup.worldcup_phasefinals import (
    filter_matches, QUARTERS_TEAMS, SEMIFINALS_TEAMS, FINALS_TEAMS
)
from worldcup.worldcup_predictor import predict_match

def generate_ranking_phase(teams):
    df = filter_matches(teams)
    rows = []

    for _, row in df.iterrows():
        home = row["team_home"]
        away = row["team_away"]
        pred = predict_match(home, away)

        rows.append({
            "team_home": home,
            "team_away": away,
            "prob_home_win": pred["prob_home_win"],
            "prob_draw": pred["prob_draw"],
            "prob_away_win": pred["prob_away_win"],
            "lambda_home": pred["lambda_home"],
            "lambda_away": pred["lambda_away"],
        })

    return pd.DataFrame(rows)

def generate_ranking_quarters():
    return generate_ranking_phase(QUARTERS_TEAMS)

def generate_ranking_semifinals():
    return generate_ranking_phase(SEMIFINALS_TEAMS)

def generate_ranking_finals():
    return generate_ranking_phase(FINALS_TEAMS)
