import unittest

from raghav import StringFunc

class Test(unittest.TestCase):
    def test_first_char(self):
        self.assertEqual(StringFunc.first_char("datadog"), "d")
        self.assertEqual(StringFunc.first_char("software"), "s")

    def test_last_char(self):
        self.assertEqual(StringFunc.last_char("datadog"), "g")
        self.assertEqual(StringFunc.last_char("software"), "e")
        
    def test_reverse(self):
        self.assertEqual(StringFunc.reverse("godatad"), "datadog")
        self.assertEqual(StringFunc.reverse("erawtfos"), "software")
