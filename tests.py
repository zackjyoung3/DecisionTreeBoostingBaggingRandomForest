from Performance import Performance
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score


# method that tests the confusion matrix and implemention of performance metrics
def test_confusion_mx():
    apples_actual = np.zeros(11)
    orange_actual = np.ones(12)
    mango_actual = np.full(13, 2)
    # actuals = np.concatenate(apples_actual, orange_actual, mango_actual)
    actuals = np.append(apples_actual, orange_actual)
    actuals = np.append(actuals, mango_actual)

    apples_predict = np.array([0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2])
    orange_predict = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2])
    mango_predict = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2])
    predictions = np.append(apples_predict, orange_predict)
    predictions = np.append(predictions, mango_predict)

    test = Performance(3)
    test.populate_confusion_mx(actuals, predictions)
    sk_confusion = confusion_matrix(actuals, predictions)
    print("Confusion Matrices")
    print("Test\n", test.confusionMx.confusionMx)
    print("sk\n", sk_confusion)
    print("Class   ", "    Precision         ", "    Recall     ", "F1")
    print("Apple   ", test.get_precision(0), test.get_recall(0), test.get_f1(0))
    print("Orange  ", test.get_precision(1), test.get_recall(1), test.get_f1(1))
    print("Mango   ", test.get_precision(2), test.get_recall(2), test.get_f1(2))
    print("Accuracy", test.get_accuracy())
    print("Accuracy sk:", accuracy_score(actuals, predictions))
    print("Micro precision: ", test.get_micro_precision())
    print("Micro Precision sk: ", precision_score(actuals, predictions, average='micro'))
    print("Micro recall: ", test.get_micro_precision())
    print("Micro Recall sk: ", recall_score(actuals, predictions, average='micro'))
    print("Micro f1: ", test.get_micro_f1())
    print("Micro F1-score sk: ", f1_score(actuals, predictions, average='micro'))
    macros = test.all_macro()
    i = 0
    for key in macros.keys():
        print("Macro", key, ":", macros[key])
        if i == 0:
            print('Macro Precision sk: ', precision_score(actuals, predictions, average='macro'))
        elif i == 1:
            print('Macro Recall sk: ', recall_score(actuals, predictions, average='macro'))
        else:
            print('Macro F1-score sk: ', f1_score(actuals, predictions, average='macro'))
        i +=1