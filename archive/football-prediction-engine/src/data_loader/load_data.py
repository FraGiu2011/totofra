import pandas as pd
import logging
import yaml
from pathlib import Path

def load_data(config_path="config/config.yaml"):
    """
    Carica il dataset definito nel file di configurazione.
    Restituisce un DataFrame pandas.
    """

    # Carica configurazione
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    dataset_path = config["dataset"]["path"]
    dataset_path = Path(dataset_path)

    logging.info(f"Caricamento dataset da: {dataset_path}")

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset non trovato: {dataset_path}")

    df = pd.read_csv(dataset_path)

    logging.info(f"Dataset caricato con successo. Righe: {len(df)}")

    return df
