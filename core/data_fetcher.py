import csv
from core.team_stats_loader import TeamStatsLoader

class DataFetcher:
    def __init__(self, league="PL"):
        self.league = league.upper()
        self.stats_loader = TeamStatsLoader(league=self.league)

    def _load_csv(self, path):
        matches = []
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                matches.append({
                    "home": row["home"],
                    "away": row["away"],
                    "home_goals": int(row.get("home_goals", 0)),
                    "away_goals": int(row.get("away_goals", 0)),
                })
        return matches

    def fetch_matches(self, competition_id="PL", matchday=None):
        competition_id = competition_id.upper()

        if competition_id == "SA":
            path = "data/serie_a_results.csv"
        elif competition_id == "PL":
            path = "data/premier_league_results.csv"
        else:
            raise ValueError(f"Competizione non supportata: {competition_id}")

        matches = self._load_csv(path)

        for m in matches:
            home = m["home"]
            away = m["away"]
            m["home_stats"] = self.stats_loader.get_team_stats(home)
            m["away_stats"] = self.stats_loader.get_team_stats(away)

        return matches
