import os
import csv
import json

def load_tennis_elo():
    path = os.path.join("data", "tennis_elo_ratings.csv")
    players = []

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            players.append({
                "player": row["player"],
                "elo": float(row["elo"])
            })

    return sorted(players, key=lambda x: x["elo"], reverse=True)


def load_tennis_elo_history():
    """
    Legge la storia Elo da tennis_elo_history.csv
    e la organizza per giocatore.
    """
    path = os.path.join("data", "tennis_elo_history.csv")
    if not os.path.exists(path):
        return {}

    history = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            player = row["player"]
            date = row["date"]
            elo = float(row["elo"])

            if player not in history:
                history[player] = []

            history[player].append({
                "date": date,
                "elo": elo
            })

    # ordina per data ogni serie
    for p in history:
        history[p] = sorted(history[p], key=lambda x: x["date"])

    return history


def generate_dashboard_tennis():

    print("[INFO] Generazione dashboard Tennis…")

    players = load_tennis_elo()
    history = load_tennis_elo_history()

    # Prendiamo solo alcuni giocatori per il grafico (es. top 5)
    top_players = [p["player"] for p in players[:5]]

    chart_data = {}
    for p in top_players:
        if p in history:
            chart_data[p] = history[p]

    # HTML
    html = []
    html.append("<html><head>")
    html.append("<meta charset='UTF-8'>")
    html.append("<title>Dashboard Tennis</title>")

    html.append("""
    <style>
        body { font-family: Arial; background: #f4f4f4; padding: 20px; }
        h1 { color: #333; }
        table { border-collapse: collapse; width: 100%; background: white; }
        th, td { padding: 10px; border-bottom: 1px solid #ddd; text-align: left; }
        th { background: #222; color: white; }
        .container { max-width: 1000px; margin: auto; }
        .section { margin-top: 40px; }
        .chart-container { background: white; padding: 20px; border: 1px solid #ccc; }
    </style>
    """)

    # Chart.js CDN
    html.append("""
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    """)

    html.append("</head><body>")
    html.append("<div class='container'>")

    html.append("<h1>Dashboard Tennis</h1>")

    # Ranking Elo
    html.append("<div class='section'>")
    html.append("<h2>Ranking Elo</h2>")
    html.append("<table>")
    html.append("<tr><th>#</th><th>Giocatore</th><th>Elo</th></tr>")

    pos = 1
    for p in players:
        html.append(f"<tr><td>{pos}</td><td>{p['player']}</td><td>{p['elo']}</td></tr>")
        pos += 1

    html.append("</table>")
    html.append("</div>")

    # Grafico Elo reale
    html.append("<div class='section'>")
    html.append("<h2>Grafico Elo (storico)</h2>")
    html.append("<div class='chart-container'>")
    html.append("<canvas id='eloChart'></canvas>")
    html.append("</div>")
    html.append("</div>")

    # Passiamo i dati al JS
    html.append("<script>")
    html.append("const eloHistory = " + json.dumps(chart_data) + ";")
    html.append("""
    const ctx = document.getElementById('eloChart').getContext('2d');

    // Costruiamo labels (date) unificate
    const allDatesSet = new Set();
    for (const player in eloHistory) {
        eloHistory[player].forEach(p => allDatesSet.add(p.date));
    }
    const labels = Array.from(allDatesSet).sort();

    const colors = [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)'
    ];

    const datasets = [];
    let colorIndex = 0;

    for (const player in eloHistory) {
        const series = eloHistory[player];
        const map = {};
        series.forEach(p => { map[p.date] = p.elo; });

        const data = labels.map(d => map[d] !== undefined ? map[d] : null);

        datasets.push({
            label: player,
            data: data,
            borderColor: colors[colorIndex % colors.length],
            backgroundColor: 'rgba(0,0,0,0)',
            spanGaps: true,
            tension: 0.2
        });

        colorIndex++;
    }

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                title: { display: false }
            },
            scales: {
                x: { title: { display: true, text: 'Data' } },
                y: { title: { display: true, text: 'Elo' } }
            }
        }
    });
    """)
    html.append("</script>")

    html.append("</div></body></html>")

    output_path = os.path.join("output", "dashboard_tennis.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    print(f"[OK] Dashboard Tennis generata: {output_path}")


if __name__ == "__main__":
    generate_dashboard_tennis()
