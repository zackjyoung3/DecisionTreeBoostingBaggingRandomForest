import sqlite3
import pandas as pd

numeric = "numeric"
categorical = "categorical"


# class that will be used to encode recieved data and store it in a local sqlite db
class Encoder:
    def __init__(self, title, option, source):
        self.option = option
        self.source = source
        self.title = title
        self.sqlite_filename = str(self.title) + '.db'
        self.data = None
        self.df = None
        self.categorical_attribute_values = {}

    def get_data(self):
        # function ie load_wine function to load data
        if self.option == "sklearn import":
            self.data = self.source(as_frame=True)
            self.df = self.data['frame']
            self.categorical_attribute_values['target'] = list(self.data['target_names'])

    # method that will format the data in an encoders df so that the df can be written to the database
    def examples_to_db_form(self):
        examples = []
        for i in range(len(self.df.index)):
            example = []
            for header in self.df.columns.values:
                example.append(self.df[header][i])
            examples.append(tuple(example))

        return examples

    # method that will convert the attributes into the correct form to write to db
    def attributes_to_db_form(self, types):
        print(types)
        attributes = []
        i = 0
        for header in self.df.columns.values:
            if types[i] == categorical:
                attributes.append((header, 0, str(self.categorical_attribute_values[header])))
            else:
                attributes.append((header, 1, 'Numeric'))
            i+=1
        return attributes

    # method that will write the contents of a dataset to an sqlite database
    def make_sp_sqlite(self):
        self.get_data()

        con = sqlite3.connect(self.sqlite_filename)
        cur = con.cursor()
        types = []
        db_execute_string = '''CREATE TABLE IF NOT EXISTS ''' + str(self.title) + '''('''
        insert_string = 'INSERT INTO ' + self.title + ' VALUES('
        for header, att_type in zip(self.df.columns.values, self.df.dtypes):
            insert_string += '?,'
            header = header.replace(" ", "_")
            header = header.replace("(", "_")
            header = header.replace(")", "")

            db_execute_string += header
            if att_type == float:
                types.append(numeric)
                db_execute_string += ''' real, '''
            elif att_type == str:
                types.append(categorical)
                db_execute_string += ''' integer, '''
            else:
                prompt = "Does attribute with integer vals " + header + " correspond to a numeric attribute?" \
                                                                        "(must be yes/no):"
                not_done = True
                while (not_done):
                    is_numeric = input(prompt)
                    if is_numeric == "yes":
                        types.append(numeric)
                        db_execute_string += ''' real, '''
                        not_done = False
                    elif is_numeric == 'no':
                        types.append(categorical)
                        db_execute_string += ''' integer, '''
                        not_done = False
        db_execute_string = db_execute_string[:-2]
        db_execute_string += ''')'''
        print(db_execute_string)

        # create the table that will hold the examples of the dataset
        cur.execute(db_execute_string)

        insert_string = insert_string[:-1]
        insert_string += ');'
        print(insert_string)
        examples = self.examples_to_db_form()
        print(examples)
        cur.executemany(insert_string, examples)

        attribute_info_db_string = '''CREATE TABLE IF NOT EXISTS ''' + str(self.title) + '''Attributes ('''
        attribute_info_db_string += '''name text, isNumeric integer, vals text)'''
        # create the table that will hold the attributes for the dataset
        print(attribute_info_db_string)
        cur.execute(attribute_info_db_string)
        attributes = self.attributes_to_db_form(types)
        insert_attributes_string = 'INSERT INTO ' + str(self.title) + 'Attributes VALUES(?,?,?);'
        print(insert_attributes_string)
        print(attributes)
        cur.executemany(insert_attributes_string, attributes)
        
        # print(attributes)
        # print(eval(attributes[4][2]))



        # commit the changes to db
        con.commit()
        # close the connection
        con.close()

    def header_test(self):
        # Connecting to sqlite
        conn = sqlite3.connect(self.sqlite_filename)

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        print('\nColumns in iris table:')
        connection_string = '''SELECT * FROM ''' + self.title
        data = cursor.execute(connection_string)
        for column in data.description:
            print(column[0])
        for col in data:
            print(col)
            # print(int.from_bytes(col[4], "little"))

        print('\nColumns in iris attribute table:')
        connection_string = '''SELECT * FROM ''' + self.title + 'Attributes'
        data = cursor.execute(connection_string)
        for column in data.description:
            print(column[0])
        i = 0
        for col in data:
            print(col)
            if i == 4:
                x = eval(col[2])
                print(type(x))
                print(x)
            i += 1


