# This file is placed in the Public Domain.


"object programming tests"


import inspect
import os
import sys
import unittest


from obj import Object, keys, values
from otb import Table


import otb 


Table.add(otb)


class Test_Table(unittest.TestCase):

    def test_mod(self):
        self.assertTrue("otb" in keys(Table.mod))
