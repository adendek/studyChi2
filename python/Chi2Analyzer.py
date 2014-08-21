__author__ = 'ja'

from AlgorithmBase import *
from ROOT import  *



class Chi2Analyzer(AlgorithmBase):

    def __init__(self):
        print "initialization Chi2Analyzer "
        self.histograms= { }

    def NeedToBeFilledInLoop(self):
        return False

    def NeedToBeRun(self,eventType):
        return True


    def Fill(self, tree):
        print "Fill Chi2Analyzer"
        self._findHistogram(tree, "chi2PerDof")
        self._findHistogram(tree, "chi2PerDofVelo")
        self._findHistogram(tree, "chi2PerDofT")
        self._findHistogram(tree, "chi2PerDofTTHits")
        self._findHistogram(tree, "chi2PerDofTTAndMatch")
        self._findHistogram(tree, "chi2PerDofVeloTMatch")


    def ProcessData(self):
        for histogram in self.histograms.itervalues():
            histogram.GetYaxis().SetTitle("Entry")

    def SaveOutput(self):
        gDirectory.mkdir("Chi2Analyzer")
        gDirectory.cd("Chi2Analyzer")
        for histogram in self.histograms.itervalues():
            histogram.Write()


    def ClearData(self):
        self.histograms= { }

    def _findHistogram(self, tree, name):
        print "Begin fill Chi2Analyzer with "+name
        histogram_name="h_"+name
        histogram_name1=histogram_name+"_track0"
        histogram_name2=histogram_name+"_track1"


        cmd1= "track0." + name + ">>" + histogram_name1
        cmd2= "track1." + name + ">>" + histogram_name2

        cutCommand1="track0."+name+"<12"
        cutCommand2="track1."+name+"<12"

        tree.tree.Draw(cmd1,cutCommand1)
        tree.tree.Draw(cmd2,cutCommand2)
        self.histograms[histogram_name1]= gROOT.FindObject(histogram_name1)
        self.histograms[histogram_name2]= gROOT.FindObject(histogram_name2)
        print "End of fill Chi2Analyzer with "+name


