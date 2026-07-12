# main_tennis.py
from core.ranking_tennis import TennisRanking
from core.odds_match_fetcher_tennis import OddsMatchFetcherTennis
from core.team_normalizer_tennis import TeamNormalizerTennis
from core.data_cleaner_tennis import DataCleanerTennis
from core.tennis_model import TennisModel
from core.comparator_tennis import ComparatorTennis
from core.output_writer import OutputWriter
from dashboard.dashboard_generator import generate_dashboard, generate_ranking_dashboard

def build_real_odds(matches):
    out = {}
    for m in matches:
        key = f"{m['player1']} - {m['player2']}"
        out[key] = m["odds"]
    return out

def main():
    print("=== TotoFra Tennis ===")

    fetcher = OddsMatchFetcherTennis()
    raw = fetcher.get_matches()

    print("[DEBUG] Matches ricevuti da OddsAPI:", len(raw))
    for m in raw[:5]:
        print("[DEBUG] Esempio match:", m["player1"], "-", m["player2"])

    matches = fetcher.parse_matches(raw)

    # 🔒 BLOCCO DI SICUREZZA TENNIS
    if len(matches) == 0:
        print("[INFO] Nessun match Tennis disponibile al momento. Quote non ancora pubblicate.")
        return

    normalizer = TeamNormalizerTennis()
    normalized = normalizer.normalize_all_matches(matches)

    cleaner = DataCleanerTennis()
    cleaned = cleaner.clean(normalized)

    # ⭐ MODELLO TENNIS CON SUPERFICIE
    model = TennisModel(surface="hard")  # "hard", "clay", "grass"
    predictions = model.predict(cleaned)

    real_odds = build_real_odds(matches)

    comparator = ComparatorTennis()
    final = comparator.compare(predictions, {}, real_odds)
    
    writer = OutputWriter()
    writer.save_json(final, "tennis")
    writer.save_schedina(final, "tennis")
    
    # ⭐ GENERA RANKING ELO TENNIS
    ranking = TennisRanking().get_ranking()
    writer.save_json(ranking, "tennis_ranking")
    writer.save_schedina(ranking, "tennis_ranking")

    # ⭐ DASHBOARD MATCH + DASHBOARD RANKING
    generate_dashboard(final, "tennis")
    generate_ranking_dashboard(ranking, "tennis")

    print("=== Fine Tennis ===")

if __name__ == "__main__":
    main()
