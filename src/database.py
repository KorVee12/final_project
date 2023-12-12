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


def create_csv(filename: str, fieldname: list):
    with open(filename, mode="w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldname)
        writer.writeheader()


def insert_csv(filename: str, fieldname: list, row_data: dict):
    with open(filename, mode="a", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldname)
        writer.writerow(row_data)


def query_read_csv(filename: str) -> list:
    with open(filename, mode="r", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        list_data = []
        for r in rows:
            list_data.append(r)
        return list_data


def get_read_csv(filename: str, id: str, field_id: str) -> dict:
    with open(filename, mode="r", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        for r in rows:
            if r[field_id] == id:
                return r


def filter_read_csv(filename: str, id: str, field_id: str):
    with open(filename, mode="r", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        list_data = []
        for r in rows:
            if r[field_id] == id:
                list_data.append(r)
        return list_data


def delete_csv(filename: str, id: str, field_id: str, fieldname: list):
    with open(filename, mode="r", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        rows = list(rows)
    for r in rows:
        if r[field_id] == id:
            rows.remove(r)
            break
    with open(filename, mode="w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldname)
        writer.writeheader()
        writer.writerows(rows)


def update_csv(filename: str, id: str, field_id: str, dict_data: dict, fieldname: list):
    with open(filename, mode="r", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        rows = list(rows)
    for r in rows:
        if r[field_id] == id:
            r.update(dict_data)
            break
    with open(filename, mode="w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldname)
        writer.writeheader()
        writer.writerows(rows)


class Database:
    def __init__(self, name_db):
        self.name = name_db
        self.tables = []
        if self.name[-3:] != "_db":
            self.name = self.name + "_db"

        if not os.path.isdir(f"{self.name}"):
            os.mkdir(f"{self.name}")

    def create_table(self, table_object: object):
        item_files = os.listdir(self.name)
        if f"{table_object.name}.csv" in os.listdir(self.name):
            pass
        else:
            create_csv(
                filename=f"{self.name}/{table_object.name}.csv",
                fieldname=table_object.get_fields(),
            )
        self.tables.append(table_object)

    def add_row_table(self, table_object: object):

        data = table_object.get_row()
        if data != []:
            for i in data:
                insert_csv(
                    filename=f"{self.name}/{table_object.name}.csv",
                    fieldname=table_object.get_fields(),
                    row_data=i,
                )

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

    def get_fields(self):
        return self.__fields

    def add_row(self, data: list):
        for row in data:
            for field in self.__fields:
                try:
                    if row[field]:
                        continue
                except:
                    raise Exception(f"Not found field '{field}'")

            self.__list_dict.append(row)

    def get_data_one(self, id: str, field_id: str, db_object):
        return get_read_csv(
            filename=f"{db_object.name}/{self.name}.csv", id=id, field_id=field_id
        )

    def add_data_one(self, fieldname: list, row_data: dict, db_object):
        return insert_csv(
            filename=f"{db_object.name}/{self.name}.csv",
            fieldname=fieldname,
            row_data=row_data,
        )

    def get_row(self):
        return self.__list_dict

    def query_row(self, db_object_name: str):
        return query_read_csv(filename=f"{db_object_name}/{self.name}.csv")

    def update_row(
        self, id: str, field_id: str, dict_data: dict, fieldname: list, db_object
    ):
        update_csv(
            filename=f"{db_object.name}/{self.name}.csv",
            id=id,
            field_id=field_id,
            dict_data=dict_data,
            fieldname=fieldname,
        )

    def delete_row(self, id: str, field_id: str, fieldname: list, db_object):
        delete_csv(
            filename=f"{db_object.name}/{self.name}.csv",
            id=id,
            field_id=field_id,
            fieldname=fieldname,
        )

    def __repr__(self) -> str:
        return f"Tables {self.name}"


if __name__ == "__main__":
    db = Database("test")
    table = Table("person")
    table.add_fields(["ID", "first", "last", "type"])
    person = [
        {"ID": "7525643", "first": "Henrikh", "last": "Mkhitaryan", "type": "faculty"},
        {"ID": "2472659", "first": "Karim", "last": "Benzema", "type": "faculty"},
    ]
    table.add_row(person)
    db.create_table(table)
    db.add_row_table(table)

    # print(db.get_tables())
    # print(get_persons())

# modify the code in the Table class so that it supports the insert operation where an entry can be added to a list of dictionary
