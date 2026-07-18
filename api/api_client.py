import os
import json
import time
import requests

# ---------------------------------------------------------
#  PATHS
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

CACHE_FILE = os.path.join(DATA_DIR, "cache_api.json")
FALLBACK_FILE = os.path.join(DATA_DIR, "matchday.json")

CACHE_TTL = 60 * 60  # 1 ora
BASE_URL = "https://api.football-data.org/v4"


# ---------------------------------------------------------
#  API KEY
# ---------------------------------------------------------
def load_api_key():
    key = os.getenv("FOOTBALL_DATA_API_KEY")
    if not key:
        print("[API] ⚠ Nessuna API Key trovata. Attivo fallback offline.")
    return key


# ---------------------------------------------------------
#  CACHE
# ---------------------------------------------------------
def load_cache():
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"[CACHE] Errore lettura cache: {e}")
    return {}


def save_cache(cache):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=4)
    except Exception as e:
        print(f"[CACHE] Errore salvataggio cache: {e}")


def cache_get(key):
    cache = load_cache()
    entry = cache.get(key)
    if not entry:
        return None

    if time.time() - entry["timestamp"] < CACHE_TTL:
        return entry["data"]

    return None


def cache_set(key, data):
    cache = load_cache()
    cache[key] = {
        "timestamp": time.time(),
        "data": data
    }
    save_cache(cache)


# ---------------------------------------------------------
#  API REQUEST
# ---------------------------------------------------------
def api_request(endpoint):
    key = load_api_key()
    if not key:
        return None

    url = f"{BASE_URL}{endpoint}"
    headers = {"X-Auth-Token": key}

    try:
        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code == 200:
            return r.json()

        print(f"[API] ❌ Errore {r.status_code}: {r.text}")
        return None

    except requests.exceptions.Timeout:
        print("[API] ⏳ Timeout, fallback offline.")
        return None

    except Exception as e:
        print(f"[API] ⚠ Eccezione: {e}")
        return None


# ---------------------------------------------------------
#  MATCHES
# ---------------------------------------------------------
def get_matches(competition_id, matchday):
    cache_key = f"matches_{competition_id}_{matchday}"

    # 1) CACHE
    cached = cache_get(cache_key)
    if cached:
        print(f"[MATCHES] Cache hit → {competition_id} MD{matchday}")
        return cached

    # 2) API
    print(f"[MATCHES] API fetch → {competition_id} MD{matchday}")
    data = api_request(f"/competitions/{competition_id}/matches?matchday={matchday}")

    if data and "matches" in data:
        cache_set(cache_key, data)
        return data

    # 3) FALLBACK
    print("[MATCHES] 🔄 Fallback → matchday.json")
    try:
        with open(FALLBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[MATCHES] ❌ Fallback fallito: {e}")
        return {"matches": []}
