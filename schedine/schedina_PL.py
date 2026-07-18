import os
import json
from core.team_normalizer import TeamNormalizer
from core.data_cleaner import DataCleaner
from core.modello_poisson import PoissonModel
from core.comparator import Comparator


def load_matchday_PL():
    """
    Carica il matchday Premier League dal file ufficiale.
    """
    path = os.path.join("output", "matchday.json")
    if not os.path.exists(path):
        raise FileNotFoundError("matchday.json non trovato in /output")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    matches = []
    for m in data.get("PL", []):
        matches.append({
            "home": m["home"],
            "away": m["away"],
            "odds": {
                "1": m["odds_1"],
                "X": m["odds_X"],
                "2": m["odds_2"]
            }
        })

    return matches


def generate_schedina_PL():

    print("[INFO] Generazione schedina Premier League…")

    # 1) Carica match
    matches = load_matchday_PL()

    # 2) Normalizzazione
    normalizer = TeamNormalizer()
    normalized = normalizer.normalize_all_matches(matches)

    # 3) Pulizia
    cleaner = DataCleaner()
    cleaned = cleaner.clean(normalized)

    # 4) Modello Poisson
    model = PoissonModel("PL")
    model.normalizer = normalizer
    predictions = model.predict(cleaned)

    # 5) Comparator (tipster mock + quote reali)
    comparator = Comparator()

    tipster_predictions = {}
    real_odds = {}

    for m in cleaned:
        key = f"{m['home']}-{m['away']}"
        tipster_predictions[key] = {
            "prob_1": 0.33,
            "prob_x": 0.33,
            "prob_2": 0.33
        }
        real_odds[key] = {
            "odds_1": m["odds"]["1"],
            "odds_X": m["odds"]["X"],
            "odds_2": m["odds"]["2"]
        }

    final = comparator.compare(predictions, tipster_predictions, real_odds)

    # 6) Genera schedina TXT
    lines = []
    lines.append("=== SCHEDINA PREMIER LEAGUE ===\n")

    for m in final:
        key = f"{m['home']}-{m['away']}"
        odds = real_odds[key]

        # Pick consigliato
        probs = {
            "1": m["prob_1"],
            "X": m["prob_x"],
            "2": m["prob_2"]
        }
        pick = max(probs, key=probs.get)

        lines.append(f"{m['home'].title()} - {m['away'].title()}")
        lines.append(f"Prob: 1={m['prob_1']:.3f}  X={m['prob_x']:.3f}  2={m['prob_2']:.3f}")
        lines.append(f"Quote: 1={odds['odds_1']}  X={odds['odds_X']}  2={odds['odds_2']}")
        lines.append(f"Pick: {pick}")
        lines.append("")

    # 7) Salvataggio
    output_path = os.path.join("output", "schedina_PL.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] Schedina Premier League generata: {output_path}")


if __name__ == "__main__":
    generate_schedina_PL()
