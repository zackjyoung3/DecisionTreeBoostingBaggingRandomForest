from abc import ABC, abstractmethod
from copy import deepcopy


# abstract base class of a classifier
class Classifier(ABC):
    # method that must be overridden that will train the model on a training set passed in
    @abstractmethod
    def train(self, train_set):
        pass

    # method that will test the trained model on a test set and return the performance that is obtained
    @abstractmethod
    def test(self, test_set):
        pass

    # method that will use the trained model to classify a single observed example
    @abstractmethod
    def classify(self, observed_example):
        pass

    # method that will be used to create a deep copy of a classifier
    def clone(self):
        return deepcopy(self)


