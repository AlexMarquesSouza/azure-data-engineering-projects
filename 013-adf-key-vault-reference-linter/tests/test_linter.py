import unittest
from src.linter import lint
class TestLinter(unittest.TestCase):
    def test_safe_reference(self):
        s=[{"name":"kv","properties":{"typeProperties":{}}},{"name":"db","properties":{"typeProperties":{"password":{"type":"AzureKeyVaultSecret","secretName":"db-pass","store":{"referenceName":"kv"}}}}}]; self.assertTrue(lint(s)["compliant"])
    def test_plaintext(self): self.assertFalse(lint([{"name":"db","properties":{"typeProperties":{"password":"unsafe"}}}])["compliant"])
    def test_unknown_store(self):
        s=[{"name":"db","properties":{"typeProperties":{"password":{"type":"AzureKeyVaultSecret","secretName":"x","store":{"referenceName":"missing"}}}}}]; self.assertEqual(lint(s)["findings"][0]["severity"],"MEDIUM")
if __name__=="__main__": unittest.main()
