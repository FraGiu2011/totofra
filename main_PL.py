# main_PL.py

from core.odds_match_fetcher_PL import OddsMatchFetcherPL
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
    print("=== TotoFra Premier League ===")

    fetcher = OddsMatchFetcherPL()
    raw = fetcher.get_matches()

    # DEBUG CORRETTO
    print("[DEBUG] Matches ricevuti da OddsAPI:", len(raw))
    for m in raw[:5]:
        print("[DEBUG] Esempio match:", m["home_team"], "-", m["away_team"])
    matches = fetcher.parse_matches(raw)

    # 🔒 BLOCCO DI SICUREZZA EPL
    if len(matches) == 0:
        print("[INFO] Nessun match EPL disponibile al momento. Quote non ancora pubblicate.")
        return


    normalizer = TeamNormalizer("PL")
    normalized = normalizer.normalize_all_matches(matches)

    cleaner = DataCleaner()
    cleaned = cleaner.clean(normalized)

    model = PoissonModel("PL", normalizer)
    predictions = model.predict(cleaned)

    real_odds = build_real_odds(matches)

    comparator = Comparator()
    final = comparator.compare(predictions, {}, real_odds)

    writer = OutputWriter()
    writer.save_json(final, "PL")
    writer.save_schedina(final, "PL")

    generate_dashboard(final, "PL")

    print("=== Fine EPL ===")

if __name__ == "__main__":
    main()
