# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file

import csv, os


def get_persons(filename_csv="persons.csv"):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    persons = []
    with open(os.path.join(__location__, filename_csv)) as f:
        rows = csv.DictReader(f)
        for r in rows:
            persons.append(dict(r))
    return persons


# add in code for a Database class


class Database:
    def __init__(self, name_db):
        self.name = name_db
        self.tables = []

    def add_table(self, table_object):
        self.tables.append(table_object)

    def get_tables(self):
        return self.tables


# add in code for a Table class
class Table:
    def __init__(self, table_name):
        self.name = table_name
        self.__list_dict = []
        self.__fields = []

    def add_fields(self, data: list):
        self.__fields = data

    def add_row(self, data: list):
        for row in data:
            for field in self.__fields:
                try:
                    if row[field]:
                        continue
                except:
                    raise Exception(f"Not found field '{field}'")

            self.__list_dict.append(row)

    def __repr__(self) -> str:
        return f"Tables {self.name}"


if __name__ == "__main__":
    db = Database("test")
    table = Table("person")
    table.add_fields(["ID", "fists", "last", "type"])
    person = [
        {"ID": "7525643", "fist": "Henrikh", "last": "Mkhitaryan", "type": "faculty"},
        {"ID": "2472659", "fist": "Karim", "last": "Benzema", "type": "faculty"},
    ]
    table.add_row(person)
    # db.add_table(table)
    # print(db.get_tables())
    # print(get_persons())

# modify the code in the Table class so that it supports the insert operation where an entry can be added to a list of dictionary
