# Evaluation Step

# Advisor
- Upon accepting the request from `lead`, `advisor` will be able to evaluate every project that `lead` has established. `advisor` must decide which project `advisor` needs to review. Subsequently, `advisor` must decide whether to `approve` or `reject` that project. The data for the project will be uploaded to `evaluation_project.csv` (the `evaluation_project table`) whether `advisor` has **approved** or **rejected** it.


# Faculty
- Upon accepting the request from `lead`, `advisor` will be able to evaluate every project that `lead` has established. `advisor` must decide which project `advisor` needs to review. Subsequently, `advisor` must decide whether to `approve` or `reject` that project. The data for the project will be uploaded to `evaluation_project.csv` (the `evaluation_project table`) whether `advisor` has **approved** or **rejected** it.


# Process Calculate
- The `status` in the `project table` of a project will change to approve if it has `approve` in the `evaluation_status` column equal to or greater than two rows in `evaluation_project.csv` (`evaluation_project table`). 
- Additionally, a project's status will change to reject if any projects in the `evaluation_project.csv``evaluation_project table` have `reject` in the `evaluation_status` column equal to or greater than two rows.
- The `lead`'s project can make changes to it if the `evaluation` step results in a rejection, and the `status` project will return to the `pendding` stage.
- The `lead`'s project can no longer be edited once it has been authorized by the `evaluation` phase.
