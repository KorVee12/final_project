import copy
import string
from src.database import Database, Table
import uuid
import datetime
import random

# initialize the database
db = Database("project_manage_db")

# initialize the tables
persons_table = Table("persons")
login_table = Table("login")
project_table = Table("project")
advisor_pending_request_table = Table("advisor_pending_request")
member_pending_request_table = Table("member_pending_request")
evaluation_project_table = Table("evaluation_project")
buff_seed = 1


class ProcessMember:
    def __init__(self, val):
        # [id,role]
        self.__data_member = val

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
        data = login_table.get_data_one(self.__data_member[0], "person_id", db)
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
                    "status": "pendding",
                }
            ]
        )
        data = login_table.get_data_one(self.__data_member[0], "person_id", db)
        self.change_role("lead", data)
        self.__data_member = [data["person_id"], data["role"]]
        print(project_table)
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
                        try:
                            v = login_table.get_data_one(v, "person_id", db)["username"]
                        except:
                            v = ""
                    if k == "status":
                        if v == "pendding":
                            v = "Pendding..."
                        elif v == "approve":
                            v = "Accept"

                    print(f"{k} : {v}")
        while show_toolbar:
            print("--------------".center(30, "-"))
            print("")
            print("1. Back to menu ⬅️")
            if self.__data_member[1] == "lead":
                print("2. Delete this project")

            print("0. Exit Program ❌")
            number_choice = input("Select choice: ")
            if number_choice == "1":
                break
            elif number_choice == "0":
                exit()
            elif number_choice == "2":
                if self.__data_member[1] == "lead":
                    self.delete_project()
                else:
                    print("You don't have permission")
                break

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
                        status = "pendding"

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

    def delete_project(self):
        print("Are you sure to delete this project ?")
        choice = input("Yes or No (y/n): ").lower()
        if choice == "y":
            data_lead = login_table.get_data_one(self.__data_member[0], "person_id", db)
            data_project = project_table.get_data_one(
                id=data_lead["person_id"], field_id="lead", db_object=db
            )

            try:
                data_member_1 = login_table.get_data_one(
                    data_project["member1"], "person_id", db
                )
            except:
                data_member_1 = None
            try:
                data_member_2 = login_table.get_data_one(
                    data_project["member2"], "person_id", db
                )
            except:
                data_member_2 = None
            data_advisor = login_table.get_data_one(
                data_project["advisor"], "person_id", db
            )

            project_table.delete_row(
                id=data_lead["person_id"],
                field_id="lead",
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

            advisor_pending_request_table.delete_row(
                id=data_advisor["person_id"],
                field_id="to_be_advisor",
                fieldname=["project_id", "to_be_advisor", "response", "response_date"],
                db_object=db,
            )
            self.change_role("faculty", data_advisor)

            if data_member_1:
                member_pending_request_table.delete_row(
                    id=data_member_1["person_id"],
                    field_id="to_be_member",
                    fieldname=[
                        "project_id",
                        "to_be_member",
                        "response",
                        "response_date",
                    ],
                    db_object=db,
                )
                self.change_role("student", data_member_1)
            if data_member_2:
                member_pending_request_table.delete_row(
                    id=data_member_2["person_id"],
                    field_id="to_be_member",
                    fieldname=[
                        "project_id",
                        "to_be_member",
                        "response",
                        "response_date",
                    ],
                    db_object=db,
                )
                self.change_role("student", data_member_2)

            self.change_role("student", data_lead)
            self.__data_member[1] = "student"
            print("Delete this project success.")

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
                advisor_pending = advisor_pending_request_table.get_data_one(
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
                    print("You are already in my team.")
                elif self.__data_member[1] == "advisor":
                    advisor_pending["response"] = "yes"
                    advisor_pending["response_date"] = datetime.datetime.now()
                    advisor_pending_request_table.update_row(
                        id=advisor_pending["project_id"],
                        field_id="project_id",
                        dict_data=advisor_pending,
                        fieldname=[
                            "project_id",
                            "to_be_advisor",
                            "response",
                            "response_date",
                        ],
                        db_object=db,
                    )
                    project_advisor = project_table.get_data_one(
                        self.__data_member[0], "advisor", db
                    )
                    project_table.update_row(
                        id=advisor_pending["project_id"],
                        field_id="project_id",
                        dict_data=project_advisor,
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
                    print(
                        "You are already be advisor for this project."
                    )
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
                    print("You have declided.")
                elif self.__data_member[1] == "advisor":
                    advisor_pending_request_table.delete_row(
                        id=advisor_pending["project_id"],
                        field_id="project_id",
                        fieldname=[
                            "project_id",
                            "to_be_advisor",
                            "response",
                            "response_date",
                        ],
                        db_object=db,
                    )
                    project_table.delete_row(
                        id=advisor_pending["project_id"],
                        field_id="project_id",
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
                    self.change_role("faculty", data)
                    self.__data_member[-1] = "faculty"
                    print("Your project has been declided.")
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

    def view_all_projects(self):
        data = project_table.query_row(db.name)
        print(" View all projects ".center(30, "-"))
        count = 0
        for i in data:
            count += 1
            print(f"{count}. Project name: {i['title']}")

        while True:
            print(f" {count} projects ".center(30, "-"))
            print("")
            print("1. Back to menu ⬅️")
            print("0. Exit Program ❌")
            number_choice = input("Select choice: ")
            if number_choice == "1":
                break
            elif number_choice == "0":
                exit()

    def evaluation_projects(self):
        data = project_table.query_row(db.name)
        print(" View all projects ".center(30, "-"), end="\n\n")
        count = 0
        for i in data:
            count += 1
            print(f"{count}. Project name: {i['title']} [{i['status']}]")
        print("")
        while True:
            try:
                number_choice = int(input("Select project's number : "))
            except:
                continue

            if number_choice > 0:
                number_choice -= 1
                data_evaluation = evaluation_project_table.query_row(db.name)
                for i in data_evaluation:
                    if data[number_choice]["status"] == "approve":
                        print("This project already approved!")
                        return 0
                    if i["project_id"] == data[number_choice]["project_id"]:
                        if i["teacher_id"] == self.__data_member[0]:
                            while True:
                                evaluation_choice = input(
                                    "You have evaluated this project and do you wanna edit? (y/n)"
                                )
                                if evaluation_choice == "y":
                                    break
                                if evaluation_choice == "n":
                                    return 0
                            break
                print("Project's details".center(30, "-"))
                for i in data[number_choice].items():
                    if i[0] == "title":
                        print("Title :", i[1])
                    if i[0] == "lead":
                        user = login_table.get_data_one(i[1], "person_id", db)
                        print("Lead :", user["username"])
                    if i[0] == "member1":
                        user = login_table.get_data_one(i[1], "person_id", db)
                        print("Member 1 :", user["username"])
                    if i[0] == "Member2":
                        user = login_table.get_data_one(i[1], "person_id", db)
                        print("Member 2 :", user["username"])
                    if i[0] == "advisor":
                        user = login_table.get_data_one(i[1], "person_id", db)
                        print("Advisor :", user["username"])
                    if i[0] == "status":
                        print("Status :", i[1])
                while True:
                    print("")
                    choice = input("Approve or Reject (a/r): ")
                    if choice == "a":
                        evaluation_project_table.add_data_one(
                            fieldname=[
                                "project_id",
                                "teacher_id",
                                "evaluation_status",
                                "evaluation_date",
                            ],
                            row_data={
                                "project_id": data[number_choice]["project_id"],
                                "teacher_id": self.__data_member[0],
                                "evaluation_status": "approve",
                                "evaluation_date": datetime.datetime.now(),
                            },
                            db_object=db,
                        )
                        break
                    elif choice == "r":
                        evaluation_project_table.add_data_one(
                            fieldname=[
                                "project_id",
                                "teacher_id",
                                "evaluation_status",
                                "evaluation_date",
                            ],
                            row_data={
                                "project_id": data[number_choice]["project_id"],
                                "teacher_id": self.__data_member[0],
                                "evaluation_status": "reject",
                                "evaluation_date": datetime.datetime.now(),
                            },
                            db_object=db,
                        )
                        break
            evaluation_projects = evaluation_project_table.query_row(db.name)
            project_current = data[number_choice]
            status_approve = 0
            status_reject = 0
            for i in evaluation_projects:
                if i["project_id"] == project_current["project_id"]:
                    if i["evaluation_status"] == "approve":
                        status_approve += 1
                    else:
                        status_reject += 1
            if status_approve >= 2:
                project_table.update_row(
                    id=project_current["project_id"],
                    field_id="project_id",
                    dict_data={
                        "project_id": project_current["project_id"],
                        "title": project_current["title"],
                        "lead": project_current["lead"],
                        "member1": project_current["member1"],
                        "member2": project_current["member2"],
                        "advisor": project_current["advisor"],
                        "status": "approve",
                    },
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
            if status_reject >= 2:
                project_table.update_row(
                    id=project_current["project_id"],
                    field_id="project_id",
                    dict_data={
                        "project_id": project_current["project_id"],
                        "title": project_current["title"],
                        "lead": project_current["lead"],
                        "member1": project_current["member1"],
                        "member2": project_current["member2"],
                        "advisor": project_current["advisor"],
                        "status": "reject",
                    },
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

    def faculty_select_action(self):
        while True:
            if self.__data_member[1] != "faculty":
                break
            print(f"Menu For {self.__data_member[1].capitalize()}".center(30, "-"))
            print("1. View all projects 📃")
            print("2. Evaluation projects 🖋️")
            print("0. Exit Program ❌")
            number_choice = input("Select choice: ")
            if number_choice == "0":
                exit()
            if number_choice == "1":
                self.view_all_projects()
            if number_choice == "2":
                self.evaluation_projects()

    def advisor_select_action(self):
        while True:
            if self.__data_member[1] != "advisor":
                break
            print(f"Menu For {self.__data_member[1].capitalize()}".center(30, "-"))
            requested = self.check_request_project()
            if requested:
                print("1. View request project 👁️")
                print("2. View all projects 📃")
                print("3. Evaluation projects 🖋️")
                print("0. Exit Program ❌")
                number_choice = input("Select choice: ")
                if number_choice == "0":
                    break
                if number_choice == "1":
                    self.response_request_project()
                if number_choice == "2":
                    self.view_all_projects()
                if number_choice == "3":
                    self.evaluation_projects()
            else:
                print("1. View project's advisor 📃")
                print("2. View all projects 📃")
                print("0. Exit Program ❌")
                if number_choice == "0":
                    exit()
                if number_choice == "1":
                    self.view_project()
                if number_choice == "2":
                    self.view_all_projects()
    def get_username(self,person_id):
        data_login = login_table.get_data_one(person_id, "person_id", db)
        return data_login["username"]
    def view_member(self):
        
        data_project = project_table.get_data_one(self.__data_member[0], "lead", db)
        data_member = member_pending_request_table.query_row(db.name)
        
        print(f" Member's project {data_project['title']} ".center(30, "-"))
        
        for i in data_member:
            if i["project_id"] == data_project["project_id"]:
                if i['response'] == "yes":
                    print(f"{self.get_username(i['to_be_member'])} - response at {i['response_date']}")
                else:
                    print(f"{self.get_username(i['to_be_member'])} - waiting for anwser...")
        
        while True:
            print("")
            print("1. Back to menu ⬅️")
            print("0. Exit Program ❌")
            number_choice = input("Select choice: ")
            if number_choice == "1":
                break
            elif number_choice == "0":
                exit()
    
    def view_advisor(self):
        data_project = project_table.get_data_one(self.__data_member[0], "lead", db)
        data_advisor = advisor_pending_request_table.get_data_one(
            data_project["project_id"], "project_id", db
        )
        print(f" Advisor's project {data_project['title']} ".center(30, "-"))
        if data_advisor['response'] == "yes":
            print(f"{self.get_username(data_advisor['to_be_advisor'])} - response at {data_advisor['response_date']}")
        else:
            print(f"{self.get_username(data_advisor['to_be_advisor'])} - waiting for anwser...")
        
        while True:
            print("")
            print("1. Back to menu ⬅️")
            print("0. Exit Program ❌")
            number_choice = input("Select choice: ")
            if number_choice == "1":
                break
            elif number_choice == "0":
                exit()

    def view_all_person(self):
        data_login_table = login_table.query_row(db.name)
        count = 1
        print(f" View all persons ".center(85, "-"))
        for i in data_login_table:
            print(f"{count}.".ljust(4," "),end=" ")
            print(f"person_id: {i["person_id"]}".ljust(22," "),end=" ")
            print(f"username: {i["username"]}".ljust(22," "),end=" ")
            print(f"password: {i["password"]}".ljust(19," "),end=" ")
            print(f"role: {i["role"]}")
            count += 1
        print(f" amount of people {len(data_login_table)} ".center(85, "-"))
        while True:
            print("")
            print("1. Back to menu ⬅️")
            print("0. Exit Program ❌")
            number_choice = input("Select choice: ")
            if number_choice == "1":
                break
            elif number_choice == "0":
                exit()

    def random_string(self,length):
        characters = string.ascii_lowercase + string.digits
        random.seed(6310545302 + datetime.datetime.now().timestamp())
        result = "".join(random.choice(characters) for i in range(length))
        return result
    
    def change_to_login(self,input_dict):
        output_dict = copy.deepcopy(input_dict)
        output_dict["person_id"] = output_dict.pop("ID")
        output_dict["username"] = output_dict.pop("fist")
        output_dict["password"] = output_dict.pop("last")
        output_dict["role"] = output_dict.pop("type")
        output_dict["username"] = "{}.{}".format(input_dict["fist"], input_dict["last"][0])
        output_dict["password"] = self.random_string(4)
        return output_dict
        
    
    def new_person(self):
        print(f" Add person to member ".center(30, "-"))
        new_person_dict = {
            "ID":"",
            "fist":"",
            "last":"",
            "type":""
        }
        field_person = ["ID","fist","last","type"]

        random.seed(datetime.datetime.now().timestamp())
        number_id = random.randint(1000000,9999999)
        data_person = persons_table.query_row(db.name)
        for i in data_person:
            if i["ID"] == number_id:
                random.seed(datetime.datetime.now().timestamp())
                number_id = random.randint(1000000,9999999)
                break
        new_person_dict["ID"] = number_id

        while True:            
            person_first= input("Enter First Name's person : ")
            if person_first != " " and person_first != "":
                new_person_dict["fist"] = person_first
                break
            else:
                print("First name must not empty")
        while True:            
            person_last= input("Enter Last Name's person : ")
            if person_last != " " and person_last != "":
                new_person_dict["last"] = person_last
                break
            else:
                print("Last name must not empty")
        while True:
            print("Choose type's person")
            print("1. admin")
            print("2. student")
            print("3. faculty")
            try:
                person_type = int(input("Select number for type : "))
                if person_type != " " and person_type != "" and type(person_type) == int:
                    if int(person_type) == 1:
                        new_person_dict["type"] = "admin"
                    if int(person_type) == 2:
                        new_person_dict["type"] = "student"
                    if int(person_type) == 3:
                        new_person_dict["type"] = "faculty"
                    break
                else:
                    print("Type must not empty")
            except:
                pass

        
        persons_table.add_data_one(field_person,new_person_dict,db)
        data_person = {}
        for i in persons_table.query_row(db.name):
            if i["ID"] == str( new_person_dict["ID"]):
                data_person = i
                break
        data = self.change_to_login(data_person)
        login_table.add_data_one(["person_id", "username", "password", "role"],data ,db)
        data_login = login_table.get_data_one(str(new_person_dict["ID"]),"person_id",db)
        print(f"{new_person_dict["fist"]} and {new_person_dict["last"]} already added by ")
        print(f"username: {data_login["username"]}")
        print(f"password: {data_login["password"]}")


        while True:
            print("")
            print("1. Back to menu ⬅️")
            print("0. Exit Program ❌")
            number_choice = input("Select choice: ")
            if number_choice == "1":
                break
            elif number_choice == "0":
                exit()
    
    def edit_person(self):
        data_login_table = login_table.query_row(db.name)
        data_persons = persons_table.query_row(db.name)
        count = 0
        print(f" Edit persons ".center(130, "-"))
        for i in data_login_table:
            print(f"{count}.".ljust(4," "),end=" ")
            print(f"person_id: {i["person_id"]}".ljust(22," "),end=" ")
            print(f"first name: {data_persons[count]['fist']}".ljust(22," "),end=" ")
            print(f"last name: {data_persons[count]['last']}".ljust(22," "),end=" ")
            print(f"username: {i["username"]}".ljust(22," "),end=" ")
            print(f"password: {i["password"]}".ljust(19," "),end=" ")
            print(f"role: {i["role"]}")
            count += 1
        
        data_person = {}

        while True:
            print("")
            number_choice_person = input("Select number of person: ")
            if number_choice_person :
                number_choice_person = int(number_choice_person)
                data_person =  data_persons[number_choice_person]
                break
        
        while True:            
            person_first= input(f"Enter new first name's person ({data_person['fist']}) : ")
            if person_first != " " and person_first != "":
                data_person["fist"] = person_first
                break
            else:
                print("First name must not empty")
        while True:            
            person_last= input(f"Enter new last name's person ({data_person['last']}) : ")
            if person_last != " " and person_last != "":
                data_person["last"] = person_last
                break
            else:
                print("Last name must not empty")
        while True:
            print("Choose type's person")
            print("1. admin")
            print("2. student")
            print("3. faculty")
            try:
                person_type = int(input(f"Select number for type ({data_person["type"]}) : "))
                if person_type != " " and person_type != "" and type(person_type) == int:
                    if int(person_type) == 1:
                        data_person["type"] = "admin"
                    if int(person_type) == 2:
                        data_person["type"] = "student"
                    if int(person_type) == 3:
                        data_person["type"] = "faculty"
                    break
                else:
                    print("Type must not empty")
            except:
                pass

        persons_table.update_row(data_person["ID"],"ID",data_person,["ID","fist","last","type"],db)
        data_login = login_table.get_data_one(data_person["ID"],"person_id",db)
        data_login["username"] = "{}.{}".format(data_person["fist"], data_person["last"][0])
        data_login["password"] = self.random_string(4)
        login_table.update_row(data_login["person_id"],"person_id",data_login,["person_id","username","password","role"],db)
        print("Update person success!")

        while True:
            print("")
            print("1. Back to menu ⬅️")
            print("0. Exit Program ❌")
            number_choice = input("Select choice: ")
            if number_choice == "1":
                break
            elif number_choice == "0":
                exit()


    def delete_person(self):
        pass

    def lead_select_action(self):
        while True:
            if self.__data_member[1] != "lead":
                break
            print(f"Menu For {self.__data_member[1].capitalize()}".center(30, "-"))
            print("1. View project's lead 📃")
            print("2. Edit project 🖋️")
            print("3. View member's project 💡")
            print("4. View advisor's project 👨")
            print("0. Exit Program ❌")
            number_choice = input("Select choice: ")
            if number_choice == "0":
                exit()
            if number_choice == "1":
                self.view_project()
            if number_choice == "2":
                self.edit_project()
            if number_choice == "3":
                self.view_member()
            if number_choice == "4":
                self.view_advisor()

    def member_select_action(self):
        while True:
            if self.__data_member[1] != "member":
                break
            print(f"Menu For {self.__data_member[1].capitalize()}".center(30, "-"))
            requested = self.check_request_project()
            requested = self.check_request_project()
            if requested:
                print("1. View request project 👁️")
                print("0. Exit Program ❌")
                number_choice = input("Select choice: ")
                if number_choice == "0":
                    exit()
                if number_choice == "1":
                    self.response_request_project()

            else:
                print("1. View project's member 📃")
                print("0. Exit Program ❌")
                number_choice = input("Select choice: ")
                if number_choice == "0":
                    exit()
                if number_choice == "1":
                    self.view_project()

    def student_select_action(self):
        while True:
            if self.__data_member[1] != "student":
                break
            print(f"Menu For {self.__data_member[1].capitalize()}".center(30, "-"))
            print("1. Create project 🪄")
            print("0. Exit Program ❌")
            number_choice = input("Select choice: ")
            if number_choice == "0":
                exit()
            if number_choice == "1":
                self.create_project()
                self.view_project()
    

    def admin_select_action(self):
        while True:
            print(f"Menu For {self.__data_member[1].capitalize()}".center(30, "-"))
            print("1. View all person 👁️")
            print("2. Add new person ➕")
            print("3. Edit persons 🖋️")
            print("0. Exit Program ❌")
            number_choice = input("Select choice: ")
            if number_choice == "0":
                exit()
            if number_choice == "1":
                self.view_all_person()
            if number_choice == "2":
                self.new_person()
            if number_choice == "3":
                self.edit_person()
            if number_choice == "4":
                self.delete_person()


    def select_action(self):
        while True:
            if self.__data_member[1] == "admin":
                self.admin_select_action()
            if self.__data_member[1] == "advisor":
                self.advisor_select_action()
            if self.__data_member[1] == "lead":
                self.lead_select_action()
            if self.__data_member[1] == "faculty":
                self.faculty_select_action()
            if self.__data_member[1] == "student":
                self.student_select_action()
            if self.__data_member[1] == "member":
                self.member_select_action()
