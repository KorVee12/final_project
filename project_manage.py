# import database module
from database import Database, Table, get_persons
import copy
import random
import string

# start by adding the admin related code
db = Database("project_manage")


# create an object to read an input csv file, persons.csv
class Persons:
    def __init__(self):
        self.persons = get_persons("persons.csv")


persons = Persons().persons


# create a 'persons' table
persons_table = Table("persons")
persons_table.add_fields(["ID", "fist", "last", "type"])
persons_table.add_row(persons)


# add the 'persons' table into the database
db.add_table(persons_table)


# create a 'login' table
login_table = Table("login")


# the 'login' table has the following keys (attributes):
login_table.add_fields(["person_id", "username", "password", "role"])


def change_name_in_dict(input_dict):
    output_dict = copy.deepcopy(input_dict)
    for item in output_dict:
        item["person_id"] = item.pop("ID")
        item["username"] = item.pop("fist")
        item["password"] = item.pop("last")
        item["role"] = item.pop("type")

    return output_dict


def random_string(length):
    characters = string.ascii_lowercase + string.digits
    result = "".join(random.choice(characters) for i in range(length))
    return result


def change_username_password(login_member):
    for i in login_member:
        i["username"] = i["username"] + "." + i["password"][0]
        i["password"] = random_string(4)
    return login_member


login_member = change_name_in_dict(persons)
login_member = change_username_password(login_member)
print(login_member)
# person_id
# username
# password
# role

# a person_id is the same as that in the 'persons' table
# let a username be a person's fisrt name followed by a dot and the first letter of that person's last name
# let a password be a random four digits string
# let the initial role of all the students be Member
# let the initial role of all the faculties be Faculty

# you create a login table by performing a series of insert operations; each insert adds a dictionary to a list

# add the 'login' table into the database

# add code that performs a login task; asking a user for a username and password; returning [person_id, role] if valid, otherwise returning None
