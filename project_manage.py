# BEGIN part 1

# import database module
from database import Database, Table, get_persons
import copy
import random
import string

db = Database("project_manage")
buff_seed = 1
# define a funcion called initializing

# here are things to do in this function:
def initializing():

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
    # person_id
    # username
    # password
    # role
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
        global buff_seed
        characters = string.ascii_lowercase + string.digits
        random.seed(6310545302 + buff_seed)
        buff_seed += 1
        result = "".join(random.choice(characters) for i in range(length))
        return result

    def change_username_password(login_member):
        for i in login_member:
            i["username"] = "{}.{}".format(i["username"], i["username"][0])
            i["password"] = random_string(4)
        return login_member

    # a person_id is the same as that in the 'persons' table

    # let a username be a person's fisrt name followed by a dot and the first letter of that person's last name

    # let a password be a random four digits string

    login_member = change_name_in_dict(persons)
    login_member = change_username_password(login_member)

    def change_role(login_member):
        for i in login_member:

            # let the initial role of all the students be Member
            if i["role"] == "student":
                i["role"] = "member"

            # let the initial role of all the faculties be Faculty
            if i["role"] == "faculty":
                i["role"] = "faculty"
        return login_member

    login_member = change_role(login_member)

    # create a login table by performing a series of insert operations; each insert adds a dictionary to a list
    login_table.add_row(login_member)

    # add the 'login' table into the database
    db.add_table(login_table)

    # for i in login_member:
    #     print(i)


# define a funcion called login


def login():
    while True:
        username = input("Enter username: ")
        if username:
            break

    while True:
        password = input("Enter password: ")
        if password:
            break

    users = db.get_tables()[1].get_row()

    for i in users:
        if i["username"] == username and i["password"] == password:

            # returns [person_id, role] if valid, otherwise returning None
            return [i["person_id"], i["role"]]

    return None


# here are things to do in this function:
# add code that performs a login task


# make calls to the initializing and login functions defined above

initializing()
val = login()

# print(val)

# END part 1

# CONTINUE to part 2 (to be done for the next due date)

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] = 'admin':
# do admin related activities
# elif val[1] = 'advisor':
# do advisor related activities
# elif val[1] = 'lead':
# do lead related activities
# elif val[1] = 'member':
# do member related activities
# elif val[1] = 'faculty':
# do faculty related activities
