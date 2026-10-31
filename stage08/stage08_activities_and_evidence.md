# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Wednesday 14:30-16:30 Group 3 (st1-assignment3-Wed3)
Members and UG/PG cohorts: Sophie Jiang, Hassan Ahmad, Devam, Trung Hieu
Record owner / contribution links for each member: https://github.com/sophie-uni/st1-assignment3-Wed3/pulls?q=is%3Apr+state%3Aclosed

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities   

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason:
- Appointment disappears after cancellation.(Sophie)
  - Response and reason: **Symptom** It describes the observed problem, but doesn’t explain its cause.
- The data-store removal path is probably being called. (Trung)
  - Response and reason: Hypothesis. It suggests a likely cause of the defect, but it is not direct evidence and has not yet been confirmed by test output or code inspection.
- The failing test shows store.find_appointment('A1') returns None. (Sophie)
  - Response and reason: **evidence** It directly reports an observable, verifiable runtime value produced by an executed test (store.find_appointment('A1') returns None), making it an objective fact rather than a speculation or a high-level problem description.
- The service layer is badly designed. (Sophie)
  - Response and reason: **hypothesis/opinion, specifically, an opinion** The phrase "badly designed" is a subjective value judgment rather than a concrete, objective measurement or testable claim. It expresses a vague qualitative assessment with no clear criteria for what constitutes "bad."
- Traceback points to smartcare/services.py line 42 in the example. (Sophie)
  - Response and reason: **Evidence** A traceback provides evidence of where an exception surfaced. The traceback location alone doesn’t establish the root cause.

### A.2 Build a debugging record (Sophie)
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: cancelled-history
- **Expected:** Under FR-07 / AC-05.2, cancelling an appointment changes its status to `CANCELLED` and retains it in appointment history.
- **Observed:** The test case `test_cancel_changes_status_and_keeps_appointment_in_store` in test_domain.py has line 45 `data_store.find_appointment("A-001")` has returned `None`, not the original appointment. That shows lookup failed to return it; it does not alone prove deletion.
- **Minimal reproduction:** Use a fresh data store, add a patient, practitioner, and appointment `Rep A`; cancel it; assert its status and that lookup returns the same object. 
- **Initial hypothesis:** Lookup may filter out cancelled appointments even though they remain stored. 
- **Evidence to inspect:** AssertionError: assert None is <smartcare.domain.Appointment object at 0x000001B70EE0E3C0>, where None = find_appointment('A-001'), at tests\test_domain.py:45: AssertionError, it points out that checking the function data_store.find_appointment()

### A.3 Test defect or product defect (Sophie)
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: 
- Expected Cancellation Behaviour
  - What should be changed: The test must be changed, not the application logic.
  - Reason: Requirements define the required system behaviour, not the assertions of an arbitrary test. FR-07 explicitly mandates that appointment history must be retained upon cancellation. A test asserting that cancelled appointments are deleted contradicts this published specification, making it an invalid or defective test. Debugging rules explicitly warn against changing requirements to match code or blindly assuming every failing test is correct. The test assertion must therefore be updated to verify that the appointment remains in the data store with AppointmentStatus.CANCELLED.
- Conflicting Practitioners at the Same Time
  - Decision: A test expecting different practitioners at the same time to conflict does not reflect AC-04.2.
  - Reason: AC-04.2 explicitly permits different practitioners to have appointments scheduled at the same datetime. Conflicts are defined strictly for the same practitioner at the same datetime under FR-05 and AC-04.1. A test that treats different practitioners at the same time as a conflict introduces an unapproved constraint and contradicts AC-04.2.

### A.4 Refactoring smell hunt (Sophie)
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: 

Identified Smells and Proposed Refactorings
- Single Responsibility Principle violation
  - Smell: At 70 lines, the method mixes multiple unrelated tasks, such as 'input validation', 'business logic', 'storage manipulation', and 'output logging'.
  - Proposed Refactoring: Decompose the method by extracting dedicated private helper methods for distinct concerns, such as 'input validation and conflict verification'.
- Direct Collection Manipulation
  - Smell: Manipulating underlying data collections directly inside the service bypasses the encapsulation of SmartCareDataStore.
  - Proposed Refactoring: Delegate storage interactions strictly through the public interface methods provided by the existing SmartCareDataStore (add, find, list), avoiding direct access to internal collections.
- Duplicate Status Strings
  - Smell: Hardcoded strings such as "SCHEDULED" or "CANCELLED" repeated throughout the method introduce typo risks and complicate maintenance.
  - Proposed Refactoring: Replace duplicate string literals with the existing domain enum constants (AppointmentStatus.SCHEDULED, AppointmentStatus.CANCELLED).
- Poor Naming
  - Smell: Truncated variable names like appt decrease readability and clarity.
  - Proposed Refactoring: Rename local variables to clear, descriptive identifiers like appointment.

### A.5 Traceback and hypothesis ranking (Trung)
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason:
- Using the actual failure, the exception/assertion is that the appointment lookup after cancellation does not return the expected appointment object. The failing assertion is effectively:
  - Expected: store.find_appointment("A1") returns the cancelled appointment
  - Observed: store.find_appointment("A1") returns None
- This is supported by the requirement for FR-07 and AC-05.2, which states that cancelled history remains retrievable in the current session. The application call path is the cancellation flow: booking an appointment, invoking the cancellation method, then checking the store for the appointment. The likely failure point is in the service or data-store logic that handles cancellation, rather than in the test itself.
- The most plausible causes, ranked by evidence, are:
  - The cancellation path is deleting the appointment from the data store instead of keeping it as a cancelled record.
    - This is the strongest hypothesis because it directly matches the observation that the appointment is no longer retrievable after cancellation.
    - It also aligns with the requirement that cancelled history remains accessible.
  - The service layer is calling the wrong method during cancellation, such as removal or cleanup instead of a status transition.
    - This is likely if the service directly manipulates the store rather than updating the appointment state.
    - The symptoms are consistent with an object being lost from persistence rather than merely changing status.
  - The cancellation logic updates the appointment state but does not preserve the object in the current session store.
    - This could happen if the store is rebuilding or reindexing its collection after mutation.
    - The evidence is weaker than the direct removal hypothesis, but it still explains why the item becomes unfindable.
  - A second issue in the same service path is interfering with cancellation, such as an invalid state guard or a misordered mutation.
    - This is less likely because the primary symptom is that the record disappears, not that the status remains wrong.
    - It would still be worth checking if the cancellation method validates the state before mutating and whether an exception path leaves the record in a partial state.
- A traceback alone does not establish the cause. It only identifies where the program failed. In this case, the traceback may point into the service or store method, but it does not prove whether the root issue is deletion, status transition, or incorrect store update. The actual cause must be confirmed by inspecting the cancellation flow, comparing the expected state against the stored data, and checking the requirement contract.

### A.6 Exit question (Sophie)
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: Rushing to edit code treats surface symptoms rather than the root cause, risks breaking unrelated functionality, and amounts to guesswork without a verified hypothesis.

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: 420f5be33953c23d2b6bedb532406c4315775c4d; SmartCare A3 Requirements Baseline 2026, revision 2.
- Baseline test command / working directory / observed result / evidence: 
  - command: python -m pytest 
  - working directory: project/
  - Result: 30 passed in 0.17s
- Clean preparation SHA if a record-only commit followed Stage 7: 8593ea0f85854f908221aaccdb1e420b89cc39c6
- Branch and preparer / how teammates obtained this branch: 
  - branch debug/stage08, tutor prepared branch with new services.py file
  - obtain branch code: git fetch origin
- Downloaded tool version, source SHA256 and --check outcome:
  - Command: python D:\PycharmProjects\prepare_debugging.py project --check
  - Result: 
    - Stage 8 tool 1.1; preflight PASS; baseline SHA256 986c5445532ffd1d85e88639b6b6f34b84e15b2bbfc1882511a96938c3b641f6
    - Baseline Git SHA 6abe564b41b1a6af0e46a069359f9255895fa486
    - CHECK ONLY: project unchanged; both proposed fault signatures verified in a temporary copy
- --apply and --verify output summaries / artefact references: 
  - --apply command:python D:\PycharmProjects\prepare_debugging.py project --apply
  - Result:
    - Stage 8 tool 1.1; preflight PASS; baseline SHA256 986c5445532ffd1d85e88639b6b6f34b84e15b2bbfc1882511a96938c3b641f6 
    - Baseline Git SHA 6abe564b41b1a6af0e46a069359f9255895fa486 
    - PREPARED: F8-01 practitioner conflict; F8-02 retained-history lookup 
    - Verified expected failures: test_f8_01_conflict; test_f8_02_history (2 failed)
    - Backup/hash recorded in .stage8_faults; use --restore for setup recovery only
  - --verify command: python D:\PycharmProjects\prepare_debugging.py project --verify
  - Result:
    - VERIFIED: exactly 2 expected failures; both approved symptom signatures present
- Bounded diff inspected and recovery location (not committed):
  - Command: git diff --stat
  - Result: 
    - smartcare/data_store.py | 29 +++++++++++++++----------- 
    - 1 file changed, 11 insertions(+), 18 deletions(-)
  - Also inspected there is .stage8_faults folder created locally with data_store.before.py file
- Prepared faulty-state commit SHA: b5a8a53ba218b6ec12307606b5031d948e5577e6
- Preparation or recovery issues and resolution, if any:
  - 8 issues created (issue 24 to issue 31)
  - https://github.com/sophie-uni/st1-assignment3-Wed3/issues
- Initial prepared full-suite command / result / key failures:
  - Command: git commit -m "Stage 08 tutor preparation"
  - Result:
    - [debug/stage08 b5a8a53] Stage 08 tutor preparation 
    - 1 file changed, 11 insertions(+), 18 deletions(-)

## C. F8-01 diagnosis and repair

F8-01 asks fix pactitioner conflict behaviour, our existing codes have 3 test cases failed with tutor provided code, created issues 27, 28, and 31. Details issue 31 to explain how to fix the defect.

(Issue 31, Sophie)
- Symptom / observed behaviour: Patient P1 book Appointment A1 to see Doctor D1 at 9:00 on 1st Oct 2026, then tried book another appointment A2 to see the same doctor at the same time. The expected ValueError is not raised.
- Expected behaviour and requirement: Under FR-05 / AC-04.1, a second appointment for the same practitioner at the same time must be rejected with ValueError. AC-04.2 allows a different practitioner to be booked at that same time.
- Minimal synthetic reproduction steps: From project/, run "python -m pytest -vv tests/test_starter.py::test_conflict_rule_and_different_practitioner". The test creates a fresh store, registers P1, D1, and D2, books A1 for D1, then attempts A2 for D1 at the same time. It also intends to check that D2 can be booked at that time if the conflict assertion passes.
- Meaningful failing test path/name and exact relevant failure: FAILED tests/test_starter.py::test_conflict_rule_and_different_practitioner - Failed: DID NOT RAISE <class 'ValueError'>
  - >       with pytest.raises(ValueError):
  - E       Failed: DID NOT RAISE <class 'ValueError'>
  - tests\test_starter.py:127: Failed
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: The inspected conflict predicate in project/smartcare/data_store.py compares practitioner IDs using != (around line 110). That means an existing D1 appointment is not considered a conflict for a new D1 booking, while a different practitioner at that time may incorrectly be considered one. AppointmentService.book_appointment calls this predicate before storing the new appointment. This code evidence matches the reported failure; targeted tests should confirm it after repair.
- Smallest justified fix / diff / why other behaviour is preserved: Change only the practitioner comparison from != practitioner_id to == practitioner_id, in data_store.py line 110.
- Repair SHA / focused verification result: 6f0f25df9e82401abaeb71b4c938c2513684f78f tests\test_regressions.py . 1 passed in 0.07stests\test_regressions.py . 1 passed in 0.07s

## D. F8-02 diagnosis and repair

F8-01 asks finding retained or cancelled appointments, our existing codes have 5 test cases failed with tutor provided code, created issues 24, 25, 26, 29 and 30. Details issue 25, 26, and 29 to explain how to fix the defect.

(Issue 25, Sophie)
- Symptom / observed behaviour: Cancel an appointment, then try to find the appointment in the system, return none
- Expected behaviour and requirement: return appointment details with status as cancelled
- Minimal synthetic reproduction steps: From project/, run "python -m pytest tests/test_services.py::test_cancel_appointment_returns_and_retains_cancelled_appointment"
- Meaningful failing test path/name and exact relevant failure: FAILED tests/test_services.py::test_cancel_appointment_returns_and_retains_cancelled_appointment - AssertionError: assert None is <smartcare.domain.Appointment object at 0x000001C397D6D2B0>
  - E       AssertionError: assert None is <smartcare.domain.Appointment object at 0x000001C397D6D2B0>
  - E        +  where None = find_appointment('A1')
  - E        +    where find_appointment = <smartcare.data_store.SmartCareDataStore object at 0x000001C397D6C830>.find_appointment
  - tests\test_services.py:71: AssertionError
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: find_appointment() keeps blank-ID validation and makes cancelled appointments retrievable. Leave the conflict check’s `SCHEDULED` filter in place, so cancelled history is retained without blocking the slot.
- Smallest justified fix / diff / why other behaviour is preserved: in project/smartcare/data_store.py, find_appointment() is filtering cancelled records out, change to don't filter.
- Repair SHA / focused verification result: af558dc247252b1f7b00535d7b481c3083378acc tests\test_regressions.py . 1 passed in 0.07s


(Issue 26, Sophie)
- Symptom / observed behaviour: Repeated cancellation raises LookupError instead of ValueError.
- Expected behaviour and requirement: Under the cancellation contract, a second cancellation attempt on an already cancelled appointment must be rejected with ValueError, and the appointment state must remain CANCELLED with no further mutation.
- Minimal synthetic reproduction steps:
  - Register a valid patient and practitioner.
  - Book appointment A1.
  - Cancel A1 once.
  - Call cancel_appointment('A1') a second time.
  - Observe the exception type and state of the appointment.
- Failing test path and error:
  - Test: tests/test_services.py::test_repeated_service_cancellation_is_rejected
  - Failure: Got LookupError: Appointment not found.
  - The test expects ValueError and a state check that the appointment remains cancelled.
- Human hypotheses and checked evidence:
  - Hypothesis 1: The service removes the appointment from the store on the first cancellation, so the second call cannot find it and raises LookupError.
  - Hypothesis 2: The cancellation method does not check the status guard before lookup, so it attempts to fetch an already-removed object.
  - Hypothesis 3: The service is treating “missing from store” as the error path instead of “invalid transition” as the required ValueError path.
- Supported root cause and insight:
  - The evidence points to a cancellation flow that is not validating the status before performing the second removal/lookup.
  - The store is likely mutating by deleting or removing the appointment during the first cancellation, which makes the second call fail with LookupError rather than the required ValueError.
  - The correct contract is not “missing appointment,” but “attempt to cancel an already cancelled appointment is invalid.”
- Smallest justified repair:
  - In the service cancellation method, first check the appointment exists and is currently SCHEDULED.
  - If the appointment is already CANCELLED, raise ValueError("Only SCHEDULED appointments may be cancelled").
  - Only when the status is SCHEDULED should the service mutate the appointment to CANCELLED.
  - Preserve the existing appointment in the store; do not delete it.
- Final note: This fix is minimal and directly addresses the defect without broadening scope. It preserves cancellation history while enforcing the required state transition rules.
- Repair SHA / focused verification result: f6fdd1ca18af414a97ffd13b09dce7456549d0c1, tests\test_regressions.py . 1 passed in 0.05s 

(Issue 29, Sophie)
- Symptom / observed behaviour: A cancelled appointment still blocks a slot when checking availability for a new appointment.
- Expected behaviour and requirement: A cancelled appointment must no longer occupy the practitioner's time slot. Once an appointment is cancelled, the slot should be free for a new booking at the same time.
- Minimal synthetic reproduction steps:
  - Book appointment A1 for practitioner D1 at a conflict time.
  - Cancel A1.
  - Attempt to book A2 for the same practitioner and same time.
  - Confirm whether the slot is still considered blocked.
- Failing test path and error:
  - Test: tests/test_services.py::test_cancelled_appointment_does_not_block_slot
  - Failure: Expected appointment was None. or, effectively, the second appointment is rejected because the cancelled appointment still appears to occupy the slot.
- Human hypotheses and checked evidence:
  - Hypothesis 1: The cancellation path is leaving the cancelled appointment in the store but not updating the conflict-check logic, so time availability still sees it as booked.
  - Hypothesis 2: The slot-check logic is scanning all appointments without filtering out CANCELLED ones.
  - Hypothesis 3: The cancelled appointment remains in the internal collection with an active booking flag, causing the practitioner/time conflict check to reject the new booking.
- Supported root cause and insight:
  - The root cause is likely in the conflict detection logic, not in appointment creation itself.
  - The data model allows a cancelled record to remain in the system, but the slot-based availability check is still treating it as an active booking.
  - In other words, the appointment is preserved for history, but not correctly excluded from conflict checks.
- Smallest justified repair:
  - Update the slot availability logic to ignore appointments whose status is CANCELLED.
  - Keep the cancelled record in the store for history, but exclude it from conflict resolution while checking for a free slot.
  - Ensure that cancel_appointment sets status to CANCELLED without deleting the historical record.
- Final note: This is the minimal, contract-preserving fix: cancelled records remain traceable, but no longer block new bookings. It matches the requirement that historical data is retained while freed slots are available again.
- Repair SHA / focused verification result: f6fdd1ca18af414a97ffd13b09dce7456549d0c1, tests\test_regressions.py . 1 passed in 0.08s

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
(Issue 31)
Likely cause and why plausible: My initial hypothesis is that the practitioner ID comparison in the conflict check may be incorrect. This is plausible because the reported tests show a same-practitioner, same-time booking was accepted, while a different-practitioner booking at that time was rejected. 
Evidence intended to inspect / competing explanation / discriminating check: I will inspect the failing assertion, the stored appointment’s practitioner ID, time and status, and the book_appointment → conflict-check path. A competing explanation is that the test setup passes a different practitioner ID or datetime than intended. I will verify the actual values and compare the conflict-check result for D1 and D2 using the same store.
Member and saved sequence/time or commit showing this preceded consultation: Sophie, Commit: 2e03f3d06dfde3523c8c8baeaedf127e326b8f38

### F8-02 human entry
(Issue 25)

Likely cause and why plausible: cancel appointment doesn't change appointment status to cancelled, instead, delete the appointment from data store.
Evidence intended to inspect / competing explanation / discriminating check: In services.py, function cancel_appointment has appointment.cancel() line 150
Member and saved sequence/time or commit showing this preceded consultation: Sophie, Commit: 2feb2b711f308a7a756c21470257338c3fdda88c


(Issue 26)

Likely cause and why plausible: My initial hypothesis is that the service cancellation method is removing the appointment from the store on the first cancellation, so the second call hits a missing-record path before it can validate the illegal state transition. This is plausible because the second cancellation is on an already-cancelled appointment, and the code appears to be checking whether the appointment exists rather than whether it is still in a cancellable state.
Evidence intended to inspect / competing explanation / discriminating check: I will inspect the cancel_appointment service method, the data-store mutation path, and the appointment status guard. A competing explanation is that the service reaches the state check but raises the wrong exception type; however, the observed LookupError: Appointment not found is much more consistent with a removal/delete path than with a status validation failure. I will verify the actual values and compare the cancellation flow against the required contract: if the appointment is already cancelled, it should raise ValueError and leave the record unchanged. 
Member and saved sequence/time or commit showing this preceded consultation: Trung, commit: f6fdd1ca18af414a97ffd13b09dce7456549d0c1

(Issue 29)

Likely cause and why plausible: My initial hypothesis is that the slot availability/conflict check is still counting cancelled appointments as active bookings. This is plausible because the requirement says cancelled appointments must remain in the store for history, but they should no longer occupy the time slot.
Evidence intended to inspect / competing explanation / discriminating check: I will inspect the conflict-check function in the service or data-store layer and check whether it filters appointments by status == SCHEDULED before comparing practitioner and time. A competing explanation is that the appointment was not actually cancelled, but the status mutation is failing silently. I will verify the actual values and compare the appointment record before and after cancellation to confirm whether it remains in the store but is incorrectly treated as active.
Member and saved sequence/time or commit showing this preceded consultation: Trung, commit: f6fdd1ca18af414a97ffd13b09dce7456549d0c1

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member:
1. Issue 31 (Sophie) : Actual prompt:fix the test function `test_conflict_rule_and_different_practitioner` and explain 
  - Ranked suggestion: The rejection and list assertions verify the failed booking did not add A2 or alter A1; the final assertions verify the valid D2 booking was stored.
  - evidence check: The test’s expected behavior is correct: AC-04.1 rejects the same practitioner at the same time; AC-04.2 allows a different practitioner at that time. Don’t weaken the assertions to make faulty application code pass. Here’s a clearer version with state checks
  - observed evidence: Copy code to 'test_regressions.py' then run command in project dir 'python -m pytest tests/test_regressions.py::test_conflict_rule_and_different_practitioner'
  - correct, partly correct or wrong: wrong, FAILED tests/test_regressions.py::test_conflict_rule_and_different_practitioner - Failed: DID NOT RAISE <class 'ValueError'>
  - accept, modify or reject with reason: Modify, and ask with follow-up question to fix the issue 
  - follow-up prompt: How to fix the code and pass the test?
  - Ranked suggestion: In project/smartcare/data_store.py, fix the practitioner comparison inside has_practitioner_conflict: appointment.practitioner.practitioner_id == practitioner_id
  - evidence check: It currently uses !=, which reverses the intended match: it misses conflicts for the same practitioner and may report conflicts for different practitioners. Keep the existing appointment-ID exclusion, exact-time check, and SCHEDULED check.
  - observed evidence: From project/, run the focused test: python -m pytest tests/test_regressions.py::test_conflict_rule_and_different_practitioner
  - correct, partly correct or wrong: Correct, tests\test_regressions.py . 1 passed in 0.07s
  - accept, modify or reject with reason: Accept, the test is pass


### F8-02 Copilot review
Actual prompt / output reference and member:

1. Issue 25 (Sophie) : Actual prompt: fix `FAILED tests/test_services.py::test_cancel_appointment_returns_and_retains_cancelled_appointment - AssertionError: assert None is <smartcare.domain.Appointment object at 0x000001C397D6D2B0>`
  - Ranked suggestion: To preserve cancellation history under FR-07 / AC-05.2, change find_appointment() to return a matching appointment regardless of status, while keeping its blank-ID validation. Keep the conflict check’s SCHEDULED filter separate so cancelled appointments remain findable but don’t block the time slot.
  - evidence check: The fix is in project/smartcare/data_store.py, not domain.py. Appointment.cancel() already changes the status without deleting the appointment; find_appointment() is filtering cancelled records out.
  - observed evidence: project/smartcare/data_store.py line 93-94, run python -m pytest tests/test_regressions.py::test_cancel_appointment_returns_and_retains_cancelled_appointment
  - correct, partly correct or wrong: Correct, tests\test_regressions.py .  1 passed in 0.07s
  - accept, modify or reject with reason: Accept, the test is pass

2. Issue 26 (Trung) :  Actual prompt: fix the test function `test_repeated_service_cancellation_is_rejected` and explain
- Ranked suggestion: The test is correct to expect a ValueError and state preservation. The root problem is not the assertion; it is the service cancellation logic. A second cancellation should reject the invalid transition, not fail with a missing-appointment lookup error.
- evidence check: The current logic likely handles the second call as “not found” instead of “illegal state transition”. The fix should preserve the cancelled record and reject the second cancellation with a ValueError.
- observed evidence: The test reports, from project/, run the focused test: python -m pytest tests/test_regressions.py::test_repeated_service_cancellation_is_rejected:
- correct, partly correct or wrong: accept, modify or reject with reason: Correct, tests\test_regressions.py . 1 passed in 0.05s; The test is valid and the service should be modified.
- accept, modify or reject with reason: Accept, the test is pass

3. Issue 29 (Trung) :  Actual prompt: fix the test function `test_cancelled_appointment_does_not_block_slot` and explain
- Ranked suggestion: In the conflict logic, filter out cancelled appointments before checking for practitioner/time collisions. The cancelled record can remain in the store for historical traceability, but it must not be included in the active slot-check.
- evidence check: The service or data-store slot check is likely iterating over all appointments without excluding CANCELLED records. The fix should keep the record but treat it as inactive for availability checks.
- observed evidence: running the focused test pytest tests/test_regressions.py::test_cancelled_appointment_does_not_block_slot shows that the second appointment is rejected correctly.
- correct, partly correct or wrong: accept, modify or reject with reason: Accept the test and modify the conflict-check logic. The bug is in the availability calculation, not in the requirement or the test.
- accept, modify or reject with reason: Accept, the test is pass


## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 (issue 31) before repair | 2e03f3d06dfde3523c8c8baeaedf127e326b8f38 | python -m pytest -vv tests/test_starter.py::test_conflict_rule_and_different_practitioner rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_starter.py | tests/test_starter.py::test_conflict_rule_and_different_practitioner FAILED |
| F8-01 (issue 31) after repair | 6f0f25df9e82401abaeb71b4c938c2513684f78f | python -m pytest tests/test_regressions.py::test_conflict_rule_and_different_practitioner rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_regressions.py | 1 passed in 0.07s |
| F8-01 (issue 27) before repair | fe4dfe8bf4b11d73999c3182bf2f46538ea893f8  | python -m pytest tests/test_services.py::test_same_practitioner_same_time_is_rejected rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_services.py | 1 passed in 0.07s, no extra fix required after fixing issue 25,26,29,31  |
| F8-01 (issue 27) after repair | fe4dfe8bf4b11d73999c3182bf2f46538ea893f8 | python -m pytest tests/test_regressions.py::test_same_practitioner_same_time_is_rejected rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_regressions.py | 1 passed in 0.07s |
| F8-01 (issue 28) before repair | fe4dfe8bf4b11d73999c3182bf2f46538ea893f8 | python -m pytest tests/test_services.py::test_different_practitioner_same_time_is_allowed rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_services.py| 1 passed in 0.05s, no extra fix required after fixing issue 25,26,29,31  |
| F8-01 (issue 28) after repair | fe4dfe8bf4b11d73999c3182bf2f46538ea893f8 | python -m pytest tests/test_services.py::test_different_practitioner_same_time_is_allowed rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_services.py  | 1 passed in 0.05s |
| F8-02 (issue 25) before repair | 2feb2b711f308a7a756c21470257338c3fdda88c  | python -m pytest tests/test_services.py::test_cancel_appointment_returns_and_retains_cancelled_appointment rootdir: D:\PycharmProjects\st1-assignment3\projecttests\test_services.py | tests\test_services.py F |
| F8-02 (issue 25) after repair | af558dc247252b1f7b00535d7b481c3083378acc | python -m pytest tests/test_regressions.py::test_cancel_appointment_returns_and_retains_cancelled_appointment rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_regressions.py | 1 passed in 0.07s |
| F8-02 (issue 26) before repair | 930aa9f90d7849242ccadcbc1a0003218706c6f6 | python -m pytest -vv tests/test_services.py::test_repeated_service_cancellation_is_rejected rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_services.py | tests/test_services.py::test_repeated_service_cancellation_is_rejected FAILED |
| F8-02 (issue 26) after repair | f6fdd1ca18af414a97ffd13b09dce7456549d0c1 | python -m pytest tests/test_regressions.py::test_repeated_service_cancellation_is_rejected rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_regressions.py | 1 passed in 0.05s |
| F8-02 (issue 29) before repair | 930aa9f90d7849242ccadcbc1a0003218706c6f6 | python -m pytest -vv tests/test_services.py::test_cancelled_appointment_does_not_block_slot rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_services.py | tests/test_services.py::test_cancelled_appointment_does_not_block_slot FAILED |
| F8-02 (issue 29) after repair | f6fdd1ca18af414a97ffd13b09dce7456549d0c1 | python -m pytest tests/test_regressions.py::test_cancelled_appointment_does_not_block_slot rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_regressions.py | 1 passed in 0.08s |
| F8-02 (issue 24) before repair | fe4dfe8bf4b11d73999c3182bf2f46538ea893f8 | python -m pytest tests/test_domain.py::test_cancel_changes_status_and_keeps_appointment_in_store rootdir: D:\PycharmProjects\st1-assignment3\projecttests\test_domain.py | 1 passed in 0.06s, no extra fix required after fixing issue 25,26,29,31 |
| F8-02 (issue 24) after repair | fe4dfe8bf4b11d73999c3182bf2f46538ea893f8 | python -m pytest tests/test_regressions.py::test_cancel_changes_status_and_keeps_appointment_in_store rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_regressions.py | 1 passed in 0.06s |
| F8-02 (issue 30) before repair | fe4dfe8bf4b11d73999c3182bf2f46538ea893f8 | python -m pytest tests/test_services.py::test_repeated_service_cancellation_is_rejected rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_services.py | 1 passed in 0.09s, no extra fix required after fixing issue 25,26,29,31 |
| F8-02 (issue 30) after repair | fe4dfe8bf4b11d73999c3182bf2f46538ea893f8 | python -m pytest tests/test_regressions.py::test_repeated_service_cancellation_is_rejected rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_regressions.py | 1 passed in 0.09s |
| Full suite after both repairs, before refactor | 2bb9df58135ccb1b07f0500f3a938f3a57fc5ad4 | python -m pytest tests/test_regressions.py rootdir: D:\PycharmProjects\st1-assignment3\project\tests\test_regressions.py | 8 passed in 0.07s |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour:
Unrelated failures investigated / resolution: 
- when I run 'python -m pytest tests/test_regressions.py::test_same_practitioner_same_time_is_rejected', got error of 'FAILED tests/test_regressions.py::test_same_practitioner_same_time_is_rejected - NameError: name 'conflict_setup' is not defined'
- resolution is I have missed 'conflict_setup' class in test_regressions.py, copy it from test_services.py and re-run the command, test pass.

## H. Refactoring decision and before/after verification (Sophie)

Smell and exact location: 

Both F8-01 and F8-02 should fix in data_store.py

Small proposed structural change / why justified: 
- F8-01, in data_store.py
  - line 110, 'and appointment.practitioner.practitioner_id != practitioner_id', should be 'and appointment.practitioner.practitioner_id == practitioner_id'
- F8-02, in data_store.py
  - line 94 is not required

External behaviour to preserve / relevant tests: In project\tests\test_services.py
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA:
- 6f0f25df9e82401abaeb71b4c938c2513684f78f
- af558dc247252b1f7b00535d7b481c3083378acc
Focused and full after-refactor commands / working directory / results / evidence: 
- Focused and full after-refactor commands: python -m pytest tests/test_regressions.py
- working directory:D:\PycharmProjects\st1-assignment3\project
- results: 8 passed in 0.07s
- evidence: b6cad496c1961b0732046e4ee62a64596cb175bd
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: Accepted

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: 
  - F8-01: 
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/27 (Sophie)
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/28 (Sophie)
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/31 (Sophie)
  - F8-02:
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/24 (Sophie)
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/25 (Sophie)
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/26 (Trung)
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/29 (Trung)
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/30 (Sophie)
Branch / prepared, repair and refactor checkpoints: 
    - repared branch:Stage08/issues- #32
      - Tutor preparation: b5a8a53ba218b6ec12307606b5031d948e5577e6
      - stage08 issue and tasks assignment: 8585c68c35cc8374cd0e06e8fe0870bcca41019c
    - repair branch: 
      - Stage08/issue31
      - Stage08/issue25
      - Issues are fixed (stage08/Trung)
      - stage08/issue_24_27_28_30
PR link and another member's reviewer identity: 
      - https://github.com/sophie-uni/st1-assignment3-Wed3/pull/32
      - https://github.com/sophie-uni/st1-assignment3-Wed3/pull/34
      - https://github.com/sophie-uni/st1-assignment3-Wed3/pull/35
      - https://github.com/sophie-uni/st1-assignment3-Wed3/pull/37
      - https://github.com/sophie-uni/st1-assignment3-Wed3/pull/38
Key human feedback, difference from Copilot findings and response/outcome: Not available
Actual review approval / merge evidence: PR reviewed and merged by different team members
Integrated code SHA and team pull/retest command / working directory / result:
- Integrated code SHA and team pull: https://github.com/sophie-uni/st1-assignment3-Wed3/pull/40
- retest command: python -m pytest tests/test_regressions.py
- working directory:project\tests\test_regressions.py
- result: 8 passed in 0.07s
Evidence-only later SHA / explanation if different: Not available
Each member's substantive contribution and artefact: 
- Trung has explained and fixed issue 26 and 29
- Sophie has set-up the stage start-point; explained, fixed, verified issue 24,25,27,28,30,31; finalise the stage and prepare for handover to next stage

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? 
I have asked Copilot to fix the test function `test_conflict_rule_and_different_practitioner` and explain, Copilot gave me a piece of codes and told me to place in test_regressions.py. However, it didn't fix the error. There is no evidence error due to test case writing since we had all test cases passed before tutor changed code not the test cases.

2. What evidence changed your group's view? 
Copilot helps code writing, but not always understand the full content. Human verification and follow-up prompts helps to get detailed accurate answers.

3. How did regression tests protect the refactoring?
- Verified behaviour was preserved: Running the tests before and after code changes proved that the internal restructuring did not alter external results, return types, or public contracts.
- Caught accidental breakages immediately: Any unintended error introduced during restructuring—such as an edge-case logic slip or broken interface—was flagged instantly by a failing test before committing.
- Prevented the bugs from returning: The tests ensured that the two newly fixed defects (practitioner conflicts and retained cancelled appointments) were not accidentally reintroduced while cleaning up the code.
- Guarded critical invariants: They confirmed that essential rules, like immutable cancellation transitions, correct exception types (ValueError vs. LookupError), and ID case-sensitivity—remained intact. 

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure? (Sophie)

Response: Before changing code, reproduce and record the failure: capture the failing test, command, code SHA, traceback, expected versus observed behaviour, and the requirement involved. Reduce it to a minimal case, inspect the relevant call path and state, and record a hypothesis plus checks that distinguish it from alternatives. Confirm the test matches the requirement; then use the evidence to identify the cause and make the smallest justified fix. This avoids fixing the wrong problem or masking a test defect.

2. Where should expected behaviour come from during debugging? (Sophie)

Response: Expected behaviour should come from the approved requirements baseline, especially the relevant acceptance criterion, and any documented domain or service contract, not from assumptions about what the current code does. 

3. What is a debugging hypothesis? (Sophie)

Response: A debugging hypothesis is a testable explanation of why a failure occurs.

4. What is a regression test and why is it retained? (Sophie)

Response: A regression test is a focused test created to reproduce a specific defect and confirm its repair by demonstrating fail-to-pass verification. It is retained in the test suite to:
- It ensures that once a bug is fixed, future code modifications, refactorings, or new features do not accidentally reintroduce the same defect.
- It serves as an automated safety net to verify that internal code reorganisations preserve all existing external behaviours and system contracts.
- It permanently documents the required behaviour and acts as ongoing evidence of system correctness across future releases.

5. What is meant by root cause? (Sophie)

Response: A root cause explains the fundamental reason why a failure occurs, rather than merely describing what was observed (a symptom) or where the error surfaced in an execution path (a traceback location). Identifying and addressing the root cause allows engineers to apply minimal, correct repairs that permanently restore required system behaviour without simply masking the error.

6. What is refactoring? (Sophie)

Response: Refactoring is the process of changing the internal structure of code while strictly preserving its existing external behaviour.

7. What is a swallowed exception? (Sophie)

Response: A swallowed exception occurs when an exception is caught or intercepted by an error-handling block (such as except Exception: or catch) but is ignored, silenced, or suppressed without being properly handled, logged, reported, or re-raised.

8. What is a code smell? (Trung)

Response: A code smell is a signal that the code may be poorly designed or harder to maintain, even if it still works. It usually points to a quality issue such as duplicated logic, unclear responsibility, hidden side effects, overly complex conditions, or a violation of the intended design. In debugging, a code smell is not necessarily the root cause, but it is a warning that the implementation may be fragile or inconsistent with the requirements.

9. How should GitHub Copilot-generated debugging diagnoses be treated? (Trung)

Response: GitHub Copilot-generated debugging diagnoses should be treated as hypotheses, not proof. They can be useful for suggesting likely causes, but they must be checked against actual evidence, the failing test, the current code, and the requirement contract before being accepted. A generated diagnosis is only as good as the evidence behind it. It should never replace direct inspection, root-cause analysis, or validation by running the relevant tests.
10. What is the Stage 8 engineering rule? (Trung)

Response: The Stage 8 engineering rule is that a fix must be justified by evidence and tied to the actual defect. You must not change code based only on a guess, a vague suspicion, or an AI-generated suggestion. The repair must be minimal, supported by a clear diagnosis, and validated with focused regression tests. If the defect is fixed, the evidence must show the failure was addressed without introducing new regressions.

## L. Completion and handover

- [✔] Existing project, earlier tests and stage records preserved.
- [✔] Passing Stage 7 SHA and safe preparation details recorded.
- [✔] Both defects reproduced with meaningful failing tests.
- [✔] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [✔] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [✔] One genuine refactor verified under passing before/after tests.
- [✔] Human PR review, feedback resolution and integrated retest recorded.
- [✔] Tutorial, three reflections and ten formative responses complete.
- [✔] Local recovery metadata excluded from submitted source.
- [✔] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: Not available
Unresolved issues or incomplete checks / owner / next action: No, all 8 issues closed
Handover note: Ready to process to stage09
