import json

def load_output(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def esito_1x2(p_home, p_draw, p_away):
    if p_home > p_draw and p_home > p_away:
        return "1"
    elif p_away > p_home and p_away > p_draw:
        return "2"
    else:
        return "X"

def esito_doppia(p_home, p_draw, p_away):
    # Doppia intelligente
    probs = {"1": p_home, "X": p_draw, "2": p_away}
    sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    return sorted_probs[0][0] + sorted_probs[1][0]

def main():
    data = load_output("output/matchday_32.json")

    print("\n=== SCHEDINA UFFICIALE TOTO FRA ===\n")

    print(">>> 1X2 SECCA\n")
    for match in data:
        home = match["model"]["home"]
        away = match["model"]["away"]

        p_home = match["model"]["p_home"]
        p_draw = match["model"]["p_draw"]
        p_away = match["model"]["p_away"]

        esito = esito_1x2(p_home, p_draw, p_away)

        print(f"{home} - {away}: {esito}")

    print("\n>>> DOPPIE INTELLIGENTI (CPT)\n")
    for match in data:
        home = match["model"]["home"]
        away = match["model"]["away"]

        p_home = match["model"]["p_home"]
        p_draw = match["model"]["p_draw"]
        p_away = match["model"]["p_away"]

        doppia = esito_doppia(p_home, p_draw, p_away)

        print(f"{home} - {away}: {doppia}")

if __name__ == "__main__":
    main()
