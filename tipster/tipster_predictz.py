import requests
from bs4 import BeautifulSoup
from tipster.base_tipster import BaseTipster

class PredictZTipster(BaseTipster):

    def get_predictions(self, date_str: str):
        url = "https://www.predictz.com/predictions/"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        predictions = []

        rows = soup.select("table.predictions tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            home = cols[0].get_text(strip=True)
            away = cols[1].get_text(strip=True)
            pick = cols[2].get_text(strip=True)
            odds = cols[3].get_text(strip=True).replace(",", ".")

            try:
                odds = float(odds)
            except:
                odds = None

            predictions.append({
                "source": "PredictZ",
                "home": home,
                "away": away,
                "market": "1X2",
                "pick": pick,
                "prob": None,
                "odds": odds
            })

        return predictions
