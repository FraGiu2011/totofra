from odds_fetcher import OddsFetcher

odds = OddsFetcher()
data = odds.get_odds(sport_key="soccer_epl")

print("Matches trovati:", len(data))
for m in data:
    print(m["home_team"], "-", m["away_team"])
