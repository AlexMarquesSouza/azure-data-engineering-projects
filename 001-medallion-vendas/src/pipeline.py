"""Pipeline didatico bronze/silver/gold para vendas em lote."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from collections import defaultdict
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

COLUNAS = (
    "pedido_id",
    "data_pedido",
    "cliente_id",
    "produto",
    "quantidade",
    "preco_unitario",
)


def validar(linha: dict[str, str]) -> tuple[dict[str, str] | None, str | None]:
    """Valida e normaliza uma venda; retorna o motivo quando invalida."""
    ausentes = [campo for campo in COLUNAS if not linha.get(campo, "").strip()]
    if ausentes:
        return None, f"campos obrigatorios vazios: {', '.join(ausentes)}"

    try:
        data_pedido = date.fromisoformat(linha["data_pedido"].strip())
        quantidade = int(linha["quantidade"])
        preco = Decimal(linha["preco_unitario"].replace(",", "."))
    except (ValueError, InvalidOperation):
        return None, "tipo de dado invalido"

    if quantidade <= 0:
        return None, "quantidade deve ser maior que zero"
    if preco <= 0:
        return None, "preco_unitario deve ser maior que zero"

    normalizada = {
        "pedido_id": linha["pedido_id"].strip().upper(),
        "data_pedido": data_pedido.isoformat(),
        "cliente_id": linha["cliente_id"].strip().upper(),
        "produto": linha["produto"].strip(),
        "quantidade": str(quantidade),
        "preco_unitario": f"{preco:.2f}",
        "valor_total": f"{preco * quantidade:.2f}",
    }
    return normalizada, None


def escrever_csv(caminho: Path, linhas: list[dict[str, str]], campos: list[str]) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(linhas)


def executar(entrada: Path, destino: Path) -> dict[str, object]:
    """Executa todas as camadas de maneira idempotente por pedido_id."""
    inicio = datetime.now(timezone.utc)
    conteudo = entrada.read_bytes()
    lote = hashlib.sha256(conteudo).hexdigest()[:12]

    bronze = destino / "bronze" / f"vendas_{lote}.csv"
    bronze.parent.mkdir(parents=True, exist_ok=True)
    bronze.write_bytes(conteudo)

    validas: list[dict[str, str]] = []
    rejeitadas: list[dict[str, str]] = []
    vistos: set[str] = set()

    with entrada.open(newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        if tuple(leitor.fieldnames or ()) != COLUNAS:
            raise ValueError(f"schema inesperado; esperado: {', '.join(COLUNAS)}")
        for numero, linha in enumerate(leitor, start=2):
            normalizada, erro = validar(linha)
            pedido_id = linha.get("pedido_id", "").strip().upper()
            if not erro and pedido_id in vistos:
                erro = "pedido_id duplicado no lote"
            if erro:
                rejeitadas.append({**linha, "linha_origem": str(numero), "motivo": erro})
                continue
            assert normalizada is not None
            vistos.add(pedido_id)
            validas.append(normalizada)

    campos_silver = list(COLUNAS) + ["valor_total"]
    silver = destino / "silver" / "vendas_validas.csv"
    escrever_csv(silver, validas, campos_silver)

    campos_quarentena = list(COLUNAS) + ["linha_origem", "motivo"]
    quarentena = destino / "quarantine" / "vendas_rejeitadas.csv"
    escrever_csv(quarentena, rejeitadas, campos_quarentena)

    agregado: dict[str, dict[str, Decimal | int]] = defaultdict(
        lambda: {"pedidos": 0, "itens": 0, "receita": Decimal("0")}
    )
    for venda in validas:
        dia = agregado[venda["data_pedido"]]
        dia["pedidos"] = int(dia["pedidos"]) + 1
        dia["itens"] = int(dia["itens"]) + int(venda["quantidade"])
        dia["receita"] = Decimal(dia["receita"]) + Decimal(venda["valor_total"])

    gold_rows = [
        {
            "data_pedido": dia,
            "pedidos": str(valores["pedidos"]),
            "itens": str(valores["itens"]),
            "receita": f"{Decimal(valores['receita']):.2f}",
        }
        for dia, valores in sorted(agregado.items())
    ]
    gold = destino / "gold" / "vendas_diarias.csv"
    escrever_csv(gold, gold_rows, ["data_pedido", "pedidos", "itens", "receita"])

    relatorio = {
        "lote": lote,
        "inicio_utc": inicio.isoformat(),
        "fim_utc": datetime.now(timezone.utc).isoformat(),
        "registros_validos": len(validas),
        "registros_rejeitados": len(rejeitadas),
        "arquivos": [str(bronze), str(silver), str(gold), str(quarentena)],
    }
    relatorio_path = destino / "run-report.json"
    relatorio_path.write_text(json.dumps(relatorio, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return relatorio


def enviar_azure(destino: Path, conta: str) -> None:
    """Envia as camadas a containers Azure usando identidade sem senha."""
    try:
        from azure.identity import DefaultAzureCredential
        from azure.storage.blob import BlobServiceClient
    except ImportError as exc:
        raise RuntimeError("instale requirements.txt para usar --upload-azure") from exc

    cliente = BlobServiceClient(
        account_url=f"https://{conta}.blob.core.windows.net",
        credential=DefaultAzureCredential(),
    )
    for camada in ("bronze", "silver", "gold", "quarantine"):
        container = cliente.get_container_client(camada)
        try:
            container.create_container()
        except Exception as exc:
            if getattr(exc, "status_code", None) != 409:
                raise
        for arquivo in (destino / camada).glob("*.csv"):
            with arquivo.open("rb") as dados:
                container.upload_blob(arquivo.name, dados, overwrite=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/input/vendas.csv"))
    parser.add_argument("--output", type=Path, default=Path("data"))
    parser.add_argument("--upload-azure", metavar="CONTA", help="nome da Storage Account")
    args = parser.parse_args()
    relatorio = executar(args.input, args.output)
    if args.upload_azure:
        enviar_azure(args.output, args.upload_azure)
    print(json.dumps(relatorio, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
