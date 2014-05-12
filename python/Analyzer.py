__author__ = 'ja'

from ROOT import *
from Exceptions import  *
import os.path


class Analyzer:
    def __init__(self, fileName, eventType):
        self.histograms={ }
        "initialization of the NTuple"



    def runAnalysis(self,fileName, eventType):
        if not os.path.isfile(fileName):
            raise InputError( fileName)
        f = TFile(fileName, 'read')
        if f is None:
            raise InputError("openError"+fileName)
        dir=f.Get(eventType)
        if dir is None:
            raise InputError("directory Error"+eventType)
        self.tree=dir.Get('particle')
        self.tree.Clone("particle")
        # start process
        self.basicPlots()

        # finalize process
        self.saveHistogramsIntoFile("../out/MC.root")



    def saveHistogramsIntoFile(self,fileOut):
        print isinstance(self.tree,TTree)
        fout=TFile(fileOut,"RECREATE")
        for histogram in self.histograms.itervalues():
            histogram.Write()
        fout.Close()

    def basicPlots(self):
                # put data into histograms
        self.tree.Draw("track0.chi2PerDof>>h_chi2PerDof_track0")
        self.tree.Draw("track1.chi2PerDof>>h_chi2PerDof_track1")

        self.histograms["h_chi2PerDof_track0"]= gROOT.FindObject("h_chi2PerDof_track0")
        self.histograms["h_chi2PerDof_track1"]= gROOT.FindObject("h_chi2PerDof_track1")
        list=TList()
        list.Add(self.histograms["h_chi2PerDof_track0"])
        list.Add(self.histograms["h_chi2PerDof_track1"])





if __name__ == "__main__":
    a=Analyzer('../data/new_NTuple.root','StdLooseJpsi2MuMuTuple')
    a.runAnalysis('../data/new_NTuple.root','StdLooseJpsi2MuMuTuple')