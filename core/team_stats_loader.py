import os
import csv

class TeamStatsLoader:

    def __init__(self, league="SA"):
        self.league = league
        self.file_map = {
            "SA": "serie_a_team_stats.csv",
            "PL": "premier_league_team_stats.csv",
            "worldcup": "worldcup_team_stats_extended.csv"
        }
        self.stats = self._load_stats()

    def _load_stats(self):
        filename = self.file_map.get(self.league)
        if not filename:
            raise ValueError(f"Lega non supportata: {self.league}")

        path = os.path.join("data", filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"File stats non trovato: {path}")

        stats = {}

        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                team = row["team"].strip().lower()

                # NUOVO FORMATO COMPATIBILE
                stats[team] = {
                    "corners_for": float(row["corners_for"]),
                    "corners_against": float(row["corners_against"]),
                    "xg_for": float(row["xg_for"]),
                    "xg_against": float(row["xg_against"]),
                    "shots_for": float(row["shots_for"]),
                    "shots_against": float(row["shots_against"]),
                }

        return stats

    def get_team_stats(self, team):
        team = team.lower().strip()
        return self.stats.get(team, None)
