# This file is placed in the Public Domain.


"configuration tests"


import os
import sys


sys.path.insert(0, os.getcwd())


import unittest


from ofc import edit
from okr import Config
from obj import Object, update
from opr import parse


class Test_Config(unittest.TestCase):

    def test_parse(self):
        p = Config()
        parse(p, "mod=irc")
        self.assertEqual(p.sets.mod, "irc")

    def test_parse2(self):
        p = Config()
        parse(p, "mod=irc,rss")
        self.assertEqual(p.sets.mod, "irc,rss")

    def test_edit(self):
        d = Object()
        update(d, {"mod": "irc,rss"})
        edit(Config, d)
        self.assertEqual(Config.mod, "irc,rss")
