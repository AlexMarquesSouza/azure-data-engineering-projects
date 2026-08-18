import argparse, json
from pathlib import Path

def plan(triggers, failed):
    by_name={x["name"]:x for x in triggers}; errors=[]
    for item in triggers:
        for dep in item.get("depends_on",[]):
            if dep not in by_name: errors.append(f'{item["name"]}: dependência inexistente: {dep}')
    if failed not in by_name: errors.append(f"Trigger inexistente: {failed}")
    if errors: return {"valid":False,"errors":errors,"rerun_order":[]}
    affected={failed}; changed=True
    while changed:
        changed=False
        for item in triggers:
            if item["name"] not in affected and any(x in affected for x in item.get("depends_on",[])): affected.add(item["name"]); changed=True
    order=[]; pending=set(affected)
    while pending:
        ready=sorted(x for x in pending if not (set(by_name[x].get("depends_on",[])) & pending))
        if not ready: return {"valid":False,"errors":["Ciclo de dependências detectado"],"rerun_order":[]}
        order.extend(ready); pending-=set(ready)
    return {"valid":True,"errors":[],"failed_trigger":failed,"affected_count":len(affected),"rerun_order":order}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",default="data/triggers.json"); p.add_argument("--failed",default="bronze_hourly"); p.add_argument("--output",default="data/output/plan.json"); a=p.parse_args()
    report=plan(json.loads(Path(a.config).read_text())["triggers"],a.failed); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n"); print(json.dumps(report,ensure_ascii=False,indent=2)); raise SystemExit(0 if report["valid"] else 2)
if __name__=="__main__": main()
