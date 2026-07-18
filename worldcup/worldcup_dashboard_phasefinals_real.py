import pandas as pd
from worldcup.worldcup_phasefinals_real_loader import load_phasefinals_real

# ============================================================
# HTML TEMPLATE
# ============================================================

HTML_TEMPLATE = """
<html>
<head>
    <meta charset="UTF-8">
    <title>World Cup 2026 - Fase Finale Reale</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f0f0;
            padding: 20px;
        }

        h1 {
            text-align: center;
            margin-bottom: 40px;
        }

        .stage-title {
            font-size: 22px;
            margin-top: 40px;
            margin-bottom: 10px;
            font-weight: bold;
        }

        .bracket {
            display: flex;
            flex-direction: row;
            justify-content: space-around;
            margin-top: 20px;
        }

        .match-box {
            background: white;
            padding: 12px;
            margin: 10px;
            border-radius: 8px;
            width: 260px;
            box-shadow: 0px 0px 6px rgba(0,0,0,0.2);
        }

        .team {
            display: flex;
            align-items: center;
            font-size: 16px;
            margin-bottom: 6px;
        }

        .team-logo {
            width: 32px;
            height: 32px;
            margin-right: 6px;
        }

        .vs {
            text-align: center;
            font-weight: bold;
            margin: 6px 0;
        }

        .date {
            text-align: center;
            font-size: 14px;
            margin-top: 6px;
        }

        .countdown {
            text-align: center;
            font-size: 14px;
            margin-top: 4px;
            color: #0077cc;
            font-weight: bold;
        }
    </style>
</head>

<body>
    <h1>World Cup 2026 - Fase Finale Reale</h1>

    {content}

    <script>
        function updateCountdown() {
            document.querySelectorAll('.countdown').forEach(el => {
                const target = new Date(el.dataset.date);
                const now = new Date();
                const diff = target - now;

                if (isNaN(target.getTime())) {
                    el.innerHTML = "";
                    return;
                }

                if (diff <= 0) {
                    el.innerHTML = "In corso";
                    return;
                }

                const days = Math.floor(diff / (1000*60*60*24));
                const hours = Math.floor((diff / (1000*60*60)) % 24);
                const minutes = Math.floor((diff / (1000*60)) % 60);

                el.innerHTML = days + "g " + hours + "h " + minutes + "m";
            });
        }

        setInterval(updateCountdown, 60000);
        updateCountdown();
    </script>

</body>
</html>
"""

# ============================================================
# BRACKET CELL (con loghi + countdown)
# ============================================================

def bracket_cell(home, away, date, logo_home, logo_away):
    countdown_html = ""
    if date not in ["TBD", None]:
        countdown_html = f"<div class='countdown' data-date='{date}'></div>"

    return f"""
        <div class='match-box'>
            <div class='team'>
                <img src='{logo_home}' class='team-logo'>
                {home}
            </div>
            <div class='vs'>vs</div>
            <div class='team'>
                <img src='{logo_away}' class='team-logo'>
                {away}
            </div>
            <div class='date'>{date}</div>
            {countdown_html}
        </div>
    """

# ============================================================
# GENERA BRACKET HTML
# ============================================================

def generate_bracket_html(data):
    html = ""

    # --------- OTTAVI ---------
    if "round_of_16" in data:
        html += "<div class='stage-title'>Ottavi di Finale</div>"
        html += "<div class='bracket'>"
        for _, m in data["round_of_16"].iterrows():
            html += bracket_cell(
                m["home"], m["away"], m["date"],
                m.get("logo_home", ""), m.get("logo_away", "")
            )
        html += "</div>"

    # --------- QUARTI ---------
    html += "<div class='stage-title'>Quarti di Finale</div>"
    html += "<div class='bracket'>"
    for _, m in data["quarters"].iterrows():
        html += bracket_cell(
            m["home"], m["away"], m["date"],
            m.get("logo_home", ""), m.get("logo_away", "")
        )
    html += "</div>"

    # ... semifinali e finale come già hai
    return html
    # ---------------- SEMIFINALI ----------------
    html += "<div class='stage-title'>Semifinali</div>"
    html += "<div class='bracket'>"

    for _, m in data["semifinals"].iterrows():
        html += bracket_cell(
            m["home"], m["away"], m["date"],
            m.get("logo_home", ""), m.get("logo_away", "")
        )
    html += "</div>"

    # ---------------- FINALE ----------------
    html += "<div class='stage-title'>Finale</div>"
    html += "<div class='bracket'>"

    for _, m in data["final"].iterrows():
        html += bracket_cell(
            m["home"], m["away"], m["date"],
            m.get("logo_home", ""), m.get("logo_away", "")
        )
    html += "</div>"

    return html

# ============================================================
# GENERA HTML COMPLETO
# ============================================================

def generate_dashboard_phasefinals_real_html():
    data = load_phasefinals_real()
    content = generate_bracket_html(data)
    return HTML_TEMPLATE.replace("{content}", content)

# ============================================================
# MAIN
# ============================================================

def run_dashboard_phasefinals_real():
    html = generate_dashboard_phasefinals_real_html()
    output_path = "output/dashboard_phasefinals_real.html"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Dashboard Fase Finale Reale salvata:", output_path)

