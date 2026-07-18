import pandas as pd
import logging

REQUIRED_COLUMNS = ["HomeTeam", "AwayTeam", "FTHG", "FTAG"]

def clean_data(df):
    """
    Pulisce e valida il dataset delle partite.
    - Controlla che le colonne richieste esistano
    - Converte i goal in interi
    - Rimuove righe con valori mancanti
    """

    logging.info("Inizio pulizia dataset...")

    # Controllo colonne richieste
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Colonne mancanti nel dataset: {missing}")

    # Conversione tipi
    df["FTHG"] = pd.to_numeric(df["FTHG"], errors="coerce")
    df["FTAG"] = pd.to_numeric(df["FTAG"], errors="coerce")

    # Rimozione righe con valori mancanti
    before = len(df)
    df = df.dropna(subset=REQUIRED_COLUMNS)
    after = len(df)

    logging.info(f"Righe rimosse per valori mancanti: {before - after}")

    # Reset index
    df = df.reset_index(drop=True)

    logging.info("Pulizia completata.")

    return df
