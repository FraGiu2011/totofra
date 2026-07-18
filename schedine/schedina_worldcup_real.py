from api.api_football import APIFootball
from api.odds_api import get_odds_for_match_SA
from core.value_calculator import (
    OutcomeProbabilities,
    OutcomeOdds,
    calculate_value_1x2,
    as_dict as value_to_dict
)
from core.probability_calculator import calculate_probabilities_1x2


def generate_schedina_worldcup_2026():
    print("\n=== SCHEDINA MONDIALE 2026 (API‑FOOTBALL + VALUE) ===\n")

    api = APIFootball()

    # 1) Carichiamo i match reali del Mondiale 2026 (con fallback 2022)
    fixtures = api.get_worldcup_fixtures()

    if not fixtures:
        print("⚠️ Nessun match trovato dal Mondiale 2026.")
        input("\nPremi INVIO per tornare al menu…")
        return

    print(f"[DEBUG] Match trovati: {len(fixtures)}")
    print(f"[DEBUG] Esempio: {fixtures[0]['teams']['home']['name']} vs {fixtures[0]['teams']['away']['name']}")

    # 2) Ciclo sui match
    for m in fixtures:
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

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
        # 2) Probabilità 1X2 dal modello Poisson
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

    print("\n=== FINE SCHEDINA MONDIALE 2026 ===\n")
    input("Premi INVIO per tornare al menu…")
