# BEGIN part 1

# import database module
from database import Database, Table, get_persons
import copy
import random
import string
import os
import uuid

# initialize the database
db = Database("project_manage_db")

# initialize the tables
persons_table = Table("persons")
login_table = Table("login")
project_table = Table("project")
advisor_pending_request_table = Table("advisor_pending_request")
member_pending_request_table = Table("member_pending_request")
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
    persons_table.add_fields(["ID", "fist", "last", "type"])
    persons_table.add_row(persons)

    # add the 'persons' table into the database
    db.create_table(persons_table)

    if f"{persons_table.name}.csv" not in os.listdir(db.name):
        db.add_row_table(persons_table)

    # create a 'login' table
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

            if i["role"] == "student":
                i["role"] = "student"

            # let the initial role of all the faculties be Faculty
            if i["role"] == "faculty":
                i["role"] = "faculty"
        return login_member

    login_member = change_role(login_member)

    # create a login table by performing a series of insert operations; each insert adds a dictionary to a list
    login_table.add_row(login_member)

    # add the 'login' table into the database
    db.create_table(login_table)
    if f"{login_table.name}.csv" not in os.listdir(db.name):
        db.add_row_table(login_table)

    # create a 'project' table
    project_table.add_fields(
        [
            "project_id",
            "title",
            "lead",
            "member1",
            "member2",
            "advisor",
            "status",
        ]
    )
    # add the 'project' table into the database
    db.create_table(project_table)

    # create a 'advisor_pending_request' table
    advisor_pending_request_table.add_fields(
        [
            "project_id",
            "to_be_advisor",
            "response",
            "response_date",
        ]
    )

    # add the 'advisor_pending_request' table into the database
    db.create_table(advisor_pending_request_table)

    # create a 'member_pending_request' table
    member_pending_request_table.add_fields(
        [
            "project_id",
            "to_be_member",
            "response",
            "response_date",
        ]
    )

    # add the 'member_pending_request' table into the database
    db.create_table(member_pending_request_table)


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
# val = login()
# 4788888,Thiago.T,sa4a,member
# 4720327,David.D,vm0y,faculty
val = ["4788888", "member"]
# END part 1

# CONTINUE to part 2 (to be done for the next due date)

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id


class ProcessMember:
    def __init__(self, val):
        self.__data_member = val

    # ! Yet not complete !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def check_request_project(self) -> bool:
        self.__data_member
        return False

    def create_project(self):
        title = input("Enter title Project: ")
        data = login_table.get_data_one(val[0], "person_id", db)
        # member 1 and member 2 and advisor will for loop show data all of select
        project_table.add_row(
            [
                uuid.uuid4(),
                title,
                data["username"],
                "member1",
                "member2",
                "advisor",
                "pedding_member",
            ]
        )

        # self.__data_member

        # send request to students from data login table

    def select_action(self):
        print("Menu for member".center(30, "-"))
        print("1. View projects")
        print("2. Create projects")
        requested = self.check_request_project()
        # number_choice = input("Select choice: ")
        number_choice = "2"
        if number_choice == "1":
            print("View projects")
        elif number_choice == "2":
            if not requested:

                # ? create project
                self.create_project()

                # ? change role to lead at login table for this member
                # self.change_role_lead_login()

            else:
                print("You have already requested")


if val[1] == "admin":
    pass
elif val[1] == "advisor":
    pass
elif val[1] == "lead":
    pass
elif val[1] == "member":
    ProcessMember(val).select_action()
elif val[1] == "faculty":
    pass
