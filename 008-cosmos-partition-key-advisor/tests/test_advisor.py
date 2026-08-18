import tempfile,unittest
from pathlib import Path
from src.advisor import executar
class TestAdvisor(unittest.TestCase):
 def test_equilibra_cardinalidade_e_consultas(self):
  raiz=Path(__file__).parents[1]
  with tempfile.TemporaryDirectory() as t:
   r=executar(raiz/"data/items.csv",raiz/"workload.json",Path(t)/"r.json");self.assertEqual(r["recommended"],"/tenant_id");status=next(x for x in r["evaluations"] if x["key"]=="status");self.assertEqual(status["cardinality"],2)
if __name__=="__main__":unittest.main()
