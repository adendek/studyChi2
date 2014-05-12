__author__ = 'Adam Dendek'


class AnalysisError(Exception):
    """Base class for exceptions in this analysis.    Attributes:
        expr -- input expression in which the error occurred
       """
    def __init__(self):
        self.msg = 'some error occurred'
    pass

class InputError(AnalysisError):
    """Exception raised for errors in the input.

    file -- filename
    """
    def __init__(self, file):
        self.msg="File open error " + file







