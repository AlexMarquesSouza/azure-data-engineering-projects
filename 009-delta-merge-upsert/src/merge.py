import argparse,csv,json
from pathlib import Path
def read(p):
 with p.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def executar(target,updates,out):
 table={r["id"]:r for r in read(target)}; latest={}
 for r in read(updates):
  if r["id"] not in latest or r["updated_at"]>latest[r["id"]]["updated_at"]:latest[r["id"]]=r
 inserted=updated=0
 for k,r in latest.items():
  if k in table:
   if r["updated_at"]>table[k]["updated_at"]:table[k]=r;updated+=1
  else:table[k]=r;inserted+=1
 out.parent.mkdir(parents=True,exist_ok=True)
 with out.open("w",newline="",encoding="utf-8") as f:w=csv.DictWriter(f,fieldnames=["id","name","city","updated_at"]);w.writeheader();w.writerows(sorted(table.values(),key=lambda x:x["id"]))
 return {"inserted":inserted,"updated":updated,"rows":len(table)}
def main():
 p=argparse.ArgumentParser();p.add_argument("--target",type=Path,default=Path("data/target.csv"));p.add_argument("--updates",type=Path,default=Path("data/updates.csv"));p.add_argument("--output",type=Path,default=Path("data/output/merged.csv"));a=p.parse_args();print(json.dumps(executar(a.target,a.updates,a.output),indent=2))
if __name__=="__main__":main()
