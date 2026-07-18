# ============================================================
# TENNIS LOADER — Ranking ATP + Forma Giocatori
# ============================================================

import pandas as pd

def load_atp_ranking():
    # Ranking ATP semplificato (puoi collegarlo a un CSV reale)
    data = [
        {"player": "Jannik Sinner", "rank": 1, "elo": 2150},
        {"player": "Carlos Alcaraz", "rank": 2, "elo": 2120},
        {"player": "Novak Djokovic", "rank": 3, "elo": 2100},
        {"player": "Daniil Medvedev", "rank": 4, "elo": 2050},
        {"player": "Holger Rune", "rank": 5, "elo": 2000},
        {"player": "Alexander Zverev", "rank": 6, "elo": 1980},
        {"player": "Stefanos Tsitsipas", "rank": 7, "elo": 1960},
        {"player": "Tommy Paul", "rank": 8, "elo": 1940},
        {"player": "Ben Shelton", "rank": 9, "elo": 1930},
        {"player": "Frances Tiafoe", "rank": 10, "elo": 1920},
    ]
    return pd.DataFrame(data)


def load_player_form(player):
    # Forma semplificata (puoi collegarla a un CSV reale)
    form_data = {
        "Jannik Sinner": 0.88,
        "Carlos Alcaraz": 0.85,
        "Novak Djokovic": 0.80,
        "Daniil Medvedev": 0.78,
        "Holger Rune": 0.75,
        "Alexander Zverev": 0.74,
        "Stefanos Tsitsipas": 0.72,
        "Tommy Paul": 0.70,
        "Ben Shelton": 0.68,
        "Frances Tiafoe": 0.67,
    }
    return form_data.get(player, 0.50)
