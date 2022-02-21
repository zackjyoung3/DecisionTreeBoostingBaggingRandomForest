import numpy as np
from ConfusionMatrix import ConfusionMatrix


# class that will be used to accumulate performance across folds
class PerformanceAccumulator:
    def __init__(self):
        self.acumm_metrics = np.zeros(7)
        self.performances_added = 0

    def __iadd__(self, performance):
        self.acumm_metrics[0] += performance.get_accuracy()
        self.accum_metrics[1] += performance.get_micro_precision()
        self.accum_metrics[2] += performance.get_micro_recall()
        self.accum_metrics[3] += performance.get_micro_f1()
        macro = performance.all_macro()
        self.accum_metrics[4] += macro["macro_precision"]
        self.accum_metrics[5] += macro["macro_recall"]
        self.accum_metrics[6] += macro["macro_f1"]
        self.performances_added += 1

    def get_averages(self):
        return self.acumm_metrics/self.performances_added


# Class that represent the accumulated performance metrics for a classifier
class Performance:
    # Performance constructor that will create a performance object for a problem with n classes
    def __init__(self, n_classes):
        self.confusionMx = ConfusionMatrix(n_classes)
        self.n_classes = n_classes

    # using np arrays of actual values vs predicted values, populate the confusion matrix
    def populate_confusion_mx(self, actuals, predicted_vals):
        # increment the vals in the confusion mx appropriately
        for actual, predicted in zip(actuals, predicted_vals):
            self.confusionMx.add(int(actual), int(predicted))

        # print(self.confusionMx.confusionMx)

    # method that will compute the accuracy from the confusion mx
    def get_accuracy(self):
        # tp+tn/(tp+tn+fp+fp)
        # for this, just do correct/total
        correct = 0
        for i in range(self.n_classes):
            correct += self.confusionMx.get_tp(i)
        total = self.confusionMx.total_predictions

        return correct / total

    # method that will get the precision for the class label passed in
    def get_precision(self, class_label):
        tp = self.confusionMx.get_tp(class_label)
        fp = self.confusionMx.get_fp(class_label)

        # precision is tp/(tp+fp)
        return tp / (tp + fp)

    # method that will return the recall for the class label passed in
    def get_recall(self, class_label):
        tp = self.confusionMx.get_tp(class_label)
        fn = self.confusionMx.get_fn(class_label)

        # recall is tp / (tp + fn)
        return tp / (tp + fn)

    # method that will return the f1 measure for the class label passed in
    def get_f1(self, class_label):
        recall = self.get_recall(class_label)
        precision = self.get_precision(class_label)

        # f1 is 2*r*p/(r+p)
        return 2 * recall * precision / (recall + precision)

    # method that will return the macro performance metric for the performance measure that is passed in
    # note macro averaging is assigning an equal weight to each class label's measure
    def macro(self, metric_function):
        # accumulate the precision across all class labels
        accum_metric = 0
        for i in range(self.n_classes):
            accum_metric += metric_function(i)

        return accum_metric / self.n_classes

    # method that will return a dictionary with all macro metrics
    def all_macro(self):
        return {'macro_precision': self.macro(self.get_precision),
                'macro_recall': self.macro(self.get_recall),
                'macro_f1': self.macro(self.get_f1)}

    # method that will get the micro precision assigning an equal weight to each record
    def get_micro_precision(self):
        # accumulate tp and fn over all class labels
        tp = 0
        fp = 0
        for i in range(self.n_classes):
            tp += self.confusionMx.get_tp(i)
            fp += self.confusionMx.get_fp(i)

        # return micro precision
        return tp / (tp + fp)

    # method that will return the micro recall assigning an equal weight to each record
    def get_micro_recall(self):
        # accumulate tp and fn over all class labels
        tp = 0
        fn = 0
        for i in range(self.n_classes):
            tp += self.confusionMx.get_tp(i)
            fn += self.confusionMx.get_fn(i)

        # return micro recall
        return tp / (tp + fn)

    # method that will return the micro f1 measure assigning an equal weight to each record
    def get_micro_f1(self):
        micro_recall = self.get_micro_recall()
        micro_precision = self.get_micro_precision()

        # f1 is 2*r*p/(r+p) and now want micro measure
        return 2 * micro_recall * micro_precision / (micro_recall + micro_precision)
