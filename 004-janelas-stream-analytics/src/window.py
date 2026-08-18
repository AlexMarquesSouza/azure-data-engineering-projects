"""Agrega telemetria em janelas fixas, como TumblingWindow."""
from __future__ import annotations
import argparse,json
from collections import defaultdict
from datetime import datetime,timezone,timedelta
from pathlib import Path
def executar(entrada:Path,saida:Path,minutos:int=5)->list[dict]:
 grupos=defaultdict(list)
 for texto in entrada.read_text(encoding="utf-8").splitlines():
  if not texto.strip():continue
  e=json.loads(texto);dt=datetime.fromisoformat(e["event_time"].replace("Z","+00:00")).astimezone(timezone.utc);inicio=dt.replace(minute=(dt.minute//minutos)*minutos,second=0,microsecond=0);grupos[(inicio,e["device_id"])].append(float(e["temperature"]))
 rows=[]
 for (inicio,device),valores in sorted(grupos.items()):rows.append({"window_start":inicio.isoformat(),"window_end":(inicio+timedelta(minutes=minutos)).isoformat(),"device_id":device,"events":len(valores),"avg_temperature":round(sum(valores)/len(valores),2),"max_temperature":max(valores)})
 saida.parent.mkdir(parents=True,exist_ok=True);saida.write_text("".join(json.dumps(x)+"\n" for x in rows),encoding="utf-8");return rows
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,default=Path("data/events.jsonl"));p.add_argument("--output",type=Path,default=Path("data/output/windows.jsonl"));p.add_argument("--minutes",type=int,default=5);a=p.parse_args();print(json.dumps(executar(a.input,a.output,a.minutes),indent=2))
if __name__=="__main__":main()
