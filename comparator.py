# core/comparator.py

class Comparator:
    """
    Confronta:
    - Probabilità Poisson
    - Quote reali Bet365
    - Tipster (online + offline)
    """

    def compare(self, predictions, tipsters, real_odds):
        final = []

        for p in predictions:
            key = f"{p['home']} - {p['away']}"

            # Quote reali Bet365
            odds = real_odds.get(key, {"1": None, "X": None, "2": None})

            # Value betting
            value_1 = self._value(p["prob_1"], odds["1"])
            value_x = self._value(p["prob_x"], odds["X"])
            value_2 = self._value(p["prob_2"], odds["2"])

            # Tipster
            tipster_votes = self._collect_tipsters(tipsters, key)

            final.append({
                "match": key,
                "home": p["home"],
                "away": p["away"],

                # Poisson
                "lambda_home": p["lambda_home"],
                "lambda_away": p["lambda_away"],
                "prob_1": p["prob_1"],
                "prob_x": p["prob_x"],
                "prob_2": p["prob_2"],

                # Quote reali
                "odds_1": odds["1"],
                "odds_x": odds["X"],
                "odds_2": odds["2"],

                # Value
                "value_1": value_1,
                "value_x": value_x,
                "value_2": value_2,

                # Tipster
                "tipsters": tipster_votes
            })

        return final

    def _value(self, prob, odd):
        """
        Value betting:
        value = prob * odd
        Se > 1 → valore positivo
        """
        if prob is None or odd is None:
            return None
        return round(prob * odd, 3)

    def _collect_tipsters(self, tipsters, match_key):
        """
        Raccoglie i pronostici dei tipster per il match.
        """
        votes = {}

        for name, t in tipsters.items():
            if match_key in t:
                votes[name] = t[match_key]

        return votes
