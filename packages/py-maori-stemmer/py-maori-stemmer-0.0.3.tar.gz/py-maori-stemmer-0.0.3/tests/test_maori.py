# -*- coding: utf-8 -*-
import unittest

from py_maori_stemmer import MaoriStemmer


class Test(unittest.TestCase):
    def test(self):
        stemmer = MaoriStemmer()
        self.assertTrue('waihanga', stemmer.stemWord('waihangatia'))
        self.assertEqual(['i', 'waihanga', 'mō', 'ngā', 'akoma', 'kaupap'],
                         stemmer.stemWords('i waihangatia mō ngā akomanga kaupapa'.split(' ')))
