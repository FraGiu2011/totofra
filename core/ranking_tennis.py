import csv

class TennisRanking:
    def __init__(self):
        self.ranking = self._load_elo()

    def _load_elo(self):
        data = []
        try:
            with open("data/tennis_elo_ratings.csv", encoding="utf-8") as f:
                r = csv.DictReader(f)
                for row in r:
                    data.append({
                        "player": row["player"].lower(),
                        "elo": float(row["elo"])
                    })
        except:
            print("[WARNING] Impossibile caricare tennis_elo_ratings.csv")
        return data

    def get_ranking(self):
        return sorted(self.ranking, key=lambda x: x["elo"], reverse=True)
