__author__ = 'Adam Dendek'
from ROOT import *
from Exceptions import  *
import os.path

class NTupleHandler(object):

    def __init__(self, fileName, eventType):
        self.getTree(fileName, eventType)





    def getTree(self,fileName, eventType):
        if not os.path.isfile(fileName):
            raise InputError( fileName)
        self.f = TFile(fileName, 'read')
        if self.f is None:
            raise InputError("openError"+fileName)
        self.dir=self.f.Get(eventType)
        if self.dir is None:
            raise InputError("directory Error"+eventType)
        self.tree =self.dir.Get('particle')

    def getEntry(self):
        return self.tree.GetEntriesFast()
