# class for an attribute
class Attribute:
    def __init__(self, name):
        self.name = name
        self.is_numeric = None


# class for a numeric attribute
class NumericAttribute(Attribute):
    def __init__(self, name):
        super().__init__(name)
        self.is_numeric = True

    def __str__(self):
        return self.name + ": numeric"


# class for a categorical attribute
class CategoricalAttribute(Attribute):
    def __init__(self, name, values_list):
        super().__init__(name)
        self.values_list = values_list
        self.is_numeric = False

    def __str__(self):
        return self.name + ": categorical with values... " + str(self.values_list)

    def __setitem__(self, key, value):
        self.values_list[int(key)] = value

    def __getitem__(self, item):
        return self.values_list[int(item)]

    def __delitem__(self, key):
        self.values_list.pop(key)

    def __len__(self):
        return len(self.values_list)


# class that will hold all the attributes for a dataset
class Attributes:
    def __init__(self):
        self.attributes = []
        self.class_label_index = -1

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def __getitem__(self, item):
        return self.attributes[item]

    def __delitem__(self, key):
        self.attributes.pop(key)

    def append(self, attribute):
        self.attributes.append(attribute)

    def get_class_label(self):
        return self.attributes[self.class_label_index]

    def __len__(self):
        return len(self.attributes)

    def __str__(self):
        att_string = "Attributes:\n"
        for attribute in self.attributes:
            att_string += str(attribute) + "\n"

        return att_string

    def parse_attributes(self, attributes_data):
        for attribute in attributes_data:
            if attribute[1] == 1:
                self.attributes.append(NumericAttribute(attribute[0]))
            else:
                self.attributes.append(CategoricalAttribute(attribute[0], eval(attribute[2])))
