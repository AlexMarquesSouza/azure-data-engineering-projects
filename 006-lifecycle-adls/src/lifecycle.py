"""Avalia ações de lifecycle por idade e prefixo sem alterar blobs."""
from __future__ import annotations
import argparse,csv,json
from datetime import date
from pathlib import Path
def acao(prefixo:str,idade:int)->str:
 if prefixo.startswith("tmp/") and idade>90:return "delete"
 if idade>180:return "archive"
 if idade>30:return "cool"
 return "keep"
def executar(entrada:Path,saida:Path,hoje:date)->dict:
 with entrada.open(newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
 decisoes=[]
 for r in rows:
  idade=(hoje-date.fromisoformat(r["last_modified"])).days;decisoes.append({"path":r["path"],"age_days":idade,"current_tier":r["tier"],"action":acao(r["path"],idade),"size_mb":int(r["size_mb"])})
 resumo={a:sum(1 for x in decisoes if x["action"]==a) for a in ("keep","cool","archive","delete")};resultado={"as_of":hoje.isoformat(),"summary":resumo,"decisions":decisoes};saida.parent.mkdir(parents=True,exist_ok=True);saida.write_text(json.dumps(resultado,indent=2)+"\n");return resultado
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,default=Path("data/blobs.csv"));p.add_argument("--output",type=Path,default=Path("data/output/lifecycle-report.json"));p.add_argument("--date",type=date.fromisoformat,default=date(2026,8,9));a=p.parse_args();print(json.dumps(executar(a.input,a.output,a.date),indent=2))
if __name__=="__main__":main()
