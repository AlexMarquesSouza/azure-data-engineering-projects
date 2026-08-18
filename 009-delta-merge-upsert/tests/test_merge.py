import tempfile,unittest,csv
from pathlib import Path
from src.merge import executar
class T(unittest.TestCase):
 def test_merge(self):
  r=Path(__file__).parents[1]
  with tempfile.TemporaryDirectory() as t:
   o=Path(t)/"o.csv";x=executar(r/"data/target.csv",r/"data/updates.csv",o)
   with o.open(newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
   self.assertEqual(x,{"inserted":1,"updated":1,"rows":3});self.assertEqual(rows[0]["city"],"Campinas")
