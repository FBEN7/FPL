"""Small client for the public fantasy game API, with an on-disk cache.

The game's terms forbid automated extraction, so the tool stays
personal-use (phase 1) and every response is cached to keep requests rare.
"""

import json
import time
from pathlib import Path

import requests

BASE_URL = "https://fantasy.premierleague.com/api"
CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"
HEADERS = {"User-Agent": "fantasy-football-tool/0.1 (personal use)"}


def get_json(path, ttl_seconds=3600):
    """Return the JSON at BASE_URL/path, reusing a cached copy younger than ttl_seconds."""
    cache_file = CACHE_DIR / (path.strip("/").replace("/", "_") + ".json")
    if cache_file.exists() and time.time() - cache_file.stat().st_mtime < ttl_seconds:
        return json.loads(cache_file.read_text())

    response = requests.get(f"{BASE_URL}/{path.strip('/')}/", headers=HEADERS, timeout=30)
    response.raise_for_status()
    data = response.json()

    CACHE_DIR.mkdir(exist_ok=True)
    cache_file.write_text(json.dumps(data))
    return data


def bootstrap():
    """Players, teams, gameweeks and game settings."""
    return get_json("bootstrap-static")


def fixtures():
    """Every fixture of the season, with its difficulty rating for each side."""
    return get_json("fixtures")


def team_picks(entry_id, gameweek):
    """The 15 players a manager picked for a gameweek (public once the deadline has passed)."""
    return get_json(f"entry/{entry_id}/event/{gameweek}/picks", ttl_seconds=6 * 3600)
