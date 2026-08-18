import unittest
from src.planner import plan
class TestPlanner(unittest.TestCase):
    def test_orders_affected_chain(self):
        t=[{"name":"a"},{"name":"b","depends_on":["a"]},{"name":"c","depends_on":["b"]},{"name":"x"}]; self.assertEqual(plan(t,"a")["rerun_order"],["a","b","c"])
    def test_unknown_dependency(self): self.assertFalse(plan([{"name":"a","depends_on":["x"]}],"a")["valid"])
    def test_cycle(self): self.assertFalse(plan([{"name":"a","depends_on":["b"]},{"name":"b","depends_on":["a"]}],"a")["valid"])
if __name__=="__main__": unittest.main()
