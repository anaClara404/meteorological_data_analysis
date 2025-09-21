import requests, time, os, json
from datetime import datetime

def fetch_weather(city_dict, api_key, endpoint="https://api.openweathermap.org/data/2.5/weather"):
    """
    city_dict: {"name": "São Paulo", "lat": -23.55, "lon": -46.63}
    """
    params = {
        "lat": city_dict["lat"],
        "lon": city_dict["lon"],
        "appid": api_key
    }
    for attempt in range(1,4):
        try:
            r = requests.get(endpoint, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()

            # adiciona o nome manualmente para consistência
            data["city_name_custom"] = city_dict["name"]

            ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            fname = f"data/raw/{city_dict['name'].replace(' ','_')}_{ts}.json"
            os.makedirs("data/raw", exist_ok=True)
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return data
        except requests.exceptions.RequestException as e:
            if attempt == 3:
                raise
            time.sleep(2**attempt)

