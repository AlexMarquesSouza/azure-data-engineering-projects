import unittest
from src.advisor import advise
class TestAdvisor(unittest.TestCase):
    def test_recommends_optimize(self):
        rows=[{"partition":"p","size_mb":"4"} for _ in range(10)]; self.assertEqual(advise(rows)["partitions"][0]["action"],"OPTIMIZE")
    def test_healthy_files(self):
        rows=[{"partition":"p","size_mb":"100"},{"partition":"p","size_mb":"120"}]; r=advise(rows); self.assertEqual(r["optimize_count"],0); self.assertEqual(r["partitions"][0]["recommended_output_files"],2)
if __name__=="__main__": unittest.main()
