import csv
from collections import defaultdict
import os

class FormCalculator:
    def __init__(self, csv_path="data/serie_a_results.csv"):
        self.csv_path = csv_path
        self.form = defaultdict(list)

    def load(self):
        if not os.path.exists(self.csv_path):
            print("[FORMA] Nessun file risultati trovato.")
            return

        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                home = row["home"]
                away = row["away"]
                hg = int(row["home_goals"])
                ag = int(row["away_goals"])

                # Risultato casa
                if hg > ag:
                    self.form[home].append(3)
                    self.form[away].append(0)
                elif hg < ag:
                    self.form[home].append(0)
                    self.form[away].append(3)
                else:
                    self.form[home].append(1)
                    self.form[away].append(1)

    def get_form_score(self, team):
        if team not in self.form or len(self.form[team]) == 0:
            return 50  # neutro

        last5 = self.form[team][-5:]
        score = sum(last5) / (5 * 3) * 100
        return round(score)
