"""Compara cardinalidade, distribuição de RU e alinhamento de consultas."""
from __future__ import annotations
import argparse,csv,json,statistics
from collections import defaultdict
from pathlib import Path
def executar(dados:Path,workload:Path,saida:Path)->dict:
 with dados.open(newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
 filtros=json.loads(workload.read_text())["query_filters"];candidatos=["tenant_id","customer_id","status","id"];avaliacoes=[]
 for c in candidatos:
  grupos=defaultdict(int)
  for r in rows:grupos[r[c]]+=int(r["ru"])
  cargas=list(grupos.values());media=sum(cargas)/len(cargas);skew=round(max(cargas)/media,2);alinhamento=filtros.get(c,0);score=round(len(grupos)*2+alinhamento-skew*10,2);avaliacoes.append({"key":c,"cardinality":len(grupos),"max_to_avg_ru":skew,"query_alignment_pct":alinhamento,"score":score})
 avaliacoes.sort(key=lambda x:x["score"],reverse=True);resultado={"recommended":"/"+avaliacoes[0]["key"],"evaluations":avaliacoes,"warning":"Validar limites, crescimento e consultas reais"};saida.parent.mkdir(parents=True,exist_ok=True);saida.write_text(json.dumps(resultado,indent=2)+"\n");return resultado
def main():
 p=argparse.ArgumentParser();p.add_argument("--data",type=Path,default=Path("data/items.csv"));p.add_argument("--workload",type=Path,default=Path("workload.json"));p.add_argument("--output",type=Path,default=Path("data/output/advice.json"));a=p.parse_args();print(json.dumps(executar(a.data,a.workload,a.output),indent=2))
if __name__=="__main__":main()
