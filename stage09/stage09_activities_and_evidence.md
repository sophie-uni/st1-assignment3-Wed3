# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Wednesday 14:30-16:30 Group 3 (st1-assignment3-Wed3)
Members and responsibilities: Sophie Jiang (Team leader), Hassan Ahmad (Team member), Trung Hieu (Team member)
Stage 8 integrated SHA, command, working directory and actual result: 399e222d74dd50010addc29b244f48380a233fae, https://github.com/sophie-uni/st1-assignment3-Wed3/pull/41

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason | Who |
|---|---|---| ---|
| Patient identity | Domain state | Patient details are persistent data that must be stored and available across multiple visits and sessions. | Sophie |
| Appointment history | Domain state | Appointment records are part of the patient's long-term medical and administrative history and need to be retained for future reference, reporting, and continuity of care. | Sophie |
| Temporary menu choice | | | Hassan |
| Practitioner specialty | | | Hassan |
| Debug print output | | | Trung |
| Appointment status | | | Trung |

What is intentionally lost on exit? (Hassan) <!-- response -->

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint | Who |
|---|---|---|---|---|---|
| appointment_sort_key | | | | | Trung |
| select_appointments | | | | | Hassan |
| Service listing (select_appointments) | practitioner_id: str |  appointments: list[Appointment] | Retrieves all appointments associated with the practitioner_id. Validate that practitioner_id is not null, empty, and matches an existing practitioner record. | In data_strore, practitioner must exist and be active | Sophie |
| Console (run_menu)| User menu selection: str; user-entered data (patient ID, name, appointment ID, practitioner ID, date/time): str | Displayed menus, prompts, error messages, confirmation messages | Presents the application menu; collects and validates user input; calls domain/service functions such as register, find, book, cancel and list; handles expected input errors; and keeps the session running until exit is selected. Validate menu choices and ensure required fields are not empty before calling services. | Uses data maintained by the patient and appointment services. Must only accept valid menu options such as register, find, book, cancel, list and exit, also comply with business rules enforced by the domain layer. | Sophie |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: <!-- response -->

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason | Who |
|---|---|---|---|
| Appointment.cancel reads input | | | Trung |
| Service prints/reads the menu | | | Hassan |
| Query sorts its source in place | A query should not modify the data it receives. Calling appointments.sort changes the caller's list and creates an unintended side effect. | The query operation should work on a copy of the data and return the result. Queries are responsible for retrieving or filtering data, not mutating domain state. | Sophie |
| Store prints Appointment saved | The store is performing user interface work. Printing messages mixes persistence responsibilities with presentation responsibilities. | The store should save and return the Appointment object or a result value. The Console/UI layer is responsible for displaying messages such as "Appointment saved". This keeps persistence and presentation concerns separated. | Sophie |

### A4 Sorting comparison (Trung)

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: <!-- response -->

Score-example prediction and explanation of passing the named key: <!-- response -->

### A5 Exit question (Hassan)

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: <!-- response -->

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: <!-- response -->

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-04-1 Known practitioner with no appointments or no matching status | practitioner_id | find_appointment returns a empty list | New empty list; no error | T-QRY-04-1 |
| QRY-04-2 Valid unknown practitioner ID | practitioner_id | Validate practitioner existence in data store returns null | LookupError| T-QRY-04-2 |
| QRY-04-3 Blank or invalid ID | practitioner_id | Validate practitioner_id format, null or invalid | ValueError | T-QRY-04-3 |
| QRY-04-4 Known practitioner with a non-enum status such as 'scheduled' | practitioner_id | Validate status | ValueError; do not treat it as no matches | T-QRY-04-4 |
| QRY-04-5 Omitted status | practitioner_id | find_appointment returns a list of appointments | list appointments include every status and preserve history | T-QRY-04-5 |
| | | | | |
| | | | | |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: <!-- response -->

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
|T-QRY-04-1 | In test_services.py test_known_practitioner_with_no_matching_appointments() | Existing practitioner with no appointments. Assert result == [] | | |
|T-QRY-04-2 | In test_services.py test_unknown_practitioner() | Unknown practitioner ID. Assert LookupError is raised. | Pass | |
|T-QRY-04-3 | In test_services.py test_invalid_practitioner_id(practitioner_id) | Blank, whitespace, or None ID. Assert ValueError is raised. | Pass | |
|T-QRY-04-4 | In test_services.py test_non_enum_status() | Status supplied as "scheduled" string. Assert ValueError is raised. | Pass | |
|T-QRY-04-5 | In test_services.py test_omitted_status_returns_all() | Status omitted. Assert scheduled and cancelled appointments are both returned. | | |
| | | | | |

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
| UI-01 full menu workflow | | | | |
| UI-02 invalid-input recovery | | | | |
| Automated service workflow | | | | |

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

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| F-1 | test_known_practitioner_with_no_matching_appointments, test_omitted_status_returns_all | The intended helper is select_appointments in queries.py, but that helper—and its sort-key function—are still unimplemented. | Pending, wait for missing functions completed | No change | |
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers (Hassan)

1. What makes select_appointments pure, and what side effect breaks purity? <!-- response -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- response -->
3. How can a new list reuse Appointment objects safely? <!-- response -->
4. Why use a named key, and what breaks equal-time ties? <!-- response -->
5. How do default and explicit status filters differ? <!-- response -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- response -->
7. Which console errors recover, and how is unchanged state checked? <!-- response -->
8. What is data integrity for registered participants, conflicts and history? <!-- response -->
9. What is Copilot's review role, and who verifies findings? <!-- response -->
10. How do pure functions and OOP responsibilities work together? <!-- response -->

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
