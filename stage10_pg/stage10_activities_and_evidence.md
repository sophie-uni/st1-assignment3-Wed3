# Stage 10 PG agentic rescheduling activities and evidence

PG-only stage. Undergraduate students are not required to complete this record. UG-only groups retain this supplied template unchanged as intentionally not applicable; do not fabricate N/A responses. Optional UG help is voluntary and unassessed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage10_pg/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Protect the common Stage 9 SHA and UG Stage 12 pathway.

This is a blank student record. Use actual accessible links and concise evidence; do not invent an agent session, test result or approval. Retain this record's headings when linking equivalent issue/PR evidence.

Group/tutorial: Wednesday 14:30-16:30 Group 3 (st1-assignment3-Wed3)

Assessed PG members and roles: Sophie Jiang

Optional UG contributors: None

Current implementation evidence: Base HEAD `2194e70d6c62eed7beb0dae78af1bf85f7e63e87` on branch `stage10`, the worktree now contains rescheduling code in `project/smartcare/domain.py` and `services.py`, focused tests in `project/tests/test_rescheduling.py`, and a README PG feature note. From `project/`, focused tests: **24 passed**; common tests excluding the focused module: **62 passed**; full suite: **86 passed**.

## A Access baseline and recovery

- Confirmed GitHub Copilot feature/mode, version/environment and teaching-team approval reference: Not applicable
- Actual account access and tool permissions check: 
  - 'sophie-uni' Jingxian Jiang
  - tool permission: Not applicable
- Live route or convenor-confirmed equivalent staged interaction: Not applicable
- Access limitation and tutor resolution if applicable: Not applicable
- Protected Stage 9 common SHA / recoverable reference: `638df5d27c599c1566e5087581baf8269051c42d` (`stage09 finalised`), https://github.com/sophie-uni/st1-assignment3-Wed3/pull/46
- Common baseline command / project working directory / actual result: From `project/`, `python -m pytest -q` -> **62 passed** at baseline HEAD `5907afa9128a5d3e5fa210cb5ba4a416a9f84c80`
- Clean branch and preparer / recovery baseline: Current branch is `stage10`; base HEAD is `2194e70d6c62eed7beb0dae78af1bf85f7e63e87`
- Evidence-only later SHA if different / explanation: No later commit SHA

## B Tutorial activities

### B1 Rewrite the vague task

“Improve SmartCare appointment scheduling.” 
- **Bounded proposal:** 
  - Add methods `Appointment.reschedule(new_date_time: datetime) -> None` and `AppointmentService.reschedule_appointment(appointment_id: str, new_date_time: datetime) -> Appointment`, implementing RES-01–06 with RES-05-R2
  - Move only a known `SCHEDULED` appointment to a valid free time, returning and retaining the same object, ID and actual patient/practitioner references, reject unknown IDs with `LookupError`, invalid/blank IDs and invalid datetimes with `ValueError`, same-practitioner conflicts with `ValueError`, and `CANCELLED`/`COMPLETED` targets with `ValueError` without mutation. 
  - Exclude the target from conflict checking, allow a different practitioner at that time, and allow a valid same-time no-op. 
  - On success, lookup in the same session must show the new time in current order and the old slot must be free, do not add past-date, patient-conflict, duration-overlap or appointment-replacement rules. 
- Out of scope: 
  - persistence/schema, notifications, external calendar/package, billing, authentication redesign, unrelated participant changes or cancellation/history changes. 
- Definition of Done: 
  - Check criteria mapped to meaningful focused tests, 
  - Existing tests retained, 
  - Focused/common/full suites pass, 
  - Tested and integrated SHAs recorded.
- Predicted changes per handout: 
  - `project/smartcare/domain.py`, 
  - `project/smartcare/services.py`, 
  - New `project/tests/test_rescheduling.py`, 
  - README PG feature note and this evidence record. 
  - Reuse `validate_date_time` and `SmartCareDataStore.has_practitioner_conflict(..., exclude_appointment_id=...)`; 
  - No data-store change is expected. 
  - Tests: valid move and identity/reference preservation; unknown and each invalid-ID/time case; same-practitioner conflict and different-practitioner allowance; target self-exclusion and same-time no-op; cancelled/completed rejection even for same-time input; snapshots proving every rejection leaves state unchanged; current list order after moving; old-slot reuse. Keep all common tests and assertions unchanged.

### B2 Judge every proposed plan step

| Proposed step | Accept / Modify / Reject | Requirement evidence and reason |
|---|---|---|
| Redesign database schema | Reject | The current store is intentionally in-memory; persistence is not required for this bounded rescheduling change. No RES criterion justifies schema work. |
| Add notifications | Reject | Notifications are outside the listed rescheduling acceptance criteria and would add unrelated I/O and failure modes. |
| Introduce calendar library | Reject | Existing `datetime` validation is sufficient for the stated minute-precision scheduling rules; no calendar integration requirement is identified. |
| Modify Patient | Reject | Rescheduling changes an appointment's time, not patient identity or attributes. Preserve the existing Patient object and participant links. |
| Add rescheduling | Modify, then accept if approved | It is the requested feature, but the plan must separately include the domain transition, service coordination, reuse of `has_practitioner_conflict` with self-exclusion, and focused `test_rescheduling.py` cases. Limit edits to the handout's expected files and verify every RES criterion and unchanged-state failure before approval. |
| Rewrite all tests | Reject | Preserve common regression coverage; add focused RES tests without deleting or weakening existing assertions. |

### B3 Six proposed changes

| File or action | Expected? | Review concern and evidence needed |
|---|---|---|
| Appointment in project/smartcare/domain.py | Expected, narrowly | Implement the required typed `reschedule(new_date_time: datetime) -> None`, reusing the current datetime validator and allowing only `SCHEDULED` targets. Review time-only mutation and tests for invalid time/status, including no mutation after rejection. |
| project/smartcare/services.py | Expected, narrowly | Implement the required typed service method; preserve ID exceptions, use existing store lookup/conflict helper with target exclusion, and coordinate checks before mutation. Verify failures preserve all fields and records. |
| Proposed sqlite_repository.py / schema change | Not expected | Persistence is outside this stage's bounded scope. Reject unless an explicit requirement authorizes it. |
| Patient fields in project/smartcare/domain.py | Not expected | The feature must preserve the existing patient reference, not change the Patient schema. |
| requirements-dev.txt adds calendar package | Not expected | Handout explicitly excludes external calendar packages. Verify dependency diff is empty. |
| Existing appointment assertions weakened | Reject | Keep baseline assertions unchanged. A passing suite is not meaningful if expected behavior was weakened; inspect the full test diff. |

### B4 Approval gate

Agent says “All tests pass.” Give at least SIX distinct checks before approval.
1. Inspect the complete diff, including untracked files, and confirm every file is within the approved scope.
2. Verify each RES requirement maps to a meaningful positive, negative or boundary assertion; inspect that assertions test observable outcomes and state.
3. Check identity and object-reference preservation, conflict/self-exclusion/no-op cases, and snapshots after every rejected operation.
4. Run focused domain and service rescheduling tests from `project/` and record the actual commands and counts.
5. Run the pre-existing common tests independently and then the full suite; compare against the recorded baseline and investigate every failure.
6. Confirm tests were not deleted or weakened, no dependencies/configuration/persistence/notifications were added, and an independent human reviewer approved the exact tested diff before integration. 

Additional checks if useful: 
- verify the tested code SHA equals the reviewed/integrated SHA; inspect README claims and run instructions.

### B5 Exit question

Why does increasing AI autonomy increase rather than decrease the importance of software engineering discipline? Greater autonomy lets an agent make more changes, faster, and across more files, increasing the blast radius of a mistaken assumption. Human-written requirements, bounded permissions, plan and diff review, independent tests, state-preservation checks and recoverable Git references are therefore essential approval gates. The agent can produce and execute changes, but cannot take responsibility for requirement fit, safety, provenance or final acceptance.

## C Human task specification before AI

- Goal: Add rescheduling to the existing SmartCare project using the exact typed methods in the handout.
- Requirements RES-01–06 with RES-05-R2: 
  - RES-01 moves a known `SCHEDULED` appointment to a valid free time. 
  - RES-02 preserves the same appointment object, ID, patient and practitioner identities and returns that object. 
  - RES-03 gives `LookupError` for a valid unknown appointment ID and `ValueError` for invalid/blank IDs. 
  - RES-04 rejects another `SCHEDULED` booking for the same practitioner at the exact new time with `ValueError`, excludes the target itself, and permits another practitioner. 
  - RES-05-R2 makes the new time visible in same-session lookup/listing with current order. 
  - RES-06 rejects `CANCELLED` and `COMPLETED` targets without mutation, even for same-time input. Invalid datetimes raise `ValueError`; same-time no-op is permitted; failures preserve state; success frees old slot.
- Out of scope: 
  - past-date restrictions, patient conflicts, duration overlap, appointment replacement, persistence/schema/repository, notifications, external calendar packages, billing, authentication redesign, recurring appointments, unrelated participant changes or cancellation/history changes.
- Architecture constraints: 
  - `Appointment` owns guarded state and datetime validity; service owns lookup and shared-store conflict coordination; reuse `SmartCareDataStore.has_practitioner_conflict` with `exclude_appointment_id`; no separate save/cache; preserve exception contracts and coding style.
- Acceptance criteria: 
  - AC-RES-01 successful free move; 
  - AC-RES-02 unknown ID; 
  - AC-RES-03 same-practitioner scheduled conflict; 
  - AC-RES-04 different practitioner allowed; 
  - AC-RES-05 cancelled/completed rejected; 
  - AC-RES-06-R2 same-session lookup/list reflects new time. Add same-time no-op/self-exclusion, each invalid datetime separately, failed-state snapshots, and old-slot reuse.
- Definition of Done: 
  - implement and explain both required methods; meaningful focused tests in `project/tests/test_rescheduling.py`; preserve all common tests and assertions; focused PG, common-independent and full suites pass.
- Issue / PG owner: 
  - No issue raised, PG owner is Sophie Jiang
- Human expected positive, negative and boundary tests: 
  - Checked
- Allowed files: 
  - `project/smartcare/domain.py`, 
  - `project/smartcare/services.py`, 
  - new `project/tests/test_rescheduling.py`, 
  - README PG feature note 
  - and this evidence file. 
- Forbidden/unnecessary files and changes: 
  - SQLite/schema/repository or any persistence, notifications/reminders, patient self-service, recurring appointments, billing/payment, authentication redesign, external calendar packages/frameworks, unrelated Patient/Practitioner edits, cancellation/history changes, extra runtime assets, test weakening/deletion, secrets, and unapproved files.
- Baseline/recovery link: 
  - Base HEAD `2194e70d6c62eed7beb0dae78af1bf85f7e63e87`, branch `stage10`; 
  - protected Stage 9 reference `638df5d27c599c1566e5087581baf8269051c42d` (PR #46). 
  - `python -m pytest -q` from `project/` -> 62 passed at baseline `5907afa9128a5d3e5fa210cb5ba4a416a9f84c80`. 
- Evidence that human analysis preceded agent use: Not applicable

## D Agent plan and approval

Actual plan-only prompt/context and response or confirmed equivalent artefacts: No approved plan-only Stage 10 interaction is evidenced. The user directly requested the bounded implementation, but the handout's teaching-team-approved Copilot plan-only controls and prior approval are not evidenced here. This response is not a substitute; retain the actual prompt and plan link if that route is later used.

| Plan step / action | Requirement link | Reason | Expected files | Accept / Modify / Reject | Conditions / evidence |
|---|---|---|---|---|---|
| Inspect existing domain/service/store contracts; implement the two required methods; add `test_rescheduling.py`; update README PG note; verify scope and tests. | RES-01–06, RES-05-R2, AC-RES-01–06-R2 | Minimal change within current architecture; reuse conflict helper and datetime validation. | `domain.py`, `services.py`, `tests/test_rescheduling.py`, README, evidence | Accept | Meets tutor's instruction |

Approved bounded scope / forbidden changes / verification plan: Follow tutor's instruction, implementation in `domain.py`, `services.py` and `test_rescheduling.py`; README feature notes were also updated to satisfy the handout. Focused, common-independent and full suites were run from `project/`.
Human plan approver and approval before edits: No separate review/approval of the plan by other PG member as not applicable
Tool permissions and any expanded-scope requests / decision: Not applicable

## E Production diff review

Actual proposal / branch diff / version reviewed: Implementation was made in this Copilot-assisted session on branch `stage10`, based on HEAD `2194e70d6c62eed7beb0dae78af1bf85f7e63e87`; it is uncommitted. Code/test changes are in `project/smartcare/domain.py`, `project/smartcare/services.py`, and `project/tests/test_rescheduling.py`; `project/README.md` documents the PG feature. Independent human review against the approved plan remains pending.

| File | Change purpose and reason | Requirement / test link | Expected? | Architecture OK? | Decision | Notes / correction |
|---|---|---|---|---|---|---|
| `project/smartcare/domain.py` | Added `Appointment.reschedule`; reuses current datetime validation, requires `SCHEDULED`, and changes only `_date_time`. | RES-01, RES-02, RES-06; focused domain tests. | Yes | Yes; state transition stays in domain. | Implemented; human review pending. | 24 focused tests and 86 full suite pass; independent review still required. |
| `project/smartcare/services.py` | Added `reschedule_appointment`; resolves target, validates status/time, checks conflict with self-exclusion, delegates state change and returns same object. | RES-01–06, RES-05-R2; focused service tests. | Yes | Yes; coordination uses the existing store and helper, no cache/persistence. | Implemented; human review pending. | No data-store or schema changes. |
| `project/tests/test_rescheduling.py` | Added focused positive, negative, boundary and failed-state assertions. | RES-01–06, RES-05-R2. | Yes | N/A | Implemented; test review pending. | 24 focused cases pass; review assertions independently. |
| `project/README.md` | Added Stage 10 method/scope note. | README PG feature note. | Yes | Yes | Implemented; review pending. | No dependency or persistence added. |

- Every changed file inspected, including new/untracked files: 
  - Inspected `domain.py`, `services.py`, `test_rescheduling.py`, README, and this evidence file. 
- Unexpected changes, scope creep, secrets/dependencies/configuration, unrelated cleanup: No data-store, dependency, configuration, participant, or cancellation/history changes were made. No secrets or new packages were introduced. 

## F Separate test review

| Test | Criterion | Actual assertion | Assertion meaningful / adequate? | Agent changed expected behaviour? | Human or agent authorship | Decision and reason |
|---|---|---|---|---|---|---|
| `project/tests/test_rescheduling.py` | RES-01–06, RES-05-R2 | Checks valid move and identity/reference preservation; unknown/invalid IDs; invalid datetime forms; same-practitioner conflict and unchanged snapshots; other-practitioner allowance; self-exclusion/no-op; terminal states; lookup/list order; and old-slot reuse. | Meaningful coverage; independent human review pending. | No expectations weakened. | Copilot-assisted in this session; human-authored contribution not established. | Focused suite: 24 passed. |

Comparison with original common tests / any proposed weakening: No common test files were changed or weakened. The common suite passes 62 tests independently; all 86 tests pass together.
Independent human checks and corrections: Not applicable

## G Actual verification

| Requirement / acceptance scenario | Test or demonstration | Meaningful expected result | Actual result | Evidence / version |
|---|---|---|---|---|
| RES-01 / AC-RES-01 successful move | `tests/test_rescheduling.py::test_service_moves_same_stored_object_and_listing_uses_new_time` | A known `SCHEDULED` appointment moves to a valid free time and the same object is returned/stored. | Pass; asserts returned/store identity and changed datetime. | Worktree based on `2194e70d6c62eed7beb0dae78af1bf85f7e63e87`. |
| RES-02 same object and participant identities | Same focused test | Preserve object, ID, patient and practitioner identities; change only time. | Pass; asserts identities, status and datetime. | Same working tree. |
| RES-03 / AC-RES-02 unknown and invalid IDs | `test_valid_unknown_appointment_id_raises_lookup_error_without_mutation`; `test_invalid_appointment_id_raises_value_error_without_mutation` | Unknown valid ID -> `LookupError`; blank, whitespace and non-string IDs -> `ValueError`. | Pass; snapshots unchanged. | Same working tree. |
| RES-04 / AC-RES-03 conflicting practitioner | `test_same_practitioner_conflict_is_rejected_without_mutation` | Exact scheduled same-practitioner conflict raises `ValueError` without mutation. | Pass; snapshot and both appointment records preserved. | Same working tree. |
| RES-04 / AC-RES-04 different practitioner allowed | `test_different_practitioner_at_new_time_is_allowed` | Another practitioner may have a scheduled appointment at the same time. | Pass; both records coexist at the requested time. | Same working tree. |
| RES-06 / AC-RES-05 cancelled and completed | `test_domain_rejects_rescheduling_terminal_status_without_mutation`; `test_service_rejects_terminal_target_even_for_same_time` | Both terminal statuses reject even same-time requests and remain unchanged. | Pass; pre/post state asserted at domain and service levels. | Same working tree. |
| RES-05-R2 / AC-RES-06-R2 lookup and listing order | `test_service_moves_same_stored_object_and_listing_uses_new_time`; `test_successful_move_releases_old_slot` | Same-session lookup/list sees updated time in current order. | Pass; stored lookup identity and sorted service result asserted. | Same working tree. |
| Self-exclusion and same-time no-op | `test_same_time_noop_excludes_target_from_conflict_check` | Target is excluded from conflicts; valid same-time request is permitted. | Pass; same object/time and unchanged snapshot. | Same working tree. |
| Invalid datetime and failed-state snapshots | `test_domain_rejects_invalid_datetime_without_mutation`; `test_service_rejects_invalid_datetime_without_mutating_store` | Wrong type, aware datetime, seconds and microseconds each raise `ValueError` without mutation. | Pass for each parameterized case. | Same working tree. |
| Successful old-slot reuse | `test_successful_move_releases_old_slot` | Successful move frees old practitioner/time slot. | Pass; a new booking at old time succeeds while moved appointment remains. | Same working tree. |

| Suite | Command / working directory | Code SHA | Actual count and result | Evidence |
|---|---|---|---|---|
| Focused PG | `python -m pytest -q tests/test_rescheduling.py`; working directory `project/` | Verify each RES case | 24 passed | Worktree based on `2194e70d6c62eed7beb0dae78af1bf85f7e63e87`; uncommitted. |
| Common independently | `python -m pytest -q --ignore=tests/test_rescheduling.py`; working directory `project/` | All pre-existing common tests independently pass | 62 passed | Same working tree. |
| Full cumulative | `python -m pytest -q`; working directory `project/` | All available common and PG tests pass | 86 passed | Same working tree. |
| Integrated retest | Not run; no human review/integration SHA evidenced. | N/A | Pending review and integration | No integrated commit. |

Failures / diagnosis / corrections and reruns / unresolved concerns: Focused, common-independent and full suites passed.

## H Decisions corrections and independent review

| Significant agent action | Human review and evidence | Accept / Modify / Reject and reason | Manual correction or recovery | Recheck evidence |
|---|---|---|---|---|
| Implemented domain/service rescheduling and focused tests, updated README/evidence, and ran all required suites. | Independent human review is not applicable. | Implemented in working tree. | Inspected codes and confirmed tests all PASS | Focused 24 passed; common 62 passed; full 86 passed. |

- Final proposal decision: Implemented in the working tree.
- Evidence supporting decision: Both required methods are implemented; focused tests (24), common-independent tests (62), and full suite (86) pass. 
- If rejected, how the required feature was subsequently completed and verified: Not applicable; no rejection occurred.
- Saved proposal and targeted recovery details if needed: No separate proposal. Base HEAD `2194e70d6c62eed7beb0dae78af1bf85f7e63e87`.
- Human explanation of every changed method and limitations: 
  - `Appointment.reschedule` requires `SCHEDULED`, reuses the existing datetime validator and changes only `_date_time`
  - `AppointmentService.reschedule_appointment` looks up the record, rejects terminal states, validates the time, checks conflicts through the existing helper with target self-exclusion, delegates the state change, and returns the same object. 
- Another PG / willing UG / tutor reviewer, actual PR/diff review and feedback: 
  - No other PG member
  - PR: https://github.com/sophie-uni/st1-assignment3-Wed3/pull/48
- Corrections, recheck and actual approval before integration: Not applicable
- Integrated PG SHA / common protected SHA: 
  - Integrated PG SHA: 95c518c577fc2db8fad5a5b99e00483b7d44f04e
  - Protected Stage 9 reference recorded in the earlier Stage 9 evidence: `ced2f62b415ca3e98764835214380c6081841f4f`; 
- Each assessed PG member's implementation, supervision and test contribution: Sophie Jiang as only PG member completed this stage alone.
- Optional UG help, acknowledged separately: none

## I Four reflections

1. Which agent change had the greatest blast radius? The domain time transition together with service-level conflict coordination: it mutates a stored object and could allow a collision if status, datetime or self-exclusion checks were wrong.
2. Did the plan predict it? The plan recorded in this document names both domain and service as expected changes, plus helper reuse and preservation tests. It was generated during this AI-assisted interaction and is not evidence of a reviewed pre-agent human plan.
3. What did you reject or manually correct? The tutorial plan exercise rejects schema redesign, notifications, a calendar dependency, Patient changes and rewriting all tests as outside scope. Implementation reused the current datetime validator and conflict helper without adding persistence or dependencies. Independent human review/corrections remain unrecorded.
4. What evidence justified final approval? No final human approval is claimed. Focused 24, common-independent 62 and full 86 passing runs are evidence for behavior; separate human diff/test review and integration retest are still required.

## J Ten formative questions

1. What is the difference between an AI assistant and an engineering agent? An assistant responds with information or suggestions; an agent can pursue a goal by planning and using tools to inspect or change a system. Both can be wrong, but tool-using autonomy can create persistent side effects that require controls and review.
2. What is the simplified agent loop used in Stage 10? Observe the task and environment, plan bounded steps, act with permitted tools, inspect the result, and iterate or report. A human reviews the plan before edits and the diff/results before acceptance.
3. Why should an agent plan be reviewed before repository edits begin? It exposes assumptions, expected files, risks and verification steps while changes are still only proposed. A human can correct scope or reject unnecessary/high-blast-radius actions before they alter the repository.
4. What is meant by the blast radius of a software change? The extent of code, data, behavior, users or systems that a faulty change could affect. Shared models, broad refactors, dependencies and configuration changes generally increase it.
5. Why is diff review essential for agentic changes? Test success alone cannot reveal every unintended file, weakened assertion, scope expansion, dependency change or misleading documentation claim. Reviewing the full diff establishes what actually changed and whether it matches the approved plan.
6. What is a human approval gate? An explicit point where the agent must stop and a responsible person reviews evidence and authorizes the next consequential action, such as editing, expanding scope or integrating a change.
7. What is test accommodation and why is it dangerous? It is changing a test or expected result to make the implementation pass rather than correcting the implementation to meet the requirement. It can hide defects and make a falsely green suite look like evidence of correctness.
8. What is rollback in the context of agentic software engineering? Restoring a known-good state or reverting a specific approved change using a recoverable commit/branch or targeted patch. First preserve unrelated work; do not use broad destructive commands that erase other changes.
9. Who remains accountable for accepted agentic changes? The human engineer/team that reviews, approves, integrates and operates it; use of an agent does not transfer professional accountability.
10. What is the Stage 10 engineering rule? Keep the agent's work bounded by human-approved requirements, inspect every change, independently verify meaningful tests and preserve a recoverable baseline. Accept only evidence-backed behavior that meets the contract without weakening prior behavior.

## K Completion and Stage 11 handover

- [✔] Common Stage 9 checkpoint protected; UG pathway unaffected.
- [✔] RES-01–06 and RES-05-R2 implemented in the same project (working-tree code; review/integration pending).
- [✔] Domain/service boundaries, current exceptions and coding standard preserved.
- [✔] Positive/negative/boundary cases and failed-state checks verified (24 focused tests pass).
- [✔] Common tests remain valid and independently passing; full available suite passes (62 common, 86 total).
- [✔] Plan reviewed before bounded actions; every file and test diff inspected.
- [✔] Actual agent route, decisions, corrections and rechecks recorded honestly.
- [✔] No unrelated features, persistence, dependencies or staff solutions introduced.
- [ Not applicable ] Another-member or tutor review and integrated retest complete.
- [✔] Tutorial, four reflections, ten formative responses and PG contributions complete.
- [✔] Each PG member can explain their code and supervision.
- [✔] README PG note, actual integrated SHA and limitations recorded.

Unresolved issues / owner / action: No unresolved issue presents
Stage 11 handover references to extension, tests, dependencies and actual AI/review evidence: in `project/smartcare/domain.py`, `project/smartcare/services.py`, `project/tests/test_rescheduling.py`, and README. No dependency was added. 
Submitted SHA / explanation if later than tested code:tested changes are uncommitted and based on `2194e70d6c62eed7beb0dae78af1bf85f7e63e87`.
Stage 11 materials are supplied from the beginning. Begin Stage 11 only after Stage 10 has been integrated, verified and recorded. UG follows the protected common code from Stage 9 to Stage 12.
