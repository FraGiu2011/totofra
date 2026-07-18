import logging

from src.data_loader.load_data import load_data
from src.data_cleaning.clean_data import clean_data
from src.models.poisson_model import train_poisson_model
from src.predictors.predict_matches import predict_matches
from src.tipsters.compare_tipsters import compare_with_tipsters
from src.exporters.export_results import export_results


def run_pipeline():
    """
    Esegue l'intera pipeline end-to-end:
    - Caricamento dati
    - Pulizia
    - Addestramento modello
    - Previsioni
    - Confronto tipster
    - Esportazione risultati
    """

    logging.info("=== Avvio pipeline previsioni calcio ===")

    df = load_data()
    df_clean = clean_data(df)
    model = train_poisson_model(df_clean)
    preds = predict_matches(model, df_clean)
    comp = compare_with_tipsters(preds)
    output_path = export_results(comp)

    logging.info(f"Pipeline completata. Risultati salvati in: {output_path}")

    return output_path
import schedule
import time
import yaml
import logging
from datetime import datetime

def start_scheduler(config_path="config/config.yaml"):
    """
    Avvia lo scheduler giornaliero.
    Se l'orario è già passato oggi, esegue subito la pipeline.
    """

    print("[Scheduler] Caricamento configurazione...")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    run_time = config["scheduler"]["run_time"]

    print(f"[Scheduler] Avviato. La pipeline girerà ogni giorno alle {run_time}")
    logging.info(f"Scheduler avviato. La pipeline girerà ogni giorno alle {run_time}")

    # --- CONTROLLO AUTOMATICO ---
    now = datetime.now().strftime("%H:%M")

    if now > run_time:
        print(f"[Scheduler] L'orario {run_time} è già passato oggi ({now}).")
        print("[Scheduler] Eseguo SUBITO la pipeline...")
        logging.info("Orario già passato: esecuzione immediata della pipeline.")
        run_pipeline()
        print("[Scheduler] Pipeline eseguita. Prossima esecuzione domani.")
    else:
        print(f"[Scheduler] L'orario {run_time} non è ancora passato. Attendo normalmente.")

    # --- PROGRAMMAZIONE GIORNALIERA ---
    schedule.every().day.at(run_time).do(run_pipeline)

    # --- LOOP ---
    while True:
        print("[Scheduler] In attesa dell’orario programmato...")
        schedule.run_pending()
        time.sleep(10)
