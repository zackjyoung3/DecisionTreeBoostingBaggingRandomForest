import sqlite3
import numpy as np
from Attributes import Attributes, NumericAttribute, CategoricalAttribute
from Examples import Examples


# class that will hold all the information for a dataset
class DataSet:
    # constructor where the title of the file that contains the information for the dataset is passed in as a parameter
    def __init__(self, title):
        self.title = title
        self.source_file = title + ".db"
        self.attributes = Attributes()
        self.examples = None

    def load_data(self):
        # connecting to the sqlite that contains the data
        conn = sqlite3.connect(self.source_file)
        cursor = conn.cursor()

        # load all of the attributes for this dataset
        connection_string = '''SELECT * FROM ''' + self.title + 'Attributes'
        attributes_data = cursor.execute(connection_string)
        self.attributes.parse_attributes(attributes_data)
        self.examples = Examples(self.attributes)

        # load all of the examples for this dataset
        connection_string = '''SELECT * FROM ''' + self.title
        examples_data = cursor.execute(connection_string)
        self.examples.parse_examples(examples_data)

    def __str__(self):
        data_set_str = "Title: " + self.title + "\n\n" + str(self.attributes) + "\n" + str(self.examples)
        return data_set_str
