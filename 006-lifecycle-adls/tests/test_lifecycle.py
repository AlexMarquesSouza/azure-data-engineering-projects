import tempfile,unittest
from datetime import date
from pathlib import Path
from src.lifecycle import executar
class TestLifecycle(unittest.TestCase):
 def test_classifica_sem_executar_acoes(self):
  raiz=Path(__file__).parents[1]
  with tempfile.TemporaryDirectory() as t:
   r=executar(raiz/"data/blobs.csv",Path(t)/"r.json",date(2026,8,9));self.assertEqual(r["summary"],{"keep":1,"cool":1,"archive":1,"delete":1});self.assertEqual(r["decisions"][3]["action"],"delete")
if __name__=="__main__":unittest.main()
