class ComparatorTennis:
    def compare(self, predictions, _, real_odds):
        final = []

        for p in predictions:
            # Normalizziamo la chiave per evitare mismatch
            key = f"{p['player1']} - {p['player2']}".lower()

            # Normalizziamo anche le chiavi delle quote
            normalized_real_odds = {k.lower(): v for k, v in real_odds.items()}

            odds = normalized_real_odds.get(key, {})

            if "1" not in odds or "2" not in odds:
                continue

            value1 = p["prob_1"] * odds["1"]
            value2 = p["prob_2"] * odds["2"]

            final.append({
                "match": key,
                "prob_1": round(p["prob_1"], 3),
                "prob_2": round(p["prob_2"], 3),
                "odds_1": odds["1"],
                "odds_2": odds["2"],
                "value_1": round(value1, 3),
                "value_2": round(value2, 3),
            })

        return final
