import numpy as np
from Attributes import Attributes
from copy import deepcopy


# class that will contain all of the examples for a dataset
class Examples:
    def __init__(self, *args):
        if len(args) == 1:
            self.examples = None
            self.example_weights = None
            self.attributes = args[0]
        else:
            self.examples = args[1]
            self.example_weights = None
            self.attributes = args[0]

    def __setitem__(self, key, value):
        self.examples[key] = value

    def __getitem__(self, item):
        return self.examples[item]

    def __delitem__(self, key):
        self.examples.pop(key)

    def append(self, attribute):
        self.examples.append(attribute)

    def __len__(self):
        return len(self.examples)

    def __str__(self):
        ex_string = "Examples:"
        for example in self.examples:
            ex_string += "\n"
            for attribute_val, attribute in zip(example, self.attributes):
                if attribute.is_numeric:
                    ex_string += str(attribute_val) + " "
                else:
                    ex_string += str(attribute[attribute_val]) + " "

        return ex_string

    def parse_examples(self, examples_data):
        examples = []
        for example in examples_data:
            temp_example = []
            for attribute_value in example:
                if type(attribute_value) == bytes:
                    attribute_value = int.from_bytes(attribute_value, "little")
                temp_example.append(attribute_value)
            examples.append(temp_example)

        self.examples = np.array(examples)
        self.example_weights = np.ones(len(examples))

    # will return k random sets of examples all with approximately equal numbers of examples
    def get_k_sets(self, k):
        shuffle_copy = deepcopy(self.examples)
        np.random.shuffle(shuffle_copy)
        sets = np.array_split(shuffle_copy, k)

        return sets