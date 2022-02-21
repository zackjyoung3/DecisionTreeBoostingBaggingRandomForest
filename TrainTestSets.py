# class representing a training and testing dataset
class TrainTestSets:
    # constructor that will create a TrainTestSets from training and testing datasets passed in
    def __init__(self, train, test):
        self.train = train
        self.test = test

    def __str__(self):
        return "Train-" + str(self.train) + "\n\nTest-" + str(self.test)
