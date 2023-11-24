# Outline

## database.py
   
- `get_persons(filename_csv="persons.csv")` 
  This function use for called `persons.csv` and return list of persons in dictionary. 

```py
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
```

- `Database` is a class to use for collect the data from `Table` class. 

```py
class Database:
    def __init__(self, name_db):
        self.name = name_db
        self.tables = []

    def add_table(self, table_object):
        self.tables.append(table_object)

    def get_tables(self):
        return self.tables
```

-  `def __init__(self, name_db)` add two attribute are `name` and `tables`.

- `add_table(self, table_object)` this method use to add `table_object` in `tables` list.

- `get_tables(self)` return `tables`

- `Table` is a class for creating table objects.
```py
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

    def get_row(self):
        return self.__list_dict

    def __repr__(self) -> str:
        return f"Tables {self.name}"
```
- `def __init__(self, table_name)` add three attribute are `name`, `__list_dict` and `__fields`.

- `add_fields(self, data: list)` this method use to add `data` in `__fields` list for create field in table.

- `add_row(self, data: list)` this method use to add `data` in `__list_dict` list for create row in table.

- `get_row(self)` return `__list_dict`

- `def __repr__(self)` return `Tables {self.name}`

# project_manage.py

```py
from database import Database, Table, get_persons
import copy
import random
import string

db = Database("project_manage")
buff_seed = 1
```

- `from database import Database, Table, get_persons` import `Database`, `Table` and `get_persons` from `database` module.
- `db = Database("project_manage")` create `db` object.
- `buff_seed = 1` for random seed

### `def initializing()`

- create an object to read an input csv file, persons.csv
```py
class Persons:
        def __init__(self):
            self.persons = get_persons("persons.csv")
persons = Persons().persons
```

- create a 'persons' table
```py
persons_table = Table("persons")
persons_table.add_fields(["ID", "fist", "last", "type"])
persons_table.add_row(persons)
```

- add the 'persons' table into the database
```py
db.add_table(persons_table)
```

- create a 'login' table
```py
login_table = Table("login")
```

- the 'login' table has the following keys (attributes)  person_id , username ,password , role this function change the keys from 'ID' to 'person_id' , 'fist' to 'username' , 'last' to 'password' , 'type' to 'role'
```py
def change_name_in_dict(input_dict):
    output_dict = copy.deepcopy(input_dict)
    for item in output_dict:
        item["person_id"] = item.pop("ID")
        item["username"] = item.pop("fist")
        item["password"] = item.pop("last")
        item["role"] = item.pop("type")

    return output_dict
```
- a person_id is the same as that in the 'persons' table
```py
item["person_id"] = item.pop("ID")
``` 

- let a username be a person's fisrt name followed by a dot and the first letter of that person's last name
```py
def change_username_password(login_member):
    for i in login_member:
        i["username"] = "{}.{}".format(i["username"], i["username"][0])
        i["password"] = random_string(4)
    return login_member
```

- let a password be a random four digits string
```py
def random_string(length):
    global buff_seed
    characters = string.ascii_lowercase + string.digits
    random.seed(6310545302 + buff_seed)
    buff_seed += 1
    result = "".join(random.choice(characters) for i in range(length))
    return result
```

- let the initial role of all the students be Member and the initial role of all the faculties be faculty
```py
def change_role(login_member):
    for i in login_member:

        # let the initial role of all the faculties be Faculty
        if i["role"] == "faculty":
            i["role"] = "faculty"
    return login_member
```

- create a login table by performing a series of insert operations; each insert adds a dictionary to a list
```py
login_table.add_row(login_member)
```

- add the 'login' table into the database
```py
db.add_table(login_table)
```

### `def login()`

- ask a user for a username and password
```py
while True:
    username = input("Enter username: ")
    if username:
        break

while True:
    password = input("Enter password: ")
    if password:
        break
```

- get data from 'login' table
```py
users = db.get_tables()[1].get_row()
```

- check the username and password have the same in login table returns [person_id, role] if valid, otherwise returning None
```py
for i in users:
    if i["username"] == username and i["password"] == password:

        # returns [person_id, role] if valid, otherwise returning None
        return [i["person_id"], i["role"]]

return None
```