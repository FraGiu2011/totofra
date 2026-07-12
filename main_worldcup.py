import argparse

from worldcup.worldcup_schedina import run_worldcup_schedina
from worldcup.worldcup_ranking import run_worldcup_ranking
from worldcup.worldcup_ranking_real import run_worldcup_ranking_real
from worldcup.worldcup_dashboard import run_worldcup_dashboard
from worldcup.worldcup_dashboard_real import run_worldcup_dashboard_real


# ============================================================
#  RUN ALL MODULES
# ============================================================

def run_all():
    print("\n=== GENERAZIONE SCHEDINA MONDIALE ===")
    run_worldcup_schedina()

    print("\n=== GENERAZIONE RANKING MONDIALE (SIMULATO) ===")
    run_worldcup_ranking()

    print("\n=== GENERAZIONE RANKING MONDIALE (REALE) ===")
    run_worldcup_ranking_real()

    print("\n=== GENERAZIONE DASHBOARD MONDIALE ===")
    run_worldcup_dashboard()

    print("\n=== GENERAZIONE DASHBOARD MONDIALE REALE ===")
    run_worldcup_dashboard_real()

    print("\n=== COMPLETATO: MODULO MONDIALE ===")


# ============================================================
#  MAIN ARGUMENT PARSER
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Modulo Mondiale - TotoFra")

    parser.add_argument(
        "--schedina",
        action="store_true",
        help="Genera la schedina Mondiale"
    )

    parser.add_argument(
        "--ranking",
        action="store_true",
        help="Genera il ranking Mondiale simulato"
    )

    parser.add_argument(
        "--ranking-real",
        action="store_true",
        help="Genera il ranking Mondiale reale"
    )

    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Genera il dashboard Mondiale"
    )

    parser.add_argument(
        "--dashboard-real",
        action="store_true",
        help="Genera il dashboard Mondiale reale"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Esegue tutto il modulo Mondiale"
    )

    args = parser.parse_args()

    # Esecuzioni singole
    if args.schedina:
        run_worldcup_schedina()
    if args.ranking:
        run_worldcup_ranking()
    if args.ranking_real:
        run_worldcup_ranking_real()
    if args.dashboard:
        run_worldcup_dashboard()
    if args.dashboard_real:
        run_worldcup_dashboard_real()

    # Esecuzione completa
    if args.all:
        run_all()


# ============================================================
#  ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
