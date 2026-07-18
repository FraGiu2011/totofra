import pandas as pd
from src.models.poisson_model import train_poisson_model

def test_model():
    df = pd.DataFrame({
        "HomeTeam": ["A", "B"],
        "AwayTeam": ["C", "D"],
        "FTHG": [1, 2],
        "FTAG": [0, 1]
    })

    model = train_poisson_model(df)

    lambda_home, lambda_away = model.predict("A", "C")

    assert lambda_home >= 0
    assert lambda_away >= 0
