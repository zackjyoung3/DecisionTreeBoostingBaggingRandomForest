import numpy as np
from Attributes import Attributes


# class that will contain all of the examples for a dataset
class Examples:
    def __init__(self, attributes):
        self.examples = None
        self.example_weights = None
        self.attributes = attributes

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