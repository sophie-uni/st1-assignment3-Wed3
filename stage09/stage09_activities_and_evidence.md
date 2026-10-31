# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: <!-- complete -->
Members and responsibilities: <!-- complete -->
Stage 8 integrated SHA, command, working directory and actual result: <!-- complete -->

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason | Who |
|---|---|---| ---|
| Patient identity | | | Sophie |
| Appointment history | | | Sophie |
| Temporary menu choice | Transient interaction state | It only decides which service call runs on that pass of the menu loop and means nothing once the command finishes. | Hassan |
| Practitioner specialty | Required session/domain state | A validated `Practitioner` field set at registration and shown whenever the practitioner or their appointments are displayed. | Hassan |
| Debug print output | | | Trung |
| Appointment status | | | Trung |

What is intentionally lost on exit? (Hassan) Every patient, practitioner and appointment, including cancelled history. All records live in one in-memory `SmartCareDataStore` created when the program starts, so a new launch begins empty. Restart persistence (FR-10) is retired, so this is the declared scope rather than a defect.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint | Who |
|---|---|---|---|---|---|
| appointment_sort_key | | | | | Trung |
| select_appointments | `appointments: list[Appointment]`, `practitioner_id: str`, `status: AppointmentStatus \| None = None` | A new `list[Appointment]` containing the same objects, ordered by `appointment_sort_key` | Selects the given practitioner's appointments and, if a status is given, only that status; `None` keeps every status. Does no validation (registration and status type are checked by the service), never changes the source list or objects, and performs no input/output. | `appointment.practitioner.practitioner_id` from the actual linked `Practitioner`; `appointment.status` enum; ordering uses `date_time` and `appointment_id` | Hassan |
| Service listing | | | | | Sophie |
| Console | | | | | Sophie |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: (Hassan) `Patient(patient_id, name)` and `Practitioner(practitioner_id, name, specialty)` trim and require every field, their IDs are read-only properties, and the store rejects duplicate IDs. `Appointment` holds the actual registered `Patient` and `Practitioner` objects (the store checks this with `is`), a validated naive minute-precision `date_time`, and an `AppointmentStatus` that only `cancel()` changes. `select_appointments` filters on the linked practitioner's `practitioner_id` and on the `status` enum, and orders on `date_time` then `appointment_id`. It reads these existing fields only and adds none. Names and specialty are not used by the query; the console reads them from the same linked objects when displaying results.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason | Who |
|---|---|---|---|
| Appointment.cancel reads input | | | Trung |
| Service prints/reads the menu | The service would own input and presentation, so it could not be reused or tested without a keyboard, and the caller could not decide how to handle errors. | The console owns the menu loop, prompts and messages. The service only coordinates the store and domain objects, returning objects or raising `ValueError`/`LookupError` for the console to report. | Hassan |
| Query sorts its source in place | | | Sophie |
| Store prints Appointment saved | | | Sophie |

### A4 Sorting comparison (Trung)

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: <!-- response -->

Score-example prediction and explanation of passing the named key: <!-- response -->

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

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: <!-- response -->

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| T-QRY01-1, 2 (Hassan) | `project/smartcare/queries.py` `select_appointments` | D1 query returns only `A9, A1, A2, A4, A3`; D2 control returns `B1, B2`; an unregistered ID returns `[]` | Passed | [test_queries.py](../project/tests/test_queries.py) |
| T-QRY02-1 to 3 (Hassan) | same | Default includes all three statuses; each status keeps only itself; D2 with COMPLETED returns `[]` | Passed | same |
| T-QRY03-1, 2 (Hassan) | same | Equal 09:00 times ordered `A1, A2, A4`; A9 first by date; source order and fields unchanged | Passed | same |
| T-FP01-1, 2 (Hassan) | same | Three calls give identical results in different lists; no printing or input | Passed | same |
| T-FP02-1 to 3 (Hassan) | same | Empty and already-sorted inputs return a new list; results are the same unchanged objects | Passed | same |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: (Hassan) `select_appointments` reads only its three parameters. It creates a local list, appends matching appointments to it, and returns `sorted(...)` of that local list. There is no module-level state, no `global`, no store or service import, no `print`, `input` or file access, no `sort()` call on the argument, and no call that changes an appointment (such as `cancel()`). The only other name it uses is `appointment_sort_key`, which is also side-effect free.

What the tests do and do not establish: (Hassan) For the chosen fixtures, the tests show correct practitioner isolation, every status filter including the default, date-then-ID ordering with an equal-time tie, a new list on every call (including empty and already-sorted inputs), unchanged source order and fields, repeatable results, and no console input/output. They cannot prove purity for every possible input; that rests on the code inspection above. They do not test performance on large lists or service-level validation. IDs are compared as text, so `A10` sorts before `A2` at equal times; this is a known limitation, not tested as desired behaviour.

## D. Integrated console and workflow evidence (Sophie)

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | | | | |
| UI-02 invalid-input recovery | | | | |
| Automated service workflow | | | | |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: (Hassan) Context: `project/smartcare/queries.py` (`select_appointments`), `project/smartcare/domain.py` (unchanged contracts), `project/tests/test_queries.py` and the passing test result. Prompt: the Stage 9 handout reviewer prompt, unchanged.
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: (Hassan, query part) The pure query only selects and orders the list it is given. It does not validate, store, print or change anything, so domain rules stay in the domain classes, collections stay in the data store, validation stays in the service, and interaction stays in the console. <!-- others: response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? (Hassan) Where validation lives. The pure query cannot tell an unknown practitioner from a registered one with no appointments, because both give `[]`. If validation were left out, `'D9'` would quietly return an empty list. So the service must check registration and status type first, then pass the registered ID to the query. This keeps the query pure while still giving the user the right error.
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

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
