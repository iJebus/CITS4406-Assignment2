__author__ = 'Liam'from collections import Counterfrom statistics import mean, mode, median_low, median, median_highclass Analyser(object):    def __init__(self, clean_data):        self.common_types = Counter(clean_data).most_common(5)        self.mode = mode(clean_data)'''def match(col_data): return truedef report(col_data): return {}'''class StringAnalyser(Analyser):    def __init__(self, string_data):        super().__init__(string_data)        #  TODO Implement some string exclusive statistics.class NumericalAnalyser(Analyser):    def __init__(self, numerical_data):        super().__init__(numerical_data)        self.min = min(numerical_data)        self.max = max(numerical_data)        self.mean = mean(numerical_data)        self.median_low = median_low(numerical_data)        self.median = median(numerical_data)        self.median_high = median_high(numerical_data)    '''    def report(col_data): {'min': min(col_data)}'''"""class IntegerAnalyser(Analyser):"""