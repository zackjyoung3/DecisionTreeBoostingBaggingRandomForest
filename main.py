import numpy as np
from tests import test_confusion_mx
from Encoder import Encoder
from sklearn.datasets import load_wine
from sklearn.datasets import load_iris
import pandas as pd
from DataSet import DataSet
from Examples import Examples
from_sk = "sklearn import"

if __name__ == '__main__':
    # demonstrates the correctness of implementation for confusion mx through showing identical results to sklearn
    # test_confusion_mx()
    # hoss = Encoder("Iris", from_sk, load_iris)
    # hoss.get_data()
    # df = hoss.df
    # for header in df.columns.values:
    #     print(type(header))
    # for t in df.dtypes:
    #     print(t == float)
    # hoss.make_sp_sqlite()
    # hoss.header_test()

    test = DataSet("Iris")
    test.load_data()
    print(test)