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
        if eventType == "StdLooseJpsi2MuMuTuple":
            return True
        else:
            return False


    def Fill(self, tree):
        print "Begin fill RooFitMassJPsi with"
        branchName="MM"
        self.histogramName="h_"+branchName
        cmd= branchName+ ">>" + self.histogramName

        tree.tree.Draw(cmd)
        self.histograms[self.histogramName]= gROOT.FindObject(self.histogramName)
        print "End of fill RooFitMassJPsi"


    def ProcessData(self):
        # this is a little bit silly but without default initialization of RooFit object the program doesnt work
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

        nsig= RooRealVar("nsig","#signal events",39600,0.,1e10)
        nsig1= RooFormulaVar("nsig1","@0 * @1",RooArgList(frac,nsig))
        nsig2=RooFormulaVar("nsig2","@0 * @1",RooArgList(frac2,nsig))
        nbkg=RooRealVar("nbkg","#background events",2430,100,1e10)

        #create the model
        model = RooAddPdf("model","(g1+g2)+a",RooArgList(gauss1,gauss2,background),RooArgList(nsig1,nsig2,nbkg))

        # get data
        ral = RooArgList(x) # according to RooTalk advice
        data=RooDataHist("data","data",ral,RooFit.Import(self.histograms[self.histogramName]))
        #fit to data and

        result=model.fitTo(data,RooFit.Extended(), RooFit.Minos(), RooFit.Save())
        self.histograms["fited"]=data

        # create output
        xframe=x.frame(RooFit.Title("Mass Fit JPsi"))
        data.plotOn(xframe,RooFit.Name("data"),RooFit.DataError(RooAbsData.SumW2))
        model.plotOn(xframe, RooFit.Name("model"))
        model.plotOn(xframe, RooFit.Components("gauss1"),RooFit.LineColor(kBlack), RooFit.LineStyle(ROOT.kDashed))
        model.plotOn(xframe, RooFit.Components("gauss2"),RooFit.LineColor(kGreen), RooFit.LineStyle(kDashed))
        model.plotOn(xframe, RooFit.Components("background"),RooFit.LineColor(kRed),RooFit. LineStyle(kDashed))
        self.histograms["Fit"]=xframe
        ################### residual and pull distributions ######################################
        hresid = xframe.residHist("data","model")

        #Construct a histogram with the pulls of the data w.r.t the curve
        hpull = xframe.pullHist("data","model")
        #Create a new frame to draw the residual distribution and add the distribution to the frame
        frame1 = x.frame(RooFit.Title("Residual Distribution"))
        frame1.addPlotable(hresid,"P")
        self.histograms["Residual"]=frame1

        #Create a new frame to draw the pull distribution and add the distribution to the frame
        frame2 = x.frame(RooFit.Title("Pull Distribution"))
        frame2.addPlotable(hpull,"P")
        self.histograms["Pull"]=frame2


    def SaveOutput(self):
        gDirectory.mkdir("RooFitMassJPsi")
        gDirectory.cd("RooFitMassJPsi")
        for histogram in self.histograms.itervalues():
            histogram.Write()


    def ClearData(self):

        self.histograms= { }



