import os
import json
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
from openai import OpenAI
from openai import OpenAI, OpenAIError


# Carrega variáveis de ambiente (.env)
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("Chave da OpenAI não encontrada. Defina OPENAI_API_KEY no .env")

client = OpenAI(api_key=API_KEY)

# ---------------------------
# Função principal
# ---------------------------

def analyze_with_openai(weather_data: list[dict], model: str = "gpt-4.1-mini") -> dict:
    """
    Envia os dados meteorológicos para o modelo GPT e retorna análise estruturada em JSON.
    Args:
        weather_data (list[dict]): lista de registros meteorológicos (ex.: df.to_dict(orient="records"))
        model (str): nome do modelo a ser usado
    Returns:
        dict: análise estruturada com resumo, melhor/pior cidade, recomendações, tendência.
    """
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

    for attempt in range(1, 4):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Você é um assistente que sempre responde apenas JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                timeout=30,
                response_format={"type": "json_object"}  # força JSON
            )

            text = response.choices[0].message.content.strip()
            analysis = json.loads(text)

            if "metadata" not in analysis:
                analysis["metadata"] = {
                    "gerado_em": datetime.now(timezone.utc).isoformat(),
                    "total_cidades": len(weather_data)
                }

            return analysis

        except OpenAIError as e:
            print(f"[ERRO] Falha na API (tentativa {attempt}): {e}")
            if attempt == 3:
                raise
            time.sleep(2**attempt)

        except json.JSONDecodeError:
            print(f"[ERRO] Resposta não era JSON válido (tentativa {attempt})")
            if attempt == 3:
                raise
            time.sleep(2**attempt)
