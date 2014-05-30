__author__ = 'ADendek'



from AlgorithmBase import *
from ROOT import  *



class CorrelationAnalysis(AlgorithmBase):

    def __init__(self):
        print "initialization Correlation Algorithm "
        self.chi2Types=["chi2PerDof","chi2PerDofVelo","chi2PerDofT","chi2PerDofTTHits","chi2PerDofTTAndMatch","chi2PerDofVeloTMatch"]
        self.corrTypes=["p","pt"]
        self.histograms={}
        self.isIntialized=False



    def NeedToBeFilledInLoop(self):
        return True

    def NeedToBeRun(self,eventType):
        return True


    def Fill(self, tree):
        #check if histograms has been initialized
        if not self.isIntialized:
            self._initHistograms(tree)

        #chi2 correlations
        for histogramName in self.histograms.iterkeys():
            #retrive values names
            xValueName=histogramName[len("h_"):histogramName.find("_vs_")]
            yValueName=histogramName[histogramName.find("_vs_")+len("_vs_"):]
            #retrive values. It is little bit tricky
            xValue=tree.tree.GetLeaf(xValueName).GetValue()
            yValue=tree.tree.GetLeaf(yValueName).GetValue()
            self.histograms[histogramName].Fill(xValue,yValue)




    def ProcessData(self):
        for histogramName, histogram in self.histograms.iteritems():
            #process filename
            xAxisName=histogramName[len("h_"):histogramName.find("_vs_")]
            yAxisName=histogramName[histogramName.find("_vs_")+len("_vs_"):]
            # set axis name
            histogram.GetYaxis().SetTitle(yAxisName)
            histogram.GetXaxis().SetTitle(xAxisName)
            #set name
            histogram.SetName("profile of "+xAxisName+" versus "+ yAxisName)

    def SaveOutput(self):
        gDirectory.mkdir("Correlation")
        gDirectory.cd("Correlation")
        for histogram in self.histograms.itervalues():
            histogram.SetDrawOption("CONT4 ")
            histogram.Write()


    def ClearData(self):
        self.histograms={}
        self.isIntialized=False

    def _initHistograms(self,tree):
        #initialize chi2 histograms
        for corrType in self.corrTypes:
            for chi2Type in self.chi2Types:
                branchChi2Name="track0."+chi2Type
                self._initHistogram(tree,corrType,branchChi2Name)
                branchChi2Name="track1."+chi2Type
                self._initHistogram(tree,corrType,branchChi2Name)
        self.isIntialized=True


    def _initHistogram(self,tree,nameX, nameY):
        #get values of TH2D ranges
        xMin,xMax=self._getHistogramRange(tree,nameX)
        yMin,yMax=self._getHistogramRange(tree,nameY)
        histogram_name="h_"+nameX+"_vs_"+nameY

        #create TH2D object
        binNumber=20
        histogram=TH2D(histogram_name,histogram_name,binNumber,xMin,xMax,binNumber,yMin,yMax)
        self.histograms[histogram_name]= histogram



    def _getHistogramRange(self,tree,branch):
        histogramName="h_"+branch
        cmd= branch+">>" + histogramName
        tree.tree.Draw(cmd)
        tmpHistogram= gROOT.FindObject(histogramName)
        xMax=tmpHistogram.GetXaxis().GetXmax()
        xMin=tmpHistogram.GetXaxis().GetXmin()
        return xMin,xMax