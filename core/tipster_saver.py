import csv
import os
from datetime import datetime

class TipsterSaver:
    """
    Salva i pronostici finali in CSV per archivio.
    """

    def save(self, predictions, folder="output"):
        os.makedirs(folder, exist_ok=True)

        filename = f"{folder}/pronostici_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "home", "away",
                "prob_1", "prob_x", "prob_2",
                "tipster_pick", "tipster_confidence",
                "totofra_score"
            ])

            for m in predictions:
                writer.writerow([
                    m["home"], m["away"],
                    m.get("prob_1", 0),
                    m.get("prob_x", 0),
                    m.get("prob_2", 0),
                    m.get("tipster_pick", "N/D"),
                    m.get("tipster_confidence", 0),
                    m.get("totofra_score", 0)
                ])

        print(f"[SALVATAGGIO] Pronostici salvati in {filename}")
        return filename
