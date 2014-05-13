__author__ = 'ja'
from Analyzer import *

if __name__ == "__main__":
    a=Analyzer('../data/new_NTuple.root',"../out/MC.root")
    a.runAnalysis()