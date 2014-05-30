__author__ = 'ja'
from Analyzer import *

if __name__ == "__main__":
    a=Analyzer('../data/MC.root',"../out/MC_resid.root")
    a.runAnalysis()