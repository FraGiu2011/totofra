import pandas as pd
from worldcup.worldcup_quarterfinals import filter_quarterfinal_matches
from worldcup.worldcup_predictor import predict_match
from core.output_writer import OutputWriter

def generate_ranking_quarters():
    df = filter_quarterfinal_matches()
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

def run_ranking_quarters():
    df = generate_ranking_quarters()
    writer = OutputWriter()
    writer.save_json(df.to_dict(orient="records"), "worldcup_ranking_quarters")
    print("Ranking Quarti salvato.")
    return df
