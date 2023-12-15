# Project manager

# Student Role
- [X]  Create a project.
- [X]  Send the request invite message to others `student`.
- [X]  Send the request invite message to `faculty` to be my `advisor`.
- [x]  After `student` have created the project, the `student` will change their role to be `lead`.

# Member Role
- [X]  Accept or reject the request invite message from `lead`.
- [X]  if `member` accept the request, `member` can view the project's detail.
- [X]  if `member` reject the request, `member` will change their role back to `student` and then they can do the same thing like `student` role.

# Lead Role
- [X] `Lead` can view the project's detail.
- [X] `Lead` can edit the project.
- [X] After `lead` have edited `member` and if `lead` have selected a new `member` and the new `member` is not the same with the old `member` then the old `member` will change the role back to `student`.
- [X] After lead have edited `advisor` and if lead have selected a new `advisor` and the new `advisor` is not the same with the old `advisor` then the old `advisor` will change the role back to `faculty`.
- [X] `Lead` can delete the project in view project's `lead`.
- [X] If `lead` delete the project, `member` will change their role back to `student`.
- [X] If `lead` delete the project, `adivisor` will change their role back to `faculty`.
- [X] If `lead` delete the project, `lead` will change their role back to `student`.
- [X] `Lead` can check all `member`'s `status` and if `member` have responded then response_date will be shown, but if not have responed then response_date will be `waiting for answer...`

# Advisor role
- [X]  `accept` or` reject` the request invite message from `lead`.
- [X]  If `advisor` accept the request, `advisor` can view the project's detail.
- [X]  If `advisor` `reject` the request, `advisor` will change their role back to `faculty` and then they can do the same thing like `faculty` role and `advisor` will delete that project then `lead`'s role will change back to `student`. 
- [X]  `Advisor` can view all project.
- [X]  `Advisor` can view their own project.
- [X]  `Advisor` can evaluation the project, then `Advisor` must choose the project that `Advisor` have to evaluation.
- [X]   If `Advisor` have selected `approve` or `reject`, then project will add in table's evaluation project.
- [X]   If `Faculty` or `advisor` have approved more than 2 people then project will change status to be `approve`.
- [X]   If `Faculty` or `advisor` have rejected more than 2 people then project will change status to be `reject`.
- [X]   If `Advisor` have evaluated then will have notice about do you want edit or not.

# Faculty role
- [X]  `Faculty` can view all project.
- [X]  `Faculty` can evaluation the project, then `Faculty` must choose the project that `Faculty` have to evaluation.
- [X]   If `Faculty` have selected `approve` or `reject`, then project will add in table's evaluation project.
- [X]   If `Faculty` or `advisor` have approved more than 2 people then project will change status to be `approve`.
- [X]   If `Faculty` or `advisor` have rejected more than 2 people then project will change status to be `reject`.
- [X]   If `Faculty` have evaluated then will have notice about do you want edit or not.

# Admin role
- [X]  `Admin` can view person's information in system.
- [X]  `Admin` can add others person to system.
- [X]  `Admin` after add person then the data will be in `login.csv` follow the format.
- [ ]  `Admin` can edit person's information in system.
- [ ]  `Admin` can delete person in system.