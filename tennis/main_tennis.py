# ============================================================
# MAIN TENNIS — TotoFra
# ============================================================
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from tennis.tennis_predictor import predict_match
from tennis.tennis_schedina_wimbledon_2026 import run_schedina

def main():
    print("=== TotoFra Tennis ===\n")

    # Esempio: pronostico singolo match
    result = predict_match("Sinner", "Alcaraz")
    print(result)

    # Esegui schedina Wimbledon
    run_schedina()


if __name__ == "__main__":
    main()
