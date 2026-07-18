import math
from core.team_stats_loader import TeamStatsLoader

class PoissonModel:

    def __init__(self, league="SA"):
        self.league = league
        self.stats_loader = TeamStatsLoader(league=self.league)

        # dizionari per i parametri
        self.attack = {}
        self.defense = {}

        self._build_model()

    def _build_model(self):
        """
        Costruisce i parametri del modello Poisson usando:
        - xG
        - tiri
        - corner
        """

        stats = self.stats_loader.stats

        for team, s in stats.items():

            # ATTACCO = media pesata tra xG e tiri
            attack_value = (
                s["xg_for"] * 0.6 +
                s["shots_for"] * 0.3 +
                s["corners_for"] * 0.1
            )

            # DIFESA = media pesata tra xG contro e tiri contro
            defense_value = (
                s["xg_against"] * 0.6 +
                s["shots_against"] * 0.3 +
                s["corners_against"] * 0.1
            )

            self.attack[team] = attack_value
            self.defense[team] = defense_value

    def _poisson(self, lam, k):
        return (lam ** k) * math.exp(-lam) / math.factorial(k)

    def predict_match(self, home, away):
        """
        Calcola le probabilità 1X2 usando:
        - attacco casa
        - difesa trasferta
        - attacco trasferta
        - difesa casa
        """

        home = home.lower()
        away = away.lower()

        if home not in self.attack or away not in self.attack:
            return None

        # intensità gol
        lambda_home = max(0.1, self.attack[home] - self.defense[away])
        lambda_away = max(0.1, self.attack[away] - self.defense[home])

        # probabilità 1X2
        p_home = 0
        p_draw = 0
        p_away = 0

        for h in range(0, 6):
            for a in range(0, 6):
                p = self._poisson(lambda_home, h) * self._poisson(lambda_away, a)

                if h > a:
                    p_home += p
                elif h == a:
                    p_draw += p
                else:
                    p_away += p

        return {
            "prob_1": p_home,
            "prob_x": p_draw,
            "prob_2": p_away
        }

    def predict(self, matches):
        results = []
        for m in matches:
            res = self.predict_match(m["home"], m["away"])
            if res:
                results.append({
                    "home": m["home"],
                    "away": m["away"],
                    **res
                })
        return results
