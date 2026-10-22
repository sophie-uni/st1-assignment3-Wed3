# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Group 3 / Wed 2:30 - 4:30 Group 3
- Members, GitHub usernames and cohorts:
- Repository URL: \[response\]
- Starting SHA: \[response\]

## A Requirement to issue activities

### FR-02 Patient Search

- Title: FR-02 Patient Search
- Context: The clinic needs a reliable way to find existing patient records before creating duplicates. Patient records contain a patient ID, name, DOB, phone, email, and medical notes. The system must permit a receptionist to search by name or patient ID without creating a duplicate record or inventing fuzzy search logic.
- Requirement: The system must enable receptionists to search for existing patients by patient ID or name and return the actual stored Patient record when an ID matches. Invalid or blank IDs must raise a ValueError or return a clear validation error. Search must be deterministic and not invent or silently return a different record.
- Acceptance criteria:

1. Given a valid patient ID, when the receptionist searches, then the system returns the exact stored Patient record associated with that ID.
2. Given an unknown patient ID, when the receptionist searches, then the system raises LookupError and does not create or return a replacement record.
3. Given a blank or invalid patient ID, when the receptionist searches, then the system raises a ValueError or LookupError with a clear message.
4. Given a valid patient name, when the receptionist searches, then the system returns matching patient records or a clear "No patients found" message.
5. Given a duplicate patient scenario, when the receptionist searches, then the system identifies existing records before creating a new one.
6. Scope: This issue is limited to patient lookup behaviour and validation. It does not include patient record creation, UI, or broader patient management workflows.

- Definition of Done:

1. Lookup method behavior matches the requirement contract.
2. Validation is implemented for blank, invalid, or unknown IDs.
3. Existing tests for patient lookup pass.
4. No fuzzy or implicit matching is introduced beyond the specified requirements.

- Owner: \[insert name/role\]; Actual issue link: \[response\]

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: FR-06 Appointment Cancellation with FR-07 retained history
- Context: The clinic requires appointment cancellation without losing the original appointment record. A cancellation must trigger the domain transition from SCHEDULED to CANCELLED, while retaining the original appointment object and recording cancellation reason and timestamp. This ensures the system preserves auditability and history
- Requirement: The system must allow cancellation of a scheduled appointment through the domain method Appointment.cancel(). Cancellation must update the domain status to CANCELLED and record the reason and timestamp, while preserving the original object. The system must not silently delete the record or replace it with a new object. Repeated cancellation or cancellation of a completed appointment must raise a ValueError or domain-specific error without changing state.
- Acceptance criteria:
  - Given a scheduled appointment, when the receptionist cancels it, then the appointment status becomes CANCELLED and the cancellation reason/timestamp are recorded.
  - Given a cancelled appointment, when the same cancellation is attempted again, then the system raises a ValueError and the state remains unchanged.
  - Given a completed appointment, when cancellation is attempted, then the system raises a ValueError and does not change state.
  - Given a valid cancellation request, when cancellation occurs, then the original appointment object remains in memory/history and is not replaced by a new object.
  - Given a scheduled appointment, when the system cancels it, then the record remains retrievable and its history remains intact.
- Scope: This issue covers the cancellation transition, reason/timestamp retention, and the requirement to keep the original appointment object in memory. It does not include UI, notifications, or broader workflow changes outside the cancellation contract.
- Definition of Done:
  - Domain transition is enforced in the model.
  - Historical records remain available after cancellation.
  - Validation for invalid state transitions is implemented.
  - Existing tests for appointment cancellation and retrieval pass.
- Actual issue link: \[response\]

## B Commit quality

| Original example                                 | Strong or Weak | Reason                                                                                                                                                                |
| ------------------------------------------------ | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _changes_                                        | Weak           | Too vague. It does not explain what changed, why it changed, or what behaviour it affects. It provides no evidence of a specific requirement or test being addressed. |
| _final version_                                  | Weak           | It is not descriptive enough to explain intent. It does not communicate the change in behaviour or the reason behind it.                                              |
| _Add patient search by ID_                       | Strong         | This clearly states the feature and target behaviour. It communicates a specific requirement and is easy to understand in context.                                    |
| _fix stuff_                                      | Weak           | It is non-specific and gives no useful information about what was fixed or why. It does not support traceability or review.                                           |
| _Prevent cancellation of completed appointments_ | Strong         | This clearly describes the logic change, the domain rule, and the relevant requirement being enforced. It is easy to validate and review.                             |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR changes unrelated patient field names and refactors code outside the cancellation feature. This broadens the scope beyond the requirement being implemented.
- Responsibility and architecture concerns: The PR mixes domain logic (cancellation state transition) with unrelated refactoring and naming cleanup. That makes the responsibility boundaries less clear and reduces reviewability.
- Testing and review concerns: The review should focus on whether the cancellation behaviour is correctly implemented and whether the retained-history requirement is preserved. It should not be used to approve unrelated refactors or dependency changes without justification.
- Changes to remove or separate, with reasons:
  - Rename unrelated patient fields: remove or separate, because it is not required by the cancellation contract and changes unrelated domain semantics.
  - Restructure unrelated code: remove or separate, because it introduces churn outside the issue and makes review harder.
  - Add new dependency: remove or separate, because it broadens the system footprint without evidence tied to the requirement.
  - Keep only the cancellation logic and the retained-history logic, because those are directly linked to FR-06 and FR-07.
- Outcome: This PR should be narrowed to a single feature concern: cancellation behaviour and retained history. All unrelated changes should be reverted or moved to a separate issue/PR.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

Missing evidence:

- No test names or commands are listed.
- No evidence of the exact requirement being checked.
- No proof that both positive and negative transitions were exercised.
- No evidence of the retained-history requirement or path through the domain object.
- No check that the requirement contract is preserved in the object state, not just those tests.

Follow-up review questions:

1. Which test specifically validates that a cancelled appointment remains retrievable and does not get silently deleted?
2. How do you verify that the system raises a ValueError when canceling an already cancelled appointment or a completed appointment?
3. Which assertion proves the original object is retained and not replaced by a new instance?
4. What evidence shows the appointment status change is enforced inside the domain object rather than in the service layer?
5. Which test confirms the cancellation reason and timestamp are preserved and not lost?
6. What is the exact command and result for the relevant test suite you ran?
7. Which requirement IDs are being verified by these tests: FR-06, FR-07, and the related acceptance criteria?
8. Does the review examine invalid input, unknown IDs, and cancelled/completed state transitions, or only the happy path?
9. Has the review checked that this PR does not include out-of-scope refactoring or dependency changes?
10. What evidence shows that the new code preserves the intended business rule and not just superficial test pass status?

Additional questions if useful:

- Did the review inspect the actual diff or only the green status?
- Which assertion confirms that the domain object remains unchanged when invalid cancellation is attempted?
- Which requirement did the AI review test against, and which one was not tested?

## E Team workflow agreement

| Practice                              | Team agreement                                                                                                                                                                                                          |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _Branch naming_                       | Use a consistent branch naming convention such as: feature/&lt;short-name&gt;, fix/&lt;issue&gt;, or bugfix/&lt;issue&gt;. Branches must be short, descriptive, and tied to the issue or requirement being implemented. |
| _Commit message convention_           | Use imperative, behaviour-based commit messages. Example: "Prevent cancellation of completed appointments". Commit messages should say what changed, not generic labels like "changes" or "final version".              |
| _PR size_                             | Keep PRs small and focused. One feature or one issue per PR. Large refactors or unrelated cleanup must be separated into a different branch or PR.                                                                      |
| _Another-member review requirement_   | At least one different team member must review each PR before merge. Self-review is useful preparation but cannot satisfy the requirement.                                                                              |
| _Merge rule_                          | Merge only after acceptance criteria are satisfied, review comments are addressed, and the main branch is still green. PRs must not be merged with unresolved review concerns.                                          |
| _Significant Copilot disclosure rule_ | Any significant Copilot usage must be disclosed in the PR description or review record. This includes generated code, major logic suggestions, or large refactors.                                                      |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link  | Requirement                                                | Owner    | Acceptance criteria or precise link                                                                                                                                                                                 | Status |
| ----------- | ---------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| \[issue 1\] | FR-02 Patient Search                                       | \[name\] | Search by valid patient ID returns the exact stored record; invalid/blank IDs raise ValueError or LookupError; unknown IDs raise LookupError; no silent false matches                                               | Open   |
| \[issue 2\] | FR-06 Appointment Cancellation with FR-07 retained history | \[name\] | Cancelling a scheduled appointment sets status CANCELLED, records reason/timestamp, retains the original object; repeated cancellation and cancellation of completed appointment raises ValueError; state unchanged | Open   |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: \[response\]
- Linked issue and requirement: \[response\]
- Feature branch: \[response\]
- Changed behaviour: \[response\]
- Meaningful commits: \[links\]
- Test command, directory and observed result: \[response\]
- Another-member reviewer: \[response\]
- Human observations recorded before Copilot: \[link and time\]
- Requirement, responsibilities, test assertions and unrelated-scope checks: \[response\]
- Key feedback: \[response\]
- Author response/change and verification: \[response\]
- Reviewer recheck and approval: \[link\]
- Merge outcome and SHA: \[response\]
- Significant Copilot assistance: \[summary or none\]
- Linked issue closure: \[response\]
- Each member updated main: \[member and confirmation\]
- Integrated verification after merge: \[command, directory, result and code SHA\]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: \[response\]
- Prompt/purpose and relevant issue/diff: \[response\]
- Summary of output: \[response\]
- Human check against actual code, requirements and tests: \[response\]
- Decision — Accept / Modify / Reject: \[select\]
- Reason: \[response\]
- Verification/evidence: \[link and result\]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot:
  - The issue boundaries
  - The exact requirement wording
  - The difference between service contract and domain object state
  - The need to preserve history and not replace objects
  - The difference between duplicate prevention and invalid search semantics
- Copilot noticed:
  - Additional edge cases such as blank/unknown IDs
  - The need for explicit validation and error conditions
  - The need to preserve history and not silently lose object state
- Overlap: Both human reviewer and Copilot identified the need to validate blank/unknown IDs and preserve exact-record semantics.
- Where Copilot was limited:
  - It did not know the project's actual requirement context unless prompted with the exact requirement IDs
  - It could suggest generic validation but could not replace the human review of scope, architecture, and domain responsibility
- What did the human reviewer notice that Copilot did not:
  - That the PR had unrelated renames and refactoring
  - That the cancellation issue had to preserve the original appointment object in memory
  - That the change must be limited to the service contract, not broaden into patient field cleanup
- Human judgement accepted, modified, or rejected:
  - Accepted: validation for blank/unknown IDs
  - Modified: some AI suggestions required domain-specific naming and state checks
  - Rejected: notification logic, extra dependencies, unrelated refactors
- Why evidence justified the human review:
  - The actual requirement text, domain model, and acceptance criteria were used to evaluate the change
  - The human review checked the real object contract and state transition, not just "green tests"
- Final outcome: A human review is stronger than a Copilot review because it checks requirement traceability, architectural boundaries, and the actual business contract.

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: \[response\]
- Implementation: \[work and evidence\]
- Testing: \[work and evidence\]
- Review: \[work and evidence\]
- Issue refinement: \[work and evidence\]
- Design and responsibility discussion: \[work and evidence\]
- Debugging or integration: \[work and evidence\]
- Documentation or team support: \[work and evidence\]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

A high commit count does not necessarily indicate strong contribution because commit count measures volume, not quality, traceability, or correctness. A large number of small or noisy commits can include refactors, duplicate work, or low-value changes without addressing the requirements or acceptance criteria. In contrast, a smaller, well-scoped set of commits may demonstrate deeper understanding, clearer design decisions, focus, and stronger evidence. A strong contribution is one that:

1. is tied to a requirement and acceptance criterion
2. contains meaningful behavioural changes
3. includes tests or verification evidence
4. addresses the actual domain rule and not unrelated churn
5. is reviewed and discussed, not just created
6. preserves scope boundaries and avoids unnecessary complexity

In this project, contribution quality is judged by:

1. requirement traceability
2. test evidence
3. issue and PR scope discipline
4. correct domain behaviour
5. review quality and resolve of concerns
6. whether the changes are meaningful and not just commit volume

## L Stage 6 formative questions

1. What is version control?

🡺 Version control tracks changes to files over time. It lets teams collaborate, compare versions, revert mistakes, and keep a clear history of the project. Git is the most common example.

1. Why is a feature branch useful?

🡺 A feature branch isolates one change from the main branch. It reduces conflict, keeps work focused, and makes review and testing easier before merging.

1. What makes a commit a good engineering commit?

🡺 A good commit is small, intentional, and clearly explains a specific change or behaviour. It should match a requirement or test and be easy for others to review.

1. What is a pull request?

🡺 A pull request is a request to merge code from one branch into another. It is a review checkpoint where team members inspect the diff, check requirements, and decide whether the change is ready to merge.

1. .What is the purpose of code review?

🡺 Code review checks correctness, scope, quality, and requirements coverage. It helps catch bugs, design issues, and over-scoped changes before they reach the main branch.

1. What does a Git diff show?

🡺 A Git diff shows exactly what changed between versions: added, removed, or modified lines. It helps reviewers understand the change and spot unintended edits.

1. What is a Definition of Done?

🡺 A Definition of Done is the agreed standard for when a task is complete. It usually includes meeting the requirement, passing relevant tests, code review, and no unresolved issues.

1. What is the appropriate role of GitHub Copilot in pull-request review?

🡺 Copilot can suggest edge cases and review checks, but it should not replace human judgement. Humans must still verify requirements, architecture, scope, and correctness.

1. Why should individual contribution not be judged only by commit count?

🡺 Commit count measures volume, not value. A small number of well-scoped, correct, tested changes can be more valuable than a large number of weak or unrelated commits.

10\. What is the Stage 6 engineering rule?

🡺 The Stage 6 rule is that work must be evidence-based, requirement-linked, reviewed, and scoped. Strong engineering is about correctness, traceability, and collaboration, not just raw commit volume.

## M Completion and handover

- Starting SHA: \[response\]
- Final Stage 6 code SHA: \[response\]
- Test command: \[response\]
- Working directory: \[response\]
- Observed result: \[response\]
- PR and another-member reviewer: \[links\]
- Unresolved issue or none: \[response\]
- Stage 7 handover status: \[ready for tutor checkpoint / unresolved work\]
- Final submitted SHA if later than tested SHA: \[response and evidence-only difference\]
- [ ] &nbsp;

Three Stage 6 service targets completed and checked.

- [ ] &nbsp;

Original supplied tests retained and passing.

- [ ] &nbsp;

At least two focused issues link requirements and acceptance criteria.

- [ ] &nbsp;

Feature work reviewed by another member using the actual diff.

- [ ] &nbsp;

Human-first review and required Copilot comparison recorded.

- [ ] &nbsp;

Feedback resolved and approval recorded before merge.

- [ ] &nbsp;

Everyone pulled main and integrated checks passed.

- [ ] &nbsp;

Required activities, quiz responses and contribution notes completed.

- [ ] &nbsp;

Only synthetic data included; confidential peer material kept out.

- [ ] &nbsp;

Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.