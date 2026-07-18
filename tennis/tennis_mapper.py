# ============================================================
# TENNIS MAPPER — Normalizzazione Nomi Giocatori
# ============================================================

def normalize_player(name):
    name = name.strip().lower()

    mapping = {
        "sinner": "Jannik Sinner",
        "alcaraz": "Carlos Alcaraz",
        "djokovic": "Novak Djokovic",
        "medvedev": "Daniil Medvedev",
        "rune": "Holger Rune",
        "zverev": "Alexander Zverev",
        "tsitsipas": "Stefanos Tsitsipas",
        "paul": "Tommy Paul",
        "shelton": "Ben Shelton",
        "tiafoe": "Frances Tiafoe",
    }

    return mapping.get(name, name.title())
