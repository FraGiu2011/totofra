import json
from core.team_normalizer_tennis import TeamNormalizerTennis
from core.data_cleaner_tennis import DataCleanerTennis
from core.tennis_model import TennisModel
from core.comparator_tennis import ComparatorTennis
from core.ranking_tennis import TennisRanking
from main_tennis import build_real_odds

def load_mock():
    with open("tests/mock_odds_tennis.json", encoding="utf-8") as f:
        return json.load(f)

def test_main_tennis():
    print("=== TEST MAIN TENNIS (MOCK) ===")

    raw = load_mock()
    print("[DEBUG] Mock matches:", len(raw))

    # Simula parse_matches()
    matches = []
    for m in raw:
        outcomes = m["bookmakers"][0]["markets"][0]["outcomes"]
        matches.append({
            "player1": outcomes[0]["name"],
            "player2": outcomes[1]["name"],
            "odds": {
                "1": outcomes[0]["price"],
                "2": outcomes[1]["price"]
            }
        })

    print("[DEBUG] Matches parsed:", matches)

    # Normalizzazione
    normalizer = TeamNormalizerTennis()
    normalized = normalizer.normalize_all_matches(matches)
    print("[DEBUG] Normalized:", normalized)

    # Pulizia
    cleaner = DataCleanerTennis()
    cleaned = cleaner.clean(normalized)
    print("[DEBUG] Cleaned:", cleaned)

    # Modello Elo + superficie
    model = TennisModel(surface="hard")
    predictions = model.predict(cleaned)
    print("[DEBUG] Predictions:", predictions)

    # Quote reali
    real_odds = build_real_odds(matches)

    # Comparator
    comparator = ComparatorTennis()
    final = comparator.compare(predictions, {}, real_odds)
    print("[DEBUG] Final:", final)

    # Ranking Elo
    ranking = TennisRanking().get_ranking()
    print("[DEBUG] Ranking:", ranking[:5])

    print("=== TEST COMPLETATO ===")

if __name__ == "__main__":
    test_main_tennis()
