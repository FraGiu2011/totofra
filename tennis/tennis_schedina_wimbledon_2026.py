# ============================================================
# SCHEDINA TENNIS — OTTAVI DI FINALE WIMBLEDON 2026
# ============================================================

MATCHES = [
    ("Sinner", "Shelton"),
    ("Alcaraz", "Rune"),
    ("Zverev", "Tiafoe"),
    ("Tsitsipas", "Paul"),
    ("Djokovic", "Hurkacz"),
    ("Medvedev", "De Minaur"),
    ("Rublev", "Dimitrov"),
    ("Ruud", "Musetti"),
]

from tennis.tennis_predictor import predict_match

def run_schedina():
    print("\n==============================================")
    print("   SCHEDINA TENNIS — OTTAVI WIMBLEDON 2026")
    print("==============================================\n")

    for p1, p2 in MATCHES:
        result = predict_match(p1, p2)
        print(f"{result['player1']} vs {result['player2']}")
        print(f"Probabilità: {result['prob1']}% – {result['prob2']}%")
        print("----------------------------------------------")

    print("\nSchedina completata.\n")
