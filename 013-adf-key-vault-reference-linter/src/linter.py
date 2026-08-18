import argparse,json
from pathlib import Path
SENSITIVE={"password","connectionString","accountKey","clientSecret","sasToken"}
def lint(services):
    names={x.get("name") for x in services}; findings=[]
    for svc in services:
        props=svc.get("properties",{}).get("typeProperties",{})
        for field in SENSITIVE & props.keys():
            value=props[field]
            if not isinstance(value,dict) or value.get("type")!="AzureKeyVaultSecret": findings.append({"service":svc.get("name"),"field":field,"severity":"HIGH","reason":"credencial não usa AzureKeyVaultSecret"}); continue
            store=value.get("store",{}).get("referenceName")
            if not value.get("secretName") or store not in names: findings.append({"service":svc.get("name"),"field":field,"severity":"MEDIUM","reason":"referência Key Vault incompleta ou inexistente"})
    return {"compliant":not findings,"services_checked":len(services),"findings":findings}
def main():
    p=argparse.ArgumentParser(); p.add_argument("input",nargs="?",default="data/linked-services.json"); p.add_argument("--output",default="data/output/report.json"); a=p.parse_args(); report=lint(json.loads(Path(a.input).read_text())["linkedServices"]); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n"); print(json.dumps(report,ensure_ascii=False,indent=2)); raise SystemExit(0 if report["compliant"] else 2)
if __name__=="__main__": main()
