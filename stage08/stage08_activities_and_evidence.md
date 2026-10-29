# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Wednesday 14:30-16:30 Group 3 (st1-assignment3-Wed3)
Members and UG/PG cohorts: Sophie Jiang, Hassan Ahmad, Devam, Trung Heiu
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
- The failing test shows store.find_appointment('A1') returns None. (Hassan)
- The service layer is badly designed. (Devam)
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

### A.3 Test defect or product defect (Hassan)
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [complete]

### A.4 Refactoring smell hunt (Devam)
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [complete]

### A.5 Traceback and hypothesis ranking (Trung)
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]

### A.6 Exit question (Hassan)
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [complete]

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
(Issue 31)
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

(Issue 25)
- Symptom / observed behaviour: Cancel an appointment, then try to find the appointment in the system, return none
- Expected behaviour and requirement: return appointment details with status as cancelled
- Minimal synthetic reproduction steps: From project/, run "python -m pytest tests/test_services.py::test_cancel_appointment_returns_and_retains_cancelled_appointment"
- Meaningful failing test path/name and exact relevant failure: FAILED tests/test_services.py::test_cancel_appointment_returns_and_retains_cancelled_appointment - AssertionError: assert None is <smartcare.domain.Appointment object at 0x000001C397D6D2B0>
  - E       AssertionError: assert None is <smartcare.domain.Appointment object at 0x000001C397D6D2B0>
  - E        +  where None = find_appointment('A1')
  - E        +    where find_appointment = <smartcare.data_store.SmartCareDataStore object at 0x000001C397D6C830>.find_appointment
  - tests\test_services.py:71: AssertionError
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

- Symptom / observed behaviour: [complete]
- Expected behaviour and requirement: [complete]
- Minimal synthetic reproduction steps: [complete]
- Meaningful failing test path/name and exact relevant failure: [complete]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [complete]
- Expected behaviour and requirement: [complete]
- Minimal synthetic reproduction steps: [complete]
- Meaningful failing test path/name and exact relevant failure: [complete]
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
(Issue 31)
Likely cause and why plausible: My initial hypothesis is that the practitioner ID comparison in the conflict check may be incorrect. This is plausible because the reported tests show a same-practitioner, same-time booking was accepted, while a different-practitioner booking at that time was rejected. 
Evidence intended to inspect / competing explanation / discriminating check: I will inspect the failing assertion, the stored appointment’s practitioner ID, time and status, and the book_appointment → conflict-check path. A competing explanation is that the test setup passes a different practitioner ID or datetime than intended. I will verify the actual values and compare the conflict-check result for D1 and D2 using the same store.
Member and saved sequence/time or commit showing this preceded consultation: Sophie, Commit: 2e03f3d06dfde3523c8c8baeaedf127e326b8f38

(Issue 25)
Likely cause and why plausible: cancel appointment doesn't change appointment status to cancelled, instead, delete the appointment from data store.
Evidence intended to inspect / competing explanation / discriminating check: In services.py, function cancel_appointment has appointment.cancel() line 150
Member and saved sequence/time or commit showing this preceded consultation: Sophie, Commit: 2feb2b711f308a7a756c21470257338c3fdda88c

Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

### F8-02 human entry
Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

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

2. Issue 25 (Sophie) : Actual prompt: fix `FAILED tests/test_services.py::test_cancel_appointment_returns_and_retains_cancelled_appointment - AssertionError: assert None is <smartcare.domain.Appointment object at 0x000001C397D6D2B0>`
  - Ranked suggestion: To preserve cancellation history under FR-07 / AC-05.2, change find_appointment() to return a matching appointment regardless of status, while keeping its blank-ID validation. Keep the conflict check’s SCHEDULED filter separate so cancelled appointments remain findable but don’t block the time slot.
  - evidence check: The fix is in project/smartcare/data_store.py, not domain.py. Appointment.cancel() already changes the status without deleting the appointment; find_appointment() is filtering cancelled records out.
  - observed evidence: project/smartcare/data_store.py line 93-94, run python -m pytest tests/test_regressions.py::test_cancel_appointment_returns_and_retains_cancelled_appointment
  - correct, partly correct or wrong: Correct, tests\test_regressions.py .  1 passed in 0.07s
  - accept, modify or reject with reason: Accept, the test is pass

3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 (issue 31) before repair | 2e03f3d06dfde3523c8c8baeaedf127e326b8f38 | python -m pytest -vv tests/test_starter.py::test_conflict_rule_and_different_practitioner [stage08/issue31](D:\PycharmProjects\st1-assignment3\project>) | tests/test_starter.py::test_conflict_rule_and_different_practitioner FAILED |
| F8-01 (issue 31) after repair | 6f0f25df9e82401abaeb71b4c938c2513684f78f | python -m pytest tests/test_regressions.py::test_conflict_rule_and_different_practitioner rootdir: D:\PycharmProjects\st1-assignment3\project | tests\test_regressions.py . 1 passed in 0.07s |
| F8-01 (issue 25) before repair | 2feb2b711f308a7a756c21470257338c3fdda88c  | python -m pytest tests/test_services.py::test_cancel_appointment_returns_and_retains_cancelled_appointment | [complete] |
| F8-01 (issue 25) after repair | [complete] | [complete] | [complete] |
| F8-01 before repair | [complete]  | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-01 before repair | [complete]  | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification (Sophie)

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: 
  - F8-01: 
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/27 ()
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/28 ()
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/31 (Sophie)
  - F8-02:
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/24 ()
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/25 (Sophie)
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/26 ()
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/29 ()
    - https://github.com/sophie-uni/st1-assignment3-Wed3/issues/30 ()
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure? (Sophie)

Response: Before changing code, reproduce and record the failure: capture the failing test, command, code SHA, traceback, expected versus observed behaviour, and the requirement involved. Reduce it to a minimal case, inspect the relevant call path and state, and record a hypothesis plus checks that distinguish it from alternatives. Confirm the test matches the requirement; then use the evidence to identify the cause and make the smallest justified fix. This avoids fixing the wrong problem or masking a test defect.

2. Where should expected behaviour come from during debugging? (Sophie)

Response: Expected behaviour should come from the approved requirements baseline, especially the relevant acceptance criterion, and any documented domain or service contract, not from assumptions about what the current code does. 

3. What is a debugging hypothesis? (Hassan)

Response: [complete]

4. What is a regression test and why is it retained? (Hassan)

Response: [complete]

5. What is meant by root cause? (Devam)

Response: [complete]

6. What is refactoring? (Devam)

Response: [complete]

7. What is a swallowed exception? (Devam)

Response: [complete]

8. What is a code smell? (Trung)

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated? (Trung)

Response: [complete]

10. What is the Stage 8 engineering rule? (Trung)

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [✔] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
