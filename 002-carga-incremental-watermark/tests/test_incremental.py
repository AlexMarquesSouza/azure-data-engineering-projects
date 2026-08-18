import csv, tempfile, unittest
from pathlib import Path
from src.incremental import executar

class TestIncremental(unittest.TestCase):
    def test_segunda_execucao_nao_recopia(self):
        raiz=Path(__file__).parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            t=Path(tmp); primeira=executar(raiz/"data/input/clientes.csv",t/"delta.csv",t/"state.json"); segunda=executar(raiz/"data/input/clientes.csv",t/"delta.csv",t/"state.json")
            self.assertEqual(primeira["registros_extraidos"],3); self.assertEqual(segunda["registros_extraidos"],0)
    def test_novo_registro_avanca_watermark(self):
        with tempfile.TemporaryDirectory() as tmp:
            t=Path(tmp); entrada=t/"in.csv"; entrada.write_text("cliente_id,nome,email,atualizado_em\n1,A,a@x.com,2026-08-04T10:00:00Z\n",encoding="utf-8")
            r=executar(entrada,t/"out.csv",t/"state.json"); self.assertEqual(r["watermark_atual"],"2026-08-04T10:00:00+00:00")
if __name__ == "__main__": unittest.main()
