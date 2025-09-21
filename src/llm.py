import os
import json
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
from openai import OpenAI
from openai import OpenAI, APIError, RateLimitError, APITimeoutError, ServiceUnavailableError

# Carrega variáveis de ambiente (.env)
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("Chave da OpenAI não encontrada. Defina OPENAI_API_KEY no .env")

client = OpenAI(api_key=API_KEY)

# ---------------------------
# Função principal
# ---------------------------

def analyze_with_openai(weather_data: list[dict]) -> dict:
    """
    Envia os dados meteorológicos para o modelo GPT e retorna análise estruturada em JSON.
    Args:
        weather_data (list[dict]): lista de registros meteorológicos (ex.: df.to_dict(orient="records"))
    Returns:
        dict: análise estruturada com resumo, melhor/pior cidade, recomendações, tendência.
    """
    # prompt para o modelo
    prompt = f"""
Com base nos seguintes dados meteorológicos (em JSON):
{json.dumps(weather_data, ensure_ascii=False, indent=2)}

Gere uma análise em português contendo APENAS um JSON válido com as chaves:
- resumo: string (resumo das condições atuais)
- melhor_cidade: {{"cidade": "...", "motivo": "..."}}
- pior_cidade: {{"cidade": "...", "motivo": "..."}}
- recomendacoes: lista de strings (atividades recomendadas/evitadas)
- tendencia: string (tendência geral do clima, ex: "estável", "chuvas fortes", "queda de temperatura")
- metadata: {{"gerado_em": UTC timestamp ISO, "total_cidades": número}}

Retorne somente JSON (sem texto extra).
"""

    # até 3 tentativas
    for attempt in range(1, 4):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # pode trocar por gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": "Você é um assistente que sempre responde apenas JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                timeout=30
            )

            text = response.choices[0].message.content.strip()

            # tenta carregar como JSON
            analysis = json.loads(text)

            # se não houver metadata, adiciona
            if "metadata" not in analysis:
                analysis["metadata"] = {
                    "gerado_em": datetime.now(timezone.utc).isoformat(),
                    "total_cidades": len(weather_data)
                }

            return analysis

        except (RateLimitError, APIError, APITimeoutError, ServiceUnavailableError) as e:
            print(f"[ERRO] Falha na API (tentativa {attempt}): {e}")
            if attempt == 3:
                raise
            time.sleep(2**attempt)

        except json.JSONDecodeError:
            print(f"[ERRO] Resposta não era JSON válido (tentativa {attempt})")
            if attempt == 3:
                raise
            time.sleep(2**attempt)
