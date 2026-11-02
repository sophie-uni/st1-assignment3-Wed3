# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Wednesday 14:30-16:30 Group 3 (st1-assignment3-Wed3)
Members and responsibilities: Sophie Jiang (Team leader), Hassan Ahmad (Team member), Trung Hieu (Team member)
Stage 8 integrated SHA, command, working directory and actual result: 399e222d74dd50010addc29b244f48380a233fae, https://github.com/sophie-uni/st1-assignment3-Wed3/pull/41

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason | Who |
|---|---|---| ---|
| Temporary menu choice | Transient interaction state | It only decides which service call runs on that pass of the menu loop and means nothing once the command finishes. | Hassan |
| Practitioner specialty | Required session/domain state | A validated `Practitioner` field set at registration and shown whenever the practitioner or their appointments are displayed. | Hassan |
| Patient identity | Domain state | Patient details are persistent data that must be stored and available across multiple visits and sessions. | Sophie |
| Appointment history | Domain state | Appointment records are part of the patient's long-term medical and administrative history and need to be retained for future reference, reporting, and continuity of care. | Sophie |
| Debug print output | Transient interaction state | Diagnostic output is only for the current run and should never be persisted or treated as domain state. It exists to support debugging, not to change the model. | Trung |
| Appointment status | Domain state | Appointment status is a core business datum: scheduled, cancelled, completed, etc. It determines validity, filtering, and whether a record blocks a slot. It must be retained as part of the appointment’s history and used in validation logic. | Trung |

What is intentionally lost on exit? (Hassan) Every patient, practitioner and appointment, including cancelled history. All records live in one in-memory `SmartCareDataStore` created when the program starts, so a new launch begins empty. Restart persistence (FR-10) is retired, so this is the declared scope rather than a defect.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint | Who |
|---|---|---|---|---|---|
| appointment_sort_key | appointment: Appointment | tuple[datetime, str] | Produces a stable sort key so appointments are ordered consistently for display and filtering. It must use date/time, then appointment id. | Domain ordering is based on appointment date/time and id; this is a pure helper and should not mutate state. | Trung |
| select_appointments | `appointments: list[Appointment]`, `practitioner_id: str`, `status: AppointmentStatus` &#124; `None = None` | A new `list[Appointment]` containing the same objects, ordered by `appointment_sort_key` | Selects the given practitioner's appointments and, if a status is given, only that status; `None` keeps every status. Does no validation (registration and status type are checked by the service), never changes the source list or objects, and performs no input/output. | `appointment.practitioner.practitioner_id` from the actual linked `Practitioner`; `appointment.status` enum; ordering uses `date_time` and `appointment_id` | Hassan |
| Service listing (select_appointments) | `practitioner_id: str` | `appointments: list[Appointment]` | Retrieves all appointments associated with the practitioner_id. Validate that practitioner_id is not null, empty, and matches an existing practitioner record. | In data_store, practitioner must exist and be active | Sophie |
| Console (run_menu) | User menu selection: `str`; user-entered data (patient ID, name, appointment ID, practitioner ID, date/time): `str` | Displayed menus, prompts, error messages, confirmation messages | Presents the application menu; collects and validates user input; calls domain/service functions such as register, find, book, cancel and list; handles expected input errors; and keeps the session running until exit is selected. Validate menu choices and ensure required fields are not empty before calling services. | Uses data maintained by the patient and appointment services. Must only accept valid menu options such as register, find, book, cancel, list and exit, also comply with business rules enforced by the domain layer. | Sophie ||

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: (Hassan) `Patient(patient_id, name)` and `Practitioner(practitioner_id, name, specialty)` trim and require every field, their IDs are read-only properties, and the store rejects duplicate IDs. `Appointment` holds the actual registered `Patient` and `Practitioner` objects (the store checks this with `is`), a validated naive minute-precision `date_time`, and an `AppointmentStatus` that only `cancel()` changes. `select_appointments` filters on the linked practitioner's `practitioner_id` and on the `status` enum, and orders on `date_time` then `appointment_id`. It reads these existing fields only and adds none. Names and specialty are not used by the query; the console reads them from the same linked objects when displaying results.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason | Who |
|---|---|---|---|
| Appointment.cancel reads input | The domain method should not read user input or prompt the user. It should only perform the state transition for the appointment itself. | The domain object should only validate and update its own state; input parsing and prompting belong to the console or service layer. This keeps the model reusable and testable without a keyboard or menu. | Trung |
| Service prints/reads the menu | The service would own input and presentation, so it could not be reused or tested without a keyboard, and the caller could not decide how to handle errors. | The console owns the menu loop, prompts and messages. The service only coordinates the store and domain objects, returning objects or raising `ValueError`/`LookupError` for the console to report. | Hassan |
| Query sorts its source in place | A query should not modify the data it receives. Calling appointments.sort changes the caller's list and creates an unintended side effect. | The query operation should work on a copy of the data and return the result. Queries are responsible for retrieving or filtering data, not mutating domain state. | Sophie |
| Store prints Appointment saved | The store is performing user interface work. Printing messages mixes persistence responsibilities with presentation responsibilities. | The store should save and return the Appointment object or a result value. The Console/UI layer is responsible for displaying messages such as "Appointment saved". This keeps persistence and presentation concerns separated. | Sophie |

### A4 Sorting comparison (Trung)

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: <!-- response -->

Score-example prediction and explanation of passing the named key:
- For an appointments.sort(key=appointment_sort_key) and result = sorted(appointments, key=appointment_sort_key), predict source order, return value and result identity. Give a meaningful mutation check:
  - appointments = [a3, a1, a2] 
    original = appointments.copy()

    appointments.sort(key=appointment_sort_key)

        # Source list is mutated in place 
        # appointments now contains the reordered list
        # original remains unchanged because it was a copy before the sort

    result = sorted(appointments, key=appointment_sort_key)
        # result is a new list
        # appointments is still in the sorted order
        # result is not the same object as appointments
        # result == appointments
        # result is not appointments
- Expected behaviour:
  - sort() mutates the original list in place and returns None.
  - sorted() does not mutate the original list; it returns a new list.
  - appointment_sort_key must be a pure function based on the appointment’s date/time and id.
  - The key function must not mutate the appointment object or depend on console state, user input, or the current menu context.
- This is the correct boundary: sorting is a query/presentation concern, not a domain mutation. The domain model remains unchanged; only a new ordered collection is created when needed.

### A5 Exit question (Hassan)

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: Cancellation changes the status of the retained appointment object, so its history and participant links stay available for the rest of the session. The slot is freed only because the conflict rule counts SCHEDULED appointments. Deletion would lose the record entirely. To check this, after cancelling A1: finding A1 returns the same booked object with status CANCELLED; listing D1 with the default (all statuses) still returns that object; listing D1 with SCHEDULED only leaves it out, because it is no longer scheduled. That shows the filter works, not that the record was removed.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning:

Query decisions (Hassan):
- `select_appointments` does no validation. It cannot know which practitioners are registered without a store, and giving it one would add hidden state, so registration and status-type checks belong in the service.
- It returns a new list but reuses the same Appointment objects instead of copying them, so identity checks hold and later status changes stay visible.
- It filters with `appointment.status is status`, so only a real `AppointmentStatus` member can match, and `None` means every status.
- It never calls `sort()` on its argument; it sorts its own local list with `sorted(..., key=appointment_sort_key)`.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence        |
|---|---|---|---|------------------------|
| QRY-01 (Hassan) | D1 and D2 appointments in one list | `select_appointments(source, 'D1')`, pure query | Only D1 objects; D2 query returns only D2; unregistered ID returns `[]` | T-QRY01-1, T-QRY01-2   |
| QRY-02 (Hassan) | D1 has SCHEDULED, CANCELLED and COMPLETED appointments | Query with `None` and each enum member | Default keeps all; each enum keeps only that status; no match gives `[]` | T-QRY02-1 to T-QRY02-3 |
| QRY-03 (Hassan) | Unsorted source; A1, A2, A4 share 09:00 | Query ordering through the named key | `A9, A1, A2, A4, A3`; source order and fields unchanged | T-QRY03-1, T-QRY03-2   |
| FP-01 (Hassan) | Same arguments three times | Query | Equal results in distinct lists; no input/output | T-FP01-1, T-FP01-2     |
| FP-02 (Hassan) | Empty, already-sorted and unsorted lists | Query | New list each time containing the same unchanged objects | T-FP02-1 to T-FP02-3   |
| FP-03 (Trung) | Valid source list, practitioner_id, optional status | `select_appointments(source, practitioner_id, status)` in the pure query helper; no validation, no hidden state, no I/O | New list only; same object references preserved; source list and objects unchanged | T-FP03-1  |
| QRY-04-1 (Sophie) Known practitioner with no appointments or no matching status | practitioner_id | find_appointment returns a empty list | New empty list; no error | T-QRY-04-1 |
| QRY-04-2 (Sophie) Valid unknown practitioner ID | practitioner_id | Validate practitioner existence in data store returns null | LookupError| T-QRY-04-2 |
| QRY-04-3 (Sophie) Blank or invalid ID | practitioner_id | Validate practitioner_id format, null or invalid | ValueError | T-QRY-04-3 |
| QRY-04-4 (Sophie) Known practitioner with a non-enum status such as 'scheduled' | practitioner_id | Validate status | ValueError; do not treat it as no matches | T-QRY-04-4 |
| QRY-04-5 (Sophie) Omitted status | practitioner_id | find_appointment returns a list of appointments | list appointments include every status and preserve history | T-QRY-04-5 |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: <!-- response -->

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| T-QRY01-1, 2 (Hassan) | `project/smartcare/queries.py` `select_appointments` | D1 query returns only `A9, A1, A2, A4, A3`; D2 control returns `B1, B2`; an unregistered ID returns `[]` | Passed | [test_queries.py](../project/tests/test_queries.py) |
| T-QRY02-1 to 3 (Hassan) | same | Default includes all three statuses; each status keeps only itself; D2 with COMPLETED returns `[]` | Passed | same |
| T-QRY03-1, 2 (Hassan) | same | Equal 09:00 times ordered `A1, A2, A4`; A9 first by date; source order and fields unchanged | Passed | same |
| T-FP01-1, 2 (Hassan) | same | Three calls give identical results in different lists; no printing or input | Passed | same |
| T-FP02-1 to 3 (Hassan) | same | Empty and already-sorted inputs return a new list; results are the same unchanged objects | Passed | same |
| T-FP03-1 (Trung) | same | The pure helper works on supplied valid objects and filter values; it does not establish whether a practitioner is registered. That validation belongs in service listing. Do not modify any source object or collection. A new container may contain the same object references. Do not use a hidden global store or perform input/output. | Passed | same |
| T-QRY-04-1 (Sophie) | In test_services.py test_known_practitioner_with_no_matching_appointments() | Existing practitioner with no appointments. Assert result == [] | Pass | f9739fce2046cd0a4a9ca5fd9dc1897521cdada9 |
| T-QRY-04-2 (Sophie) | In test_services.py test_unknown_practitioner() | Unknown practitioner ID. Assert LookupError is raised. | Pass | 76d25fa7ba6b8ba8ebfc58fe13901af6eb6648a1 |
| T-QRY-04-3 (Sophie) | In test_services.py test_invalid_practitioner_id(practitioner_id) | Blank, whitespace, or None ID. Assert ValueError is raised. | Pass | 76d25fa7ba6b8ba8ebfc58fe13901af6eb6648a1 |
| T-QRY-04-4 (Sophie) | In test_services.py test_non_enum_status() | Status supplied as "scheduled" string. Assert ValueError is raised. | Pass | 76d25fa7ba6b8ba8ebfc58fe13901af6eb6648a1 |
| T-QRY-04-5 (Sophie) | In test_services.py test_omitted_status_returns_all() | Status omitted. Assert scheduled and cancelled appointments are both returned. | Pass | f9739fce2046cd0a4a9ca5fd9dc1897521cdada9 |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

The test suite covers:
- Practitioner isolation: only appointments belonging to the specified practitioner are returned.
- Status filtering: each AppointmentStatus enum value is tested individually, and omission of the status parameter returns appointments of every status.
- Default-all behaviour: status=None returns the complete appointment history for the practitioner.
- Equal-time ordering: appointments with the same appointment time are ordered using the required appointment ID tie-break rule.
- Named-key reuse: repeated calls using the same filter parameters produce equivalent results.
- Repeated-call behaviour: multiple invocations return correct results without accumulating state.
- Empty-list handling: a known practitioner with no matching appointments returns a new empty list.
- Already-sorted inputs: ordering remains correct when data is already in the required order.
- Fresh-list result: callers receive a new list rather than a reference to internal storage.
- Source preservation: the query operation does not modify appointment objects, field values, or the original collection order.
- Known-empty case: known practitioner with no matching appointments returns [].
- Unknown practitioner case: raises LookupError.
- Invalid practitioner ID case: raises ValueError.
- Invalid status case: non-AppointmentStatus values raise ValueError.
- Retained history: cancelled and historical appointments remain available when status filtering is omitted.

Purity explanation from code inspection, including absence of hidden state and I/O:

list_practitioner_appointments() behaves as a query operation.

Code inspection shows that the method:
- Reads appointment data from the data store.
- Performs validation of the supplied parameters.
- Filters appointments through select_appointments().
- Returns a list result.

The method does not:
- Call input().
- Call print().
- Read or write files.
- Access network resources.
- Modify stored appointments.
- Modify practitioner records.
- Update any service or datastore state.
- Depend on mutable hidden state between calls.

Given the same datastore contents and arguments, the method will return the same result each time. This indicates query-style behaviour with no observable side effects.

What the tests do and do not establish: 

The tests establish that:
- Required validation rules are enforced.
- Correct exceptions are raised for invalid inputs.
- Practitioner filtering works correctly.
- Status filtering works correctly.
- Ordering requirements are satisfied.
- Empty-result behaviour is correct.
- Historical appointments are preserved.
- Query operations do not modify source data.

The tests do not establish that:
- The implementation is optimal in terms of performance.
- The implementation is thread-safe.
- External persistence behaves correctly, because the datastore is in-memory only.
- Every possible appointment count or date combination has been tested.
- The absence of hidden side effects beyond those observable through the tested public interface.

Instead, the tests provide evidence that the implementation satisfies the specified functional requirements QRY-04-1 through QRY-04-5 and behaves consistently for representative normal, boundary, and error cases.

## D. Integrated console and workflow evidence (Sophie)

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | `cd project`; `python -m pytest tests/test_workflows.py::test_menu_completes_register_book_cancel_list_and_exit -q` | Register/find participants; book, find, cancel, list/filter; reject a same-practitioner conflict; allow another practitioner and reuse the cancelled slot; exit cleanly. | The test drives those inputs through the real menu. It verifies participant lookup output, conflict error, scheduled and cancelled appointment output, list filtering, successful slot reuse and exit; records remain visible through the session until exit. Result: 1 passed. | `project/tests/test_workflows.py::test_menu_completes_register_book_cancel_list_and_exit` |
| UI-02 invalid-input recovery | `cd project`; `python -m pytest tests/test_workflows.py::test_menu_recovers_from_invalid_input_without_losing_session -q` | Recover from unknown choices, blank/duplicate IDs, unknown records, malformed/impossible dates, invalid status and repeated cancellation; then accept a valid action and exit. | The test verifies an error is shown for each invalid action, subsequent valid input is processed, and appointment state remains scheduled after rejected operations and cancelled after the first valid cancellation. Result: 1 passed. | `project/tests/test_workflows.py::test_menu_recovers_from_invalid_input_without_losing_session` |
| Automated service workflow | `cd project`; `python -m pytest tests/test_services.py -q` | Service contracts for registration, lookup, booking/conflicts, cancellation and practitioner appointment listing hold without console input/output. | Result: 27 passed. Service tests check returned/stored object identity and state, exception behavior, slot conflicts/reuse, and ordered/status-filtered listing. | `project/tests/test_services.py` |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

(Sophie, F-1)
Human design completed before AI: QRY-04, after test cases, I have run 'python -m pytest tests/test_services.py', got 2 errors:
- FAILED tests/test_services.py::test_known_practitioner_with_no_matching_appointments - NameError: name 'select_appointments' is not defined
- FAILED tests/test_services.py::test_omitted_status_returns_all - NameError: name 'select_appointments' is not defined

Actual prompt/context supplied: 

fix 'FAILED tests/test_services.py::test_known_practitioner_with_no_matching_appointments - NameError: name 'select_appointments' is not defined
FAILED tests/test_services.py::test_omitted_status_returns_all - NameError: name 'select_appointments' is not defined'

Actual response: 

The failure is caused by services.py calling select_appointments, which isn’t defined. The intended helper is select_appointments in queries.py, but that helper—and its sort-key function—are still unimplemented. The plan is to implement those helpers, connect the service to them, and run the focused and module tests.

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| F-1 | test_known_practitioner_with_no_matching_appointments, test_omitted_status_returns_all | The intended helper is select_appointments in queries.py, but that helper—and its sort-key function—are still unimplemented. | Pending, wait for missing functions completed | No change | Fixed by queries.py completed, tests passed in f9739fce2046cd0a4a9ca5fd9dc1897521cdada9 |

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: (Hassan) Context: `project/smartcare/queries.py` (`select_appointments`), `project/smartcare/domain.py` (unchanged contracts), `project/tests/test_queries.py` and the passing test result. Prompt: the Stage 9 handout reviewer prompt, unchanged.
Actual response: <!-- accessible reference -->

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: (Hassan, query part) The pure query only selects and orders the list it is given. It does not validate, store, print or change anything, so domain rules stay in the domain classes, collections stay in the data store, validation stays in the service, and interaction stays in the console. <!-- others: response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? (Trung)
Where validation lives. The pure query cannot tell an unknown practitioner from a registered one with no appointments, because both give `[]`. If validation were left out, `'D9'` would quietly return an empty list. So the service must check registration and status type first, then pass the registered ID to the query. This keeps the query pure while still giving the user the right error.
2. Which Copilot suggestion did you reject as over-engineering, and why? (Trung)
Any suggestion that added hidden state, validation, or printing into select_appointments. That would make the query depend on external state and violate purity, reuse, and the stage contract.
3. How did you prove cancelled appointments remain retrievable and listable in the same session? (Trung)
After cancellation, the same appointment object is still found by ID and keeps status == CANCELLED.
Listing without a status filter still includes it.
Listing with SCHEDULED only excludes it.
This proves it was retained, not deleted, while still no longer blocking a slot.

## G. Ten formative answers (Hassan)

1. What makes select_appointments pure, and what side effect breaks purity? 
- `select_appointments` uses only its arguments, builds and returns its own new list, and has no hidden state or input/output, so the same inputs always give the same result. Calling `appointments.sort()` on the argument, changing an appointment's status, printing, reading input or reading a global store would break purity.
2. Which explicit inputs are needed, and why avoid a global store? 
- It needs the appointment list, the practitioner ID and the optional status. A global store would hide a dependency, make the result depend on whatever happens to be stored, and make tests share state.
3. How can a new list reuse Appointment objects safely? 
- The query only reads the objects and puts references to them in its own list. Because it never changes them, sharing is safe and keeps object identity, so later changes such as a cancellation stay visible.
4. Why use a named key, and what breaks equal-time ties? 
- A named key can be tested on its own, reused with `sorted()` and checked in tests. The key `(date_time, appointment_id)` breaks equal-time ties by appointment ID, so A1, A2 and A4 at 09:00 always appear in that order.
5. How do default and explicit status filters differ? 
- The default `None` keeps every status, including CANCELLED and COMPLETED. An explicit `AppointmentStatus` keeps only appointments with exactly that status.
6. How do empty, unknown practitioner and invalid filter cases differ? 
- Empty means a registered practitioner with nothing matching, which returns `[]`. Unknown means a valid ID that is not registered, which raises `LookupError`. Invalid means a blank ID or a status that is not the enum, which raises `ValueError`, so a bad filter is never mistaken for "no results".
7. Which console errors recover, and how is unchanged state checked? 
- Unknown menu choices and every `ValueError`/`LookupError` recover: blank, unknown or duplicate IDs, unknown participants, malformed or impossible dates, conflicts, repeated cancellation and invalid status. Unchanged state is checked by recording the stored objects and fields before the failed action, comparing them afterwards, and then completing a successful action.
8. What is data integrity for registered participants, conflicts and history? 
- Appointments link only to the actual registered patient and practitioner objects. A practitioner never has two SCHEDULED appointments at the same time. Duplicate IDs are rejected, failed operations leave records unchanged, and cancelled appointments are kept, not deleted.
9. What is Copilot's review role, and who verifies findings? 
- Copilot acts as a reviewer that suggests possible issues from the supplied code and tests. The team decides whether each finding is correct, checks it against the code, tests and requirements, and records the decision and the actual verification.
10. How do pure functions and OOP responsibilities work together? 
- Objects keep their own rules (validation, the cancellation guard and store integrity), services coordinate them, and pure functions process the lists the services give them. The console only collects input and shows output, so interaction never controls a domain rule.

## H. Review, completion and common handover

Issues and bounded branches:
- stage09/servicelisting (Sophie)
- stage09/console (Sophie)
- stage09-1 (Hassan)
- stage09/Trung (Trung)
PR/diff and another-member human reviewer: 
- https://github.com/sophie-uni/st1-assignment3-Wed3/pull/42
- https://github.com/sophie-uni/st1-assignment3-Wed3/pull/43
- https://github.com/sophie-uni/st1-assignment3-Wed3/pull/44
- https://github.com/sophie-uni/st1-assignment3-Wed3/pull/45
Review responses and Copilot comparison: Not available
Integrated common Stage 9 SHA: ced2f62b415ca3e98764835214380c6081841f4f
Full regression command, working directory, actual count/result and evidence: 
- regression command: 'python -m pytest tests/test_queries.py', 'python -m pytest tests/test_workflows.py', 'python -m pytest tests/test_services.py'
- working directory: project\tests\
- tests\test_queries.py: 15 passed in 0.08s
- tests\test_workflows.py: 2 passed in 0.08s
- tests\test_services.py: 27 passed in 0.10s
README run instructions and scope/limitations: 'python main.py --interactive'
Unresolved issues and support/action: Not available
UG common candidate / PG future branch plan: -> stage10 -> stage11

- [✔] Query contracts, purity, new lists and named-key ordering verified.
- [✔] Service empty/unknown/invalid cases and cancellation history verified.
- [✔] Every console command and invalid-input recovery demonstrated.
- [✔] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [✔] Human design, Copilot critique, review and integration recorded honestly.
- [✔] Reflections and ten formative responses completed.
- [✔] README updated; earlier code/tests/records preserved.
- [✔] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
