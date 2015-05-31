__author__ = 'Liam'

import csv


class Reader(object):
    def __init__(self, csv_file):
        self.csv_data, self.invalid_data = self.data_reader(csv_file)

    @staticmethod
    def data_reader(csv_file):
        read_data = csv.reader(open(csv_file, 'r'))

        rows = []
        invalid_data = []
        for row in read_data:
            if len(rows) == 0:
                rows.append(row)
            elif len(row) != len(rows[0]):
                invalid_data.append(row)
            else:
                rows.append(row)

        csv_data = []
        for i in range(len(rows[0])):
            column = []
            for j in range(len(rows)):
                column.append(rows[j][i])
            csv_data.append([rows[0][i], column[1:]])

        return csv_data, invalid_data
