import logging
import pandas as pd

def compare_with_tipsters(predictions):
    """
    Confronta le previsioni del modello con quelle dei tipster.
    Versione base: aggiunge un pronostico fittizio del tipster.
    """

    logging.info("Confronto previsioni modello vs tipster...")

    df = predictions.copy()

    # Placeholder: tipster dice sempre "Over 1.5"
    df["tipster_prediction"] = "Over 1.5"

    # Confronto semplice: se lambda_home + lambda_away > 1.5 → modello concorda
    df["model_prediction"] = df["lambda_home"] + df["lambda_away"]
    df["agreement"] = df["model_prediction"] > 1.5

    logging.info("Confronto completato.")

    return df
