import pandas as pd
from worldcup.worldcup_loader import load_worldcup_results
from worldcup.worldcup_predictor import predict_match
from core.output_writer import OutputWriter

def generate_worldcup_ranking():
    df = load_worldcup_results()
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
            "lambda_away": pred["lambda_away"]
        })

    return pd.DataFrame(rows)

def run_worldcup_ranking():
    ranking = generate_worldcup_ranking()
    writer = OutputWriter()
    writer.save_json(ranking.to_dict(orient="records"), "worldcup_ranking")
    print("Ranking Mondiale simulato salvato.")
