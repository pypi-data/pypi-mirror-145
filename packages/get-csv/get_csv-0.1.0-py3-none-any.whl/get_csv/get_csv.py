import csv

class get_csv:
    """
    Initiate a get csv operation.
    Please declare your location path
    """
    def __init__(self, location):
        self.location = location
    def get_header_name(location):
        with open(location) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            header = next(csv_reader)
            print(header)