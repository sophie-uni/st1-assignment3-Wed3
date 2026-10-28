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

1. "Appointment disappears after cancellation." — **Symptom.** It describes what someone observed, without a concrete value or a cause. "Disappears" could mean it is missing from a lookup, from the list, or has been replaced.
2. "The data-store removal path is probably being called." — **Hypothesis.** It is a tentative explanation ("probably") that can be tested. The current SmartCareDataStore has no public delete operation, so it can be checked directly: if list_appointments() still contains A1 after cancellation, nothing was removed and the hypothesis is rejected.
3. "The failing test shows store.find_appointment('A1') returns None." — **Evidence.** It is a concrete, repeatable value observed in a run. It shows what the lookup returned, not why.
4. "The service layer is badly designed." — **Opinion.** It names no specific behaviour, value or check that could confirm or reject it, and it does not explain this failure.
5. "Traceback points to smartcare/services.py line 42 in the example." — **Evidence (of location).** It is a fact taken from the run, but it shows where the failure surfaced, not where the cause was introduced. The faulty decision may be in an earlier call, such as a store method.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: Cancelled-history scenario.

- **Expected behaviour:** after cancel_appointment('A1'), the same A1 object is CANCELLED and is still returned by data_store.find_appointment('A1') and AppointmentService.find_appointment('A1'), and still appears in list_appointments(). Requirements: FR-06/AC-05.1 (status change), FR-07/AC-05.2 (cancelled history is retained in the current session), FR-08/AC-06.1 (a known appointment ID returns that appointment).
- **Observed behaviour:** [fill from your run, e.g. data_store.find_appointment('A1') returns None after cancellation]
- **Minimal reproduction:** new SmartCareDataStore; register P1 "Alex Example" and D1 "Taylor Example", "General"; book A1 for P1 with D1 at 2026-10-01 09:00; cancel_appointment('A1'); call data_store.find_appointment('A1').
- **Initial hypothesis:** cancellation removes A1 from the store instead of only changing its status.
- **Evidence to inspect:** list_appointments() straight after cancellation (if A1 is still listed, it was not removed); the body of Appointment.cancel() and AppointmentService.cancel_appointment(); the body of SmartCareDataStore.find_appointment(); git diff between the Stage 7 SHA and the prepared SHA for data_store.py.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: The test should be changed, not the product. It is a test defect: its expected result contradicts FR-07 and AC-05.2, which require a cancelled appointment to stay stored and retrievable in the session. Changing the code to delete appointments would break the approved requirement and other correct tests just to satisfy a wrong oracle. The test should instead expect the same object, status CANCELLED, still found by lookup and still listed.

A test expecting different practitioners at the same time to conflict does not reflect AC-04.2. AC-04.2 states that another practitioner at the same time is allowed; a conflict needs the same practitioner, the exact time and an existing SCHEDULED appointment. That test is also a test defect and should be corrected to expect the second booking to be stored as SCHEDULED.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason:

Smells and small refactorings, applied one at a time with the full suite run between each:

| Smell | Why it is a problem | Small refactoring |
|---|---|---|
| Long method (70 lines) | Several responsibilities in one place; hard to read and review. | Extract small private helpers with clear names (e.g. participant lookup, conflict check). |
| Duplicate status strings | Magic strings can drift from the real states and are easy to mistype. | Use the existing AppointmentStatus members. |
| Direct collection manipulation | Bypasses SmartCareDataStore's add/find/list checks (type, duplicate ID, registered objects). | Call the existing data_store.add_appointment/find_appointment/list_appointments. |
| Printing inside the service | Mixes console output with business logic and makes the service harder to test. | Return the object or raise the documented exception; leave printing to console.py. |
| Repeated validation | Duplicates rules already enforced by the domain constructors and required_text. | Rely on the domain objects for field validation. |
| Four nested conditionals | Deep nesting hides the order of checks. | Use guard clauses that raise early, keeping the same order of checks. |

Classification:
- Rename appt to appointment — **refactoring** (naming only).
- Extract a repeated conflict helper — **refactoring** (structure only, same rule).
- Add rescheduling — **feature** (new behaviour, out of scope for Stage 8).
- Restore retained cancellation lookup — **repair** (restores required FR-07 behaviour).
- Replace a magic status string with the existing enum — **refactoring**, provided the string meant the same state; if it was a wrong value, the change would be a repair.

Behaviour that must remain unchanged: the same registered objects are returned and stored; ValueError and LookupError are raised in the same situations; only SCHEDULED can become CANCELLED; a rejected operation leaves stored state unchanged; the exact-time, same-practitioner, SCHEDULED-only conflict rule; and cancelled appointments stay retrievable.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [Check every value below against your own prepared run and replace the line number and values with what you actually saw.]

- **Failure used:** tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_retrievable
- **Exception/assertion:** AssertionError on `assert data_store.find_appointment('A1') is booked`
- **Expected / observed:** expected the booked A1 object; observed None.
- **Test line:** tests/test_regressions.py:[line]
- **Application call path:** test → AppointmentService.cancel_appointment('A1') → AppointmentService.find_appointment → SmartCareDataStore.find_appointment → Appointment.cancel(); then test → SmartCareDataStore.find_appointment('A1') returns None.
- **Supporting requirement:** FR-07 / AC-05.2 (cancelled history retained); FR-08 / AC-06.1 (known ID returns that appointment).

Ranked causes:
1. **find_appointment() does not return CANCELLED appointments** (best fit: the cancellation itself returned the right object with CANCELLED status, and only the later lookup failed). Check: compare list_appointments() with find_appointment('A1') after cancellation, and read the find_appointment() body. If A1 is listed but not found, the lookup is at fault.
2. **Cancellation removes A1 from the store.** Check: list_appointments() after cancellation. If A1 is still listed, this is rejected; there is also no public delete operation to call.
3. **The stored object is replaced or stored under a different key** (e.g. an untrimmed or changed ID). Check: `cancelled is booked`, the appointment_id of the listed object, and whether find_appointment returns a different object rather than None.

A traceback alone does not establish the cause because it shows where the wrong value was noticed (an assertion in the test file), not which code produced it. The faulty decision may be in a method that ran earlier or inside a store method that the traceback does not show. Only a check that separates the candidate causes, such as list versus lookup, identifies the root cause.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: It replaces diagnosis with guessing. The line where a failure appears is often not where the cause is, so an immediate edit may hide the symptom while the real fault stays. It can break behaviour that other tests protect, "fix" correct code to match a wrong test, and lose the original failing evidence. When several things are changed at once, nobody can say which change mattered. Reproducing the failure, stating the expected behaviour from the requirement and testing a hypothesis first leads to the smallest correct repair.


Classification responses (1–5, each with reason): see A.1.
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: see A.2.
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: see A.5.

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: 420f5be33953c23d2b6bedb532406c4315775c4d; SmartCare A3 Requirements Baseline 2026, revision 2.
- Baseline test command / working directory / observed result / evidence: python -m pytest / project/ / 30 passed in 0.17s
- Clean preparation SHA if a record-only commit followed Stage 7: [complete]
- Branch and preparer / how teammates obtained this branch: [complete]
- Downloaded tool version, source SHA256 and --check outcome: [complete]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete]
- Prepared faulty-state commit SHA: [complete]
- Preparation or recovery issues and resolution, if any: [complete]
- Initial prepared full-suite command / result / key failures: [complete]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [fill from your run, e.g. a second booking for D1 at exactly 2026-10-01 09:00 is accepted instead of rejected — "DID NOT RAISE ValueError"]
- Expected behaviour and requirement: FR-05 / AC-04.1 — with A1 SCHEDULED for D1 at 09:00, a booking for D1 at exactly 09:00 must raise ValueError and leave the store unchanged (A2 not stored, A1 still SCHEDULED). AC-04.2 — a booking for D2 at 09:00 must still be allowed. No patient-conflict or duration-overlap rule applies.
- Minimal synthetic reproduction steps: new store; register P1, P2, D1, D2; book A1 (P1, D1, 2026-10-01 09:00); book A2 (P2, D1, 09:00) and expect ValueError; check find_appointment('A2') is None, list_appointments() == [A1], A1 SCHEDULED; then book A3 (P2, D2, 09:00) and expect it to be stored as SCHEDULED.
- Meaningful failing test path/name and exact relevant failure: project/tests/test_regressions.py::test_f8_01_same_practitioner_same_time_conflict_is_rejected — [paste the exact failing line, e.g. "Failed: DID NOT RAISE <class 'ValueError'>" at line …]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis — name the exact faulty condition in SmartCareDataStore.has_practitioner_conflict(), quote the line, and the evidence that confirmed it, e.g. `git diff <Stage 7 SHA> <prepared SHA> -- project/smartcare/data_store.py` and has_practitioner_conflict('D1', 09:00) returning False while A1 is SCHEDULED]
- Smallest justified fix / diff / why other behaviour is preserved: [complete — change only the faulty condition so the check again requires the same practitioner, the exact date/time and SCHEDULED status. Other behaviour is preserved because the method signature, return type and no-mutation contract are unchanged, and it is still only called from book_appointment.]
- Repair SHA / focused verification result: [SHA] / [e.g. "1 passed"]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [fill from your run, e.g. after cancel_appointment('A1'), data_store.find_appointment('A1') returns None and AppointmentService.find_appointment('A1') raises LookupError]
- Expected behaviour and requirement: FR-06 / AC-05.1 — cancellation changes SCHEDULED to CANCELLED on the same object. FR-07 / AC-05.2 and BR-07 — the cancelled appointment stays stored and retrievable in the session. FR-08 / AC-06.1 — a known ID returns that appointment. AC-05.3 — a second cancellation is still rejected with ValueError without changing state. The store returns None only for a valid unknown ID; the service raises LookupError only for an unknown ID.
- Minimal synthetic reproduction steps: new store; register P1 and D1; book A1 (P1, D1, 2026-10-01 09:00); cancel_appointment('A1'); compare data_store.find_appointment('A1'), AppointmentService.find_appointment('A1') and list_appointments(); then cancel A1 again and expect ValueError.
- Meaningful failing test path/name and exact relevant failure: project/tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_retrievable — [paste the exact failing line, e.g. "assert None is <Appointment …>" at line …]
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis — name the exact faulty decision in the store method (e.g. SmartCareDataStore.find_appointment() treating a CANCELLED appointment as absent), quote the line, and the evidence: A1 still in list_appointments() while find_appointment('A1') is None, plus the git diff against the Stage 7 SHA]
- Smallest justified fix / diff / why other behaviour is preserved: [complete — remove only the faulty decision so find_appointment again returns the stored object for any known ID regardless of status. Other behaviour is preserved because blank IDs still raise ValueError, unknown IDs still return None, and duplicate-ID checks in book_appointment, which also use find_appointment, still work.]
- Repair SHA / focused verification result: [SHA] / [e.g. "1 passed"]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: The practitioner/time conflict check in SmartCareDataStore.has_practitioner_conflict() no longer matches a SCHEDULED appointment for the same practitioner at the exact time. This is plausible because the utility changes only two store method bodies, booking only rejects a conflict when this method returns True, and the booking itself still succeeds with valid objects.
Evidence intended to inspect / competing explanation / discriminating check: Inspect has_practitioner_conflict() line by line (practitioner comparison, date/time comparison, status comparison, excluded ID) and the git diff of data_store.py against the Stage 7 SHA. Competing explanation: book_appointment() does not call the check or ignores its result. Discriminating check: call data_store.has_practitioner_conflict('D1', datetime(2026, 10, 1, 9, 0)) directly after booking A1. If it returns False, the store method is at fault; if it returns True but the booking still succeeds, the service is at fault.
Member and saved sequence/time or commit showing this preceded consultation: [member] / [commit SHA or timestamp of this record before Copilot was used]

### F8-02 human entry
Likely cause and why plausible: Cancellation removes A1 from the store, or the store lookup no longer returns cancelled appointments. Plausible because the symptom is a missing appointment straight after cancellation, and the utility changes store method bodies.
Evidence intended to inspect / competing explanation / discriminating check: Inspect Appointment.cancel(), AppointmentService.cancel_appointment(), SmartCareDataStore.find_appointment() and list_appointments(), and the git diff of data_store.py. Competing explanations: (a) the record is deleted; (b) the record is kept but the lookup hides it. Discriminating check: after cancellation, compare list_appointments() with find_appointment('A1'). If A1 is listed but not found, (b) is supported and (a) is rejected; if it is not listed, (a) is supported.
Member and saved sequence/time or commit showing this preceded consultation: [member] / [commit SHA or timestamp of this record before Copilot was used]

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member:

```text
Observed behaviour: [paste from C, e.g. booking A2 for D1 at 2026-10-01 09:00 is accepted although A1 is SCHEDULED for D1 at that time]
Expected behaviour: FR-05 / AC-04.1: the same practitioner at the exact same time with an existing SCHEDULED appointment must be rejected with ValueError and the store left unchanged. AC-04.2: a different practitioner at the same time is allowed.
Steps to reproduce: new SmartCareDataStore; register P1, P2, D1, D2; book A1 (P1, D1, 2026-10-01 09:00); book A2 (P2, D1, 2026-10-01 09:00).
Failing test: tests/test_regressions.py::test_f8_01_same_practitioner_same_time_conflict_is_rejected — [paste exact failure line]
My hypothesis: has_practitioner_conflict() in data_store.py no longer matches a SCHEDULED appointment for the same practitioner at the exact time.
Relevant code: [paste the current has_practitioner_conflict() body and the conflict lines of book_appointment()]
Task:
Rank the three most likely causes. For each, identify
the evidence I should inspect to distinguish it from
the other possible causes.
Do not rewrite the entire application.
Do not invent requirements.
Treat all suggested explanations as hypotheses.
```

Member / output reference: [member] / [link or saved screenshot/file of Copilot output]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete from the actual Copilot output]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete from the actual Copilot output]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete from the actual Copilot output]
Final human conclusion and comparison with initial hypothesis: [complete — state the confirmed cause and whether it matched the E hypothesis exactly, partly, or not]

### F8-02 Copilot review
Actual prompt / output reference and member:

```text
Observed behaviour: [paste from D, e.g. after cancel_appointment('A1'), data_store.find_appointment('A1') returns None]
Expected behaviour: FR-06 / AC-05.1: cancellation changes SCHEDULED to CANCELLED on the same object. FR-07 / AC-05.2: the cancelled appointment remains stored and retrievable in the session. FR-08 / AC-06.1: a known ID returns that appointment. AC-05.3: a repeated cancellation raises ValueError without changing state.
Steps to reproduce: new SmartCareDataStore; register P1 and D1; book A1 (P1, D1, 2026-10-01 09:00); cancel_appointment('A1'); call data_store.find_appointment('A1') and data_store.list_appointments().
Failing test: tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_retrievable — [paste exact failure line]
My hypothesis: either cancellation removes A1 from the store, or find_appointment() no longer returns cancelled appointments.
Relevant code: [paste the current find_appointment() and list_appointments() bodies from data_store.py, Appointment.cancel(), and AppointmentService.cancel_appointment()]
Task:
Rank the three most likely causes. For each, identify
the evidence I should inspect to distinguish it from
the other possible causes.
Do not rewrite the entire application.
Do not invent requirements.
Treat all suggested explanations as hypotheses.
```

Member / output reference: [member] / [link or saved screenshot/file of Copilot output]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete from the actual Copilot output]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete from the actual Copilot output]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete from the actual Copilot output]
Final human conclusion and comparison with initial hypothesis: [complete — e.g. whether the list-versus-lookup check rejected the deletion idea]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [prepared SHA + commit adding test_regressions.py] | `python -m pytest tests/test_regressions.py::test_f8_01_same_practitioner_same_time_conflict_is_rejected` / project/ | [e.g. 1 failed — DID NOT RAISE ValueError] |
| F8-01 after repair | [F8-01 repair SHA] | same command / project/ | [e.g. 1 passed] |
| F8-02 before repair | [prepared SHA + commit adding test_regressions.py] | `python -m pytest tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_retrievable` / project/ | [e.g. 1 failed — assert None is <Appointment …>] |
| F8-02 after repair | [F8-02 repair SHA] | same command / project/ | [e.g. 1 passed] |
| Full suite after both repairs, before refactor | [SHA] | `python -m pytest -q` / project/ | [e.g. N passed] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour:

- **F8-01:** pytest.raises(ValueError) wraps only the conflicting booking, so the test fails if a same-practitioner, same-time booking is accepted. The checks afterwards (A2 not stored, the store holds only A1, A1 still SCHEDULED) catch a check that raises but still saves or changes a record. The final D2 booking catches the opposite mistake: a repair that rejects every same-time booking, which would break AC-04.2.
- **F8-02:** `cancelled is booked` and the CANCELLED status confirm the transition happened on the stored object. Separate checks on the store lookup, the service lookup and the list catch a hidden, deleted or replaced record, and keep None (store) and LookupError (service) apart. The repeated cancellation inside pytest.raises(ValueError), followed by the status and list checks, makes sure the repair does not weaken the cancellation guard.
- All earlier Stage 6 and Stage 7 tests stay in the suite, so the repairs are also checked against the previously verified registration, booking, conflict and cancellation behaviour.

Unrelated failures investigated / resolution: [complete — "none" if every prepared failure traced to F8-01 or F8-02; otherwise describe]

## H. Refactoring decision and before/after verification

Smell and exact location: Long method with mixed responsibilities — AppointmentService.book_appointment() in project/smartcare/services.py. It resolves both participants and raises their absence errors, builds the appointment, checks for a duplicate ID, checks for a conflict and stores the result, all in one body.

Small proposed structural change / why justified: Extract the participant lookup and its two absence checks into a private method `_find_participants(patient_id, practitioner_id)` that returns `(patient, practitioner)`; book_appointment() calls it. This gives the lookup step a name, shortens book_appointment() so the booking rules (duplicate ID, conflict, store) are easier to read, and keeps the change inside one class. The lookup order stays the same: both store lookups run before either absence check, so a blank ID still raises ValueError before any LookupError.

External behaviour to preserve / relevant tests: LookupError for an unknown patient or practitioner; ValueError for a blank ID; the appointment links the actual registered objects; nothing is stored when booking is rejected; duplicate-ID and conflict checks unchanged; the stored appointment is returned. Tests: test_starter.py::test_registration_and_booking and ::test_unregistered_participants_rejected; test_services.py FR-05 tests; test_regressions.py F8-01; and two guard tests added before the refactor because no existing test covered these paths: test_services.py::test_book_unknown_practitioner_is_rejected (R8-1) and ::test_book_blank_practitioner_id_is_rejected (R8-2).

Before result: see G, full passing suite.

Actual change / diff / separate refactor SHA: [refactor SHA]

```diff
@@ book_appointment
-        patient = self.data_store.find_patient(patient_id)
-        practitioner = self.data_store.find_practitioner(practitioner_id)
-        if patient is None:
-            raise LookupError('Patient not found')
-        if practitioner is None:
-            raise LookupError('Practitioner not found')
+        patient, practitioner = self._find_participants(
+            patient_id,
+            practitioner_id,
+        )
@@ new private method
+    def _find_participants(
+        self,
+        patient_id: str,
+        practitioner_id: str,
+    ) -> tuple[Patient, Practitioner]:
+        """Return the registered patient and practitioner for booking.
+
+        Raise ValueError for a blank/invalid ID and LookupError for an
+        absent participant. Do not create or change records.
+        """
+        patient = self.data_store.find_patient(patient_id)
+        practitioner = self.data_store.find_practitioner(practitioner_id)
+        if patient is None:
+            raise LookupError('Patient not found')
+        if practitioner is None:
+            raise LookupError('Practitioner not found')
+        return patient, practitioner
```

Focused and full after-refactor commands / working directory / results / evidence:
- Focused (project/): `python -m pytest tests/test_services.py::test_book_unknown_practitioner_is_rejected tests/test_services.py::test_book_blank_practitioner_id_is_rejected tests/test_starter.py::test_unregistered_participants_rejected tests/test_starter.py::test_registration_and_booking` — [e.g. 4 passed]
- Full (project/): `python -m pytest -q` — [e.g. N passed, the same count as before the refactor]
- `python main.py` still prints the demo appointment — [confirm]

Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [Accepted after review by …] The full suite gave the same result before and after, including the guard tests for the unknown practitioner and the blank ID, so exceptions, object identity and non-mutation on rejection are unchanged. Only the internal structure of book_appointment() changed.

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [link] F8-01 practitioner conflict not enforced — [owner]; [link] F8-02 cancelled appointment not found after cancellation — [owner]; [link] Refactor: extract participant lookup from book_appointment — [owner]
Branch / prepared, repair and refactor checkpoints: debug/stage8 — prepared state see B; repairs see C/D; refactor see H.
PR link and another member's reviewer identity: [PR link] / [reviewer]
Key human feedback, difference from Copilot findings and response/outcome: [complete from the real review]
Actual review approval / merge evidence: [link]
Integrated code SHA and team pull/retest command / working directory / result: [SHA] / `git switch main`, `git pull`, then `python -m pytest -q` / project/ / [result]
Evidence-only later SHA / explanation if different: [SHA and explanation, or not applicable]
Each member's substantive contribution and artefact:

| Member | Substantive contribution | Artefact |
|---|---|---|
| Sophie Jiang | [complete] | [link] |
| Hassan Ahmad | [complete] | [link] |
| Devam | [complete] | [link] |
| Trung | [complete] | [link] |

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete from your actual Copilot output; if none fits, report that honestly and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete from your actual run — e.g. for F8-02, if A1 was still in list_appointments() while find_appointment('A1') returned None, that rejected the deletion hypothesis and pointed to the lookup; for F8-01, a direct call to has_practitioner_conflict() separated a store fault from a service fault]
3. How did regression tests protect the refactoring? The refactor started from a fully passing suite, and two guard tests were added first because no existing test covered booking with an unknown or blank practitioner ID, which is exactly the code being moved. The same suite was run after the change with the same result, so the exception types, the use of the registered objects and the no-mutation behaviour were shown to be unchanged. The F8-01 regression test also protected the conflict check that follows the extracted lookup in book_appointment().

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure? (Sophie)

Response: Read the failure fully, reproduce it with small synthetic input, state the expected behaviour from the requirement, and decide whether the product or the test is wrong. Then form a hypothesis and run a check that confirms or rejects it before making the smallest change.

2. Where should expected behaviour come from during debugging? (Sophie)

Response: From the approved requirements and published contracts (the revision 2 baseline, acceptance criteria and the documented method contracts), not from what the current code happens to return, from a failing test's assumption or from a Copilot suggestion.

3. What is a debugging hypothesis? (Hassan)

Response: A specific, testable explanation of why a failure occurs, together with a check that could prove it wrong. For example, "the lookup hides cancelled appointments" can be tested by comparing list_appointments() with find_appointment().

4. What is a regression test and why is it retained? (Hassan)

Response: A test that exposes a defect, fails before the repair and passes after it. It stays in the suite so that if a later change brings the defect back, the suite fails straight away.

5. What is meant by root cause? (Devam)

Response: The underlying faulty decision that produces the failure, as opposed to where the symptom is seen. Fixing the root cause stops the failure; fixing only the symptom leaves it able to return.

6. What is refactoring? (Devam)

Response: Changing the internal structure of code to make it clearer or easier to maintain without changing its external behaviour: the same results, exceptions and state changes. Tests passing before and after is the evidence that behaviour was preserved.

7. What is a swallowed exception? (Devam)

Response: An exception that is caught and then ignored or hidden, for example `except Exception: pass`. The program carries on as if nothing went wrong, so the real failure is hidden and becomes harder to diagnose.

8. What is a code smell? (Trung)

Response: A sign in the code that its design may cause problems, such as a long method, duplicated code, magic strings, unclear names or misplaced responsibility. A smell is not a bug by itself, but it is a reason to consider a small refactor.

9. How should GitHub Copilot-generated debugging diagnoses be treated? (Trung)

Response: As unverified hypotheses. Each suggestion is checked against the requirement and against real evidence from the code and test runs, then accepted, modified or rejected with a reason. Confident wording is not proof, and Copilot does not replace human diagnosis or another member's review.

10. What is the Stage 8 engineering rule? (Trung)

Response: Diagnose before you fix. Reproduce the failure, record a human hypothesis, gather evidence, make the smallest repair the evidence supports, keep a regression test, and refactor only under passing tests.

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
Unresolved issues or incomplete checks / owner / next action: [complete, or "none"]
Handover note: The same project/ is handed over with both store defects repaired, the two regression tests in tests/test_regressions.py, the refactor guard tests in tests/test_services.py and all earlier tests retained, at integrated SHA [SHA]. Practitioner conflict and cancelled-history behaviour are restored. Stage 9 query and console TODOs are untouched; session-only storage remains the scope.
