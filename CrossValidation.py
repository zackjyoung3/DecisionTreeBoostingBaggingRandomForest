from DataSet import DataSet
from Performance import Performance, PerformanceAccumulator


# class that will be used for k fold cross validation
class CrossValidation:
    # constructor for CrossValidation
    # by default 10-fold cross validation
    def __init__(self, data_set, classifier, k=10):
        self.k = k
        self.classifier = classifier
        self.data_set = data_set

    # method that will perform k fold cross validation
    def evaluate(self):
        self.data_set.get_k_folds(self.k)
        total_performance = PerformanceAccumulator()
        for i in range(self.k):
            cloned_classifer = self.classifier.clone()
            train_test = self.data_set.train_test_holdout(i)
            cloned_classifer.train(train_test.train)
            performance = cloned_classifer.test(train_test.test)
            total_performance += performance

        return total_performance.get_averages()
