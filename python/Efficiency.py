from __future__ import division
__author__ = 'ADendek'

from AlgorithmBase import *
from ROOT import  *
from array import array

class Efficiency(AlgorithmBase):

    def __init__(self):
        print "initialization Efficiency "
        self.histograms= { }
        self._initDictionary()

    def NeedToBeFilledInLoop(self):
        return True

    def NeedToBeRun(self,eventType):
        self._setMcPid(eventType)
        return True


    def Fill(self, tree):
        #print "Fill Efficiency"
        p=tree.tree.p
        eta=tree.tree.eta
        pt=tree.tree.pt
        if tree.tree.truepid == self.PID:
            self._fillTrueDictionary(p,pt,eta)
        self._fillAllDictionary(p,pt,eta)

    def ProcessData(self):
        self._fillHistogram("eta",self.etaTrue,self.etaAll)
        self._fillHistogram("pt",self.ptTrue,self.ptAll)
        self._fillHistogram("p",self.pTrue,self.pAll)


    def SaveOutput(self):
        gDirectory.mkdir("Efficiency")
        gDirectory.cd("Efficiency")
        for histogram in self.histograms.itervalues():
            histogram.Write()


    def ClearData(self):
        self.histograms= { }

    def _setMcPid(self,eventType):
        if eventType == "StdLooseJpsi2MuMuTuple":
            self.PID=443 # pid of J/Psi
        else:
            self.PID=310 # pid of Ks

    def _initDictionary(self):
        self.etaTrue={k: 0. for k in range(2,10)}
        self.etaAll={k: 0. for k in range(2,10)}
        self.ptTrue={k: 0. for k in range(0,20)}
        self.ptAll={k: 0. for k in range(0,20)}
        self.pTrue={k: 0. for k in range(0,200,2)}
        self.pAll={k: 0. for k in range(0,200,2)}


    def _fillDictionary(self,value,dictionary):
        for key in dictionary.iterkeys():
            if key>=value:
                dictionary[key]+=1
                return

    def _fillAllDictionary(self,p,pt,eta):
        self._fillDictionary(eta,self.etaAll)
        self._fillDictionary(p,self.pAll)
        self._fillDictionary(pt,self.ptAll)

    def _fillTrueDictionary(self,p,pt,eta):
        self._fillDictionary(eta,self.etaTrue)
        self._fillDictionary(p,self.pTrue)
        self._fillDictionary(pt,self.ptTrue)


    def _fillHistogram(self,name,dictionaryTrue,dictionaryAll):
        numerator =dictionaryTrue.values()
        denominator=dictionaryAll.values()
        fraction=[]
        for num,den in zip(numerator,denominator):
            if num != 0:
                fraction.append(float(num)/den)
            else:
                fraction.append(0)
        x= array('d',dictionaryAll.keys())
        y= array('d',fraction)

        print numerator
        print denominator
        print fraction
        self.histograms[name]=TGraph(len(y),x, y)
        self.histograms[name].SetTitle("efficiency_vs_"+name)
        self.histograms[name].SetName("efficiency_vs_"+name)
        self.histograms[name].GetYaxis().SetTitle("efficiency")
        self.histograms[name].GetXaxis().SetTitle(name)
        self.histograms[name].GetYaxis().SetRangeUser(0.1,1.1)



