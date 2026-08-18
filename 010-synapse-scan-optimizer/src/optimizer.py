import argparse,csv,json
from pathlib import Path
def executar(inp,out,year=2026,month=2):
 with inp.open(newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
 total=sum(int(r["size_mb"]) for r in rows);selected=[r for r in rows if int(r["year"])==year and int(r["month"])==month];scan=sum(int(r["size_mb"]) for r in selected);res={"full_scan_mb":total,"partition_scan_mb":scan,"reduction_pct":round((1-scan/total)*100,2),"recommended_path":f"sales/year={year}/month={month:02d}/*.parquet","format":"PARQUET"};out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(res,indent=2)+"\n");return res
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,default=Path("data/files.csv"));p.add_argument("--output",type=Path,default=Path("data/output/plan.json"));a=p.parse_args();print(json.dumps(executar(a.input,a.output),indent=2))
if __name__=="__main__":main()
