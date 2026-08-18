import tempfile,unittest
from pathlib import Path
from src.router import executar
class TestRouter(unittest.TestCase):
 def test_filtra_roteia_e_deduplica(self):
  raiz=Path(__file__).parents[1]
  with tempfile.TemporaryDirectory() as t:
   r=executar(raiz/"data/events.jsonl",Path(t)/"r.json");self.assertEqual(r["routes"],{"sales":["e1"],"customers":["e2"],"ignored":["e3"]});self.assertEqual(r["duplicates_ignored"],1)
if __name__=="__main__":unittest.main()
