"""Reads CSV file for information, provides basic cleaning of data and then
runs analysis on said data."""

import csv
import re
from collections import Counter
from statistics import mean, mode, median_low, median, median_high, \
    StatisticsError, Decimal


#  Config
threshold = 0.9
invalid_values = ['-', '*', '_']
re_float = re.compile('^\d*?\.\d+$')
re_int = re.compile('^[1-9]\d*$')


class Analyser(object):
    """Base analysis class object. Initiate the object, and assigns the 
    statistical mode, if any.
    
    Class variables:
    mode -- Returns the mode of the column analysed.
    
    Child Classes and associated variables:
    StringAnalyser -- String column analysis.
    EnumAnalyser -- Enumerated column analysis.
    NumericalAnalyser - String/Float column analysis.
        min -- Minimum value in column values.
        max -- Maximum value in column values.
        mean -- Mean value in column values.
        median_low -- Low median for column values.
        median -- Median value for column values.
        median_high -- High median for column values.
                    
    """
    def __init__(self, values):
        try:
            self.mode = mode(values)
        except StatisticsError:
            self.mode = 'N/A'


class StringAnalyser(Analyser):
    """Run string analysis."""
    def __init__(self, values):
        super().__init__(values)
        #  TODO Implement some string exclusive statistics.


class EnumAnalyser(Analyser):
    """Run enumeration analysis."""
    def __init__(self, values):
        super().__init__(values)
        #  TODO Implement some enum exclusive statistics.


class NumericalAnalyser(Analyser):
    """Runs numeric analysis."""
    def __init__(self, values):
        values = [eval(i) for i in values]
        super().__init__(values)
        self.min = min(values)
        self.max = max(values)
        self.mean = Decimal(mean(values)).quantize(Decimal('.00000'))
        self.median_low = median_low(values)
        self.median = median(values)
        self.median_high = median_high(values)


class Column(object):
    """Object to hold data from each column within the provided CSV file.
    
    Methods:
    change_misc_values -- Removes misc/unclear values from column 
        values.
    drop_greater_than -- Removes '<', '>' from column values.
    define_most_common -- Sets object variable to hold 15 most common values
        for that column.
    define_type -- Sets object variable to type (e.g., String) according
        to column values.
    
    Variables:
    most_common -- <= 15 most common results within the column values.
    empty -- Boolean value of whether the column holds values or not.
    header -- Column header/title.
    type -- The type of data in column, e.g., String, Float, Integer,
        Enumerated.
    values -- List of CSV values for the column.
    analysis -- Analysis object associated with this column.
    outliers -- List of values in column but outside threshold of column type.

    """
    def __init__(self, header=''):
        self.most_common = []
        self.empty = False
        self.header = header
        self.type = ''
        self.values = []
        self.analysis = None
        self.outliers = []
        #  Todo: Does initialising as None even make sense?

    def change_misc_values(self):
        """
        Replaces identified values of unclear meaning or inexact value, i.e., 
        '-', with an agreed value.
        """
        for index, value in enumerate(self.values):
            if value in invalid_values:
                self.values[index] = ''
                
    def drop_greater_than(self):
        pass
        #  Todo: Implement method to handle (strip?) '<', '>'.

    def define_most_common(self):
        """Set 15 most common results to class variable, and set object variable 
        empty if appropriate.
        """
        self.most_common = Counter(self.values).most_common(15)
        if self.most_common[0][0] == '' \
                and self.most_common[0][1] / len(self.values) >= threshold:
            self.empty = True

    def define_type(self):
        """Run column data against regex filters and assign object variable type
        as appropriate.
        """
        float_count = 0
        int_count = 0
        boolean = ['true', 'false']
        #  Todo: Define date type.

        for value in self.values:
            if re_float.match(value):
                float_count += 1
            elif re_int.match(value):
                int_count += 1
        if float_count / len(self.values) >= threshold:
            self.type = 'Float'
        elif int_count / len(self.values) >= threshold:
            self.type = 'Integer'
        elif len(self.most_common) <= 2:
            if self.most_common[0][0].lower() in boolean:
                self.type = 'Bool'
        elif len(self.most_common) < 10:
            self.type = 'Enum'
        else:
            self.type = 'String'

    def define_outliers(self):
        if self.type == 'Float':
            for value in self.values:
                if not re_float.match(value):
                    self.outliers.append(value)
        elif self.type == 'Integer':
            for value in self.values:
                if not re_int.match(value):
                    self.outliers.append(value)


class Data(object):
    """Main store for CSV data, reading the data from the CSV file and then 
    assigning out to relevant variables.
    
    Methods:
    read -- Reads the CSV file and outputs to raw_data variable.
    remove_invalid -- Reads from raw_data variable and assigns rows to 
        valid_rows or invalid_rows according to their length.
    create_columns -- Creates column object according to valid_rows, assigning
        column header and column values.
    clean -- Calls column cleaning methods to run 'cleaning' on all columns.
    analyse -- Calls column analysis methods to run 'analysis' on all columns.
    
    Variables:
    columns -- List of column objects.
    headers -- List of column headers.
    invalid_rows -- List of invalid rows (i.e., more or less columns than
        number of headers).
    raw_data -- List of raw CSV data as rows.
    valid_rows -- List of valid rows (i.e., same number of columns as headers).
    """
    def __init__(self, csv_file):
        self.columns = []
        self.headers = []
        self.invalid_rows = []
        self.raw_data = []
        self.valid_rows = []
        self.read(csv_file)
        self.remove_invalid()
        self.create_columns()

    def read(self, csv_file):
        """Opens and reads the CSV file, line by line, to raw_data variable."""
        f = csv.reader(open(csv_file))
        for row in f:
            self.raw_data.append(row)

    def remove_invalid(self):
        """For each row in raw_data variable, checks row length and appends to 
        valid_rows variable if same length as headers, else appends to 
        invalid_rows variable.
        """
        for index, row in enumerate(self.raw_data):
            if len(row) != len(self.raw_data[0]):
                self.invalid_rows.append([index + 1, row])
            else:
                self.valid_rows.append(row)

    def create_columns(self):
        """For each row in raw_data variable, assigns the first value to the 
        headers variable and creates a Column object with that header provided.
        Then removes header row from valid_rows. (Todo: Maybe can read straight 
        from valid rows? Why/Why not?). Then for each row in valid_rows,
        populates relevant column object with row data.
        """
        for value in self.raw_data[0]:
            self.columns.append(Column(header=value))
            self.headers.append(value)
        self.valid_rows.pop(0)

        for row in self.valid_rows:
            for index, value in enumerate(row):
                self.columns[index].values.append(value)

    def clean(self):
        """Calls cleaning methods on all columns."""
        for column in self.columns:
            column.change_misc_values()
            column.drop_greater_than()

    def analyse(self):
        """Calls analysis methods on all columns, checking if they are empty
        first.
        """
        analysers = {'String': StringAnalyser, 'Integer': NumericalAnalyser,
                     'Float': NumericalAnalyser, 'Enum': EnumAnalyser}
        for column in self.columns:
            column.define_most_common()
            if not column.empty:
                column.define_type()
                column.define_outliers()
                if column.type in analysers:
                    column.analysis = analysers[column.type](column.values)
