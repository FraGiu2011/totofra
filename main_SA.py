# main_SA.py

from core.odds_match_fetcher_SA import OddsMatchFetcherSA
from core.team_normalizer import TeamNormalizer
from core.data_cleaner import DataCleaner
from core.modello_poisson import PoissonModel
from core.comparator import Comparator
from core.output_writer import OutputWriter
from dashboard.dashboard_generator import generate_dashboard

def build_real_odds(matches):
    out = {}
    for m in matches:
        key = f"{m['home']} - {m['away']}"
        out[key] = m["odds"]
    return out

def main():
    print("=== TotoFra Serie A ===")

    fetcher = OddsMatchFetcherSA()
    raw = fetcher.get_matches()

    print("[DEBUG] Matches ricevuti da OddsAPI:", len(raw))
    for m in raw[:5]:
        print("[DEBUG] Esempio match:", m["home_team"], "-", m["away_team"])

    matches = fetcher.parse_matches(raw)

    # 🔒 BLOCCO DI SICUREZZA SERIE A
    if len(matches) == 0:
        print("[INFO] Nessun match di Serie A disponibile al momento. Quote non ancora pubblicate.")
        return

    normalizer = TeamNormalizer("SA")
    normalized = normalizer.normalize_all_matches(matches)


    cleaner = DataCleaner()
    cleaned = cleaner.clean(normalized)

    model = PoissonModel("SA", normalizer)
    predictions = model.predict(cleaned)

    real_odds = build_real_odds(matches)

    comparator = Comparator()
    final = comparator.compare(predictions, {}, real_odds)

    writer = OutputWriter()
    writer.save_json(final, "SA")
    writer.save_schedina(final, "SA")

    generate_dashboard(final, "SA")

    print("=== Fine Serie A ===")

if __name__ == "__main__":
    main()
