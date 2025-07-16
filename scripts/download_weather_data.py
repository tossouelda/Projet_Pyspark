import os
import requests
import json
from datetime import datetime
from pathlib import Path

API_KEY = "a14e6ab35e30e3c1aa3e1379c1b14cdf"
CITY_ID = "5128581"  
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def download_weather_data():
    params = {
        'id': CITY_ID,
        'appid': API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f" Erreur API météo : {e}")
        return

    # Définir le chemin absolu vers data_lake/weather depuis la racine du projet
    root_dir = Path(__file__).resolve().parents[1]  # remonte de /scripts/ vers la racine
    output_dir = root_dir / "data" / "weather"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    file_path = output_dir / f"weather_{timestamp}.json"

    with open(file_path, "w") as f:
        json.dump(data, f)

    print(f" Données météo enregistrées dans : {file_path}")

if __name__ == "__main__":
    download_weather_data()