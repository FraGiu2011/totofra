# core/comparator.py

class Comparator:
    def __init__(self):
        pass

    def safe_value(self, prob, quota):
        """
        Calcola il value in modo sicuro:
        - Se quota è None → return None
        - Se prob è None → return None
        """
        if prob is None or quota is None:
            return None
        return round(prob * quota - 1, 3)

    def compare(self, model_predictions, tipster_predictions, real_odds):
        """
        Confronta Poisson + Tipster + Quote reali Bet365.
        Aggiunge value betting sicuro.
        """
        for m in model_predictions:

            home = m["home"]
            away = m["away"]
            key = f"{home} - {away}"

            # Quote reali Bet365
            odds = real_odds.get(key, {})

            q1 = odds.get("1")
            qx = odds.get("X")
            q2 = odds.get("2")

            # Probabilità Poisson
            p1 = m.get("prob_1")
            px = m.get("prob_x")
            p2 = m.get("prob_2")

            # Value betting sicuro
            m["value_1"] = self.safe_value(p1, q1)
            m["value_x"] = self.safe_value(px, qx)
            m["value_2"] = self.safe_value(p2, q2)

            # Tipster
            m["tipsters"] = {}

            for name, tips in tipster_predictions.items():
                pick = tips.get(key)
                m["tipsters"][name] = pick

        return model_predictions
