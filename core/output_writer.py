# core/output_writer.py

import json
import os

class OutputWriter:
    def __init__(self):
        os.makedirs("output", exist_ok=True)

    def save_json(self, predictions, league_code):
        path = f"output/predictions_{league_code}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(predictions, f, indent=4, ensure_ascii=False)
        print(f"[OUTPUT] Salvato JSON: {path}")

    def save_schedina(self, predictions, league_code):
        """
        Salva schedina TXT compatibile con il nuovo formato:
        - usa prob_1, prob_x, prob_2
        - usa value_1, value_x, value_2
        - NON usa più p['poisson']
        """
        path = f"output/schedina_{league_code}.txt"

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"=== SCHEDINA {league_code} ===\n\n")

            for p in predictions:
                home = p["home"]
                away = p["away"]

                prob1 = round(p.get("prob_1", 0), 3)
                probx = round(p.get("prob_x", 0), 3)
                prob2 = round(p.get("prob_2", 0), 3)

                v1 = p.get("value_1")
                vx = p.get("value_x")
                v2 = p.get("value_2")

                f.write(f"{home} - {away}\n")
                f.write(f"  Prob: 1={prob1}  X={probx}  2={prob2}\n")
                f.write(f"  Value: 1={v1}  X={vx}  2={v2}\n")
                f.write("\n")

        print(f"[OUTPUT] Salvata schedina colorata: {path}")
