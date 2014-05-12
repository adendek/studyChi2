__author__ = 'ja'

import unittest
from NTupleHandler import *
from Exceptions import  *


class MyTestCase(unittest.TestCase):

    def testHandlerInitializationShouldnotRised(self):
        try:
            handler= NTupleHandler('../data/new_NTuple.root','StdLooseJpsi2MuMuTuple')

        except AnalysisError as e:
            self.failureException()
    def testHandlerShouldReturnNoEvents(self):

        handler= NTupleHandler('../data/new_NTuple.root','StdLooseJpsi2MuMuTuple')
        self.assertLess(handler.getEntry(),10)
        handler.getEntry()

if __name__ == '__main__':
     unittest.main()

