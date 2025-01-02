import csv


class CsvReader:
    def __init__(self, filename: str, delimiter: str = '|'):
        self.filename = filename
        self.delimiter = delimiter

    def read(self):
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file, delimiter=self.delimiter)
            return list(reader)