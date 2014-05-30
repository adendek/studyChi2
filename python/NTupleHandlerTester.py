__author__ = 'ja'

import unittest
from NTupleHandler import *
from Exceptions import  *


class MyTestCase(unittest.TestCase):

    def testHandlerInitializationShouldnotRised(self):
        try:
            handler= NTupleHandler('../data/MC.root','StdLooseJpsi2MuMuTuple')

        except AnalysisError as e:
            self.failureException()
    def testHandlerShouldReturnNoEvents(self):

        handler= NTupleHandler('../data/MC.root','StdLooseJpsi2MuMuTuple')
        self.assertGreater(handler.getEntries(),0)


if __name__ == '__main__':
     unittest.main()

