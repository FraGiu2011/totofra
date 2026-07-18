from api_fetcher import get_matches

# Serie A = "SA"
# Matchday di test = 1 (puoi cambiarlo)
competition = "SA"
matchday = 1

print("🔵 TEST: Richiesta partite Serie A (matchday 1)")
data = get_matches(competition, matchday)

if data and "matches" in data:
    print(f"✔ API OK — trovate {len(data['matches'])} partite")
    for m in data["matches"][:3]:
        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]
        print(f"  - {home} vs {away}")
else:
    print("❌ Nessun dato ricevuto (API o fallback)")
