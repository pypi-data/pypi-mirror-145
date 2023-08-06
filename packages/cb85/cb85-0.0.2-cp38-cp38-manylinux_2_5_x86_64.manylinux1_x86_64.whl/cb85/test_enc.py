import base64
import pyximport; pyximport.install()
import unittest

from .enc import b85encode

class TestEnc(unittest.TestCase):
    def assertSame(self, s):
        self.assertEqual(
            b85encode(s),
            base64.b85encode(s, pad=True)
        )

    def test_empty(self):
        self.assertSame(b'')

    def test_ascii(self):
        self.assertSame(bytes(range(256)))

    def test_a(self):
        self.assertSame(b'a' * 1)

    def test_aa(self):
        self.assertSame(b'a' * 2)

    def test_aaa(self):
        self.assertSame(b'a' * 3)

    def test_aaaa(self):
        self.assertSame(b'a' * 4)

    def test_aaaaa(self):
        self.assertSame(b'a' * 5)

if __name__ == '__main__':
    unittest.main()
