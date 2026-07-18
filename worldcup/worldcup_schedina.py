import pandas as pd
from worldcup.worldcup_loader import load_worldcup_results
from worldcup.worldcup_predictor import predict_match
from api.odds_worldcup import WorldCupOdds

def generate_schedina():
    df = load_worldcup_results()
    odds_api = WorldCupOdds()
    schedina = []

    for _, row in df.iterrows():
        home = row["team_home"]
        away = row["team_away"]

        prediction = predict_match(home, away)
        odds = odds_api.get_odds(home, away) or {"1": 2.50, "X": 3.00, "2": 2.80}

        schedina.append({
            "home": home,
            "away": away,
            "prob_1": prediction["prob_home_win"],
            "prob_x": prediction["prob_draw"],
            "prob_2": prediction["prob_away_win"],
            "value_1": prediction["prob_home_win"] * odds["1"],
            "value_x": prediction["prob_draw"] * odds["X"],
            "value_2": prediction["prob_away_win"] * odds["2"],
        })

    return schedina

def run_worldcup_schedina():
    schedina = generate_schedina()
    print("Schedina Mondiale generata:", len(schedina))
