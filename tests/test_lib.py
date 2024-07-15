import unittest
from dtext import dtext

class TestLib(unittest.TestCase):

    def test_write(self):
        self.assertEqual(dtext.open("unittest.txt", text="testytest", temp=True), "testytest")


if __name__ == "__main__":
    unittest.main()