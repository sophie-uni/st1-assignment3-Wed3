# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Group 3 - Wednesday 4:30 - 6:30
- Members, GitHub usernames and cohorts: Hassan Ahmad, Devam, Trung Heiu, UG; Sophie
- Repository URL: https://github.com/sophie-uni/st1-assignment3-Wed3
- Starting SHA: eb03522feb93fa4fe519ebada15cbc063076d79b

## A Requirement to issue activities

### FR-02 Patient Search

- Title: FR-02 Patient Search: find a registered patient by patient ID
- Context: Patients are registered through PatientService and held in the shared SmartCareDataStore, but PatientService.find_patient still raises NotImplementedError. Booking and appointment workflows need a reliable way to retrieve the exact patient record that was registered, and to be told clearly when an ID is invalid or not registered.
- Requirement: FR-02 Patient Search. PatientService.find_patient(patient_id) returns the actual Patient object held in SmartCareDataStore. Patient IDs are strings, trimmed, non-blank and case-sensitive. An invalid or blank ID raises ValueError; a valid ID that is not registered raises LookupError. A lookup never creates a replacement object or returns a different record.
- Acceptance criteria:
  1. Given synthetic patient P001 is registered, find_patient("P001") returns the same object held in the store (identity check with `is`), with ID P001 and the registered name.
  2. Given P001 is registered, find_patient("  P001  ") returns that same stored object, because surrounding whitespace is trimmed.
  3. Given P001 is registered, find_patient("p001") raises LookupError, because IDs are case-sensitive and no case-insensitive match is made.
  4. find_patient("P999"), a valid but unregistered ID, raises LookupError and the number of stored patients is unchanged.
  5. find_patient("") and find_patient("   ") raise ValueError, and a non-string ID such as None raises ValueError.
  6. No lookup, successful or failed, adds, removes or replaces a patient in the store.
  7. The eight supplied tests in tests/test_starter.py still pass unchanged.
- Scope: In scope: implementing PatientService.find_patient in project/smartcare/services.py by reusing the store's existing validation and find method, and adding focused tests to project/tests/test_services.py. Out of scope: name, partial or fuzzy search; authentication or access control; changes to Patient fields, domain.py or data_store.py; the supplied query and menu TODOs reserved for a later stage; new dependencies.
- Definition of Done: Every acceptance criterion is shown by a meaningful assertion in tests/test_services.py. `python -m pytest` run from project/ passes, including the eight supplied tests, and `python main.py` still runs. The diff touches only the scoped files. The PR links this issue, records the test command and observed result, and discloses significant Copilot assistance. Another member has reviewed the actual diff, all feedback is resolved and approval is given on the latest commit. The PR is merged to main, this issue is closed, every member has pulled main and rerun the suite, and the tested code SHA is recorded.
- Owner: Hassan
- Actual issue link: https://github.com/sophie-uni/st1-assignment3-Wed3/issues/2

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: FR-06/FR-07 Appointment Cancellation: cancel a scheduled appointment and retain it as cancelled history
- Context: Appointments can already be booked, looked up and conflict-checked, and Appointment provides a guarded cancel transition in the domain layer. AppointmentService.cancel_appointment still raises NotImplementedError, so cancellation is not available through the service layer. Clinic history depends on cancelled appointments staying in the store rather than being removed or replaced.
- Requirement: FR-06 allows an appointment to be cancelled only while its status is SCHEDULED. FR-07 requires a cancelled appointment to hold CANCELLED status and remain retrievable as part of appointment history. AppointmentService.cancel_appointment(appointment_id) locates the stored appointment, applies the transition through Appointment.cancel and returns that same object. An unknown ID raises LookupError; a blank or invalid ID raises ValueError. Repeated cancellation, or cancellation of a COMPLETED appointment, raises ValueError without changing state.
- Acceptance criteria:
  1. Given synthetic appointment A001 is booked with status SCHEDULED, cancel_appointment("A001") returns the same stored Appointment object (identity check with `is`) and its status is AppointmentStatus.CANCELLED.
  2. After cancellation, retrieving A001 through the supplied appointment lookup returns that same object with status CANCELLED, and the number of stored appointments is unchanged.
  3. Calling cancel_appointment("A001") a second time raises ValueError and the status remains CANCELLED.
  4. Given an appointment with status COMPLETED, cancel_appointment raises ValueError and the status remains COMPLETED.
  5. cancel_appointment("A999"), a valid but unknown ID, raises LookupError and no stored appointment changes.
  6. cancel_appointment("") and cancel_appointment("   ") raise ValueError.
  7. Cancelling A001 does not change the status of any other stored appointment.
  8. Booking and practitioner-conflict behaviour is unchanged, and the eight supplied tests still pass.
- Scope: In scope: implementing AppointmentService.cancel_appointment in project/smartcare/services.py so that it finds the stored appointment and delegates the state change to Appointment.cancel, plus focused tests in project/tests/test_services.py. Out of scope: deleting, archiving or recreating appointments; rescheduling; cancellation reasons, timestamps or notifications; changes to AppointmentStatus, Appointment.cancel or other domain rules; any change to how cancelled appointments affect conflict checking unless confirmed with the tutor; unrelated renames, restructuring or new dependencies.
- Definition of Done: Every acceptance criterion is shown by a meaningful assertion, including unchanged state after each failure. The diff shows the status changing only through Appointment.cancel, with no direct assignment to protected state, no deletion and no replacement record. `python -m pytest` run from project/ passes, including the eight supplied tests, and `python main.py` still runs. The PR links this issue, records the test command and observed result, and discloses significant Copilot assistance. Another member has reviewed the actual diff and approved the latest commit after all feedback is resolved. The PR is merged to main, this issue is closed, every member has pulled main and rerun the suite, and the tested code SHA is recorded.
- Owner: Hassan
- Actual issue link: https://github.com/sophie-uni/st1-assignment3-Wed3/issues/3

## B Commit quality

| Original example                               | Strong or Weak | Reason                                                                                                                                                                                                                                                                       |
|------------------------------------------------|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| changes                                        | Weak           | Every commit contains changes, so the message says nothing about what changed or why. A reviewer cannot connect it to an issue or requirement, and nobody searching the history later can tell whether this commit is the one they need.                                     |
| final version                                  | Weak           | It describes the author's sense of progress, not a behaviour. It stops being true as soon as another fix follows, gives no scope, and suggests a large mixed commit rather than one coherent step.                                                                           |
| Add patient search by ID                       | Strong         | It is in the imperative, names one specific behaviour and maps directly to FR-02. A reviewer can check that the commit contains only the lookup and its tests. Adding the issue reference, for example "(#1)", would make it fully traceable.                                |
| fix stuff                                      | Weak           | It names no defect, component or behaviour, and "stuff" implies several unrelated fixes bundled together. The commit cannot be reviewed against a requirement or safely reverted on its own.                                                                                 |
| Prevent cancellation of completed appointments | Strong         | It states the exact rule being enforced, which is the FR-06 guard that cancellation is only allowed from SCHEDULED. It describes behaviour rather than files, so a reviewer knows to look for the guard and for a test showing that a COMPLETED appointment stays COMPLETED. |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR is linked to FR-06/FR-07, but the patient-field renames, the restructuring and the new dependency have no connection to that issue or its acceptance criteria. Mixing them makes the diff much larger, hides the cancellation lines among unrelated changes, and means that approving the PR also approves work nobody asked for or agreed to. The changes also cannot be reverted independently: if the rename causes a defect, rolling it back would remove cancellation as well.
- Responsibility and architecture concerns: Renaming Patient fields changes the public interface of a domain object that PatientService, the data store, main.py, the supplied tests and other members' open branches depend on, so it is a cross-cutting decision that needs team agreement. Restructuring unrelated code risks moving responsibilities, for example pulling state rules out of Appointment into a service or a new manager class, which conflicts with the design where Appointment owns its transitions and services only coordinate the store and domain objects. The new dependency changes the runtime environment for every member and for marking, even though cancellation can be met with the existing domain method and the standard library; its licence, security and provenance would also need review.
- Testing and review concerns: A green run only shows that the existing assertions still pass. It does not show that the renamed fields were updated everywhere, that no supplied test was edited to fit the rename, or that the cancellation tests check status, same-object return, continued retrieval and unchanged state after failure. A passing run on the author's machine also does not prove the new dependency installs and works on every other clone. A large mixed diff gets a weaker review, because the reviewer's attention is spread across unrelated lines, and the PR description would need to state exactly which tests were run, from which directory and at which SHA.
- Changes to remove or separate, with reasons:
  - Patient field renames: remove from this PR. They are unrelated to cancellation and change a shared interface. If there is a genuine reason, raise a separate issue, agree it as a team and make it in its own PR, keeping the supplied tests intact unless the tutor approves a change.
  - Unrelated restructuring: remove. If it has a clear benefit, it belongs in a separate refactoring issue and PR that is reviewed on its own and shown not to change behaviour.
  - New dependency: remove. It is not needed for the cancellation contract and existing runtime dependencies are to be preserved; any future dependency needs a justified issue and tutor agreement.
  - Keep: the cancel_appointment implementation that delegates to Appointment.cancel, and its focused tests in tests/test_services.py.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: The response does not say which requirement or acceptance criteria were checked, and it cites no diff lines. Copilot cannot run tests by reading a diff, so "tests pass" has no command, working directory, observed output or commit SHA behind it. It says nothing about which tests exist or what they assert, whether the status change goes through Appointment.cancel rather than direct assignment, deletion or a replacement record, how error paths behave and whether state is unchanged after a failure, whether the supplied tests are untouched, or whether the diff contains unrelated changes. It is an approval claim with no supporting evidence.
- Follow-up review question 1: Which FR-06 and FR-07 acceptance criteria did you check, and which specific diff lines satisfy each one?
- Follow-up review question 2: What test command was run, from which directory, against which commit SHA, and what was the observed output? If no run was observed, what is the claim "tests pass" based on?
- Follow-up review question 3: Which assertions prove that cancel_appointment returns the same stored object, that its status is CANCELLED, and that it can still be retrieved afterwards with the appointment count unchanged?
- Follow-up review question 4: Does any changed line assign the appointment status directly, delete the appointment or create a replacement, or is the transition made only through Appointment.cancel?
- Follow-up review question 5: What happens on a repeated cancellation, on a COMPLETED appointment, with an unknown ID and with a blank ID, and which tests show both the exception type and that state is unchanged after each failure?
- Additional questions if useful: Does the diff contain anything unrelated to the linked issue, such as renamed fields, new dependencies or edits to tests/test_starter.py? Which test shows that booking and practitioner-conflict checks still behave as before? Which inputs remain untested, for example an ID with surrounding whitespace or different letter case?

## E Team workflow agreement

| Practice                            | Team agreement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Branch naming                       | `<type>/<issue-number>-<short-description>` in lowercase kebab-case, for example `feature/1-patient-search`, `feature/2-cancel-appointment` or `fix/5-lookup-whitespace`. One branch per issue, always created from freshly pulled main. No feature work is committed directly to main.                                                                                                                                                                                                                                          |
| Commit message convention           | Imperative summary of about 60 characters or fewer that describes a behaviour or test intention, followed by the issue reference, for example "Add patient lookup by ID (#1)". A short body explains why when it is not obvious. Each commit is one coherent change, checked with `git diff --staged` for unrelated edits and secrets before committing. Messages such as "changes", "wip" or "fix stuff" are not used, and work is not split artificially.                                                                      |
| PR size                             | One issue per PR. Production changes stay within the files named in the issue scope, plus their tests, so a reviewer can read the whole diff in one sitting (normally under about 200 changed lines including tests). Anything unrelated that is noticed during the work becomes a new issue rather than part of the current PR.                                                                                                                                                                                                 |
| Another-member review requirement   | Every PR needs an approving review from a member other than the author, based on the actual diff in GitHub. The reviewer records independent observations as a PR comment before consulting Copilot. The reviewer role rotates each PR so that every member both implements and reviews. Self-review is preparation only and does not count.                                                                                                                                                                                     |
| Merge rule                          | Merge only when the linked issue's acceptance criteria are met, the full suite passes from project/ on the latest branch commit with the command and result stated in the PR, every review comment has been addressed and rechecked, and another member has approved the latest commit. Merges go through the GitHub PR using a merge commit so each member's commits stay attributable. After merging, the linked issue is closed, the branch is deleted, and the team is told so every member pulls main and reruns the tests. |
| Significant Copilot disclosure rule | Any Copilot output that shaped code, tests, issue text or review findings, beyond trivial autocompletion, is disclosed in the PR description and recorded in section H with its purpose, output summary, human check, Accept/Modify/Reject decision and verification. Only the necessary synthetic project context and diff are shared; credentials, tokens, peer-assessment material and personal information are never shared. The author must be able to explain every submitted line.                                        |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link                                                   | Requirement                                                                                                           | Owner  | Acceptance criteria or precise link                                                                                                                                                                                                                                                                                                 | Status  |
|--------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| https://github.com/sophie-uni/st1-assignment3-Wed3/issues/1  | FR-02 Patient Search                                                                                                  | Hassan | find_patient returns the same stored Patient for a trimmed, case-sensitive ID; a valid unknown ID raises LookupError; a blank or invalid ID raises ValueError; no record is created or replaced; supplied tests pass.                                                                         | Closed  |
| https://github.com/sophie-uni/st1-assignment3-Wed3/issues/2  | FR-06 Appointment Cancellation with FR-07 retained history                                                            | Hassan | cancel_appointment returns the same stored Appointment with status CANCELLED, still retrievable and not deleted; repeated or COMPLETED cancellation raises ValueError with state unchanged; unknown ID raises LookupError; blank ID raises ValueError; booking and conflict checks unchanged. | Closed  |


## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

[TO FILL: repeat this block for each other member]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

A commit count shows how often someone saved work to the history, not what that work achieved. In our Stage 6 work, implementing cancel_appointment correctly is only a few lines and can reasonably be one coherent commit together with its tests. The work that makes the change trustworthy often produces few or no commits: refining the acceptance criteria so that repeated and COMPLETED cancellations are covered, reviewing the actual diff for direct state assignment or deletion, writing assertions that prove the same object is returned and that state is unchanged after a failure, and confirming the merged result on every clone. Commit habits also differ between members, since one person may commit every small edit while another commits only complete, reviewed steps, and pairing can place shared work under one account. A count can also be inflated by splitting work artificially, which our workflow agreement rules out. Contribution is therefore judged from traceable evidence: issues refined, diffs authored, tests that check the requirement, review comments that changed the code, and integration problems resolved.

## L Stage 6 formative questions

1. What is version control?

Version control is a system that records changes to files over time as a history of commits, so a team can see who changed what, when and why, compare versions and return to an earlier state. Git is distributed, so every clone holds the full history, and GitHub hosts the shared remote repository that the team pushes to and pulls from. It allows several people to work on the same project in parallel and combine their work safely.

2. Why is a feature branch useful?

A feature branch keeps one focused change separate from main while it is being built, so main stays stable and runnable for everyone. Members can work on different issues at the same time without overwriting each other, and the branch becomes the unit that is reviewed in a pull request. If an approach does not work, the branch can be discarded without affecting main, and the link from issue to branch to PR to merge stays easy to trace.

3. What makes a commit a good engineering commit?

A good commit contains one coherent, logical change, such as a service method together with its tests, and leaves the code in a working state. It includes only related files, with no unrelated edits, secrets or generated clutter, which is confirmed with `git diff --staged` before committing. Its message describes the behaviour or intention in the imperative and references the issue, and it is small enough to review and revert on its own.

4. What is a pull request?

A pull request is a proposal to merge one branch into another, here a feature branch into main. It shows the diff, commits and linked issue, states what behaviour changed and which tests were run, and gives the team a place to comment, request changes and approve before the change is integrated.

5. What is the purpose of code review?

Code review is a check by another person of the actual changed lines before they reach main. The reviewer compares the change with the requirement and acceptance criteria and checks responsibility boundaries, correctness including error paths, the strength of the test assertions, readability and unrelated scope. Review catches defects the author missed, spreads understanding so every member can explain the code, and keeps main stable.

6. What does a Git diff show?

A Git diff shows the line-by-line differences between two states of the files: the working directory against the staging area (`git diff`), the staging area against the last commit (`git diff --staged`), or two commits or branches. Removed lines are marked with `-` and added lines with `+`, grouped into hunks with surrounding context and file names. A diff shows what changed, but not whether the change is correct or why it was made.

7. What is a Definition of Done?

A Definition of Done is a shared checklist that every work item must satisfy before the team treats it as complete. It goes beyond "code written" to include demonstrated acceptance criteria, meaningful passing tests including the existing ones, review by another member, resolved feedback, appropriate documentation, and merging with verification of the integrated result. Unlike acceptance criteria, which are specific to one item, the Definition of Done applies to every item.

8. What is the appropriate role of GitHub Copilot in pull-request review?

Copilot is an approved assistant, not the reviewer of record. It is consulted only after the human reviewer has recorded independent observations, and it is given the actual requirement, acceptance criteria and diff with synthetic data only. Its summaries, risks and questions are checked against the code, the requirements and an observed test run, then explicitly accepted, modified or rejected and disclosed. Copilot cannot approve a merge, cannot confirm that tests ran, and does not replace another member's review; the team remains accountable for every change.

9. Why should individual contribution not be judged only by commit count?

Commit count measures how often someone committed, not the value, quality or difficulty of the work. Commit habits vary, and important work such as reviewing, testing, refining issues, debugging integration, pairing and mentoring produces few commits, while counts can be inflated by splitting changes artificially. Contribution should be judged from traceable evidence such as linked issues, authored diffs, meaningful tests, review comments that changed the code and integration results.

10. What is the Stage 6 engineering rule?

No change reaches main unless it can be traced from a requirement, through a focused issue and feature branch, to meaningful tests and another member's review of the actual diff, followed by verification of the integrated result on main. Main is kept stable and runnable. Passing tests and Copilot output support this evidence, but they never replace checking the requirement and human review.

## M Completion and handover

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
