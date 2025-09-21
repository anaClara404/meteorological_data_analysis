import pandas as pd

def kelvin_to_celsius(k: float) -> float:
    """Converte Kelvin para Celsius."""
    return round(k - 273.15, 2)


def categorize_weather(weather_main: str) -> str:
    """Mapeia condição principal para categorias simplificadas."""
    mapping = {
        "Clear": "Céu limpo",
        "Clouds": "Nublado",
        "Rain": "Chuva",
        "Drizzle": "Garoa",
        "Thunderstorm": "Tempestade",
        "Snow": "Neve",
        "Mist": "Neblina",
        "Fog": "Neblina",
        "Haze": "Neblina",
        "Dust": "Poeira",
        "Smoke": "Fumaça",
        "Sand": "Areia",
    }
    return mapping.get(weather_main, "Outros")


# pipeline 

def transform_weather_data(raw_data: list[dict]) -> pd.DataFrame:
    """
    Transforma lista de JSONs brutos da API do OpenWeatherMap em DataFrame.
    Args:
        raw_data (list[dict]): lista de dicionários retornados pela API.
    Returns:
        pd.DataFrame: tabela estruturada.
    """
    rows = []
    for d in raw_data:
        main = d.get("main", {})
        wind = d.get("wind", {})
        weather = d.get("weather", [{}])[0]

        rows.append({
            "cidade": d.get("name", "Desconhecida"),
            "temp_c": kelvin_to_celsius(main.get("temp")),
            "sensacao_termica_c": kelvin_to_celsius(main.get("feels_like")),
            "temp_min_c": kelvin_to_celsius(main.get("temp_min")),
            "temp_max_c": kelvin_to_celsius(main.get("temp_max")),
            "umidade": main.get("humidity"),
            "pressao": main.get("pressure"),
            "vento_m_s": wind.get("speed", 0),
            "vento_dir": wind.get("deg", None),
            "clima_main": weather.get("main", "N/A"),
            "clima_desc": weather.get("description", "N/A"),
            "categoria_clima": categorize_weather(weather.get("main", "")),
            "timestamp": d.get("dt")
        })

    df = pd.DataFrame(rows)

    # ajustes finais
    df["cidade"] = df["cidade"].astype(str)
    df["categoria_clima"] = df["categoria_clima"].astype(str)

    return df
