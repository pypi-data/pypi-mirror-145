# -*- coding: utf-8 -*-

# @File    : test_unit_info.py
# @Date    : 2022-01-19
# @Author  : chenbo

__author__ = 'chenbo'

import unittest

from loguru import logger


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'F0O')
        self.assertEqual('foo'.upper(), 'FOO')
        print(1111111)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    TestSuite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    test_result = unittest.TextTestRunner(verbosity=0).run(TestSuite)
    # logger.info(test_result)
    print('All case number')
    print(test_result.testsRun)
    print('Failed case number')
    print(len(test_result.failures))
    for case, reason in test_result.failures:
        print(case.id())
        print(reason)
    for case, reason in test_result.skipped:
        print(case.id())
        print(reason)

