__author__ = 'ADendek'

from AlgorithmBase import *
from ROOT import *

class RooFitMassJPsi(AlgorithmBase):
    def __init__(self):
        print "initialization Chi2Analyzer "
        self.histograms= { }
        self.result=''


    def NeedToBeFilledInLoop(self):
        return False

    def NeedToBeRun(self,eventType):
        if eventType == "StdLooseKsLLTuple":
            return True
        else:
            return False


    def Fill(self, tree):
        print "Begin fill RooFitMassJPsi with"
        histogramName="MM"

        tree.tree.Draw(histogramName)
        self.histograms[histogramName]= gROOT.FindObject(histogramName)
        print "End of fill RooFitMassJPsi"


    def ProcessData(self):
        x= RooRealVar("x","mass JPsi",3.03,3.17,"GeV")

        mean1= RooRealVar("mean1","mean1",3.1,0,10)
        mean2= RooRealVar("mean2","mean2",3.0,0,10)
        sigma1= RooRealVar("sigma1","sigma1",5,0,10)
        sigma2= RooRealVar("sigma2","sigma2",8,0,10)

        gauss1= RooGaussian("gauss1","gauss1 PDF",x,mean1,sigma1)
        gauss2= RooGaussian("gauss2","gauss2 PDF",x,mean2,sigma2)
        lambdaa= RooRealVar("lambdaa", "slope",-9.9,-20,20)
        background= RooExponential("background","background",x,lambdaa)

        frac= RooRealVar("frac","signal fraction",0.1,0.,1.)
        frac2= RooRealVar ("frac2","signal fraction",0.3,0.,1.)

        nsigRooRealVar= RooRealVar("nsig","#signal events",39600,0.,1e10)
        nsig1RooRealVar= RooFormulaVar("nsig1","@0 * @1",RooArgList(frac,nsig))
        RooFormulaVar= nsig2("nsig2","@0 * @1",RooArgList(frac2,nsig))
        RooRealVar= nbkg("nbkg","#background events",2430,100,1e10)

        model = RooAddPdf("model","(g1+g2)+a",RooArgList(gauss1,gauss2,background),RooArgList(nsig1,nsig2,nbkg))

        data=RooDataHist("data","data",x,Import(self.histograms["MM"]))
        self.result=model.fitTo(data,RooFit.Extended(), RooFit.Minos(), RooFit.Save())






    def SaveOutput(self):
        gDirectory.mkdir("RooFitMassJPsi")
        gDirectory.cd("RooFitMassJPsi")
        for histogram in self.histograms.itervalues():
            histogram.Write()
        self.result.Write()


    def ClearData(self):
        self.histograms= { }
