from worldcup.worldcup_phasefinals_real_loader import load_phasefinals_real

HTML_TEMPLATE = """
<html>
<head>
    <meta charset="UTF-8">
    <title>Schedina Ottavi Mondiale 2026</title>
    <style>
        body { font-family: Arial, sans-serif; background:#f0f0f0; padding:20px; }
        h1 { text-align:center; margin-bottom:30px; }
        .match-card {
            background:white; padding:12px; margin:10px auto; max-width:480px;
            border-radius:8px; box-shadow:0 0 6px rgba(0,0,0,0.2);
        }
        .teams { display:flex; justify-content:space-between; font-size:18px; margin-bottom:8px; }
        .details { font-size:14px; color:#555; }
        .pick { margin-top:8px; font-weight:bold; color:#0077cc; }
    </style>
</head>
<body>
    <h1>Schedina Ottavi Mondiale 2026</h1>
    {content}
</body>
</html>
"""

def generate_schedina_round_of_16_html():
    data = load_phasefinals_real()
    r16 = data["round_of_16"]

    cards = []
    for _, m in r16.iterrows():
        home = m["home"]
        away = m["away"]
        date = m["date"]

        # qui puoi integrare i pronostici che abbiamo definito a mano
        if home == "USA" and away == "Belgio":
            pick = "Pronostico: 2 (Belgio) – Risultato stimato 1–2, Over 2.5, GG"
        elif home == "Argentina" and away == "Egitto":
            pick = "Pronostico: 1 (Argentina) – Risultato stimato 2–0, Over 2.5, NG"
        elif home == "Svizzera" and away == "Colombia":
            pick = "Pronostico: X – Risultato stimato 1–1, Under 2.5, GG"
        else:
            pick = "Pronostico: TBD"

        cards.append(f"""
        <div class="match-card">
            <div class="teams">
                <span>{home}</span>
                <span>{away}</span>
            </div>
            <div class="details">Data: {date}</div>
            <div class="pick">{pick}</div>
        </div>
        """)

    content = "\n".join(cards)
    return HTML_TEMPLATE.replace("{content}", content)

def run_schedina_round_of_16():
    html = generate_schedina_round_of_16_html()
    output_path = "output/schedina_round_of_16.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Schedina Ottavi salvata:", output_path)
