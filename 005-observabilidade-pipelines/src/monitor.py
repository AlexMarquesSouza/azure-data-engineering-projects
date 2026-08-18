"""Calcula indicadores operacionais e alertas de execuções de pipelines."""
from __future__ import annotations
import argparse,csv,json,math
from collections import defaultdict
from pathlib import Path
def percentil(valores:list[int],p:float)->int:
 valores=sorted(valores);return valores[max(0,math.ceil(len(valores)*p)-1)]
def executar(entrada:Path,saida:Path,sla:int=300)->dict:
 with entrada.open(newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
 grupos=defaultdict(list)
 for r in rows:grupos[r["pipeline"]].append(r)
 metricas=[];alertas=[]
 for nome,runs in sorted(grupos.items()):
  dur=[int(r["duration_seconds"]) for r in runs];falhas=sum(r["status"]!="Succeeded" for r in runs);longos=[r["run_id"] for r in runs if int(r["duration_seconds"])>sla]
  m={"pipeline":nome,"runs":len(runs),"success_rate":round((len(runs)-falhas)/len(runs)*100,2),"p95_seconds":percentil(dur,.95),"failed_runs":falhas,"sla_breaches":longos};metricas.append(m)
  if falhas:alertas.append({"pipeline":nome,"type":"failure","count":falhas})
  if longos:alertas.append({"pipeline":nome,"type":"duration_sla","run_ids":longos})
 resultado={"sla_seconds":sla,"metrics":metricas,"alerts":alertas};saida.parent.mkdir(parents=True,exist_ok=True);saida.write_text(json.dumps(resultado,indent=2)+"\n");return resultado
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,default=Path("data/pipeline_runs.csv"));p.add_argument("--output",type=Path,default=Path("data/output/monitor-report.json"));p.add_argument("--sla",type=int,default=300);a=p.parse_args();print(json.dumps(executar(a.input,a.output,a.sla),indent=2))
if __name__=="__main__":main()
