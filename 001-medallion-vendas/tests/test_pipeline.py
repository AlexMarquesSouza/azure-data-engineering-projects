import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from src.pipeline import executar


class PipelineTest(unittest.TestCase):
    def test_separa_rejeitados_e_agrega_receita(self):
        raiz = Path(__file__).parents[1]
        with tempfile.TemporaryDirectory() as temporario:
            saida = Path(temporario)
            relatorio = executar(raiz / "data/input/vendas.csv", saida)

            self.assertEqual(relatorio["registros_validos"], 4)
            self.assertEqual(relatorio["registros_rejeitados"], 3)

            with (saida / "gold/vendas_diarias.csv").open(newline="", encoding="utf-8") as arquivo:
                gold = list(csv.DictReader(arquivo))
            self.assertEqual(len(gold), 3)
            self.assertEqual(sum(Decimal(linha["receita"]) for linha in gold), Decimal("2868.40"))

    def test_reexecutar_mantem_um_unico_arquivo_bronze(self):
        raiz = Path(__file__).parents[1]
        with tempfile.TemporaryDirectory() as temporario:
            saida = Path(temporario)
            executar(raiz / "data/input/vendas.csv", saida)
            executar(raiz / "data/input/vendas.csv", saida)
            self.assertEqual(len(list((saida / "bronze").glob("*.csv"))), 1)


if __name__ == "__main__":
    unittest.main()
