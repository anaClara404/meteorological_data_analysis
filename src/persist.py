import os
import json
import pandas as pd
from datetime import datetime, timezone

# ---------------------------
# Helpers
# ---------------------------

def ensure_dir(path: str):
    """Garante que o diretório existe."""
    os.makedirs(path, exist_ok=True)


# ---------------------------
# Funções principais
# ---------------------------

def save_csv(df: pd.DataFrame, out_dir: str = "data/outputs"):
    """Salva DataFrame em CSV."""
    ensure_dir(out_dir)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fname = os.path.join(out_dir, f"weather_summary_{ts}.csv")
    df.to_csv(fname, index=False, encoding="utf-8")
    print(f"[OK] CSV salvo em {fname}")

def save_json(analysis: dict, out_dir: str = "data/outputs"):
    """Salva análise do LLM em JSON estruturado."""
    ensure_dir(out_dir)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fname = os.path.join(out_dir, f"analysis_{ts}.json")

    payload = {
        "generated_at": ts,
        "analysis": analysis
    }

    with open(fname, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"[OK] JSON salvo em {fname}")
