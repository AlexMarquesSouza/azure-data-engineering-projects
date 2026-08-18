"""Aplica Slowly Changing Dimension Type 2 a um snapshot de clientes."""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

CAMPOS=["cliente_sk","cliente_id","nome","cidade","inicio_vigencia","fim_vigencia","ativo"]

def ler(path:Path):
 with path.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def executar(dimensao:Path,snapshot:Path,saida:Path,data_carga:str)->dict:
 historico=ler(dimensao); atuais={r["cliente_id"]:r for r in historico if r["ativo"].lower()=="true"}; proxima=max([int(r["cliente_sk"]) for r in historico],default=0)+1; inseridos=alterados=0
 for novo in ler(snapshot):
  atual=atuais.get(novo["cliente_id"])
  if atual and (atual["nome"],atual["cidade"])==(novo["nome"],novo["cidade"]):continue
  if atual: atual["fim_vigencia"]=data_carga;atual["ativo"]="false";alterados+=1
  else: inseridos+=1
  historico.append({"cliente_sk":str(proxima),**novo,"inicio_vigencia":data_carga,"fim_vigencia":"","ativo":"true"});proxima+=1
 saida.parent.mkdir(parents=True,exist_ok=True)
 with saida.open("w",newline="",encoding="utf-8") as f:w=csv.DictWriter(f,fieldnames=CAMPOS);w.writeheader();w.writerows(historico)
 return {"novos":inseridos,"alterados":alterados,"inalterados":len(ler(snapshot))-inseridos-alterados,"versoes_totais":len(historico)}
def main():
 p=argparse.ArgumentParser();p.add_argument("--dimension",type=Path,default=Path("data/dimensao_atual.csv"));p.add_argument("--snapshot",type=Path,default=Path("data/snapshot.csv"));p.add_argument("--output",type=Path,default=Path("data/output/dim_cliente.csv"));p.add_argument("--date",default="2026-08-05");a=p.parse_args();print(json.dumps(executar(a.dimension,a.snapshot,a.output,a.date),indent=2))
if __name__=="__main__":main()
