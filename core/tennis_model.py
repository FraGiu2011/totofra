import math
import csv

class TennisModel:
    def __init__(self, surface="hard"):
        self.surface = surface.lower()
        self.elo = self._load_elo()
        self.surface_mod = self._load_surface_modifiers()

    # -----------------------------
    # CARICAMENTO ELO
    # -----------------------------
    def _load_elo(self):
        data = {}
        try:
            with open("data/tennis_elo_ratings.csv", encoding="utf-8") as f:
                r = csv.DictReader(f)
                for row in r:
                    name = row["player"].lower()
                    data[name] = float(row["elo"])
        except:
            print("[WARNING] Elo tennis non trovato, uso default 1500.")
        return data

    # -----------------------------
    # CARICAMENTO BONUS SUPERFICIE
    # -----------------------------
    def _load_surface_modifiers(self):
        data = {}
        try:
            with open("data/tennis_surface_modifiers.csv", encoding="utf-8") as f:
                r = csv.DictReader(f)
                for row in r:
                    name = row["player"].lower()
                    data[name] = {
                        "clay": float(row["clay"]),
                        "hard": float(row["hard"]),
                        "grass": float(row["grass"])
                    }
        except:
            print("[WARNING] Modificatori superficie non trovati, uso 1.00.")
        return data

    # -----------------------------
    # GET ELO + BONUS SUPERFICIE
    # -----------------------------
    def _get_elo(self, player):
        return self.elo.get(player, 1500)

    def _get_surface_bonus(self, player):
        if player not in self.surface_mod:
            return 1.00
        return self.surface_mod[player].get(self.surface, 1.00)

    # -----------------------------
    # PROBABILITÀ ELO
    # -----------------------------
    def _prob(self, elo1, elo2):
        return 1 / (1 + 10 ** ((elo2 - elo1) / 400))

    # -----------------------------
    # PREDIZIONE SINGOLO MATCH
    # -----------------------------
    def predict_match(self, match):
        p1 = match["player1"]
        p2 = match["player2"]

        elo1 = self._get_elo(p1)
        elo2 = self._get_elo(p2)

        bonus1 = self._get_surface_bonus(p1)
        bonus2 = self._get_surface_bonus(p2)

        # Elo modificato dalla superficie
        elo1_adj = elo1 * bonus1
        elo2_adj = elo2 * bonus2

        prob1 = self._prob(elo1_adj, elo2_adj)
        prob2 = 1 - prob1

        return {
            "player1": p1,
            "player2": p2,
            "elo1": elo1,
            "elo2": elo2,
            "elo1_adj": round(elo1_adj, 2),
            "elo2_adj": round(elo2_adj, 2),
            "surface": self.surface,
            "prob_1": round(prob1, 3),
            "prob_2": round(prob2, 3),
        }

    # -----------------------------
    # PREDIZIONE MULTIPLA
    # -----------------------------
    def predict(self, matches):
        return [self.predict_match(m) for m in matches]
        print("[DEBUG] Elo caricati:", len(self.elo))
