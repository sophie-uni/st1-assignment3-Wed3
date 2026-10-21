# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Wednesday 14:30-16:30 Group 3 (st1-assignment3-Wed3)
- Members, GitHub usernames and cohorts: Sophie Jiang (`sophie-uni`, Postgraduate/G-level)
- Repository URL: https://github.com/sophie-uni/st1-assignment3-Wed3
- Starting SHA: eb03522feb93fa4fe519ebada15cbc063076d79b

## A Requirement to issue activities

### FR-02 Patient Search

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

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | Weak | uninformative; not mentioned which files or behaviours were changed and why. |
| final version | Weak | non-descriptive and provides no architectural or functional context for future maintenance. |
| Add patient search by ID | Strong | Clear, imperative, and precisely describes the capability introduced. |
| fix stuff | Weak | Completely lacks intent, component identification, and defect traceability. |
| Prevent cancellation of completed appointments | Strong | Clear and specific; explains the exact business rule enforced. |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR violates the single-purpose review boundary. Combining unrelated code with feature work inflates review complexity, increases merge conflict risk, and obscures the feature's true diff.
- Responsibility and architecture concerns: Adding a new dependency without architectural justification risks coupling the system unnecessarily. Renaming core fields in the patient entity within an appointment PR crosses bounded context responsibilities.
- Testing and review concerns: Reviewers cannot easily determine if test failures are due to the cancellation logic or unintended side effects of the patient field renaming. It requires verifying unrelated regression paths.
- Changes to remove or separate, with reasons:
  - *Remove patient field renaming:* Extract into a separate refactoring issue and PR so impact on existing queries can be evaluated independently. 
  - *Remove architectural restructuring of unrelated files:* Keep changes strictly confined to domain, and its repository. 
  - *Remove new dependency:* Revert and evaluate whether standard library constructs satisfy current requirements without third-party libraries.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

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

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

A high commit count often reflects poor commit hygiene. For example, repeatedly saving tiny cosmetic adjustments, fixing typos, or committing broken intermediate code rather than meaningful engineering value. A single clean, cohesive, and well-tested commit that correctly implements a complex domain invariant is far more valuable. Quality is measured by adherence to requirements, architectural purity, test rigor, and maintainability, not the raw volume of Git pushes.

## L Stage 6 formative questions

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
