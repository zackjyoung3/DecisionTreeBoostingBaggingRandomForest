import numpy as np



# Class that represents a confusion matrix
class ConfusionMatrix:
    # constructor for a confusion matrix in an n class problem
    def __init__(self, n_classes):
        self.confusionMx = np.zeros((n_classes, n_classes))
        self.n_classes = n_classes
        self.total_predictions = 0

    # method that will add a prediction to the appropriate location in the confusion mx
    def add(self, actual, predicted):
        self.confusionMx[int(actual)][int(predicted)] += 1
        self.total_predictions += 1

    # method that will return the number of true positives for the class label passed in
    def get_tp(self, class_label):
        # all true positive are stored at the row for actual = class_label and column predicted = class_label
        return self.confusionMx[class_label][class_label]

    # method that will return the number of true negative predictions for the class label passed in
    def get_tn(self, class_label):
        # true negative count
        tn = 0
        # true negative is the sum of all the rows and columns excluding those for the class_label passed in
        for i in range(self.n_classes):
            if i != class_label:
                for j in range(self.n_classes):
                    if j != class_label:
                        tn += self.confusionMx[i][j]

        return tn

    # method that will return the number of false negative predictions for the class label passed in
    def get_fn(self, class_label):
        # false negative count
        fn = 0
        # the sum of all the vals in the row for the class_label excluding tp
        for i in range(self.n_classes):
            if i != class_label:
                fn += self.confusionMx[class_label][i]

        return fn

    # method that will return the number of false positive predictions for the class label passed in
    def get_fp(self, class_label):
        # false positive count
        fp = 0
        # the sum of all the vals in the column for the class_label excluding tp
        for i in range(self.n_classes):
            if i != class_label:
                fp += self.confusionMx[i][class_label]

        return fp