import tempfile,unittest
from pathlib import Path
from src.monitor import executar
class TestMonitor(unittest.TestCase):
 def test_calcula_metricas_e_alertas(self):
  raiz=Path(__file__).parents[1]
  with tempfile.TemporaryDirectory() as t:
   r=executar(raiz/"data/pipeline_runs.csv",Path(t)/"r.json");sales=next(x for x in r["metrics"] if x["pipeline"]=="ingest_sales");sla=next(x for x in r["alerts"] if x["type"]=="duration_sla");self.assertEqual(sales["success_rate"],66.67);self.assertEqual(len(r["alerts"]),2);self.assertEqual(sla["run_ids"],["r3"])
if __name__=="__main__":unittest.main()
