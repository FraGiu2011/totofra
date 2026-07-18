import csv
from collections import defaultdict
import os

class PoissonStats:
    def __init__(self, csv_path="data/serie_a_results.csv"):
        self.csv_path = csv_path
        self.team_stats = defaultdict(lambda: {
            "gf_home": 0, "ga_home": 0, "n_home": 0,
            "gf_away": 0, "ga_away": 0, "n_away": 0
        })
        self.avg_goals_home = 0.0
        self.avg_goals_away = 0.0

    def load(self):
        if not os.path.exists(self.csv_path):
            print(f"[POISSON] Nessun file risultati trovato: {self.csv_path}")
            return

        total_home_goals = 0
        total_away_goals = 0
        total_matches = 0

        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                home = row["home"]
                away = row["away"]
                hg = int(row["home_goals"])
                ag = int(row["away_goals"])

                self.team_stats[home]["gf_home"] += hg
                self.team_stats[home]["ga_home"] += ag
                self.team_stats[home]["n_home"] += 1

                self.team_stats[away]["gf_away"] += ag
                self.team_stats[away]["ga_away"] += hg
                self.team_stats[away]["n_away"] += 1

                total_home_goals += hg
                total_away_goals += ag
                total_matches += 1

        if total_matches > 0:
            self.avg_goals_home = total_home_goals / total_matches
            self.avg_goals_away = total_away_goals / total_matches

        print(f"[POISSON] Caricate statistiche per {len(self.team_stats)} squadre")

    def get_team_profile(self, team_name):
        return self.team_stats.get(team_name, None)
