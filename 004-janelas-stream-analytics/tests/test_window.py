import tempfile,unittest
from pathlib import Path
from src.window import executar
class TestWindow(unittest.TestCase):
 def test_agrega_sem_sobreposicao(self):
  raiz=Path(__file__).parents[1]
  with tempfile.TemporaryDirectory() as t:
   r=executar(raiz/"data/events.jsonl",Path(t)/"out.jsonl");self.assertEqual(len(r),4);self.assertEqual(r[0]["events"],2);self.assertEqual(r[0]["avg_temperature"],23.0);self.assertEqual(sum(x["events"] for x in r),5)
if __name__=="__main__":unittest.main()
