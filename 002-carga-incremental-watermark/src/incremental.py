"""Extrai somente registros posteriores ao watermark confirmado."""
from __future__ import annotations
import argparse, csv, json
from datetime import datetime, timezone
from pathlib import Path

INICIAL = "1970-01-01T00:00:00+00:00"

def instante(valor: str) -> datetime:
    return datetime.fromisoformat(valor.replace("Z", "+00:00")).astimezone(timezone.utc)

def executar(entrada: Path, saida: Path, estado: Path) -> dict:
    watermark = INICIAL
    if estado.exists():
        watermark = json.loads(estado.read_text(encoding="utf-8"))["watermark"]
    limite_inferior = instante(watermark)
    with entrada.open(newline="", encoding="utf-8") as arq:
        leitor = csv.DictReader(arq)
        if leitor.fieldnames != ["cliente_id", "nome", "email", "atualizado_em"]:
            raise ValueError("schema de entrada inesperado")
        delta = [linha for linha in leitor if instante(linha["atualizado_em"]) > limite_inferior]
    delta.sort(key=lambda x: instante(x["atualizado_em"]))
    saida.parent.mkdir(parents=True, exist_ok=True)
    with saida.open("w", newline="", encoding="utf-8") as arq:
        escritor = csv.DictWriter(arq, fieldnames=leitor.fieldnames)
        escritor.writeheader(); escritor.writerows(delta)
    novo = delta[-1]["atualizado_em"].replace("Z", "+00:00") if delta else watermark
    estado.parent.mkdir(parents=True, exist_ok=True)
    estado.write_text(json.dumps({"watermark": novo}, indent=2) + "\n", encoding="utf-8")
    return {"watermark_anterior": watermark, "watermark_atual": novo, "registros_extraidos": len(delta)}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--input",type=Path,default=Path("data/input/clientes.csv")); p.add_argument("--output",type=Path,default=Path("data/output/clientes_delta.csv")); p.add_argument("--state",type=Path,default=Path("state/watermark.json")); a=p.parse_args(); print(json.dumps(executar(a.input,a.output,a.state),indent=2))
if __name__ == "__main__": main()
