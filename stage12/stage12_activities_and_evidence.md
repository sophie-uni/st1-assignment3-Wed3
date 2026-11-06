# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Wednesday 14:30-16:30 Group 3 (st1-assignment3-Wed3)

Members and UG/PG applicability: Sophie Jiang (PG), Hassan Ahmad (UG), Trung Hieu (UG)


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare A3 2026 revision 2. Python 3.13 and pytest 8.3.5 verified.
Common starting SHA / branch / applicable members: Stage 9 common SHA `638df5d27c599c1566e5087581baf8269051c42d`
PG starting SHA / branch / applicable members or not applicable: PG adds branch 'Stage10' and 'Stage11', SHAs `95c518c577fc2db8fad5a5b99e00483b7d44f04e` and `eb7b155b126bac16e447530940bee3b54ae9c685`
Working-state review and approved integration: Stage 12 has only 'stage12_activities_and_evidence.md' changes
Protected common candidate and PG differences: Protected Stage 9 common SHA is `638df5d27c599c1566e5087581baf8269051c42`. PG adds Stage 10 rescheduling and Stage 11 assurance work.
Feature freeze / owner / verifier: Freeze optional feature work. Sophie Jiang is release owner. Hassan and Trung reviewed.


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: 
- run `python -m pytest`, 89 passed in 0.26s 

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Reviewer | Sufficient? | Gap/action | Who |
|---|---|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---|---|---|---|
| Cancellation history works | `Appointment.cancel()` changes a scheduled appointment to cancelled and rejects a repeated cancellation. Tests check that the same cancelled object remains retrievable and in the store, and that repeated cancellation raises an error. | smartcare/domain.py; smartcare/data_store.py; smartcare/services.py; tests/test_domain.py (T-FR07-1, T-FR07-2); tests/test_services.py; tests/test_regressions.py.: https://github.com/sophie-uni/st1-assignment3-Wed3/pull/53 (b4e81957e152086b364642943f267c77042e3b8d) | Trung; second reviewer Hassan | Partial: the supplied code and test assertions support the claim, but execution on the final candidate is not evidenced. | Run focused cancellation/history tests and the full applicable suite at the release SHA; record the actual output. Confirm the test files and collected cases at that SHA. | Trung |
| Architecture responsibilities are appropriate | Responsibilities are separated across domain objects and status transitions, the session data store, service workflows, pure appointment queries, and console interaction. | smartcare/domain.py, data_store.py, services.py, queries.py, console.py, main.py.:https://github.com/sophie-uni/st1-assignment3-Wed3/pull/53 (b4e81957e152086b364642943f267c77042e3b8d) | Trung; second reviewer Hassan | Partial: separation is apparent from source inspection; independent review and final-candidate verification are not evidenced. | Review the integrated diff and confirm the boundaries. Resolve stale “incomplete menu” comments/docstrings in console.py and main.py if they no longer describe the current implementation; record the review outcome. | Trung |
| Rescheduling is safe — PG only | Stage 10 records that rescheduling preserves appointment identity and participants, changes the time only for eligible scheduled appointments, and rejects invalid, terminal-state, and conflicting changes. Focused 24, common 62, and full 86 tests passed. | https://github.com/sophie-uni/st1-assignment3-Wed3/pull/48, SHA `95c518c577fc2db8fad5a5b99e00483b7d44f04e`                                                                                                                                                                                                                                                                                                                                                                            | Sophie Jiang; no other PG reviewer | Partial: behavior and test evidence are recorded, but independent review was not applicable. | Obtain independent review. Scope remains synthetic and in-memory. This is not clinical or concurrency assurance.  | Sophie |
| AI use is responsible — common recheck / PG assurance | Stage 11 records the identifier-echo correction and assurance tests; 3 assurance tests, 86 previous-PG tests, 62 common tests, and 89 cumulative tests passed. | https://github.com/sophie-uni/st1-assignment3-Wed3/pull/51, SHA `eb7b155b126bac16e447530940bee3b54ae9c685`                                                                                                                                                                                                                                                                                                                                                                            | Sophie Jiang; no other PG reviewer | Partial: only tests and correction are documented | Confirm the approved AI-use route and dependency provenance; record any missing prompt/version provenance and an independent review. | Sophie |
| System is maintainable | Layered package with one responsibility per module (domain, data_store, services, queries, console); 93 automated tests after correction; code review in E found two missing docstrings, seven stale ones, small layout issues and seven test cases that never ran. Behaviour-preserving corrections made and the full suite rerun. | [project/smartcare](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/smartcare), [project/tests](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/tests) at 53a31b5; corrections on branch `stage12/hassan-review` on base 53a31b5 (commit SHA: [record after push]); E and H of this record                                                                                                                                            | Hassan (review); Trung for commented-out code; Sophie for merge | Partly. Sufficient for a course release once the corrections are merged. Maintainability is a review judgement; passing tests do not prove it. | Merge H-1 and H-3 corrections. Trung to decide on remaining commented-out code (`data_store.find_appointment`, `services.py` `#raise` lines, `#Stage10`/`#stage 10` markers) and the unreachable `except NotImplementedError` in `main.py`. | Hassan |
| FR-01–03 register/find and validation | T-FR01-1 `test_register_patient_stores_valid_patient` (AC-01.1), T-FR01-2 `test_register_patient_rejects_duplicate_id` (AC-01.2), `test_blank_patient_id_rejected_by_service`, `test_find_patient_returns_registered_patient` and `test_find_patient_raises_for_unknown_id` (FR-02), `test_find_practitioner_returns_registered_practitioner`, `test_find_practitioner_raises_for_unknown_id`, `test_duplicate_patient_preserves_original`, `test_duplicate_practitioner_preserves_original`, `test_required_fields` (FR-03). Focused run: 10 passed. Console path covered by UI-02 and the D demonstration. | [test_services.py](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/tests/test_services.py), [test_starter.py](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/tests/test_starter.py) at 53a31b5                                                                                                                                                                                                                                       | Hassan; second reviewer Trung | Yes. Assertions check the stored object identity (`is`), `LookupError` for unknown IDs, `ValueError` for blank or duplicate IDs, and that a rejected duplicate leaves the original record unchanged. | No gap for the revision 2 scope. Search by patient name (raised in the Stage 6 user story) is not a revision 2 requirement, so it is out of scope, not a defect. | Hassan |
| FR-04–05 booking/conflict rules | T-FR04-D1 `test_new_appointment_starts_scheduled`, T-FR04-D2 `test_appointment_rejects_time_not_local_minute_precision` (4 cases), `test_new_appointment_starts_scheduled_by_service`, `test_registration_and_booking`, `test_duplicate_appointment_preserves_original`, `test_unregistered_participants_rejected`; T-FR05-1 (AC-04.1), T-FR05-2 (AC-04.2), T-FR05-3 (one minute either side allowed), T-FR05-4 (cancelled slot free) and their copies in `test_regressions.py`. Focused run after correction: 23 passed. | [test_domain.py](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/tests/test_domain.py), [test_services.py](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/tests/test_services.py), [test_regressions.py](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/tests/test_regressions.py) at 53a31b5; T-FR04-D tests running only on branch `stage12/hassan-review` on base 53a31b5 (commit SHA: [record after push]) | Hassan (author of T-FR04-D and T-FR05 tests); independent reviewer Sophie | Yes after correction. Before it, T-FR04-D1/D2 were recorded as passing in Stage 7 but were never collected, and on the common candidate 5907afa removing the minute-precision check still left all 62 tests green. | Fixed by H-1: the same mutation now fails two T-FR04-D2 cases. Merge H-1 into both the common and integrated candidates. Stage 7 text is kept as history and corrected by this record. | Hassan |
| FR-06–08 cancellation/history/find | Service and regression tests cover cancellation, retained lookup/history, unknown appointment cancellation, and repeated-cancellation rejection. `find_appointment` returns stored appointments rather than removing cancelled ones. | smartcare/data_store.py, services.py, domain.py; tests/test_services.py; tests/test_regressions.py; tests/test_domain.py.:https://github.com/sophie-uni/st1-assignment3-Wed3/pull/53 (b4e81957e152086b364642943f267c77042e3b8d)                                                                                                                                                                                                                                                                                                 | Trung; second reviewer Hassan | Partial: implementation and relevant assertions were supplied, but final-SHA test results are missing. Some additional test functions in the supplied test files are nested inside other tests and may not be collected independently. | Verify pytest collection; run the focused FR-06–08 checks and full suite against the release SHA. Record any test-collection correction and rerun results without removing earlier valid assertions. | Trung |
| FR-09 and QRY/FP listing/filter/order/purity | Stage 9 records QRY-01–04 and FP-01–03 checks for practitioner/status filtering, deterministic ordering, empty and unknown cases, fresh result lists, and input/object non-mutation. Stage 11 records a 62-test common recheck. | 'stage09_activities_and_evidence.md', SHA `ced2f62b415ca3e98764835214380c6081841f4f`                                                                                                                                                                                                                                                                                                                                                                                                  | Sophie Jiang | Partial: prior coverage is documented, but this Stage 12 row has no final test results yet. | Run and link the common suite against the release SHA in this stage 12 | Sophie |
| UI full console sequence and error recovery | The Stage 12 demonstration records registration/find, booking, invalid date, conflict, cancellation, repeated/unknown/blank cancellation, recovery, and exit. It links automated workflow tests UI-01/UI-02. | `stage12_activities_and_evidence.md`                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Sophie Jiang | [response] | [response] | Sophie |
| Session-only scope / FR-10 retired | `SmartCareDataStore` holds three dictionaries only; a search of `main.py` and `smartcare/` finds no `sqlite`, `open(`, `json`, `pickle`, `csv`, `os` or ABC use. The demo prints "Session-only data: records are lost on exit." and menu exit prints "Exiting. Session-only data will be lost." A new process started after registering P1 reports "Patient not found" for P1. | [data_store.py](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/smartcare/data_store.py), [console.py](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/smartcare/console.py), [project/README.md](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/README.md) at 53a31b5                                                                                                                                       | Hassan; second reviewer Trung | Yes. The behaviour and the README both state the session-only scope, so lost data on exit is the declared scope, not a defect. | No code change. The `project/README.md` heading still reads "SmartCare Stage 6 starter"; the README owner should update the title and add the release label. | Hassan |
| PG RES and assurance integration | Stage 11 records 3 assurance tests, the PG selection, common selection, and full suite passing (89 total) on its tested SHA; Stage 10 records the rescheduling integration. | `https://github.com/sophie-uni/st1-assignment3-Wed3/pull/48`, `https://github.com/sophie-uni/st1-assignment3-Wed3/pull/51`, SHA `eb7b155b126bac16e447530940bee3b54ae9c685`                                                                                                                                                                                                                                                                                                            | Sophie Jiang; no other PG reviewer | Yes: integration and tests are recorded for that SHA. | No more action required. | Sophie|


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link | Who | 
|---|---|---|---|---|---|---|
| Complete common | Python 3.13.18, pytest 8.3.5 from the pinned `requirements-dev.txt`, new virtual environment, fresh clone (Windows) | From project/: python -m pytest -q |  branch stage12/TrungReviews | Reported: 89 passed in 0.26s. Confirm this was the complete common suite on the same release candidate before treating it as final regression evidence. | PyCharm/pytest output: e4ac5bd8daa1c46dac88f18d6cdbc980b4c3bc42  | Trung |
| Complete PG if applicable | Python 3.13.18, pytest 8.3.5 | From project/: python -m pytest -q | `eb7b155b126bac16e447530940bee3b54ae9c685` | 89 passed; Stage 11 records 3 assurance, 86 previous-PG, and 62 common tests passing. | Stage 11 test record | Sophie |
| Affected focused checks after correction | Python 3.13.18, pytest 8.3.5 from the pinned `requirements-dev.txt`, new virtual environment, fresh clone (Linux) | `cd project`; `python -m pytest -q tests/test_domain.py tests/test_workflows.py tests/test_services.py`; then `python -m pytest -q` | Before: 53a31b5fc3aaeb4e3d0ac62bc675fab77523b119. After: branch `stage12/hassan-review` on base 53a31b5 (commit SHA: [record after push]) | Before: full suite 1 failed, 85 passed (`test_menu_recovers_from_invalid_input_without_losing_session`); `test_domain.py` collected 2 tests. After: focused 38 passed (`test_domain.py` collects 9); full suite 93 passed, 0 failed. Mutation check (remove the seconds/microsecond rule): two T-FR04-D2 cases now fail. | H-1, H-2 and H-3 below; PR link: [add after push] | Hassan |
| Full integrated recheck | Python 3.13.18, pytest 8.3.5 | From project/: python -m pytest -q | [response] | [response] | [response] | Sophie |

- Prior assertions preserved / reviewed test diff (Hassan): The only test file changed is `tests/test_domain.py`. `git diff -w` shows 4 insertions and 2 deletions, all blank lines: every `assert`, parametrised value and docstring is unchanged. The four nested test functions and their helper were moved to module level so pytest collects them; collected tests rose from 86 to 93 (1 + 4 parametrised + 1 + 1). No test was deleted, weakened or rewritten. The workflow failure (H-2) was corrected in `services.py`, not by editing the assertion, so `test_workflows.py` is unchanged. All other test files are unchanged (`git diff --stat`). 
- Remaining failure / limitation (Trung): The supplied implementation uses in-memory session data, so records are lost when the process exits. The final README/release notes should disclose this limitation. Also check pytest’s collected-test count: in the supplied test files, some tests appear nested inside other test functions and may not be collected as standalone tests.


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link | Who |
|---|---|---|---|---|---|
| Problem and stakeholders | None; spoken introduction before the menu run | Explain the problem and clinic-side stakeholders within the declared scope | Explained: a small clinic's front desk needs to register patients and practitioners, book appointments without double-booking a practitioner, cancel without losing history and list a practitioner's appointments, for one session. Stakeholders: reception staff (direct users), practitioners (schedules protected), clinic manager (reliable records and history), patients (affected indirectly; no portal), teaching team (release reviewers). No production or clinical claim made. | [project/README.md](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/README.md) | Hassan |
| Register and find Patient and two Practitioners | Fresh process `python main.py --interactive`: 1 → blank ID, "Blank Example"; 1 → P1, "Alex Example"; 3 → P1; 3 → P9; 2 → D1, "Taylor Example", "General practice"; 2 → D2, "Jordan Example", "Physiotherapy"; 4 → D1; 4 → D2 | FR-01–03, UI-02: blank ID rejected; registered objects found; unknown ID reported and the menu continues | "Error: Patient ID cannot be blank"; "Registered patient P1."; "P1: Alex Example"; "Error: Patient not found", then the menu reappears; "Registered practitioner D1." and "D2."; "D1: Taylor Example, General practice"; "D2: Jordan Example, Physiotherapy" | Run on corrected working tree, 5 Nov 2026; automated equivalent `tests/test_workflows.py` (UI-01, UI-02) | Hassan |
| Valid booking | 5 → A1, P1, D1, "2026-12-01 09:00"; then 5 → A9, P1, D1, "2026-13-01 09:00" and 6 → A9 | FR-04: SCHEDULED appointment linked to the registered P1 and D1; failed input creates no record | "Booked A1: P1 with D1, 2026-12-01 09:00, scheduled". Invalid month gives "Error: Invalid calendar date/time; use YYYY-MM-DD HH:MM" and A9 then reports "Appointment not found", so no partial appointment was created. | Same run; `test_new_appointment_starts_scheduled_by_service` | Hassan |
| Same practitioner exact-time conflict rejected | 5 → A2, P1, D1, "2026-12-01 09:00"; then 6 → A2 | FR-05 / AC-04.1: rejected with no stored record | "Error: Practitioner already has a SCHEDULED appointment at this time"; finding A2 gives "Error: Appointment not found"; A1 is still scheduled | Same run; T-FR05-1 asserts `find_appointment('A2') is None` and the store still holds only A1 ([test_services.py](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/tests/test_services.py)) | Hassan |
| Different practitioner same time allowed | 5 → A3, P1, D2, "2026-12-01 09:00" | FR-05 / AC-04.2: a different practitioner at the same time is accepted | "Booked A3: P1 with D2, 2026-12-01 09:00, scheduled". The same patient now has two appointments at one time; revision 2 has no patient-conflict rule, so this is a declared limitation. | Same run; T-FR05-2 | Hassan |
| Cancel SCHEDULED and retain/find CANCELLED object | 7 → A1; 6 → A1; 8 → D1, blank status | FR-06, FR-07, FR-08: status becomes CANCELLED; same appointment still found and listed | "Cancelled A1: P1 with D1, 2026-12-01 09:00, cancelled"; find returns "A1: P1 with D1, 2026-12-01 09:00, cancelled" with the same ID, participants and time; default listing for D1 still shows A1 as cancelled | Same run; T-FR06-1, T-FR07-1 | Hassan |
| Invalid/repeated cancellation rejected | 7 → A1 (again); 7 → A404; 7 → blank ID; then 9 | AC-05.3: repeated cancellation rejected; unknown ID `LookupError`; blank ID `ValueError`; state unchanged and normal exit | "Error: Only SCHEDULED appointments may be cancelled"; "Error: Appointment not found"; "Error: Appointment ID cannot be blank"; the menu continues each time; A1 stays cancelled; "Exiting. Session-only data will be lost." | Same run; T-FR06-2, T-FR06-3 | Hassan |
| Default all-status listing | `8`, `D1`, blank status | Default listing includes all states for the practitioner | Pass: scheduled/cancelled records are displayed when using blank status. | `smartcare/queries.py`, `services.py` | Trung |
| Explicit filtering / empty vs unknown / deterministic order | `8`, `D1`, `cancelled`; then `8`, `D1`, `unknown`; then empty list or no-match case from service | Filtering works, empty results are valid, and order is deterministic | Pass: results are ordered by date/time and appointment ID; unknown status and empty results are handled cleanly. | `smartcare/queries.py` (`select_appointments`) and `tests/test_queries.py` | Trung |
| Invalid date/status/menu lookup recovery and continued operation | Invalid menu choice; blank patient ID; invalid date; invalid status; invalid practitioner ID; missing patient/practitioner; repeated cancellation | Console recovers from expected input errors without losing session state | Pass: errors are printed, valid operations continue, and session state is preserved within the run. | `smartcare/console.py`, `tests/test_workflows.py` | Trung |
| Session-only limitation and normal exit | `9` to exit | Session data is lost on exit, as intended | Pass: exit message is shown and the session-only limitation is clearly communicated. | `smartcare/console.py`, `main.py` | Trung |
| One meaningful requirement-linked pytest explained | Code tests for FR-01 to FR-09 and QRY-01 to QRY-04, plus service and workflow tests | One requirement-linked test is mapped to an end-to-end demonstration and the actual logic it verifies | Pass: requirements are linked to the code and to the workflow scenario. | `tests/test_domain.py`, `tests/test_services.py`, `tests/test_queries.py`, `tests/test_workflows.py` | Trung |
| Architecture and one actual AI decision / known limitation | Source review of the architecture and the memory-only store | The final design is acceptable, and the limitation is disclosed as a real known constraint | Pass: in-memory session-only storage is a conscious design decision rather than an unacknowledged bug. | `smartcare/data_store.py`, `smartcare/console.py`, `main.py` | Trung |
| PG reschedule identity/participants/time and no-op | In-memory store; reschedule scheduled `A1` from 09:00 to 10:00, then request its existing time. | Return and retain the same appointment and participant objects; update only the time. A valid same-time request succeeds without changing state. | Tests passed | In `tests/test_rescheduling.py`: `test_service_moves_same_stored_object_and_listing_uses_new_time` and `test_same_time_noop_excludes_target_from_conflict_check` | Sophie |
| PG conflict/invalid status/failure non-mutation | Reschedule `A1` into a time already occupied by the same practitioner; try invalid datetime values and `CANCELLED`/`COMPLETED` targets. | Reject conflicts and invalid/terminal requests; preserve all stored appointments and fields after failure. | Tests passed | In `tests/test_rescheduling.py`: `test_same_practitioner_conflict_is_rejected_without_mutation`, `test_service_rejects_invalid_datetime_without_mutating_store` and `test_service_rejects_terminal_target_even_for_same_time`  | Sophie |
| PG old slot / current lookup/list ordering / assurance risks | Move `A1` from 09:00 to 10:00, book `A2` into the freed 09:00 slot, then list D1’s appointments; also test cancellation/history and a separate store with the same patient ID. | Old slot is reusable; lookup returns the same updated object; lists reflect current time order and are fresh; cancellation retains history; one store’s lookup does not leak another store’s records. | Tests passed | In `tests/test_rescheduling.py`: `test_successful_move_releases_old_slot`, In `tests/test_assurance.py`: `test_reschedule_cancel_history_and_listing_use_fresh_results`, `test_patient_lookup_is_limited_to_its_shared_store` and `test_unknown_practitioner_error_does_not_echo_input` | Sophie |

- Stable demo owner / fresh process / command: (Sophie)
  - Stable demo owner: Sophie Jiang
  - fresh process: from project/
  - command: python main.py --interactive
- PG demonstrations through service/tests or not applicable: (Sophie)
  - Rescheduling is service-level, not a console menu action; 
  - PG feature demo separately with command: python -m pytest -q tests/test_rescheduling.py tests/test_assurance.py tests/test_workflows.py

## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck | Who |
|---|---|---|---|---|
| OOP responsibilities and pure-query boundaries | `domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py` at 53a31b5 | No finding. Entities validate their own fields; `Appointment` owns status changes through `cancel()` and `reschedule()`; the store owns the three dictionaries and integrity checks; services coordinate lookup, domain call, conflict check and storage; only `console.py` reads input or prints. `queries.py` uses only its arguments and returns a new sorted list (no `print`, `input` or store access found). The conflict predicate sits in the store, as supplied, and is called only by services. | No change. Recheck: `tests/test_queries.py` 15 passed (QRY and FP purity tests). | Hassan |
| PascalCase and snake_case naming | All classes, functions and variables in `main.py` and `smartcare/` | No finding. Classes are PascalCase (`SmartCareDataStore`, `AppointmentService`, `AppointmentStatus`); functions, methods and variables are snake_case (`validate_date_time`, `has_practitioner_conflict`, `select_appointments`); enum members are upper case; private fields use a leading underscore behind read-only properties. | No change needed. | Hassan |
| Useful type hints and meaningful docstrings | `data_store.py` `find_appointment`, `has_practitioner_conflict`; `services.py` `PatientService.find_patient`, `cancel_appointment`, `list_practitioner_appointments`; `console.py` `run_menu`; `main.py`; `queries.py` module docstring | Every function has parameter and return hints. Two store methods lost their docstrings when Stage 8 fault-preparation commit b5a8a53 replaced their bodies; the old conflict docstring also said `exclude_appointment_id` "is ignored", which stopped being true when rescheduling used it. Five function docstrings and two module docstrings were stale starter text ("Stage 6 TODO … deliberately raises NotImplementedError", "Stage 9: implement …", "report the intentionally incomplete interactive menu") describing work that is now complete. | Corrected (H-3): restored accurate docstrings and rewrote stale ones to describe current behaviour; no code statement changed. Recheck: docstring scan reports none missing; full suite 93 passed on branch `stage12/hassan-review` on base 53a31b5 (commit SHA: [record after push]). | Hassan |
| Four-space indentation and imports/layout | `tests/test_domain.py`; `queries.py`, `main.py`, `services.py`, `console.py` (checked with pycodestyle 2.12.1 in the review environment only, not added to the project) | Four test functions (T-FR04-D1, T-FR04-D2, T-FR06-D1, T-FR06-D2) and their helper were indented inside another test since my Stage 7 commit 7431084, so pytest never ran them (H-1). Source layout: missing blank lines (E302 `queries.py`, E305 `main.py`), missing final newline (`queries.py`, `services.py`), two import lines from the same module in `console.py`, and a stray "# this is for test purpose only" comment left in `main.py` by my Git practice commit 762c162. | Corrected (H-1, H-3): tests moved to module level; blank lines, final newlines and the import fixed; stray comment removed. Recheck: no E302, E305 or W292 in source; full suite 93 passed. No change for five lines 1–4 characters over 79 (readable messages) or for blank-line warnings in other test files, to keep the test diff small during the freeze. E265/E115 comments are left to the dead/commented code review. | Hassan |
| Focused methods / duplication / dead or commented code | `smartcare/services.py`, `console.py`, `main.py`, `data_store.py`; `tests/test_domain.py`, `test_regressions.py`, `test_services.py` | **Finding:** stale commented-out `NotImplementedError` lines and TODO/starter wording remain in service and console code. `main.py` still describes an intentionally incomplete menu and catches `NotImplementedError`. There is commented-out code in `data_store.py`. Some tests are nested inside other test functions in `test_domain.py` and `test_regressions.py`, so pytest may not collect them as independent tests. `test_services.py` also defines `foundation()` more than once. | Review and remove obsolete comments/starter wording where appropriate; move intended tests to module level and resolve duplicate helpers without dropping assertions. Then check test collection and run the focused tests and full suite. **No correction or recheck is confirmed yet.** | Trung |
| Globals / leakage / unnecessary inheritance or frameworks | `smartcare/domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py`, `main.py` | **No significant finding in the supplied application code:** no unnecessary inheritance or framework use is visible. The `SmartCareDataStore` collections are instance state; `TIE_TIME` and `BOOKING_TIME`-style constants shown are test data. | No change indicated by the supplied files. Confirm during final diff review. | Trung |
| No SQLite/persistence/repository ABCs/speculative features | `smartcare/data_store.py`, `smartcare/console.py` | **No finding:** the app uses in-memory dictionaries and does not add SQLite or a speculative persistence/repository abstraction. This is intentionally session-only, so data is lost when the process exits. | No change. Ensure the README and release notes disclose the session-only limitation; this review does not verify those documents. | Trung |
| Synthetic data / secrets / dependencies / provenance | `smartcare/console.py`, `tests/test_*.py`; dependency manifest not supplied | **Partial finding:** the examples visible in the supplied code and tests use synthetic IDs/names, and no credentials or secrets are visible. Dependency provenance cannot be assessed because no dependency manifest or environment details were supplied. | Keep demo data synthetic. Review and record the actual dependency manifest, package sources/licences, and versions before sign-off. Don’t claim a dependency review until it has been performed. | Trung |
| Significant common Copilot contributions and human verification | `project/smartcare/queries.py`, `project/tests/test_queries.py`, `test_services.py`, and `test_workflows.py` | Copilot helped implement appointment filtering/order helpers after the human-defined QRY requirements and tests exposed missing functions. The record describes the query as pure; focused query, service, and workflow tests passed. | Implemented the helpers and connected the service; recorded results: queries 15 passed, workflows 2 passed, services 27 passed. | Sophie |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | `project/smartcare/domain.py`, `services.py`, and `tests/test_rescheduling.py` | Stage 10 records a bounded RES plan and inspected diff; its focused 24, common 62, and full 86 tests passed; Stage 11 VERIFY/TRUST records test and architecture checks and identifies an observed error-message data-minimisation issue. | Stage 11 changed the unknown-practitioner error to a generic message and added assertions; 3 assurance, 86 previous-PG, 62 common, and 89 cumulative tests passed on the recorded tested code. | Sophie |

Use actual prompt: Review Smartcare\ project

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| Medium | `project/tests/test_domain.py:74–132`, Several test functions are nested inside `test_repeated_cancellation_is_rejected_and_state_remains_cancelled` | Yes, the functions after `test_repeated_cancellation_is_rejected_and_state_remains_cancelled` position wrong, they should not belong to the function.| Accept | Move the nested tests to module scope, then rerun collection and the full suite. |
| Low | `project/main.py:11–23`; `project/README.md:1`, the interactive menu is incomplete and the project is a Stage 6 starter, although the menu is implemented. | Yes, information is missing | Accept | Update the descriptions to reflect the current project |

- Access route or approved equivalent / limitations: 
  - Reviewed `project/` at local HEAD `6e646c8315a4254f6880c59dcb65cea906d5056d`. 
  - The full suite passes (89 tests), but it misses domain tests that appear to be present in the file.
  - After move test functions in `tests/test_domain.py`, run python -m pytest, got result: 96 passed in 0.26s
- Available AI evidence and missing evidence honestly disclosed: 
  - Used Github Copilot in Pycharm as Agent mode to check


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | `project/README.md:15–19`, root `README.md:24–30` | Sophie Jiang | Purpose and common/PG stage scope are described. The project README title still calls this a “Stage 6 starter.” |
| Out-of-scope capabilities and known limitations | `project/README.md:15,19,21` | Sophie Jiang | States session-only synthetic data; no persistence, notifications, external calendar, patient-conflict, duration, or past-date rules. |
| Confirmed teaching Python version and dependency installation | `project/README.md:3,13`, `project/requirements-dev.txt` | Sophie Jiang | README specifies Python 3.13 / pytest 8.3.5 and the install command. Local environment is Python 3.13.15 and pytest 8.3.5. |
| Working directory / demo / interactive / test commands | `project/README.md:5–13`; commands run from `project/` | Sophie Jiang | `python main.py` ran and printed the demo booking. `python -m pytest` passed 96 tests. `python main.py --interactive` opened the menu and handled EOF, but the piped `9` smoke input was not accepted as a valid choice; workflow tests cover menu sequences. |
| Repository structure and architecture responsibilities | `project/README.md:17,19` | Sophie Jiang | Describes domain, store, services, and rescheduling but responsibilities for `queries.py`, `console.py`, and `main.py` are not fully explained. |
| Responsible AI summary / synthetic-data rule | Root `README.md:30,56`; `project/README.md:15` | Sophie Jiang | Synthetic-data rule and Copilot verification are mentioned in the root README. |
| Release label/version and SHA links | Root `README.md:11–14`; `project/README.md:1–3` | Sophie Jiang | [response] |

- Root README index and project/README verified: [response]
- Fresh clone or extracted ZIP / candidate identity: [response]
- Verifier and clean environment / actual version: [response]
- Setup/run/test commands and observed results: 
  - From `project/`, `python -m pytest --collect-only -q tests/test_domain.py` collected 9 tests.
  - `python -m pytest -q` passed 96.
  - `python main.py` ran successfully.
- Missing local file or setup gap / remedy and recheck: 
  - No required setup file was missing locally.
  - `requirements-dev.txt` exists and pins pytest 8.3.5.


## G Known limitations debt and release notes

- Delivered features: 
  - Common scope supports patient/practitioner registration and lookup, appointment booking with exact practitioner/time conflict checks, cancellation with retained history, appointment lookup, and practitioner listing/filtering. 
  - The PG extension adds service-level rescheduling.
- Important fixes:
  - Rescheduling preserves appointment and participant identity, rejects invalid or conflicting changes without mutation, and frees the previous slot. 
  - Removed caller-supplied practitioner IDs from unknown-practitioner errors. 
  - Moved previously nested domain tests to module scope.
- Architecture/quality improvements: 
  - Responsibilities are separated across domain entities, the in-memory store, services, pure appointment queries, and console interaction. 
  - Tests cover filtering, ordering, fresh result lists, rescheduling, store isolation, and combined workflows.
- Known limitations: 
  - Data is synthetic and session-only; there is no persistence, authentication, external calendar, or production/clinical certification. 
  - Times are local, naive, and minute-precision; duration, patient-conflict, past-date, and timezone rules are not implemented. 
  - Concurrency, operations/monitoring, and accessibility/usability are not established.
- AI-assisted development note: 
  - Copilot assisted with code and review suggestions. 
  - The record describes human checks against requirements and tests, including remediation of the error-message finding. 
  - Treat AI output as a suggestion, not approval.
  - Course AI-policy confirmation and some provenance evidence remain limitations.

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Session-only in-memory records | Data is lost when the process exits; unsuitable for durable records. | Low for the declared teaching scope; blocker for real deployment. | Add persistence only if future requirements require it, with privacy, access-control, and recovery design. | Accepted for the course scope; limitation is disclosed. |
| No explicit timezone, duration, patient-conflict, or past-date policy | Scheduling checks only the specified practitioner/exact-time rule. | Medium | Confirm requirements first; implement and test only approved rules. | Out of scope; no additional rule is assumed.|
| Release assurance/provenance follow-up | Course-policy approval, dependency provenance, and independent verification of the final application | High | Confirm policy/dependency details | Not a product feature |

- Session-only synthetic data and minute-precision local time: 
  - Deliberate scope limits; data disappears at exit and accepted times are naive local datetimes at minute precision.
- Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: 
  - Not included; do not use this coursework prototype for real patient or clinical workflows.
- Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: 
  - Not verified or specified; further requirements and evaluation would be needed before expanding beyond the teaching demonstration.
- Difference between accepted scope limit and unresolved required behaviour: 
  - The documented session-only and scheduling-policy exclusions are intentional scope limits.
- PG assurance residual risks / owner / status or not applicable: 
  - Sophie Jiang (PG owner) close the recorded assurance. 
  - The tests support the stated synthetic, in-memory behaviors but do not establish clinical/security certification.


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| H-1 (Hassan) FR-04 minute-precision contract; Stage 7 claim that T-FR04-D1/D2 and T-FR06-D1/D2 pass | `python -m pytest --collect-only -q tests/test_domain.py` at 53a31b5 collects 2 tests; the four functions are nested inside another test since 7431084. On common candidate 5907afa, removing the seconds/microsecond check in `validate_date_time` leaves all 62 tests green. | Medium. Product behaviour is correct, but release evidence was overstated and the common suite had no running test of the minute-precision rule. | Hassan: move the tests to module level (this also restores Devam's T-FR06-D tests) | `tests/test_domain.py`, indentation and blank lines only | `test_domain.py` 9 passed; the same mutation now fails two T-FR04-D2 cases; full suite 93 passed | Stage 7 text remains as history; this row records the correction |
| H-2 (found by Hassan) UI-02 error recovery and full regression | At 53a31b5 `python -m pytest -q` gives 1 failed, 85 passed. `test_menu_recovers_from_invalid_input_without_losing_session` expects "Practitioner with ID 'D999' not found."; Stage 10 commit 95c518c changed that `LookupError` text in `list_practitioner_appointments` to "Practitioner not found". b70a879: 86 passed; 95c518c: 1 failed. Common candidate 5907afa unaffected (62 passed). | High for the integrated candidate: the full suite is red. Still raises `LookupError`, so only the message changed. | Hassan proposed the fix; Sophie (Stage 10 owner) to review and approve | `services.py` `list_practitioner_appointments`: Stage 9 message restored; test assertion left unchanged | `test_workflows.py` 2 passed, `test_services.py` 27 passed; full suite 93 passed | No requirement fixes the wording; unifying messages later needs a reviewed test change, not a silent edit |
| H-3 (Hassan) Code quality: docstrings and layout | Missing or stale docstrings and layout issues listed in E | Low. No behaviour impact | Hassan | Docstrings, blank lines, one import and one stray comment in `data_store.py`, `services.py`, `console.py`, `queries.py`, `main.py` | Full suite 93 passed; `python main.py` and the menu sequence in D rerun with the same output | Commented-out code and the unreachable `except NotImplementedError` in `main.py` left for the dead-code review |
Justified no-change conclusion if no defect found: [response]
Release blockers still open / status: [response]


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: [response]
Independent reviewer / feedback / response: [response]
Integration commit / full recheck: [response]
Tracked and untracked file inspection / cleanliness: [response]
Secrets/staff material/caches/tool-metadata exclusion check: [response]
Candidate recovery plan / known-good SHA: [response]
Named substantive contributions: [response]


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: READY FOR COURSE RELEASE
Approver / date / rationale and evidence: [response]
What risks remain / conditions / owners:
Can the team explain the system: Yes
Can a change be recovered: [response]
Common decision / PG decision where different: [response]


## K Final tested release SHA

Exact common tested SHA: [response]
Exact PG tested SHA or not applicable: [response]
Final submitted SHA / repository URL: [response]
Evidence-only later commit and difference explanation: [response]
Executable changes after testing and re-verification: [response]
Source ZIP name / SHA correspondence / extracted comparison: [response]


## L Submission package verification

- [ ] Feature freeze and scoped requirements traced.
- [ ] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [ ] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: [response]
Deadline/timezone: [response]
Repository access arrangement: https://github.com/sophie-uni/st1-assignment3-Wed3
Mixed-candidate upload arrangement: [response]
Oral/video recording/accessibility arrangements: [response]
Remaining administration or release dependency: [response]


## M Formative questions

1. What is a release candidate? (Trung)
- A release candidate is an integrated version that is ready for final verification and a human release decision. It should be identified by its exact commit SHA so the tested code can be distinguished from later changes. It is not automatically approved or production-ready.

2. What is feature freeze and why is it used? (Trung)
- Feature freeze means stopping optional feature development while the team verifies the release scope, fixes genuine blockers, and prepares documentation. It reduces last-minute change risk and keeps testing focused on the candidate intended for release.

3. What is regression testing in a release context? (Trung)
- Regression testing reruns existing checks on the release candidate to see whether changes have broken required behaviour. For SmartCare, that includes registration and lookup, valid booking and conflict handling, cancellation and retained history, appointment listing, and console error recovery. Record the actual command, environment, SHA, and result; test files alone do not prove a run passed.

4. What is a known limitation? (Trung)
- A known limitation is a documented boundary of the current release, rather than a failure to meet a requirement within its declared scope. SmartCare uses in-memory session data, so records are lost when the process exits; it does not claim durable storage or production healthcare readiness.

5. What is technical debt?  (Trung)
- Technical debt is an acknowledged code or process compromise that makes future maintenance or change more costly and should be tracked with its impact and a future action. For example, in the supplied Python snapshot, obsolete starter comments and test functions nested inside other tests may create maintenance and test-discovery risk; verify these against the final candidate before recording them as release findings.

6. What are release notes? (Hassan) Release notes are a short, reader-facing summary published with one identified version. They say what that version delivers, which important defects were fixed, what changed in design or quality, what the known limitations are, and anything a user or maintainer must know, such as setup changes or how AI was used. They are tied to an exact SHA so a reader knows which code was tested, and they describe what was actually done rather than plans.

7. What is software maintenance? (Hassan) Software maintenance is the work of changing software after release so that it stays correct and useful: corrective changes fix defects, adaptive changes follow a new environment or rule, perfective changes improve maintainability or usability, and preventive changes reduce future risk, such as adding a missing test or paying down debt. Each change is reviewed, tested and released as a new identified version; it never silently replaces the version that was submitted. Release is the start of maintenance, not the end of the work.

8. What is the purpose of the individual demonstration/viva? (Hassan) It confirms that each member understands the system and their own contribution, not just that files were submitted. A member should be able to run it, explain the requirements, design, a meaningful test and its limits, a diagnosed defect and an actual AI decision in their own words, and reason about a small change. It authenticates individual understanding within the common team viva rather than creating a separate mark.

9. What should the final responsible-AI check establish before release? (Hassan) It should establish that every significant AI-assisted change is identified, understood and checked by a person against the requirements and tests, with an honest accept, modify or reject decision. It should also confirm that no unexplained change remains, that no real personal data or secret was used in prompts or committed, that no unknown or unnecessary dependency was added (the project pins only pytest), that missing evidence is disclosed rather than invented, and that a person, not the tool, makes the release decision.

10. What is the main course conclusion about AI and the role of the software engineer? (Hassan) AI can produce code, tests and review comments quickly, but its output is a candidate until a person verifies it, and it carries no responsibility for the result. The engineer still defines the requirements and acceptance criteria, designs responsibilities, judges AI output against evidence, tests, debugs, integrates and decides whether to release, and stays accountable. AI changes how much time goes into typing code; it increases, rather than removes, the need for specification, verification and judgement.


## N Reflection viva and handover

Strongest evidence SmartCare is ready: [response]
Weakest area: [response]
How AI use changed from Stage 1 to Stage 12: [response]
Start doing — engineering and AI use: [response]
Stop doing — engineering and AI use: [response]
Continue doing — engineering and AI use: [response]
What worked / caused rework / future delivery improvement: [response]
One paragraph — If AI can write code why do we still need software engineers: [response]

| Preparation item | Own explanation and evidence link | Who |
|---|---|---|
| Problem and stakeholders | SmartCare supports a small clinic's front desk for one session: register patients and practitioners, book appointments without double-booking a practitioner, cancel while keeping history, and list a practitioner's appointments. Reception staff use it directly; practitioners depend on their schedule being protected; the clinic manager needs reliable records; patients are affected indirectly and have no portal. It is a course release, not a production or clinical system. Evidence: [project/README.md](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/README.md), D demonstration. | Hassan |
| Two requirements and acceptance criteria | FR-05 Prevent practitioner conflict. AC-04.1: a booking for the same practitioner at exactly the same time as an existing SCHEDULED appointment is rejected with `ValueError` and nothing is stored. AC-04.2: a different practitioner at that time is allowed. Supporting contracts: a cancelled booking does not occupy the slot, and one minute either side is not a conflict. FR-01 Register patient. AC-01.1: valid data with an unused ID is stored and the same object is returned. AC-01.2: an existing ID is rejected and the original record is kept. Evidence: T-FR05-1 to T-FR05-4, T-FR01-1, T-FR01-2 in [test_services.py](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/tests/test_services.py). | Hassan |
| Domain model and architecture | `Patient` and `Practitioner` validate their fields and expose read-only IDs. `Appointment` links the actual registered participant objects, a local minute-precision `date_time` and an `AppointmentStatus` (SCHEDULED, CANCELLED, COMPLETED); only its guarded methods change state. `SmartCareDataStore` keeps three dictionaries keyed by ID and rejects duplicates and unregistered participants. Three services share one store and coordinate each use case. `queries.py` holds pure functions for selecting and ordering lists. `console.py` owns all input and output; `main.py` only starts the demo or menu. Flow: console → service → domain and store → query. Evidence: [project/smartcare](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/smartcare). | Hassan |
| Design trade-off | In Stage 9 I kept `select_appointments` free of validation: it filters and sorts only the list it receives. Benefit: it is pure, needs no store, and is easy to test with plain lists. Cost: it cannot tell an unknown practitioner from a registered one with no appointments (both give `[]`), so `AppointmentService.list_practitioner_appointments` must validate the ID and status first, and two places must stay consistent. I accepted that because the service already owns lookups through the store. Evidence: Stage 9 record B; [queries.py](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/smartcare/queries.py), [services.py](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/smartcare/services.py). | Hassan |
| Meaningful test and its limits / 100 percent coverage | T-FR05-1 `test_same_practitioner_same_time_is_rejected`: arrange a fresh store with P1, P2, D1 and D2 and book A1 for D1 at 09:00; act by booking A2 for D1 at 09:00; assert `ValueError`, `find_appointment('A2') is None`, the store still holds only A1, and A1 is still SCHEDULED. It is meaningful because it failed on the Stage 8 injected fault (b5a8a53) and passed after the repair (6f0f25d). Limits: one time and one store; it does not prove every time, concurrent use, the message text or the console path. 100% coverage only shows which lines ran, not that assertions check the requirement; my own T-FR04-D tests show that tests can exist in a file and still never run. Evidence: [test_services.py](https://github.com/sophie-uni/st1-assignment3-Wed3/blob/53a31b5/project/tests/test_services.py), H-1. | Hassan |
| Diagnosed defect and verification | Stage 8 fault F8-01 (issue 31, repaired by Sophie in 6f0f25d; my T-FR05-1 and T-FR05-2 were the failing evidence for issues 27 and 28). Symptom: a second D1 booking at the same time was accepted, while a D2 booking at that time was rejected. Cause: `has_practitioner_conflict` compared practitioner IDs with `!=` instead of `==`. Fix: that one operator. Verification: T-FR05-1/2 and their regression copies pass and the full suite stays green. My own Stage 12 diagnosis is H-1: `pytest --collect-only` showed only 2 domain tests, which led to the nested functions. Evidence: Stage 8 record C; H-1 above. | Hassan |
| Shared store and session-state/query responsibilities | The shared data store is responsible for data integrity, identity checks, and retrieval by ID. The query layer is responsible for selection, filtering, and ordering of a given list of appointments. The service layer coordinates these responsibilities without exposing internal mutation logic. Evidence: smartcare/data_store.py, smartcare/queries.py, smartcare/services.py. | Trung |
| What would break if session-state lookup/query responsibilities changed? | If session-state lookup and pure query responsibilities were conflated, the code would become harder to reason about and harder to test deterministically. Appointment selection should remain side-effect free; booking and cancellation should not be mixed into query functions. Evidence: smartcare/queries.py and the tests in test_queries.py. | Trung |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Cancellation changes the state of an Appointment and is therefore a domain responsibility, because it modifies the appointment’s status from SCHEDULED to CANCELLED under a guard rule. Conflict coordination (checking whether a practitioner is already booked at a time) is service-level policy because it evaluates the current store state and decides whether booking is allowed. Evidence: smartcare/domain.py and smartcare/services.py. | Trung |
| FR-07 retained history test | Cancellation changes the state of an Appointment and is therefore a domain responsibility, because it modifies the appointment’s status from SCHEDULED to CANCELLED under a guard rule. Conflict coordination (checking whether a practitioner is already booked at a time) is service-level policy because it evaluates the current store state and decides whether booking is allowed. Evidence: smartcare/domain.py and smartcare/services.py. | Trung |
| Actual AI change rejected/modified or honestly accepted with verification | The AI-generated changes were reviewed against the requirement contracts and the tests. Some changes (for example, the duplicate/lookup logic and the session-only limitation) were accepted only after validation. The final pass is honest and evidence-based: no change was accepted without checking the relevant tests. Evidence: tests/test_services.py, tests/test_queries.py, tests/test_workflows.py. | Trung |
| Unresolved limitation / future production work | The main unresolved limitation is that the application is intentionally in-memory and session-only. This is suitable for teaching and demonstration but not for real production deployment or durable patient records. Future work would include persistent storage, stronger validation, audit logging, and a production-grade user interface. Evidence: smartcare/data_store.py, smartcare/console.py, project/README.md. | Trung |
| Personal implementation contribution | Every stage, we have group Teams meeting to split tasks to group members then another group Teams meeting for finalise the stage. | Sophie, Hassan, Trung |
| Personal test/review/design/integration contribution | Each member has run own tests when impletement functions in each stage, response for PR to main. Sophie as repository owner, review and merge each PR. | Sophie, Hassan, Trung |
| PG agentic change and rescheduling verification | I scoped rescheduling to the RES requirements, then checked identity, participants, no-op, conflict, invalid status/time, non-mutation, old-slot reuse, and updated listing through focused tests. Stage 10 records 24 focused, 62 common, and 86 full tests passing on the working tree. | Sophie |
| PG responsible-AI risk/remediation or supported no finding | I verified that unknown-practitioner errors echoed caller-supplied IDs, replaced the message with a generic error, and added checks that the ID is not included in service or menu output. I also added isolation/interaction tests where no production defect was found. Evidence records synthetic data and remaining course-policy/provenance limitations. | Sophie |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: Not undertaken
Separate reflection / peer / common team viva evidence links and routing: In separate 'Assignment_3_Reflection_Report_and_Peer_Evaluation'
No further coding stage. Later corrections use the published assessment process.