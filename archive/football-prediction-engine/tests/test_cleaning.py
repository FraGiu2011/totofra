import pandas as pd
from src.data_cleaning.clean_data import clean_data

def test_clean_data():
    df = pd.DataFrame({
        "HomeTeam": ["A", "B"],
        "AwayTeam": ["C", "D"],
        "FTHG": [1, 2],
        "FTAG": [0, 1]
    })

    clean = clean_data(df)

    assert len(clean) == 2
    assert all(col in clean.columns for col in ["HomeTeam", "AwayTeam", "FTHG", "FTAG"])
