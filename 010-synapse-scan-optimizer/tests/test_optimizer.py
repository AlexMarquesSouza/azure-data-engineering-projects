import tempfile,unittest
from pathlib import Path
from src.optimizer import executar
class T(unittest.TestCase):
 def test_scan(self):
  r=Path(__file__).parents[1]
  with tempfile.TemporaryDirectory() as t:
   x=executar(r/"data/files.csv",Path(t)/"r.json");self.assertEqual(x["partition_scan_mb"],200);self.assertGreater(x["reduction_pct"],80)
