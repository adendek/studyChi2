__author__ = 'ja'

from ROOT import *
from Exceptions import  *
#algorithms
from Chi2Analyzer import *
from RooFitMassJPsi import  *
from RooFitMassKs import *
from CorrelationAnalysis import  *
from NTupleHandler import *
import os.path


class Analyzer(object):
    def __init__(self,dataFile , outFile):
        print "Start the analyzer"
        self.dataFile=dataFile
        # initialization of algorithm dictionary"
        self.algorithms={ }
        #self.algorithms["Chi2Analyzer"]=Chi2Analyzer()
        #self.algorithms["RooFitMassJPsi"]=RooFitMassJPsi()
        #self.algorithms["RooFitMassKs"]=RooFitMassKs()
        self.algorithms["CorrelationAnalysis"]=CorrelationAnalysis()
        # initialization of event types"
        self.eventTypes= ["StdLooseJpsi2MuMuTuple", "StdLooseKsLLTuple", "StdLooseKsDDTuple", "StdKs2PiPiLLTuple","StdKs2PiPiDDTuple" ]
        # create output file
        self.fout=TFile(outFile,"RECREATE")
        for eventType in self.eventTypes:
            self.fout.mkdir(eventType)


    def runAnalysis(self):
        for eventType in self.eventTypes:
            print "Start event type "+eventType
            tree=NTupleHandler(self.dataFile,eventType)
            # loop over algorithms
            for  algorithm in self.algorithms.itervalues():
                if not algorithm.NeedToBeRun(eventType):
                    continue
                # fill the historams
                if algorithm.NeedToBeFilledInLoop():
                    for event in range(tree.getEntries()):
                        tree.tree.GetEntry(event)
                        algorithm.Fill(tree)

                if not algorithm.NeedToBeFilledInLoop():
                    algorithm.Fill(tree)
                #process data
                algorithm.ProcessData()
                # save output
                self.fout.cd(eventType)
                algorithm.SaveOutput()
                #clear data
                algorithm.ClearData()

