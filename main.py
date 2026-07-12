import os
import sys

# -------------------------
# IMPORT DEI MODULI
# -------------------------

# Dashboard
from dashboard.dashboard_generator import generate_dashboard
from dashboard.dashboard_worldcup import generate_dashboard_worldcup

# Schedine
from schedine.schedina_SA import generate_schedina_SA
from schedine.schedina_PL import generate_schedina_PL
from schedine.schedina_worldcup_2026 import generate_schedina_worldcup_2026

# Ranking
from ranking.ranking_SA import generate_ranking_SA
from ranking.ranking_PL import generate_ranking_PL
from ranking.ranking_worldcup import generate_ranking_worldcup


# -------------------------
# FUNZIONI DI UTILITÀ
# -------------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def menu_principale():
    clear()
    print("=== TOTO FRA ===")
    print("1) Serie A")
    print("2) Premier League")
    print("3) Tennis")
    print("4) Mondiale")
    print("0) Esci")
    return input("\nSeleziona opzione: ")


def menu_competizione(nome):
    clear()
    print(f"=== {nome.upper()} ===")
    print("1) Dashboard")
    print("2) Schedina")
    print("3) Ranking")
    print("0) Indietro")
    return input("\nSeleziona opzione: ")


def menu_mondiale():
    clear()
    print("=== MONDIALE ===")
    print("1) Dashboard Mondiale")
    print("2) Schedina Mondiale")
    print("3) Ranking Mondiale")
    print("0) Indietro")
    return input("\nSeleziona opzione: ")


# -------------------------
# MAIN LOOP
# -------------------------

def main():
    while True:
        scelta = menu_principale()

        # -------------------------
        # SERIE A
        # -------------------------
        if scelta == "1":
            sub = menu_competizione("Serie A")

            if sub == "1":
                generate_dashboard("SA")
            elif sub == "2":
                generate_schedina_SA()
            elif sub == "3":
                generate_ranking_SA()

        # -------------------------
        # PREMIER LEAGUE
        # -------------------------
        elif scelta == "2":
            sub = menu_competizione("Premier League")

            if sub == "1":
                generate_dashboard("PL")
            elif sub == "2":
                generate_schedina_PL()
            elif sub == "3":
                generate_ranking_PL()

        # -------------------------
        # TENNIS
        # -------------------------
        elif scelta == "3":
            clear()
            print("=== TENNIS ===")
            print("Modulo in sviluppo…")
            input("\nPremi INVIO per tornare al menu…")

        # -------------------------
        # MONDIALE
        # -------------------------
        elif scelta == "4":
            while True:
                sub = menu_mondiale()

                if sub == "1":
                    generate_dashboard_worldcup()
                elif sub == "2":
                    generate_schedina_worldcup_2026()
                elif sub == "3":
                    generate_ranking_worldcup()
                elif sub == "0":
                    break

        # -------------------------
        # USCITA
        # -------------------------
        elif scelta == "0":
            sys.exit()

        else:
            print("Scelta non valida.")
            input("Premi INVIO per continuare…")


if __name__ == "__main__":
    main()
