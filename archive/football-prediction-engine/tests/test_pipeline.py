import pandas as pd
from pathlib import Path   # <--- IMPORT AGGIUNTO QUI

from src.models.poisson_model import train_poisson_model
from src.predictors.predict_matches import predict_matches
from src.tipsters.compare_tipsters import compare_with_tipsters
from src.exporters.export_results import export_results


def test_pipeline():
    df = pd.DataFrame({
        "HomeTeam": ["A", "B"],
        "AwayTeam": ["C", "D"],
        "FTHG": [1, 2],
        "FTAG": [0, 1]
    })

    model = train_poisson_model(df)
    preds = predict_matches(model, df)

    assert len(preds) == 2
    assert "lambda_home" in preds.columns
    assert "lambda_away" in preds.columns
    assert preds["lambda_home"].iloc[0] >= 0


def test_tipster_comparison():
    df = pd.DataFrame({
        "HomeTeam": ["A"],
        "AwayTeam": ["B"],
        "lambda_home": [1.2],
        "lambda_away": [0.8]
    })

    comp = compare_with_tipsters(df)

    assert "tipster_prediction" in comp.columns
    assert "agreement" in comp.columns
    assert comp["agreement"].iloc[0] in [True, False]


def test_export_results():
    df = pd.DataFrame({
        "HomeTeam": ["A"],
        "AwayTeam": ["B"],
        "lambda_home": [1.2],
        "lambda_away": [0.8],
        "tipster_prediction": ["Over 1.5"],
        "agreement": [True]
    })

    path = export_results(df, "data/predictions/test_output.csv")

    assert Path(path).exists()
from src.scheduler.run_pipeline import run_pipeline

def test_full_pipeline_runs():
    path = run_pipeline()
    assert Path(path).exists()
