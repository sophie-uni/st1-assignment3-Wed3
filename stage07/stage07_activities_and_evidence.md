# Stage 7 Testing and Verification Record

Group/tutorial: [complete]  Members/cohorts: [complete]
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement                         | Positive test                                                                                                                      | Negative test | Key assertion | Who    |
|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|----|-------------|--------|
| FR-01 Register patient              | Register a valid patient and assert the returned patient is the exact object stored, with its ID and name preserved. | Register a second patient with the same ID and expect ValueError. | Confirm the original remains stored and is the store’s only patient. | Sophie |
| FR-05 Prevent practitioner conflict | Book A1 for practitioner D1 at 2026-10-01 09:00, then book A2 for a different practitioner (D2) at the same time; A2 is stored as SCHEDULED. | With A1 SCHEDULED for D1 at 09:00, book A2 for D1 at exactly 09:00 with a different patient; the booking is rejected with ValueError. | pytest.raises(ValueError) around the second D1 booking, then data_store.list_appointments() == [first] and first.status is AppointmentStatus.SCHEDULED. Positive case: second.practitioner is the registered D2 and second.status is AppointmentStatus.SCHEDULED   | Hassan |
| FR-06 Cancel appointment            | Book A1 for P1 with D1 at 2026-10-01 09:00 (SCHEDULED), then cancel A1 through AppointmentService; the service returns the booked object, now CANCELLED.                                                                                                                                | Cancel A1, then cancel A1 again; the second cancellation is rejected with ValueError and A1 stays CANCELLED. A valid but unknown ID (A9) is rejected with LookupError.    | cancelled is appointment and cancelled.status is AppointmentStatus.CANCELLED. Negative case: pytest.raises(ValueError) around the second cancellation only, then appointment.status is AppointmentStatus.CANCELLED and data_store.list_appointments() == [appointment].   | Devam  |
| FR-07 Retain cancelled history      | Create a scheduled appointment, cancel it, and confirm it remains stored in the shared data store with the same object identity; e.g. appointment = appointment_service.book_appointment("A1", "P1", "D1", datetime(...)); cancelled = appointment_service.cancel_appointment("A1", store, "Patient request"). | Attempt to cancel the same appointment again, or cancel a completed appointment; expect ValueError and no state change; e.g. with pytest.raises(ValueError): appointment_service.cancel_appointment("A1", store, "Second cancellation") | assert data_store.find_appointment("A1") is cancelled and assert cancelled.status is AppointmentStatus.CANCELLED; for illegal transitions, with pytest.raises(ValueError): ...  | Trung  |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

(Sophie)
`assert True`
- Judgement: Weak/unclear 
- Why: It always passes and proves no application behaviour; it cannot catch a wrong result or missing side effect.

(Sophie)
`assert appointment is not None`
- Judgement: Weak/unclear  
- Why: It proves only that the value isn’t None, not that it is the correct appointment, has the required status, or was stored as expected. It would be strong only if the sole stated requirement were returning any non-None appointment.

(Hassan)
`assert appointment.status == AppointmentStatus.CANCELLED`
- Judgement: Strong for stated behaviour   
- Why: After cancelling a SCHEDULED appointment, it checks the exact status required by AC-05.1, so an appointment left SCHEDULED or moved to any other status fails. It does not show that the appointment is the same stored object, that it is still retrievable afterwards (AC-05.2) or that a second cancellation is rejected (AC-05.3). It is only meaningful when appointment is the object returned by the service or found in the shared store, not a separately constructed copy.

(Devam)
`assert len(results) > 0`
- Judgement:  Weak/unclear  
- Why: It proves only that the collection is not empty. A list holding the wrong appointment, another practitioner's booking, an appointment with the wrong status or an unexpected extra record would still pass, and it says nothing about object identity or order. It would be strong only if the stated behaviour were "at least one result is returned". For a SmartCare list the assertion should name the expected stored objects, e.g. results == [first, second] where order is promised, or the exact length plus membership of each expected object where it is not.

(Trung)
`assert data_store.find_appointment('A1') is appointment`
- Judgement: Strong for stated behaviour  
- Why: This is strong because it checks the real observable requirement that the same appointment object remains stored in the shared SmartCareDataStore after the operation: the same appointment object remains stored after cancellation, rather than being replaced by a new object or lost. It verifies identity preservation, which is the actual business behaviour required by FR-07. The limit is that it only proves the object identity and retention in the store; it does not by itself prove the cancellation reason or timestamp were recorded unless those are also asserted separately.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract:

(Sophie)
blank identifiers, whitespace-only names:
- Blank identifier: Attempt to register a patient with ID "  " and a valid name. Expect ValueError; assert the patient store remains empty.
- Whitespace-only name: Attempt to register patient P1 with name " \t\n". Expect ValueError; assert P1 was not stored and the store remains empty.

(Hassan)
same-time practitioner bookings:
- Input/state: A1 SCHEDULED for D1 at 2026-10-01 09:00; book A2 for D1 at exactly 09:00 with a different patient (P2).
- Expected result: ValueError; A2 is not stored, A1 is still SCHEDULED and the store contains only A1.
- Supporting contract: AC-04.1 — the same practitioner, the exact time and an existing SCHEDULED appointment conflict. Using a different patient shows the rule is about the practitioner, not the patient.
- Input/state: A1 SCHEDULED for D1 at 09:00; book A2 for D2 at 09:00.
- Expected result: A2 is stored as SCHEDULED with the registered D2; A1 is unaffected.
- Supporting contract: AC-04.2 — another practitioner at the same time is allowed.
- Input/state: A1 SCHEDULED for D1 at 09:00; book A2 for D1 at 08:59, and separately at 09:01.
- Expected result: each booking is stored as SCHEDULED.
- Supporting contract: a conflict needs the exact date/time; no duration-overlap rule exists, so one minute either side is the nearest permitted time. This catches an implementation that compares only the hour or treats nearby times as overlapping.
- Input/state: A1 for D1 at 09:00 has been CANCELLED; book A2 for D1 at 09:00.
- Expected result: A2 is stored as SCHEDULED; A1 remains stored as CANCELLED.
- Supporting contract: only an existing SCHEDULED appointment occupies the slot; a cancelled booking does not.
- Input/state: P1 is booked with D1 at 09:00; book P1 with D2 at 09:00.
- Expected result: allowed and stored as SCHEDULED.
- Supporting contract: no patient-conflict rule applies, so the test must not expect a rejection here.

(Devam)
cancelled appointments:
- Input/state: A1 SCHEDULED; cancel A1 through AppointmentService.
- Expected result: the same booked object is returned and its status is CANCELLED.
- Supporting contract: AC-05.1 — cancelling a SCHEDULED appointment changes it to CANCELLED; cancellation returns the same appointment.
- Input/state: A1 already CANCELLED; cancel A1 again.
- Expected result: ValueError; A1 stays CANCELLED and the store still contains only A1.
- Supporting contract: AC-05.3 — repeated cancellation is rejected.
- Input/state: A1 constructed as COMPLETED with the registered participants and added to the store; cancel A1.
- Expected result: ValueError; A1 stays COMPLETED and is still stored.
- Supporting contract: Appointment.cancel() — "Raise ValueError for an illegal transition; leave failed state unchanged." Only SCHEDULED may be cancelled.
- Input/state: A1 SCHEDULED; cancel the valid but unknown ID A9.
- Expected result: LookupError; A1 stays SCHEDULED and no record is added.
- Supporting contract: AppointmentService.cancel_appointment — "Unknown IDs raise LookupError."
- Input/state: A1 for D1 at 09:00 is CANCELLED; book A2 for D1 at 09:00.
- Expected result: A2 is accepted; the cancelled appointment no longer blocks the slot (covered by T-FR05-4).
- Supporting contract: a cancelled booking does not occupy the slot.

(Trung)
invalid status transitions:
- Input/state: attempt to cancel an appointment that is already CANCELLED
- Expected result: raise ValueError
- Supporting contract: only a SCHEDULED appointment may be cancelled; illegal transitions must be rejected and the state must remain unchanged
- Why this is a boundary case: it tests the limit of the cancellation rule at the edge of the valid state machine, ensuring the contract is enforced rather than silently accepting repeated cancellation
- Input/state: attempt to cancel an appointment that is COMPLETED
- Expected result: raise ValueError
- Supporting contract: Appointment.cancel() must reject any status other than SCHEDULED, leaving the appointment unchanged
- Why this is a boundary case: it checks that terminal states are protected and cannot be reversed through cancellation
- Input/state: attempt to cancel a new appointment that has never been booked or has invalid status
- Expected result: raise ValueError or reject the operation if the object is not in the valid state
- Supporting contract: the state machine only allows SCHEDULED -> CANCELLED; invalid transitions are not accepted 
- Why this is a boundary case: it confirms that the domain contract is enforced throughout the lifecycle and not just at the common happy path

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate                                                                                                         | What is wrong                                                                                                                                                                                                                                                                                                                                                                          | Rewritten test intention                                                                                                                                                                                                                                                                                                                                                                                       | Who          |
|-------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| 1 Weak test: patient = service.register_patient("P1", "Sophie Jiang"); assert patient is not None                 | It passes even if the patient wasn’t stored or the returned object is incorrect.                                                                                                                                                                                                                                                                                                       | Register the patient and verify the returned object is the exact object stored under P1, with the expected ID and name.                                                                                                                                                                                                                                                                                        | Sophie       |
| 2 Weak test: appointment = service.book_appointment("A1", "P1", "D1", valid_time); assert appointment is not None | It doesn’t check the appointment’s identity, participants, time, status, or whether it was stored.                                                                                                                                                                                                                                                                                     | Book the appointment and verify it is stored as A1 with the registered patient and practitioner, requested time, and SCHEDULED status.                                                                                                                                                                                                                                                                         | Sophie       |
| 3                                                                                                                 | assert True passes on every run, even if the operation before it did nothing or did the wrong thing. It only shows that execution reached the last line; it checks no observable result and traces to no criterion.                                                                                                                                                                    | With A1 SCHEDULED for D1 at 09:00, attempt to book A2 for D1 at the same time; expect ValueError, then check that A2 was not stored and A1 is still SCHEDULED (FR-05, AC-04.1).                                                                                                                                                                                                                                | Hassan True  |
| 4                                                                                                                 | It tests an SMS notification that SmartCare does not have; no revision 2 requirement mentions notifications, so the test invents a business rule. Because it passes without a real SMS feature, it can only be checking a mock or stub it created itself, so it would still pass if cancellation were broken. It traces to no acceptance criterion and adds an unnecessary dependency. | With A1 SCHEDULED, cancel it through AppointmentService; verify the returned object is A1 and its status is CANCELLED. Then cancel A1 again and expect ValueError, with A1 still CANCELLED and the store unchanged (FR-06, AC-05.1, AC-05.3).                                                                                                                                                                  | Devam SMS    |
| 5                                                                                                                 | This candidate is wrong because it assumes an SMS notification mechanism exists and tests a requirement that is not part of the SmartCare contract. It is unrelated to FR-07, which only requires that a cancelled appointment is retained in the store and remains retrievable. It does not check actual observable behaviour of the domain or service contract.                      | Verify that a cancelled appointment remains in the shared store and is the same object as before cancellation. Example: appointment = appointment_service.book_appointment("A1", "P1", "D1", datetime(...)); cancelled = appointment_service.cancel_appointment("A1", store, "Patient request"); assert data_store.find_appointment("A1") is cancelled; assert cancelled.status is AppointmentStatus.CANCELLED | Trung SMS    |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
Coverage only records which lines or branches ran during the tests, not whether the tests checked the right results. A test can call every operation and end with assert True or assert result is not None, reaching 100% coverage while a wrong status, a wrong object or a missing rejection would still pass. Coverage also cannot reveal behaviour that was never written: if the practitioner conflict check were missing entirely, there would be no uncovered line to report. It says nothing about whether the expected values match the requirements or whether the important boundaries were tested.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement                            | Acceptance criterion                                                                                                                                           | Test ID       | Test type                                             | Test name / location                                                                                  | Expected behaviour                                                                                                                                                       | Result / observed status                                           | Supplied or student-authored    | Who      |
|----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|-------------------------------------------------------|-------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|---------------------------------|----------|
| FR-01 Register patient                 | AC-01.1 — Valid required patient data with an unused ID is stored.                                                                                             | T-FR01-1      | Positive service test                                 | project/tests/test_services.py::test_register_patient_stores_valid_patient                            | Register a valid patient; verify the store returns the exact registered object with the expected ID and name.                                                            | Planned; not written or run.                                       | Student-authored                | Sophie   |
| FR-01 Register patient                 | AC-01.2 — Registration with an existing patient ID is rejected.                                                                                                | T-FR01-2      | Negative service test                                 | project/tests/test_services.py::test_register_patient_rejects_duplicate_id                            | Register a patient, then attempt another with the same ID; expect ValueError and verify the original remains stored unchanged.                                           | Planned; not written or run.                                       | Student-authored                | Sophie   |
| FR-05 Prevent practitioner conflict    | AC-04.1 — Same practitioner/exact time/SCHEDULED conflicts.                                                                                                    | T-FR05-1      | Negative service test                                 | project/tests/test_services.py::test_same_practitioner_same_time_is_rejected                          | With A1 SCHEDULED for D1 at 09:00, booking A2 for D1 at 09:00 (patient P2) raises ValueError; A2 is not stored and A1 remains the only appointment, still SCHEDULED.     | PASS                                                               | Student-authored                | Hassan   |
| FR-05 Prevent practitioner conflict    | AC-04.2 — Another practitioner at the same time is allowed.                                                                                                    | T-FR05-2      | Positive service test                                 | project/tests/test_services.py::test_different_practitioner_same_time_is_allowed                      | A2 for D2 at 09:00 is stored as SCHEDULED and references the registered D2; A1 stays SCHEDULED; the store holds exactly A1 and A2.                                       | PASS                                                               | Student-authored                | Hassan   |
| FR-05 Prevent practitioner conflict    | Supporting revision 2 contract: "Conflict means the same practitioner, exact datetime and an existing SCHEDULED appointment."                                  | T-FR05-3      | Boundary service test (parametrised: 08:59, 09:01)    | project/tests/test_services.py::test_same_practitioner_one_minute_apart_is_allowed                    | A D1 booking one minute before or after A1 is stored as SCHEDULED; A1 stays SCHEDULED.                                                                                   | PASS                                                               | Student-authored                | Hassan   |
| FR-05 Prevent practitioner conflict    | Supporting revision 2 contract: "A cancelled booking does not occupy the slot."                                                                                | T-FR05-4      | Boundary service test                                 | project/tests/test_services.py::test_cancelled_appointment_does_not_block_slot                        | After A1 is cancelled, A2 for D1 at 09:00 is stored as SCHEDULED; A1 is still stored as CANCELLED.                                                                       | PASS                                                               | Student-authored                | Hassan   |
| FR-04 Book appointment                 | AC-03.1 — partial domain evidence only (initial status and participants; storage is not covered by this test).                                                 | T-FR04-D1     | Positive domain test                                  | project/tests/test_domain.py::test_new_appointment_starts_scheduled                                   | A new Appointment is SCHEDULED and keeps its ID, the same Patient and Practitioner objects and its date/time.                                                            | PASS                                                               | Student-authored                | Hassan   |
| FR-04 Book appointment                 | Supporting revision 2 contract: "Appointment time is a local naive datetime at minute precision."                                                              | T-FR04-D2     | Negative/boundary domain test (parametrised)          | project/tests/test_domain.py::test_appointment_rejects_time_not_local_minute_precision                | A time with seconds, with microseconds, with a timezone, or given as text raises ValueError.                                                                             | PASS                                                               | Student-authored                | Hassan   |
| FR-06 Cancel appointment               | AC-05.1 — Cancelling a SCHEDULED appointment changes it to CANCELLED.                                                                                          | T-FR06-1      | Positive service test                                 | project/tests/test_services.py::test_cancel_appointment_returns_same_cancelled_object                 | cancel_appointment('A1') returns the same booked object, now CANCELLED.                                                                                                  | PASS                                                               | Student-authored                | Devam    |
| FR-06 Cancel appointment               | AC-05.3 — Repeated cancellation is rejected.                                                                                                                   | T-FR06-2      | Negative service test                                 | project/tests/test_services.py::test_repeated_service_cancellation_is_rejected                        | A second cancellation raises ValueError; A1 stays CANCELLED and is the only stored appointment.                                                                          | PASS                                                               | Student-authored                | Devam    |
| FR-06 Cancel appointment               | Supporting contract, AppointmentService.cancel_appointment: "Unknown IDs raise LookupError; invalid transitions raise ValueError and leave state unchanged."   | T-FR06-3      | Negative service test                                 | project/tests/test_services.py::test_cancel_unknown_appointment_raises_lookup_error                   | Cancelling A9 raises LookupError; A1 stays SCHEDULED and is the only stored appointment.                                                                                 | PASS                                                               | Student-authored                | Devam    |
| FR-06 Cancel appointment               | Supporting contract, Appointment.cancel: "Raise ValueError for an illegal transition; leave failed state unchanged."                                           | T-FR06-4      | Negative/boundary service test                        | project/tests/test_services.py::test_cancel_completed_appointment_through_service_is_rejected         | Cancelling a stored COMPLETED A1 raises ValueError; A1 stays COMPLETED and stored.                                                                                       | PASS                                                               | Student-authored                | Devam    |
| FR-06 Cancel appointment               | AC-05.1 — domain evidence for the status change.                                                                                                               | T-FR06-D1     | Positive domain test                                  | project/tests/test_domain.py::test_cancel_changes_status                                              | cancel() changes SCHEDULED to CANCELLED; ID and date/time are unchanged.                                                                                                 | PASS                                                               | Student-authored                | Devam    |
| FR-06 Cancel appointment               | AC-05.3 — domain evidence for repeated cancellation.                                                                                                           | T-FR06-D2     | Negative domain test                                  | project/tests/test_domain.py::test_repeated_cancel_is_rejected                                        | A second cancel() raises ValueError; status stays CANCELLED.                                                                                                             | PASS                                                               | Student-authored                | Devam    |
| FR-07                                  | 	AC-05.2 — Cancelled history remains retrievable in the current session                                                                                         | T-FR07-1      | Positive service test                                 | project/tests/test_services.py::test_cancel_changes_status_and_keeps_appointment_in_store             | After cancellation, the appointment is still retrievable by ID and remains in the current session history                                                                | Pass — appointment remains stored and traceable after cancellation | Student-authored                | Trung    |
| FR-07                                  | 	AC-05.2 — Cancelled history remains retrievable in the current session                                                                                         | T-FR07-2      | Negative service test                                 | project/tests/test_services.py::test_repeated_cancellation_is_rejected_and_state_remains_cancelled    | A cancelled appointment stays present and its state remains CANCELLED; a second cancel attempt is rejected without mutation                                              | Pass — cancelled record remains accessible and state is stable     | Student-authored                | Trung    |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID    | Requirement                          | Acceptance criterion                                                         | Positive / Negative / Boundary  | Test intention                                                                                                                                                 | Observable result expected                                                                                                        | Added evidence beyond supplied tests                                                                                                                                                                                                                   |
|------------|--------------------------------------|------------------------------------------------------------------------------|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| T-FR01-1   | FR-01 Register patient               | AC-01.1 - Valid required patient data with an unused ID is stored.           | Positive                        | test_register_patient_stores_valid_patient: register P1, Sophie Jiang in a fresh store.                                                                        | Lookup returns the exact registered object; ID/name match; the store contains that patient.                                       | Supplied tests use patient registration for setup but do not directly verify successful patient storage and returned object identity.                                                                                                                  |
| T-FR01-2   | FR-01 Register patient               | AC-01.2 - Registration with an existing patient ID is rejected.              | Negative                        | test_register_patient_rejects_duplicate_id: register P1, then attempt another registration with the same ID and expect ValueError.                             | The original remains the exact object found under P1; its name is unchanged; the store still contains only the original.          | Adds direct evidence that duplicate registration is rejected without overwriting or adding a patient.                                                                                                                                                  |
| T-FR05-1   | FR-05 Prevent practitioner conflict  | AC-04.1 - Same practitioner/exact time/SCHEDULED conflicts.                  | Negative                        | test_same_practitioner_same_time_is_rejected: book A1 (P1, D1, 09:00), then attempt A2 (P2, D1, 09:00).                                                        | ValueError; find_appointment('A2') is None; list_appointments() == [A1]; A1 still SCHEDULED.                                      | The supplied conflict check reuses the same patient and does not check state after rejection. This uses a different patient, so it shows the rule is about the practitioner, and confirms the rejected booking was not stored and A1 was not changed.  |
| T-FR05-2   | FR-05 Prevent practitioner conflict  | AC-04.2 - Another practitioner at the same time is allowed.                  | Positive                        | test_different_practitioner_same_time_is_allowed: with A1 for D1 at 09:00, book A2 for D2 at 09:00.                                                            | A2 is the stored object under A2, references the registered D2, is SCHEDULED; A1 stays SCHEDULED; store holds exactly A1 and A2.  | The supplied check only compares the returned practitioner ID. This adds storage, registered-object identity, status, and confirms the first booking is unaffected.                                                                                    |
| T-FR05-3   | FR-05 Prevent practitioner conflict  | Supporting contract: conflict needs the exact datetime.                      | Boundary                        | test_same_practitioner_one_minute_apart_is_allowed: with A1 for D1 at 09:00, book A2 for D1 at 08:59, and separately at 09:01 (parametrised).                  | Each A2 is stored, SCHEDULED, at the requested time; A1 stays SCHEDULED.                                                          | No supplied test checks nearby times. It would catch a conflict check that compares only the hour or invents a duration-overlap rule.                                                                                                                  |
| T-FR05-4   | FR-05 Prevent practitioner conflict  | Supporting contract: a cancelled booking does not occupy the slot.           | Boundary                        | test_cancelled_appointment_does_not_block_slot: book A1 (D1, 09:00), cancel it, then book A2 for D1 at 09:00.                                                  | A2 is stored as SCHEDULED; A1 is still stored and CANCELLED.                                                                      | No supplied test combines cancellation with booking. It would catch a conflict check that ignores status.                                                                                                                                              |
| T-FR04-D1  | FR-04 Book appointment               | AC-03.1 (partial domain evidence)                                            | Positive                        | test_new_appointment_starts_scheduled: construct an Appointment from a Patient, a Practitioner and 09:00 with no status argument.                              | Status is SCHEDULED; ID, date/time and the same participant objects are kept.                                                     | Keeps the "new appointment starts SCHEDULED" reference intention at domain level, separate from service storage, and checks participant identity at construction.                                                                                      |
| T-FR04-D2  | FR-04 Book appointment               | Supporting contract: local naive datetime at minute precision.               | Negative / Boundary             | test_appointment_rejects_time_not_local_minute_precision: construct with 09:00:01, 09:00:00.000001, 09:00 UTC-aware, and the text '2026-10-01 09:00'.          | Each raises ValueError.                                                                                                           | No supplied test checks date/time validation. Exact-time conflict checking depends on times being stored at minute precision.                                                                                                                          |
| T-FR06-1   | FR-06 Cancel appointment             | AC-05.1 - Cancelling a SCHEDULED appointment changes it to CANCELLED.        | Positive                        | test_cancel_appointment_returns_same_cancelled_object: book A1, then cancel_appointment('A1').                                                                 | The returned object is the booked A1 and its status is CANCELLED.                                                                 | The supplied test calls appointment.cancel() directly. This is the first check of cancellation through the completed Stage 6 service and of the returned object's identity.                                                                            |
| T-FR06-2   | FR-06 Cancel appointment             | AC-05.3 - Repeated cancellation is rejected.                                 | Negative                        | test_repeated_service_cancellation_is_rejected: cancel A1, then cancel A1 again through the service.                                                           | ValueError; A1 stays CANCELLED; list_appointments() == [A1].                                                                      | Adds the repeat-rejection check at the service boundary and confirms the rejection does not remove or duplicate the record.                                                                                                                            |
| T-FR06-3   | FR-06 Cancel appointment             | Supporting contract: unknown IDs raise LookupError.                          | Negative                        | test_cancel_unknown_appointment_raises_lookup_error: with A1 SCHEDULED, cancel 'A9'.                                                                           | LookupError; A1 stays SCHEDULED; list_appointments() == [A1].                                                                     | No supplied test covers an unknown cancellation ID. It confirms the specific exception (not ValueError) and that no other appointment is affected.                                                                                                     |
| T-FR06-D1  | FR-06 Cancel appointment             | AC-05.1 (domain evidence)                                                    | Positive                        | test_cancel_changes_status: call cancel() on a new SCHEDULED appointment.                                                                                      | Status is CANCELLED; ID and date/time unchanged.                                                                                  | Keeps the "cancellation changes status" reference intention as its own focused test, so its failure cannot be hidden by the repeat check in the supplied combined test.                                                                                |
| T-FR06-D2  | FR-06 Cancel appointment             | AC-05.3 (domain evidence)                                                    | Negative                        | test_repeated_cancel_is_rejected: cancel(), then cancel() again.                                                                                               | ValueError; status stays CANCELLED.                                                                                               | Keeps the "repeated cancellation is rejected" reference intention as its own domain test.                                                                                                                                                              |
| T-FR06-4   | FR-06 Cancel appointment             | Supporting contract: illegal transition raises ValueError, state unchanged.  | Negative / Boundary             | test_cancel_completed_appointment_through_service_is_rejected: add a COMPLETED A1 (registered participants) to the store, then cancel it through the service.  | ValueError; A1 stays COMPLETED; find_appointment('A1') is A1.                                                                     | No supplied test covers COMPLETED. It checks that the service relies on the domain guard instead of forcing the status to CANCELLED.                                                                                                                   |
| T-FR07-1   | FR-07                                | Cancellation changes status.                                                 | Positive                        | test_cancel_changes_status: create a valid appointment, call cancel(), and confirm the state transition to CANCELLED.                                          | status changes from SCHEDULED to CANCELLED and the appointment remains traceable.                                                 | Confirms the state transition is performed by the domain operation itself, not only by a service wrapper.                                                                                                                                              | 
| T-FR07-2   | FR-07                                | Repeated cancellation is rejected.                                           | Negative                        | test_repeated_cancellation_is_rejected: create a valid appointment, cancel it once, then call cancel() a second time and expect rejection.                     | A second cancel raises ValueError and the appointment remains CANCELLED without state mutation.                                   | Guards the domain against illegal repeated transitions and proves the cancellation rule is enforced.                                                                                                                                                   |
| T-FR07-3   | FR-07                                | Blank patient ID is rejected.                                                | Negative / Boundary             | test_blank_patient_id_is_rejected: create a Patient with empty or whitespace-only patient_id and expect validation to reject it.                               | ValueError is raised and no invalid Patient object is accepted.                                                                   | Confirms the required-field rule for identity is enforced before any patient record can exist.                                                                                                                                                         |
| T-FR07-4   | FR-07                                | A new appointment starts SCHEDULED.                                          | Positive                        | test_appointment_starts_scheduled: create a valid Patient and Practitioner, then construct an Appointment and verify the initial status.                       | Appointment is created successfully and appointment.status is AppointmentStatus.SCHEDULED.                                        | Verifies the initial lifecycle state of a new appointment instead of assuming a default value.                                                                                                                                                         |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID      | Arrange                                                                                                              | Act                                                                                      | Assert                                                                                                                                                                               | Why meaningful / why assertion proves criterion                                                                                                                                                                   |
|--------------|----------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| T-FR01-1     | Create a fresh SmartCareDataStore and PatientService.                                                                | patient = service.register_patient("P1", "Sophie Jiang")                                 | store.find_patient("P1") is patient; check the expected ID and name; assert store.list_patients() == [patient].                                                                      | Verifies valid required data is stored and the returned patient is the stored object, as AC-01.1 requires.                                                                                                        |
| T-FR01-2     | Create a fresh store/service and register original = service.register_patient("P1", "Sophie Jiang").                 | with pytest.raises(ValueError): service.register_patient("P1", "David Jiang")            | Assert store.find_patient("P1") is original, its name is unchanged, and store.list_patients() == [original].                                                                         | Verifies AC-01.2’s duplicate-ID rejection and confirms rejection did not overwrite or add a patient.                                                                                                              |
| T-FR05-1     | Fresh store; register P1, P2, D1, D2 with services sharing that store; first = book A1 (P1, D1, 2026-10-01 09:00).   | with pytest.raises(ValueError): book A2 (P2, D1, 09:00)                                  | find_appointment('A2') is None; list_appointments() == [first]; first.status is AppointmentStatus.SCHEDULED.                                                                         | The exception proves the conflict is detected; the state checks prove the rejected booking was not stored and the existing one was not altered, as AC-04.1 requires.                                              |
| T-FR05-2     | Same fresh setup; first = book A1 (P1, D1, 09:00).                                                                   | second = book A2 (P2, D2, 09:00)                                                         | find_appointment('A2') is second; second.practitioner is find_practitioner('D2'); second.status is SCHEDULED; first.status is SCHEDULED; the store holds exactly first and second.   | Proves the permitted case in AC-04.2 is actually stored with the registered D2, not just returned, and that it did not disturb D1's booking. Membership plus length is used because list order is not promised.   |
| T-FR05-3     | Same fresh setup; first = book A1 (P1, D1, 09:00).                                                                   | second = book A2 (P2, D1, nearby_time) for 08:59 and 09:01                               | find_appointment('A2') is second; second.date_time == nearby_time; second.status is SCHEDULED; first.status is SCHEDULED.                                                            | The nearest permitted times on both sides of the exact-time rule are accepted, so a wrong comparison (hour only, or an invented overlap window) fails.                                                            |
| T-FR05-4     | Same fresh setup; first = book A1 (P1, D1, 09:00); cancel_appointment('A1').                                         | second = book A2 (P2, D1, 09:00)                                                         | find_appointment('A2') is second; second.status is SCHEDULED; find_appointment('A1') is first; first.status is CANCELLED.                                                            | Proves only SCHEDULED appointments occupy a slot and that freeing the slot does not remove the cancelled history.                                                                                                 |
| T-FR04-D1    | Create Patient P1 and Practitioner D1 directly.                                                                      | appointment = Appointment('A1', patient, practitioner, 09:00)                            | status is SCHEDULED; appointment_id == 'A1'; patient is patient; practitioner is practitioner; date_time == 09:00.                                                                   | Proves the initial status and that the appointment keeps the same participant objects. It is partial evidence for AC-03.1 because storage is not involved.                                                        |
| T-FR04-D2    | Create Patient P1 and Practitioner D1 directly; choose one invalid time per parametrised case.                       | with pytest.raises(ValueError): Appointment('A1', patient, practitioner, invalid_time)   | ValueError for each case.                                                                                                                                                            | Each case sits just outside the minute-precision/naive rule (one second, one microsecond, a timezone, a string), so a missing check in validate_date_time fails the test.                                         |
| T-FR06-1     | Fresh store; register P1 and D1; appointment = book A1 (P1, D1, 09:00).                                              | cancelled = cancel_appointment('A1')                                                     | cancelled is appointment; cancelled.status is AppointmentStatus.CANCELLED.                                                                                                           | Proves the service changes the stored appointment itself (not a copy) from SCHEDULED to CANCELLED, as AC-05.1 requires.                                                                                           |
| T-FR06-2     | Same fresh setup; cancel_appointment('A1') once.                                                                     | with pytest.raises(ValueError): cancel_appointment('A1')                                 | appointment.status is CANCELLED; list_appointments() == [appointment].                                                                                                               | Only the second call is inside pytest.raises, so the exception comes from the repeat. The state checks prove the rejection left the record intact (AC-05.3).                                                      |
| T-FR06-3     | Same fresh setup with A1 SCHEDULED.                                                                                  | with pytest.raises(LookupError): cancel_appointment('A9')                                | appointment.status is SCHEDULED; list_appointments() == [appointment].                                                                                                               | Proves the documented absence error at the service boundary and that an unknown ID cannot cancel or add another record.                                                                                           |
| T-FR06-4     | Fresh store; register P1 and D1; add a COMPLETED A1 built from those registered objects.                             | with pytest.raises(ValueError): cancel_appointment('A1')                                 | completed.status is COMPLETED; find_appointment('A1') is completed.                                                                                                                  | Proves the service cannot bypass the domain guard for a terminal state and the stored record stays unchanged.                                                                                                     |
| T-FR06-D1    | Create a SCHEDULED appointment from fresh Patient and Practitioner objects.                                          | appointment.cancel()                                                                     | status is CANCELLED; appointment_id == 'A1'; date_time == 09:00.                                                                                                                     | Proves the domain transition on its own, without the service or store.                                                                                                                                            |
| T-FR06-D2    | Create a SCHEDULED appointment and cancel() it once.                                                                 | with pytest.raises(ValueError): appointment.cancel()                                     | status is CANCELLED.                                                                                                                                                                 | Proves the repeat is rejected and does not change the status.                                                                                                                                                     |
| [complete]   | [complete]                                                                                                           | [complete]                                                                               | [complete]                                                                                                                                                                           | [complete]                                                                                                                                                                                                        |
| [complete]   | [complete]                                                                                                           | [complete]                                                                               | [complete]                                                                                                                                                                           | [complete]                                                                                                                                                                                                        |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] |
| T-FR04-D1 | New appointment starts SCHEDULED and keeps its ID, participants and date/time | project/tests/test_domain.py::test_new_appointment_starts_scheduled | PASS SHA: [paste tested SHA] |
| T-FR04-D2 | Appointment rejects a time with seconds, microseconds, a timezone, or given as text (4 parametrised cases) | project/tests/test_domain.py::test_appointment_rejects_time_not_local_minute_precision | PASS (4 cases) SHA: [paste tested SHA] |
| T-FR06-D1 | cancel() changes SCHEDULED to CANCELLED | project/tests/test_domain.py::test_cancel_changes_status | PASS SHA: [paste tested SHA] |
| T-FR06-D2 | Repeated cancel() is rejected; status stays CANCELLED | project/tests/test_domain.py::test_repeated_cancel_is_rejected | PASS SHA: [paste tested SHA] |


## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID  | Behaviour           | Requirement / criterion | Test file/function | Result |
|----------|---------------------|---|---|---|
| T-FR01-1 | Positive            | AC-01.1 - Valid required patient data with an unused ID is stored.| test_register_patient_stores_valid_patient() | PASS SHA: e5fa120fa7d9cdbf2a58f56c9cf71087b43aa841 |
| T-FR01-2 | Negative            | AC-01.2 - Registration with an existing patient ID is rejected. | test_register_patient_rejects_duplicate_id() | PASS SHA: e5fa120fa7d9cdbf2a58f56c9cf71087b43aa841 |
| T-FR05-1 | Negative            | AC-04.1 - Same practitioner/exact time/SCHEDULED conflicts. | test_same_practitioner_same_time_is_rejected() | PASS SHA: [paste tested SHA] |
| T-FR05-2 | Positive            | AC-04.2 - Another practitioner at the same time is allowed. | test_different_practitioner_same_time_is_allowed() | PASS SHA: [paste tested SHA] |
| T-FR05-3 | Boundary            | Supporting contract - conflict needs the exact datetime. | test_same_practitioner_one_minute_apart_is_allowed() | PASS (2 cases) SHA: [paste tested SHA] |
| T-FR05-4 | Boundary            | Supporting contract - a cancelled booking does not occupy the slot. | test_cancelled_appointment_does_not_block_slot() | PASS SHA: [paste tested SHA] |
| T-FR06-1 | Positive            | AC-05.1 - Cancelling a SCHEDULED appointment changes it to CANCELLED. | test_cancel_appointment_returns_same_cancelled_object() | PASS SHA: [paste tested SHA] |
| T-FR06-2 | Negative            | AC-05.3 - Repeated cancellation is rejected. | test_repeated_service_cancellation_is_rejected() | PASS SHA: [paste tested SHA] |
| T-FR06-3 | Negative            | Supporting contract - unknown IDs raise LookupError. | test_cancel_unknown_appointment_raises_lookup_error() | PASS SHA: [paste tested SHA] |
| T-FR06-4 | Negative / Boundary | Supporting contract - illegal transition raises ValueError; state unchanged. | test_cancel_completed_appointment_through_service_is_rejected() | PASS SHA: [paste tested SHA] |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour           | Boundary/invalid input | Expected result | Test ID    |
|---------------------|------------------------|-----------------|------------|
| Negative            | Register patient P1, then attempt to register a second patient with ID P1.  | Duplicate IDs are rejected with ValueError. Afterward, assert store.find_patient("P1") is original and store.list_patients() == [original] | T-FR01-2 |
| Negative            | A1 SCHEDULED for D1 at 09:00; book A2 for D1 at exactly 09:00 with a different patient. | ValueError. Afterward, find_appointment('A2') is None, list_appointments() == [A1] and A1 is still SCHEDULED. Risk checked: a conflict that is detected but still saves or alters a record. | T-FR05-1 |
| Boundary            | A1 SCHEDULED for D1 at 09:00; book A2 for D1 at 08:59 and at 09:01. | Each booking is stored as SCHEDULED. Risk checked: a conflict check that compares only the hour or invents a duration-overlap rule. | T-FR05-3 |
| Boundary            | A1 for D1 at 09:00 is CANCELLED; book A2 for D1 at 09:00. | A2 stored as SCHEDULED; A1 still stored and CANCELLED. Risk checked: a conflict check that ignores status and blocks a freed slot. | T-FR05-4 |
| Negative / Boundary | Appointment time 09:00:01, 09:00:00.000001, 09:00 with UTC timezone, or the text '2026-10-01 09:00'. | ValueError for each. Risk checked: times stored with seconds or a timezone would make the exact-time conflict comparison unreliable. | T-FR04-D2 |
| Negative            | A1 already CANCELLED; cancel A1 again through the service. | ValueError. Afterward, A1 is still CANCELLED and list_appointments() == [A1]. Risk checked: a repeat that silently succeeds, removes or duplicates the record. | T-FR06-2 |
| Negative            | A1 SCHEDULED; cancel the valid but unknown ID 'A9'. | LookupError (not ValueError). Afterward, A1 is still SCHEDULED and list_appointments() == [A1]. Risk checked: a wrong exception type or an unknown ID affecting another record. | T-FR06-3 |
| Negative / Boundary | Stored A1 with status COMPLETED; cancel A1 through the service. | ValueError. Afterward, A1 is still COMPLETED and find_appointment('A1') is A1. Risk checked: the service forcing CANCELLED without using the domain guard. | T-FR06-4 |
| [complete]          | [complete]             | [complete]      | [complete] |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.
(Sophie)
Requirement: FR-01 Register patient
Acceptance criterion: AC-01.2 - Registration with an existing patient ID is rejected.
Behaviour to test: Negative
Human-first test idea/categories: Register patient P1 with Name 'Sophie', then register patient P1 again with name 'David', should return error, and P1 remain as 'Sophie'
Prompt and purpose: Avoid duplicated patient registration

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: How to avoid duplicated patient registration, what to verify and what requirement trace, how to assertion quality?
- What it claims to verify: The duplicate attempt raises ValueError, and the original patient remains the exact stored object, unchanged, with no extra patient added.
- Requirement trace: FR-01, AC-01.2  registration with an existing patient ID is rejected. Use test ID T-FR01-2.
- Assertion quality: Strong for this criterion—the exception assertion verifies rejection, while the identity and list assertions verify no overwrite or duplicate insertion. Checking only that an object is not None would not prove these behaviours.
- Human critique: match the requirement, test result is expected
- Decision: Accept
- Reason: strong statement and clear steps
- Final test reference if accepted/modified: e5fa120fa7d9cdbf2a58f56c9cf71087b43aa841
- Actual verification result: complete

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection
(Sophie)
Which Copilot-generated test looked convincing but was weak? 
```
def test_duplicate_patient_registration_weak() -> None:
    store = SmartCareDataStore()
    service = PatientService(store)
    original = service.register_patient("P1", "Sophie")

    try:
        service.register_patient("P1", "David")
    except ValueError:
        pass

    assert original is not None
```
Why was it weak? It passes whether the duplicate registration is correctly rejected or incorrectly accepted. The assertion only checks that the original variable exists; it doesn’t verify rejection or that the stored patient stayed unchanged.
How did you strengthen it? For a meaningful test, use pytest.raises(ValueError), then assert the store still returns the original patient and contains only that patient
Accepted / modified / rejected test decisions and evidence: commit SHA e5fa120fa7d9cdbf2a58f56c9cf71087b43aa841

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: 

    - python -m pytest tests/test_services.py::test_register_patient_stores_valid_patient()
    - 1 passed in 0.04s 
    - commit SHA d0cfa57734b01bb08ddc67ac31d00c93fa914e03
    - python -m pytest tests/test_services.py::test_register_patient_rejects_duplicate_id 
    - 1 passed in 0.07s
    - commit SHA d0cfa57734b01bb08ddc67ac31d00c93fa914e03

Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [response]
Coverage if used: [result or not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [response]
Optional fixtures/parametrisation used and why, if any: [response or not used]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task                          | Branch         | PR         | Reviewer   | Key feedback | Outcome    |
|-------------------------------------|----------------|------------|------------|--------------|------------|
| FR-01 Register patient              | stage07/FR-01  | [complete] | [complete] | [complete]   | [complete] |
| FR-05 Prevent practitioner conflict | stage07/FR-05  | [complete] | [complete] | [complete]   | [complete] |
| FR-06 Cancel appointment            | stage07/FR-05  | [complete] | [complete] | [complete]   | [complete] |
| [complete]                          | [complete]     | [complete] | [complete] | [complete]   | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member       | Actual contribution                                                                                                                                                                                                                                                              | Evidence link                                              |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| Sophie Jiang | setup stage07 start point                                                                                                                                                                                                                                                        | https://github.com/sophie-uni/st1-assignment3-Wed3/pull/13 |
| Sophie Jiang | Complete FR-01 Register patient includes test cases                                                                                                                                                                                                                              | [complete]                                                 |
| Hassan Ahmad | Designed and implemented FR-05 practitioner-conflict service tests (T-FR05-1 to T-FR05-4) and appointment construction domain tests (T-FR04-D1, T-FR04-D2); completed the FR-05 traceability, test design, Arrange–Act–Assert and boundary entries; formative questions 5 and 6  | [paste PR link]                                            |
| Devam        | Designed and implemented FR-06 cancellation service tests (T-FR06-1 to T-FR06-4) and cancellation domain tests (T-FR06-D1, T-FR06-D2); completed the FR-06 traceability, test design, Arrange–Act–Assert and boundary entries; formative questions 7 and 8                       | [paste PR link]                                            |
| [complete]   | [complete]                                                                                                                                                                                                                                                                       | [complete]                                                 |

## N Formative Questions

1. What question does verification answer? (Sophie)
“Are we building the product right?” It checks whether the software conforms to its specified requirements and design, using methods such as reviews and tests.

2. What question does validation answer? (sophie)
“Are we building the right product?” It checks whether the software meets users’ needs and intended use in its real context.

3. What is a unit test? (sophie)
A unit test checks one small, isolated part of the software, such as a function, method, or class, against its expected behaviour using controlled inputs and assertions.

4. What is a pytest fixture?
A pytest fixture is a function marked with @pytest.fixture that prepares setup, such as a fresh SmartCareDataStore. pytest calls it and passes its return value to any test that names the fixture as a parameter. With the default function scope, each test receives a new object, so tests do not share state.

5. What is parametrisation in pytest? (Hassan)
Parametrisation (@pytest.mark.parametrize) runs one test function over several input and expected-value sets. pytest collects each set as a separate case with its own result. It suits one behaviour tested with different data, such as checking that both 08:59 and 09:01 are free for the same practitioner. More data sets do not by themselves add new behaviour.

6. What is regression testing? (Hassan)
Regression testing reruns the retained, accumulated test suite after a change to confirm that behaviour which worked before still works. When a defect is found, the test that exposes it stays in the suite so the defect cannot return unnoticed.

7. What does code coverage tell us, and what does it not prove? (Devam)
Coverage reports which lines or branches executed during a test run, so it can point to code no test reaches, such as an untested cancellation branch. It does not prove that the tests checked the right result, that the expected values come from the requirements, or that the important boundaries were chosen. It also cannot reveal behaviour that was never implemented, because missing code has no line to leave uncovered.

8. What makes an assertion weak? (Devam)
An assertion is weak when a relevant wrong result could still pass it. Examples are assert True, checking only that a value is not None, checking only that a list is non-empty, checking one field when the claim is about the whole result, or catching any exception with a broad try/except or pytest.raises(Exception). A strong assertion checks the exact observable outcome the requirement promises, such as the specific status, the same stored object, the specific exception and the unchanged state after a rejection.

9. What is the appropriate role of GitHub Copilot as a test assistant? (Trung)
[response]

10. What is the Stage 7 engineering rule? (Trung)
[response]

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
