import tempfile,unittest
from pathlib import Path
from src.scd2 import executar,ler
class TestSCD2(unittest.TestCase):
 def test_preserva_historico_e_insere_novo(self):
  raiz=Path(__file__).parents[1]
  with tempfile.TemporaryDirectory() as t:
   out=Path(t)/"dim.csv";r=executar(raiz/"data/dimensao_atual.csv",raiz/"data/snapshot.csv",out,"2026-08-05");rows=ler(out)
   self.assertEqual(r,{"novos":1,"alterados":1,"inalterados":1,"versoes_totais":4});self.assertEqual(len([x for x in rows if x["cliente_id"]=="C001"]),2);self.assertEqual(len([x for x in rows if x["ativo"]=="true"]),3)
if __name__=="__main__":unittest.main()
