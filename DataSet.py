import sqlite3
import numpy as np
from Attributes import Attributes, NumericAttribute, CategoricalAttribute
from Examples import Examples
from random import randint
from copy import deepcopy
from TrainTestSets import TrainTestSets

# class that will hold all the information for a dataset
class DataSet:
    def __init__(self, *args):
        # constructor where the title of the file that contains the information
        # for the dataset is passed in as a parameter
        if len(args) == 1:
            self.title = args[0]
            self.source_file = args[0] + ".db"
            self.attributes = Attributes()
            self.examples = None
            self.folds = None
            self.num_folds = None

        # constructor that will be used to create a training or testing data set
        else:
            self.title = args[0]
            self.source_file = args[0] + ".db"
            self.attributes = args[1]
            self.examples = Examples(args[1], args[2])

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

    # method that will be used to obtain k random folds
    def get_k_folds(self, k=10):
        self.num_folds = k
        # shuffling the examples to create a random ordering
        self.folds = self.examples.get_k_sets(k)

    # method that will obtain the train and test sets by holding out the ith fold for testing
    def train_test_holdout(self, i):
        train_sets = [fold for j, fold in enumerate(self.folds) if j != i]
        train_name = "Excluding fold " + str(i) + ":"
        train = DataSet(train_name, self.attributes, deepcopy(np.concatenate(train_sets, axis=0)))

        test_name = "From fold " + str(i) + ":"
        test = DataSet(test_name, self.attributes, deepcopy(self.folds[i]))

        return TrainTestSets(train, test)


