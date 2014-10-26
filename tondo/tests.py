# -*- coding: utf-8 -*-

import random
import unittest

import tondo

class TestSequenceFunctions(unittest.TestCase):

    JSON_ITEMS = [
        'content',
        'contributor',
        'type',
        'url'
    ]

    def setUp(self):
        self.json = tondo.loadjsons()

    def test_json_integrity(self):
        for json_file in self.json:
            for item in self.json[json_file]:
                self.assertListEqual(item.keys(), self.JSON_ITEMS)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)
