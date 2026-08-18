import json,platform,shutil,sys
from pathlib import Path
def inspect_environment():
    tools={name:shutil.which(name) for name in ("python3","code","git","az")}
    return {"python":platform.python_version(),"python_supported":sys.version_info>=(3,10),"tools":tools,"required_ready":bool(tools["python3"]),"optional_cloud_ready":bool(tools["az"])}
def main():
    report=inspect_environment(); out=Path("data/output/environment.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2)); raise SystemExit(0 if report["python_supported"] else 1)
if __name__=="__main__": main()
