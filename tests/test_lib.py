import unittest
from dtext import dtext

class TestLib(unittest.TestCase):

    def test_write(self):
        self.assertEqual(dtext.open("african.swallow", text="coconut", temp=True), "coconut") # "Are you suggesting coconuts migrate?"
    
    def test_incompatible_params(self):
        with self.assertRaises(ValueError) as err:
            dtext.open(".gitignore", text="this won't work", temp=True)

        self.assertIsInstance(err.exception, ValueError)

    def test_other_editor(self):
        self.assertEqual(dtext.open("matryoshka.doll", text="matryoshka.doll", editor="code", temp=True), "matryoshka.doll")

if __name__ == "__main__":
    unittest.main()