import json
from core.value_calculator import (
    OutcomeProbabilities,
    OutcomeOdds,
    calculate_value_1x2,
    as_dict as value_to_dict
)

from api.odds_api import get_odds_for_match_SA
from core.probability_calculator import calculate_probabilities_1x2
from core.data_loader_SA import load_matches_SA


def generate_schedina_SA():
    print("\n=== SCHEDINA SERIE A (con VALUE) ===\n")

    # 1) Carichiamo i match
    matches = load_matches_SA()

    # Debug: se non ci sono match, lo diciamo chiaramente
    if not matches:
        print("⚠️ Nessun match trovato da data_loader_SA!")
        print("   Controlla la fonte OpenLigaDB o la connessione.")
        input("\nPremi INVIO per tornare al menu…")
        return

    # 2) Ciclo sui match
    for match in matches:
        home = match["home"]
        away = match["away"]

        print(f"\n📌 Match: {home} vs {away}")

        # -------------------------
        # 1) Quote da OddsAPI
        # -------------------------
        odds = get_odds_for_match_SA(home, away)

        if odds is None:
            print("  ⚠️  Quote non disponibili.")
            continue

        print(f"  Quote: 1={odds['1']}  X={odds['X']}  2={odds['2']}")

        # -------------------------
        # 2) Probabilità 1X2 dal modello TotoFra
        # -------------------------
        prob = calculate_probabilities_1x2(home, away)

        print(f"  Probabilità: P1={prob['P1']:.3f}  PX={prob['PX']:.3f}  P2={prob['P2']:.3f}")

        # -------------------------
        # 3) Calcolo VALUE 1X2
        # -------------------------
        prob_obj = OutcomeProbabilities(
            home_win=prob["P1"],
            draw=prob["PX"],
            away_win=prob["P2"]
        )

        odds_obj = OutcomeOdds(
            home_win=odds["1"],
            draw=odds["X"],
            away_win=odds["2"]
        )

        value = calculate_value_1x2(prob_obj, odds_obj)
        value_dict = value_to_dict(value)

        # -------------------------
        # 4) Output schedina
        # -------------------------
        print(f"  Value: 1={value_dict['value_1']:.3f}  X={value_dict['value_X']:.3f}  2={value_dict['value_2']:.3f}")

        # -------------------------
        # 5) Best pick
        # -------------------------
        best = max(value_dict, key=value_dict.get)
        print(f"  ⭐ Miglior value: {best} ({value_dict[best]:.3f})")

    print("\n=== FINE SCHEDINA SA ===\n")
    input("Premi INVIO per tornare al menu…")
