import logging
import pandas as pd

# IMPORTA IL MODELLO POISSON
from src.models.poisson_model import poisson_model

def predict_matches(df):
    """
    Calcola le previsioni e le stampa nel terminale.
    """
    predictions = []

    for _, row in df.iterrows():
        home = row["HomeTeam"]
        away = row["AwayTeam"]

        # Calcolo dei gol attesi
        home_goals = poisson_model.predict_home(home, away)
        away_goals = poisson_model.predict_away(home, away)

        # Risultato previsto
        if home_goals > away_goals:
            result = "1"
        elif away_goals > home_goals:
            result = "2"
        else:
            result = "X"

        predictions.append({
            "HomeTeam": home,
            "AwayTeam": away,
            "HomeGoals": home_goals,
            "AwayGoals": away_goals,
            "Prediction": result
        })

        # 🔥 STAMPA NEL TERMINALE
        print(f"[PRED] {home} - {away} → {home_goals:.2f} : {away_goals:.2f} → {result}")

    return pd.DataFrame(predictions)
