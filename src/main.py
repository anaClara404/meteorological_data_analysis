import os
from dotenv import load_dotenv

from config import CITIES
from extract import fetch_weather
from transform import transform_weather_data
from persist import save_csv, save_json
from llm import analyze_with_openai


# setup 

def main():
    # carregar variáveis do .env
    load_dotenv()
    weather_api_key = os.getenv("OPENWEATHER_API_KEY")
    llm_model = os.getenv("LLM_MODEL", "gpt-4.1-mini")  # fallback padrão

    if not weather_api_key:
        raise ValueError("OPENWEATHER_API_KEY não encontrado no .env")

    print("=== INÍCIO DO PIPELINE DE ANÁLISE METEOROLÓGICA ===")

    # 1) extrair
    print("[1] Extraindo dados da API OpenWeather...")
    raw_data = [fetch_weather(city, weather_api_key) for city in CITIES]

    # 2) transformar
    print("[2] Transformando dados com pandas...")
    df = transform_weather_data(raw_data)

    # 3) persistir (CSV + JSON)
    print("[3] Salvando dados estruturados...")
    save_csv(df)

    # 4) analisar com LLM
    print(f"[4] Gerando análise com modelo {llm_model}...")
    analysis = analyze_with_openai(df.to_dict(orient="records"), model=llm_model)

    # 5) persistir análise em JSON
    print("[5] Salvando análise do LLM...")
    save_json(analysis)

    print("=== PIPELINE CONCLUÍDO COM SUCESSO ===")


if __name__ == "__main__":
    main()

