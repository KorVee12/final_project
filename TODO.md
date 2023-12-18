# Outline

# Project manager

# Student Role
- [X] Make a project.
- [X] Forward the invitation request message to additional `student`.
- [X] Forward the message inviting `faculty` to serve as my `advisor`.
- [x] `student` will take over the job of `lead` after they have completed the assignment.


# Member Role
- [X] Select `yes` or `no` to accept the project invitation from the `lead` project.
- [X] `member` can read the project's details if they accept the request.
- [X] if `member` declines the request, `member` will revert to the role of `student` and be able to perform the same tasks as the `student` role.


# Lead Role
- [X] `lead` has access to the project's details.
- [X] The project can be edited by `lead`.
- [X] Following the editing of `member` by `lead`, if `lead` chooses a new `member` and that new `member` differs from the previous `member`, the previous `member` will revert to the role of `student`.
- [X] Once the lead has made changes to `advisor`, if they choose a new `advisor` and they are not the same as the previous `advisor`, `advisor` will revert to `faculty`.
- [X] The project can be deleted by `lead` in the view project's `lead`.
- [X] `member` will revert to the role of `student` in the event that `lead` deletes the project.
- [X] `advisor` will revert to `faculty` if `lead` deletes the project.
- [X] `lead` will revert to the role of `student` if they destroy the project.
- [X] `lead` has the can to view each `member`'s `status`. If a `member` has replied, response_date will be displayed; if not, response_date will read `waiting for answer...`.
- [X] `lead` has the can to view each `advisor`'s `status`. If a `advisor` has replied, response_date will be displayed; if not, response_date will read `waiting for answer...`.


# Advisor role
- [X] Select `yes` or `no` to accept the project invitation from the `lead` project.
- [X] `advisor` can read the project's details if they approve the request.
- [X] In the event that `advisor` `reject` the request, `advisor` will revert to `faculty` and `lead`'s role will revert to `student`. 
- [X] `advisor` has access to every project.
- [X] `advisor` has access to evaluate every project.
- [X] After `advisor` has evaluated a project, `advisor` has to select which project to evaluate.
- [X] Project will be included to the table's evaluation project if `advisor` has chosen to `approve` or `reject`.
- [X] The status of the project will change to `approve` if more than two individuals have been approved by `faculty` or `advisor`.
- [X] The status of the project will change to `reject` if more than two individuals have been rejected by the faculty or `adviser`.
- [X] After the evaluation, the `advisor` will change the project status.


# Faculty role
- [X] `faculty` has access to every project.
- [X] After `faculty` has evaluated a project, `faculty` has to select which project to evaluate.
- [X] Project will be included to the table's evaluation project if `faculty` has chosen to `approve` or `reject`.
- [X] The status of the project will change to `approve` if more than two individuals have been approved by `faculty` or `advisor`.
- [X] The status of the project will change to `reject` if more than two individuals have been rejected by the `faculty` or `adviser`.
- [X] After the evaluation, the `faculty` will change the project status.


# Admin role
- [X] `admin` has access to the person's data in the system.
- [X] `admin` Other users can be added to the system
- [X] `admin` After adding a person, the data will be in the format specified in `login.csv`.
- [X] If a `admin` modifies a person's data in the system, `login.csv` will also receive the updated information. 
- [X] If an individual is deleted from the system, the information in `login.csv` will also be changed.
