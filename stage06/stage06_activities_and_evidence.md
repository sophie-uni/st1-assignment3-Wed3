# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Wednesday 14:30-16:30 Group 3 (st1-assignment3-Wed3)
- Members, GitHub usernames and cohorts: Sophie Jiang (`sophie-uni`, Postgraduate/G-level),Hassan Ahmad, Devam, Trung Heiu
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
- Title: Implement Stored Patient Lookup by ID with Exception Handling in PatientService class in servives.py
- Context: Clinic workflows require retrieving existing, verified patient records by their unique identifier without silently substituting missing patients or accepting malformed query keys.
- Requirement: Implement find_patient(self, patient_id: str) -> Patient to return the stored Patient entity corresponding to a valid ID. The method must validate the input format and enforce strict error signaling for invalid keys or missing records rather than creating a replacement patient.
- Acceptance criteria:
  - Successful: Returns the existing Patient when a matching, valid patient_id string is provided.
  - Blank / Invalid Input: Raises ValueError if patient_id is blank, whitespace-only, or not a valid non-empty string.
  - Absence: Raises LookupError('Patient not found') if no matching patient exists in self.data_store.
  - No Replacement Patient: The system must not create, default to, or return a placeholder/replacement patient on a lookup miss.
  - Layer Purity: Coordinates lookup exclusively via self.data_store without direct SQL execution or terminal I/O statements.
- Scope: 
  - In-scope: ID format verification (ValueError), querying self.data_store.find_patient, absence check (LookupError), and unit test assertions.
  - Out-of-scope: Creating new patient records, partial name matching or search filtering, and CLI input/output rendering.
- Definition of Done: 
  - Input validation for blank/invalid strings is present.
  - All acceptance criteria pass tests.
  - Returns the exact stored Patient instance on success.
  - Peer code review completed and merged via pull request into main branch in Github.
- Owner: Sophie Jiang
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
- Title: Implement Appointment Cancellation with Retained History in AppointmentService class in services.py
- Context: Clinic workflows require booked appointments to be cancelled upon request while maintaining complete historical records for auditing, reporting, and dispute resolution without removing records from storage.
- Requirement: Implement AppointmentService.cancel_appointment(appointment_id: str) -> Appointment. The method must look up the stored appointment via the shared store, delegate cancellation to the domain object's transition method, ensure the record is retained in the data store, and return the updated appointment object. It must enforce error handling by raising LookupError for unknown or absent IDs and letting domain transition violations raise ValueError without altering appointment state.
- Acceptance criteria: 
  - Successful Cancellation: When a valid ID for an existing, cancellable appointment is provided, the method invokes the domain object's cancel() method, updates its status, and returns the modified Appointment object.
  - History Retained (FR-07): The appointment record remains in self.data_store, not be deleted or removed; future lookups retrieve the cancelled record.
  - Absence: If appointment_id is blank, invalid, or does not exist in self.data_store, a LookupError is raised or ValueError propagated if delegating to find_appointment.
  - Invalid Transition: If the appointment is in a state that cannot be cancelled, e.g., already completed or cancelled, an invalid transition ValueError is raised, leaving the appointment's state unchanged.
  - No Direct SQL/Storage Leaks: Workflow rely strictly on the Appointment entity and self.data_store interface.
- Scope: 
  - in-scope: AppointmentService.cancel_appointment, domain delegation to appointment.cancel(), exception propagation (LookupError, ValueError), and unit tests for valid/invalid state transitions.
  - Out-of-scope: Physical record deletion, patient notification dispatch, and Stage 9 practitioner listing. 
- Definition of Done: 
  - NotImplementedError is replaced with the functional implementation.
  - Passes unit tests for both successful cancellation and invalid transitions (LookupError, ValueError).
  - History retention verified: data store retains the cancelled appointment record.
  - Peer code review completed and merged into main in Github.
- Owner: Sophie Jiang
- Actual issue link: https://github.com/sophie-uni/st1-assignment3-Wed3/issues/3

## B Commit quality

| Original example                               | Strong or Weak | Reason                                                                                                                                                                                                                                                                       |
|------------------------------------------------|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| changes                                        | Weak           | Every commit contains changes, so the message says nothing about what changed or why. A reviewer cannot connect it to an issue or requirement, and nobody searching the history later can tell whether this commit is the one they need.                                     |
| final version                                  | Weak           | It describes the author's sense of progress, not a behaviour. It stops being true as soon as another fix follows, gives no scope, and suggests a large mixed commit rather than one coherent step.                                                                           |
| Add patient search by ID                       | Strong         | It is in the imperative, names one specific behaviour and maps directly to FR-02. A reviewer can check that the commit contains only the lookup and its tests. Adding the issue reference, for example "(#1)", would make it fully traceable.                                |
| fix stuff                                      | Weak           | It names no defect, component or behaviour, and "stuff" implies several unrelated fixes bundled together. The commit cannot be reviewed against a requirement or safely reverted on its own.                                                                                 |
| Prevent cancellation of completed appointments | Strong         | It states the exact rule being enforced, which is the FR-06 guard that cancellation is only allowed from SCHEDULED. It describes behaviour rather than files, so a reviewer knows to look for the guard and for a test showing that a COMPLETED appointment stays COMPLETED. |
| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | Weak | uninformative; not mentioned which files or behaviours were changed and why. |
| final version | Weak | non-descriptive and provides no architectural or functional context for future maintenance. |
| Add patient search by ID | Strong | Clear, imperative, and precisely describes the capability introduced. |
| fix stuff | Weak | Completely lacks intent, component identification, and defect traceability. |
| Prevent cancellation of completed appointments | Strong | Clear and specific; explains the exact business rule enforced. |

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
- Scope concerns: The PR violates the single-purpose review boundary. Combining unrelated code with feature work inflates review complexity, increases merge conflict risk, and obscures the feature's true diff.
- Responsibility and architecture concerns: Adding a new dependency without architectural justification risks coupling the system unnecessarily. Renaming core fields in the patient entity within an appointment PR crosses bounded context responsibilities.
- Testing and review concerns: Reviewers cannot easily determine if test failures are due to the cancellation logic or unintended side effects of the patient field renaming. It requires verifying unrelated regression paths.
- Changes to remove or separate, with reasons:
  - *Remove patient field renaming:* Extract into a separate refactoring issue and PR so impact on existing queries can be evaluated independently. 
  - *Remove architectural restructuring of unrelated files:* Keep changes strictly confined to domain, and its repository. 
  - *Remove new dependency:* Revert and evaluate whether standard library constructs satisfy current requirements without third-party libraries.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."
(Submitted by Hassan, reviewed by Sophie)
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

(Submitted by Sophie)
- Missing evidence: There was no check for whether the architectural layers were being used correctly, no review of whether unusual or edge-case scenarios were properly tested such as rules for changing statuses, and no confirmation that the data storage layer remained independent from the rest of the system.
- Follow-up review question 1: Are there unit tests verifying that attempting to cancel an already completed appointment?
- Follow-up review question 2: How would the system be affected if SmartCareDataStore were replaced with a database backed repository implementation?
- Follow-up review question 3: How do the lookup methods enforce the documented requirement to raise ValueError for blank or invalid IDs?
- Follow-up review question 4: Was the unimplemented list_practitioner_appointments() method identified during testing, and how would its absence affect system functionality?
- Follow-up review question 5: How was the separation of responsibilities between the service layer, domain objects, and persistence layer validated during the review?
- Additional questions if useful: no

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | Creating own isolate branch and each branch only apply single or simple tasks |
| Commit message convention | clear and simple description of tasks, what has been done |
| PR size | keep samll and focused |
| Another-member review requirement | Yes, team member should can review each others |
| Merge rule | Team leader confirms no conflit and merge to Main, then team member should delete own branch and push |
| Significant Copilot disclosure rule | AI-generated contents should logged in the PR description and verified by a human. |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| https://github.com/sophie-uni/st1-assignment3-Wed3/issues/1 | FR-02 Patient Search | Sophie Jiang | Returns existing Patient for valid ID; raises ValueError for blank/invalid ID; raises LookupError when absent; strictly forbids creating a replacement patient. | Closed |
| https://github.com/sophie-uni/st1-assignment3-Wed3/issues/2 | FR-06 Appointment Cancellation & FR-07 History | Sophie Jiang | Retrieves stored appointment via find_appointment; raises LookupError for absent/invalid ID; delegates state change to domain appointment.cancel(); invalid transitions raise ValueError leaving state unchanged; retains record in data_store. | Closed |

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

(Hassan) A commit count shows how often someone saved work to the history, not what that work achieved. In our Stage 6 work, implementing cancel_appointment correctly is only a few lines and can reasonably be one coherent commit together with its tests. The work that makes the change trustworthy often produces few or no commits: refining the acceptance criteria so that repeated and COMPLETED cancellations are covered, reviewing the actual diff for direct state assignment or deletion, writing assertions that prove the same object is returned and that state is unchanged after a failure, and confirming the merged result on every clone. Commit habits also differ between members, since one person may commit every small edit while another commits only complete, reviewed steps, and pairing can place shared work under one account. A count can also be inflated by splitting work artificially, which our workflow agreement rules out. Contribution is therefore judged from traceable evidence: issues refined, diffs authored, tests that check the requirement, review comments that changed the code, and integration problems resolved.
(Sophie) A high commit count often reflects poor commit hygiene. For example, repeatedly saving tiny cosmetic adjustments, fixing typos, or committing broken intermediate code rather than meaningful engineering value. A single clean, cohesive, and well-tested commit that correctly implements a complex domain invariant is far more valuable. Quality is measured by adherence to requirements, architectural purity, test rigor, and maintainability, not the raw volume of Git pushes.

## L Stage 6 formative questions
(Hassan)
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

(Sophie)
1. What is version control?

A system that tracks changes to files over time, enabling multiple developers to collaborate, inspect revision histories, revert to previous states, and maintain parallel lines of development safely.

2. Why is a feature branch useful?

It isolates work-in-progress code from the stable `main` branch, allowing developers to build, test, and review new features without breaking production stability or disrupting team members.

3. What makes a commit a good engineering commit?

It contains a single logical change, includes a concise imperative commit message describing the intent, leaves the repository in a compiling and testable state, and does not mix unrelated formatting or scope changes.

4. What is a pull request?

A formal proposal to merge changes from a feature branch into a target branch, providing a dedicated space for peer review, continuous integration test verification, and architectural critique.

5. What is the purpose of code review?

To identify defects, architectural violations, security risks, and maintainability issues early; to ensure adherence to team coding standards and requirements; and to share domain knowledge across the team.

6. What does a Git diff show?

The exact line-by-line additions, modifications, and deletions between two commits, branches, or between the working tree and the index.

7. What is a Definition of Done?

An agreed checklist of criteria that a user story or task must meet before it is considered complete.

8. What is the appropriate role of GitHub Copilot in pull-request review?

An auxiliary verification and linting tool that can highlight missed edge cases or syntax improvements. It must never act as the sole approver; human engineering judgment is required to evaluate architectural fit and requirement compliance.

9. Why should individual contribution not be judged only by commit count?

Commit frequency does not correlate with complexity or quality. Essential engineering activities, such as architectural design, refactoring, thorough code reviews, mentoring, and writing detailed specifications, do not produce inflated commit metrics.

10. What is the Stage 6 engineering rule?

Human understanding of domain rules and requirements must drive all design and refactoring decisions, using AI only to review or assist, followed by rigorous test verification.

## M Completion and handover

- Starting SHA: eb03522feb93fa4fe519ebada15cbc063076d79b
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: /st1-assignment3-Wed3
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
