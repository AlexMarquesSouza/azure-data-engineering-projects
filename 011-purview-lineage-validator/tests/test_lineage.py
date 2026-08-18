import unittest
from src.lineage import audit
class TestLineage(unittest.TestCase):
    def test_chain(self):
        d={"assets":[{"id":"a","owner":"x","classification":"I"},{"id":"b","owner":"x","classification":"I"}],"flows":[{"source":"a","target":"b"}]}; self.assertTrue(audit(d)["valid"]); self.assertEqual(audit(d)["summary"]["sinks"],["b"])
    def test_cycle_and_unknown(self):
        d={"assets":[{"id":"a"},{"id":"b"}],"flows":[{"source":"a","target":"b"},{"source":"b","target":"a"},{"source":"x","target":"a"}]}; r=audit(d); self.assertFalse(r["valid"]); self.assertTrue(any("Ciclo" in x for x in r["errors"]))
if __name__=="__main__": unittest.main()
