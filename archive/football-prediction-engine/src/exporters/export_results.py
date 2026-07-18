import logging
import pandas as pd
from pathlib import Path

def export_results(results, path="data/predictions/output.csv"):
    """
    Esporta i risultati finali in un file CSV.
    Crea la cartella se non esiste.
    """

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results.to_csv(output_path, index=False)

    logging.info(f"Risultati esportati in: {output_path}")

    return str(output_path)
