__author__ = 'ja'

import NTupleHandler
import abc
from ROOT import *

class AlgorithmBase(object):
    __metaclass__ = abc.ABCMeta


    def __init__(self):
        self.histograms= { }

    @abc.abstractmethod
    def Fill(self, tree):
        pass

    @abc.abstractmethod
    def ProcessData(self):
        pass

    @abc.abstractmethod
    def SaveOutput(self):
        pass
    @abc.abstractmethod
    def ClearData(self):
        pass

    @abc.abstractmethod
    def NeedToBeFilledInLoop(self):
        return False
