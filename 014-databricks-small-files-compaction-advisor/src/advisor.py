import argparse,csv,json,math
from collections import defaultdict
from pathlib import Path
def advise(rows,target_mb=128,small_mb=8):
    parts=defaultdict(list)
    for row in rows: parts[row["partition"]].append(float(row["size_mb"]))
    result=[]
    for name,sizes in sorted(parts.items()):
        total=sum(sizes); small=sum(x<small_mb for x in sizes); outputs=max(1,math.ceil(total/target_mb)); ratio=small/len(sizes)
        result.append({"partition":name,"files":len(sizes),"size_mb":round(total,2),"small_file_ratio":round(ratio,3),"recommended_output_files":outputs,"action":"OPTIMIZE" if len(sizes)>=10 and ratio>=0.5 else "MONITOR"})
    return {"target_file_mb":target_mb,"partitions":result,"optimize_count":sum(x["action"]=="OPTIMIZE" for x in result)}
def main():
    p=argparse.ArgumentParser(); p.add_argument("input",nargs="?",default="data/files.csv"); p.add_argument("--output",default="data/output/report.json"); a=p.parse_args()
    with open(a.input,encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f))
    report=advise(rows); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n"); print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
