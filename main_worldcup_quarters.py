from worldcup.worldcup_schedina_quarters import run_schedina_quarters
from worldcup.worldcup_ranking_quarters import run_ranking_quarters
from worldcup.worldcup_dashboard_quarters import run_dashboard_quarters

def run_all_quarters():
    print("=== QUARTI DI FINALE ===")
    run_schedina_quarters()
    run_ranking_quarters()
    run_dashboard_quarters()
    print("=== COMPLETATO: QUARTI DI FINALE ===")

if __name__ == "__main__":
    run_all_quarters()
