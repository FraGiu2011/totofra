import requests
from bs4 import BeautifulSoup

class MetLiveAPI:
    URL = "https://metlive.ai/pronostici-serie-a"

    def fetch_predictions(self):
        """
        Ritorna pronostici MetLive.
        Se il sito non risponde → ritorna lista vuota.
        """
        try:
            response = requests.get(self.URL, timeout=10)
            response.raise_for_status()
        except Exception:
            # Sito non raggiungibile → nessun crash
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        predictions = []
        cards = soup.find_all("div", class_="match-card")

        for c in cards:
            try:
                teams = c.find("h3").get_text(strip=True)
                home, away = teams.split(" Vs ")

                pick = c.find("span", class_="prediction").get_text(strip=True)
                security = c.find("span", class_="security").get_text(strip=True)

                predictions.append({
                    "home": home,
                    "away": away,
                    "pick": pick,
                    "security": security
                })
            except:
                continue

        return predictions
