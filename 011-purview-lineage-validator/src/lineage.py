import argparse, json
from pathlib import Path

def audit(doc):
    assets={x["id"]:x for x in doc.get("assets",[])}; graph={x:[] for x in assets}; errors=[]; warnings=[]
    for flow in doc.get("flows",[]):
        source,target=flow.get("source"),flow.get("target")
        if source not in assets or target not in assets: errors.append(f"Fluxo referencia ativo inexistente: {source} -> {target}")
        else: graph[source].append(target)
    for key,asset in assets.items():
        for field in ("owner","classification"):
            if not asset.get(field): warnings.append(f"{key}: metadado ausente: {field}")
    visiting=set(); visited=set()
    def visit(node):
        if node in visiting: errors.append(f"Ciclo detectado envolvendo: {node}"); return
        if node in visited: return
        visiting.add(node)
        for child in graph[node]: visit(child)
        visiting.remove(node); visited.add(node)
    for node in graph: visit(node)
    targets={x for children in graph.values() for x in children}
    return {"valid":not errors,"errors":sorted(set(errors)),"warnings":warnings,"summary":{"assets":len(assets),"flows":len(doc.get("flows",[])),"sources":sorted(set(graph)-targets),"sinks":sorted(x for x,y in graph.items() if not y)}}

def main():
    p=argparse.ArgumentParser(); p.add_argument("input",nargs="?",default="data/lineage.json"); p.add_argument("--output",default="data/output/report.json"); a=p.parse_args()
    report=audit(json.loads(Path(a.input).read_text(encoding="utf-8"))); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,ensure_ascii=False,indent=2)); raise SystemExit(0 if report["valid"] else 1)
if __name__=="__main__": main()
