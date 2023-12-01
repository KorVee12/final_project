# BEGIN part 1

# import database module
from database import Database, Table, get_persons
import copy
import random
import string
import os
import uuid
import datetime

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


def login(username=None, password=None):
    if username is None:
        while True:
            username = input("Enter username: ")
            if username:
                break

    if password is None:
        while True:
            password = input("Enter password: ")
            if password:
                break

    users = db.get_tables()[1].query_row(db.name)

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
# val = login("Hugo.H", "3oz5") # ! lead
val = login("Lionel.L", "1i1r")  # ! member
# print(val)
# ! Lionel.L,1i1r,member1
#! Robert.R,zbx1 member2
# ! Marco.M,r4yn,advisor
# val = ["4788888", "member"]
# END part 1

# CONTINUE to part 2 (to be done for the next due date)

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id


class ProcessMember:
    def __init__(self, val):
        # [id,role]
        self.__data_member = val

    # ! Yet not complete !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def check_request_project(self) -> bool:
        if self.__data_member[-1] == "member":
            member_pending = member_pending_request_table.get_data_one(
                self.__data_member[0], "to_be_member", db
            )
            if member_pending["response"] != "yes":
                return True
            else:
                return False
        elif self.__data_member[-1] == "advisor":
            advisor_pending = advisor_pending_request_table.get_data_one(
                self.__data_member[0], "to_be_advisor", db
            )
            if advisor_pending["response"] != "yes":
                return True
            else:
                return False
        else:
            return False

    def change_role(self, new_role: str, data_user: dict):
        data_user["role"] = new_role
        login_table.update_row(
            data_user["person_id"],
            "person_id",
            data_user,
            ["person_id", "username", "password", "role"],
            db,
        )

    def invite_member(self, name) -> str:
        """
        The function `invite_member` selects a member from a login table based on their role being
        "student" and returns their username.
        :return: a string, which is the username of the selected member 1.
        """
        data = login_table.query_row(db.name)
        count = 0
        print(f"Select {name}".center(30, "-"))
        for i in data:
            if i["role"] == "student":
                count += 1
                print(f"{count}. {i['username']}")
        number_member = input(f"Select invite {name}: ")
        count = 0
        if number_member:
            for i in data:
                if i["role"] == "student":
                    count += 1
                    if int(number_member) == count:
                        self.change_role("member", i)
                        self.send_request("member", i)
                        print(f"Invite {i['username']} to {name} success")
                        return i["person_id"]
        else:
            return None

    def invite_advisor(self, name) -> str:
        data = login_table.query_row(db.name)
        count = 0
        print(f"Select {name}".center(30, "-"))
        for i in data:
            if i["role"] == "faculty":
                count += 1
                print(f"{count}. {i['username']}")
        number_advisor = input(f"Select invite {name}: ")
        count = 0
        if number_advisor:
            for i in data:
                if i["role"] == "faculty":
                    count += 1
                    if int(number_advisor) == count:
                        self.change_role("advisor", i)
                        self.send_request("advisor", i)
                        print(f"Invite {i['username']} to {name} success")
                        return i["person_id"]
        else:
            return None

    def send_request(self, role_name, data_user):
        if role_name == "member":
            data = {
                "project_id": self.project_id,
                "to_be_member": data_user["person_id"],
                "response": None,
                "response_date": None,
            }

            member_pending_request_table.add_data_one(
                ["project_id", "to_be_member", "response", "response_date"], data, db
            )
        elif role_name == "advisor":
            data = {
                "project_id": self.project_id,
                "to_be_advisor": data_user["person_id"],
                "response": None,
                "response_date": None,
            }

            advisor_pending_request_table.add_data_one(
                ["project_id", "to_be_advisor", "response", "response_date"], data, db
            )

    def create_project(self):
        title = input("Enter title Project: ")
        data = login_table.get_data_one(val[0], "person_id", db)
        # member 1 and member 2 and advisor will for loop show data all of select
        self.project_id = str(uuid.uuid4())
        project_table.add_row(
            [
                {
                    "project_id": self.project_id,
                    "title": title,
                    "lead": data["person_id"],
                    "member1": self.invite_member("member 1"),
                    "member2": self.invite_member("member 2"),
                    "advisor": self.invite_advisor("advisor"),
                    "status": "pendding_member",
                }
            ]
        )
        data = login_table.get_data_one(val[0], "person_id", db)
        self.change_role("lead", data)
        self.__data_member = [data["person_id"], data["role"]]
        db.add_row_table(project_table)

        # send request to students from data login table

    def view_project(self, show_toolbar=True):
        print(" View project ".center(30, "-"))
        data = project_table.query_row(db.name)
        for i in data:
            if (
                i["lead"] == self.__data_member[0]
                or i["member1"] == self.__data_member[0]
                or i["member2"] == self.__data_member[0]
                or i["advisor"] == self.__data_member[0]
            ):
                for k, v in i.items():
                    if (
                        k == "lead"
                        or k == "member1"
                        or k == "member2"
                        or k == "advisor"
                    ):
                        v = login_table.get_data_one(v, "person_id", db)["username"]
                    if k == "status":
                        if v == "pendding_member":
                            v = "Pendding..."
                        elif v == "accept_member":
                            v = "Accept"
                        elif v == "reject_member":
                            v = "Reject"

                    print(f"{k} : {v}")
        while show_toolbar:
            print("--------------".center(30, "-"))
            print("")
            print("1. Back to menu ⬅️")
            print("0. Exit Program ❌")
            number_choice = input("Select choice: ")
            if number_choice == "1":
                break
            elif number_choice == "0":
                exit()

    def back_to_basic(self, person_id, new_role):
        data = login_table.query_row(db.name)
        for i in data:
            if i["person_id"] == person_id:
                self.change_role(new_role, i)
                break

    def update_project(self) -> dict:
        data = project_table.query_row(db.name)
        for i in data:
            if i["lead"] == self.__data_member[0]:
                for k, v in i.items():
                    if k == "project_id":
                        project_id = v
                    elif k == "title":
                        title_new = input(f"Enter new title (origin is {v}): ")
                    elif k == "lead":
                        lead = v
                    elif k == "member1":
                        member1_new = self.invite_member("member 1")
                        self.back_to_basic(v, "student")
                    elif k == "member2":
                        member2_new = self.invite_member("member 2")
                        self.back_to_basic(v, "student")
                    elif k == "advisor":
                        advisor_new = self.invite_advisor("advisor")
                        self.back_to_basic(v, "faculty")
                    elif k == "status":
                        status = v

        return {
            "project_id": project_id,
            "title": title_new,
            "lead": lead,
            "member1": member1_new,
            "member2": member2_new,
            "advisor": advisor_new,
            "status": status,
        }

    def edit_project(self):
        print("Edit project".center(30, "-"))
        data = project_table.query_row(db.name)
        for i in data:
            if i["lead"] == self.__data_member[0]:
                project_table.update_row(
                    id=i["project_id"],
                    field_id="project_id",
                    dict_data=self.update_project(),
                    fieldname=[
                        "project_id",
                        "title",
                        "lead",
                        "member1",
                        "member2",
                        "advisor",
                        "status",
                    ],
                    db_object=db,
                )
            break
        self.view_project()

    def response_request_project(self):
        self.view_project(show_toolbar=False)

        while True:
            print()
            print("Answer the request project ?")
            res = input("Yes or No (y/n) : ").lower()
            if self.__data_member[1] == "member":
                member_peding = member_pending_request_table.get_data_one(
                    self.__data_member[0], "to_be_member", db
                )
            if self.__data_member[1] == "advisor":
                advisor_peding = advisor_pending_request_table.get_data_one(
                    self.__data_member[0], "to_be_advisor", db
                )
            if res == "y":
                if self.__data_member[1] == "member":
                    member_peding["response"] = "yes"
                    member_peding["response_date"] = datetime.datetime.now()
                    member_pending_request_table.update_row(
                        id=member_peding["project_id"],
                        field_id="project_id",
                        dict_data=member_peding,
                        fieldname=[
                            "project_id",
                            "to_be_member",
                            "response",
                            "response_date",
                        ],
                        db_object=db,
                    )
                elif self.__data_member[1] == "advisor":
                    pass
                    # advisor_peding["response"] = "yes"
                    # advisor_peding["response_date"] = datetime.datetime.now()
                    # advisor_pending_request_table.update_row(
                    #     id=advisor_peding["project_id"],
                    #     field_id="project_id",
                    #     dict_data=advisor_peding,
                    #     fieldname=[
                    #         "project_id",
                    #         "to_be_advisor",
                    #         "response",
                    #         "response_date",
                    #     ],
                    #     db_object=db,
                    # )
                    # project_advisor = project_table.get_data_one(
                    #     self.__data_member[0], "advisor", db
                    # )
                    # project_advisor["status"] = "Approve"
                    # project_table.update_row(
                    #     id=advisor_peding["project_id"],
                    #     field_id="project_id",
                    #     dict_data=project_advisor,
                    #     fieldname=[
                    #         "project_id",
                    #         "title",
                    #         "lead",
                    #         "member1",
                    #         "member2",
                    #         "advisor",
                    #         "status",
                    #     ],
                    #     db_object=db,
                    # )
                break
            elif res == "n":
                if self.__data_member[1] == "member":
                    member_pending_request_table.delete_row(
                        id=member_peding["project_id"],
                        field_id="project_id",
                        fieldname=[
                            "project_id",
                            "to_be_member",
                            "response",
                            "response_date",
                        ],
                        db_object=db,
                    )
                    member1 = project_table.get_data_one(
                        self.__data_member[0], "member1", db
                    )
                    member2 = project_table.get_data_one(
                        self.__data_member[0], "member2", db
                    )
                    field_member = ""
                    member = member1 if member1 != None else member2
                    for k, v in member.items():
                        if v == self.__data_member[0]:
                            member[k] = ""
                            field_member = k
                            break

                    project_table.update_row(
                        id=self.__data_member[0],
                        field_id=field_member,
                        dict_data=member,
                        fieldname=[
                            "project_id",
                            "title",
                            "lead",
                            "member1",
                            "member2",
                            "advisor",
                            "status",
                        ],
                        db_object=db,
                    )
                    data = login_table.get_data_one(
                        self.__data_member[0], "person_id", db
                    )
                    self.change_role("student", data)
                    self.__data_member[-1] = "student"
                elif self.__data_member[1] == "advisor":
                    pass
                break

        while True:
            print("--------------".center(30, "-"))
            print("")
            print("1. Back to menu ⬅️")
            print("0. Exit Program ❌")
            number_choice = input("Select choice: ")
            if number_choice == "1":
                break
            elif number_choice == "0":
                exit()

    def select_action(self):
        while True:
            print("Menu".center(30, "-"))
            requested = self.check_request_project()
            if requested:
                print("1. View request project 📃")
                print("0. Exit Program ❌")
                number_choice = input("Select choice: ")
                if number_choice == "0":
                    break
                if number_choice == "1":
                    self.response_request_project()

            else:
                if self.__data_member[1] != "student":
                    print("1. View project 📃")

                if self.__data_member[1] == "student":
                    print("2. Create project 🪄")

                if self.__data_member[1] == "lead":
                    print("3. Edit project 🖋️")
                print("0. Exit Program ❌")

                number_choice = input("Select choice: ")
                if number_choice == "0":
                    break
                if number_choice == "1":
                    if self.__data_member[1] != "student":
                        self.view_project()
                    else:
                        print("You not lead project")
                elif number_choice == "2":
                    if self.__data_member[1] == "lead":
                        print("You are lead of project, so you can not create project")
                        return None
                    if not requested:
                        # ? create project
                        self.create_project()
                        self.view_project()
                    else:
                        print("You have already requested")
                elif number_choice == "3":
                    if self.__data_member[1] == "lead":
                        self.edit_project()
                    else:
                        print(
                            "You are not lead of project, so you can not edit project"
                        )
                        return None


if val[1] == "admin":
    pass
elif val[1] == "advisor":
    ProcessMember(val).select_action()
elif val[1] == "lead":
    ProcessMember(val).select_action()
elif val[1] == "student" or val[1] == "member":
    ProcessMember(val).select_action()
elif val[1] == "faculty":
    pass
