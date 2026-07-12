from core.comparator import Comparator

# Istanza del comparatore
comp = Comparator()

# Simulazione modello Poisson
sample_model = [{
    "home": "Inter",
    "away": "Milan",
    "prob_1": 0.62,
    "prob_x": 0.23,
    "prob_2": 0.15,
    "corner_factor": 0.4
}]

# Simulazione tipster online
sample_tip_online = {
    "home": "Inter",
    "away": "Milan",
    "prediction": "1",
    "confidence": 55,
    "source": "online"
}

# Simulazione tipster offline
sample_tip_offline = {
    "home": "Inter",
    "away": "Milan",
    "prediction": "1",
    "confidence": 75,
    "source": "offline"
}

# Uniamo i tipster
tipsters = [sample_tip_online, sample_tip_offline]

# Eseguiamo il confronto
result = comp.compare(sample_model, tipsters)

# --- OUTPUT GRAFICO MIGLIORATO ---
print("\n=== RISULTATO COMPARATOR ===")

for r in result:
    print(f"Match: {r['home']} - {r['away']}")
    print(f"Pick tipster: {r['tipster_pick']} ({r['tipster_confidence']})")
    print(f"Probabilità Poisson: {r['poisson_selected']}")
    print(f"Corner factor: {r.get('corner_factor', 'N/D')}")
    print(f"TotoFraScore: {r['totofra_score']}")
    print("-" * 40)
