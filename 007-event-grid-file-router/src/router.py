"""Valida, deduplica e roteia eventos BlobCreated por prefixo."""
from __future__ import annotations
import argparse,json
from pathlib import Path
def executar(entrada:Path,saida:Path)->dict:
 vistos=set();rotas={"sales":[],"customers":[],"ignored":[]};duplicados=0
 for texto in entrada.read_text().splitlines():
  if not texto.strip():continue
  e=json.loads(texto)
  if e["id"] in vistos:duplicados+=1;continue
  vistos.add(e["id"]);subject=e.get("subject","")
  if e.get("eventType")!="Microsoft.Storage.BlobCreated":rotas["ignored"].append(e["id"])
  elif "/blobs/sales/" in subject:rotas["sales"].append(e["id"])
  elif "/blobs/customers/" in subject:rotas["customers"].append(e["id"])
  else:rotas["ignored"].append(e["id"])
 resultado={"routes":rotas,"duplicates_ignored":duplicados};saida.parent.mkdir(parents=True,exist_ok=True);saida.write_text(json.dumps(resultado,indent=2)+"\n");return resultado
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,default=Path("data/events.jsonl"));p.add_argument("--output",type=Path,default=Path("data/output/routes.json"));a=p.parse_args();print(json.dumps(executar(a.input,a.output),indent=2))
if __name__=="__main__":main()
