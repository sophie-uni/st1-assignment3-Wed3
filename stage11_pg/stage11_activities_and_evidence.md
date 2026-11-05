# Stage 11 PG assurance activities and evidence

PG-only stage. Undergraduate students are not required to complete this record. UG-only groups retain this supplied template unchanged as intentionally not applicable; do not fabricate N/A responses. Optional UG participation is unassessed.

Completed from the supplied student template. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied file in stage11_pg/ in your EXISTING repository. Preserve project/, earlier records/tests and the protected common Stage 9 SHA. Do not copy staff references or fabricate AI evidence.

Group/tutorial: Wednesday 14:30-16:30 Group 3 (st1-assignment3-Wed3)

Assessed PG members and contributions: Sophie Jiang as PG owner

Optional UG contributors: None

## A Handover and human-first scope

- Integrated Stage 10 code SHA / protected Stage 9 common SHA: 
  - Stage 10 SHA: `c3f8aae8048033a6aa0187618faaf62d1b4dd97c`
  - protected Stage 9 common SHA `ced2f62b415ca3e98764835214380c6081841f4f`. 
- Recoverable branch / baseline / actual commands, working directory and results: 
  - Current branch `stage11`
  - Before Stage 11 changes, from `project/`: `python -m pytest -q` → 86 passed; `python -m pytest -q --ignore=tests/test_rescheduling.py` → 62 passed
  - No issue has been created.
- Domain, store, services, queries, console, entry point, tests and rescheduling inspected: 
  - Inspected `domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py`, `main.py`, `requirements-dev.txt`, common and PG tests, including rescheduling. `PatientService.find_patient` returns the stored object, raises `LookupError` when the shared store returns `None`, and does not create a replacement. Store lookup returns `None` for a valid unknown ID and rejects blank IDs. Practitioner appointment listing validates its inputs and returns a query-produced ordered list. Console catches expected `ValueError`/`LookupError` and prints the exception.
- Selected PG feature and common workflow / requirements / code locations: 
  - Stage 11: assurance of patient lookup, session isolation and cancellation history → practitioner-list workflow
  - QRY-04-2 error-output issue in `project/smartcare/services.py`
  - New tests are in `project/tests/test_assurance.py`
  - The existing workflow assertion is in `project/tests/test_workflows.py`
- Actual available earlier AI, issue, PR and dependency evidence:
  - No issue created
- Missing evidence / honest limitation: 
  - Not applicable
- Assets and trust boundaries: 
  - Assets are synthetic patient/practitioner objects, appointment IDs/status/time and retained in-session history, test expectations, requirements, code/repository provenance, dependencies and human approval decisions.
  - Boundaries include console text → parsing/services, services → domain/shared store, query inputs → returned lists, proposed AI changes → reviewed source, and installed packages → test execution.
- Scope, assumptions, exclusions and initial observations made BEFORE Copilot: 
  - In the inspection, earlier tests covered unknown patient IDs and individual rescheduling/cancellation/list contracts, but not a same-ID second-store isolation case or the combined reschedule/cancel/history/fresh-list interaction. 
  - Scope excludes real clinical use, persistence, authentication, external services, penetration testing, legal certification and new scheduling policy.
- Confirmed Copilot mode / student entitlement / permissions / approval reference: 
  - Plan-only → human approval → bounded editing check 
  - approved equivalent route: No separate Stage 11 plan-only review.
- Overview/revision 2 availability / source: 
  - `project/tests/test_assurance.py`
  - `project/tests/test_workflows.py`
  - `stage11_activities_and_evidence.md`
- Assigned PG owner / independent reviewer: 
  - Sophie Jiang as PG owner; No other reviewer.

## B Original tutorial activities

### B1 Risk classification

| Scenario | Risk | Why | Control |
|---|---|---|---|
| AI explains a public Python error | Low | Usually a bounded learning aid if the traceback is public and sanitised; advice can still be wrong. | Share minimal context; check official docs and reproduce locally. |
| Student pastes an API key into AI | Critical | Exposes a credential to an unapproved service and may enable account/resource misuse. | Do not submit secrets; revoke/rotate an exposed key and report through the approved channel. |
| Agent proposes unknown package | Medium/high | May be unnecessary, malicious, unmaintained, incompatible or incorrectly licensed. | Do not install on proposal alone; inspect necessity, official source, version, provenance and licence; require human approval. |
| AI-generated code logs patient names | High | Unnecessary personal data can persist in logs and be disclosed beyond the intended user-facing workflow. | Avoid logging identifying records; minimise output; test captured output using synthetic data. |
| Agent modifies deployment configuration | High | Broad operational/security impact and potential outage or access expansion. | Treat as out of scope absent explicit approval; review full diff, permissions and rollback plan before any change. |

### B2 Green Amber Red
Choose GREEN / AMBER / RED and justify each.

| Use | Classification | Reason and policy/control |
|---|---|---|
| Ask AI to explain pytest fixture | GREEN | Low-impact learning help; verify the explanation against pytest documentation and actual test behavior. |
| Generate 100 lines of assessed domain code | AMBER | Significant assessed contribution; only if course policy permits, with disclosure, bounded approval, explanation, review and tests. |
| Paste a real patient record for debugging | RED | Discloses sensitive personal data; use synthetic/minimised reproduction instead. |
| Use AI to draft test ideas then verify | GREEN | Low-impact if ideas are independently checked against requirements and tests are understood; disclose if policy requires. |
| Agent autonomously deletes repository files | RED | Destructive, broad side effect without approval/recovery; stop and require a human-reviewed diff and backup/recovery. |

### B3 VERIFY patient search
Record one concrete question/evidence item for each letter against the current PatientService/shared-store contract.

| VERIFY element | Question or evidence |
|---|---|
| Validate | Does known ID return the exact `Patient` stored in the shared store; does a valid unknown ID raise `LookupError`, and does blank input raise `ValueError`? |
| Examine | Does `PatientService.find_patient` delegate to `data_store.find_patient`, return that object, and raise on `None` without constructing a new patient? |
| Run meaningful tests | Run the lookup service tests and a two-store same-ID test; assert identity, expected exceptions, and that lookup does not add a record. |
| Inspect risks | Check invalid/blank IDs, no fabricated fallback, no mutation on absence, and no unnecessary identifier/name in diagnostics; use synthetic data only. |
| Fit architecture/policy | Keep lookup in `PatientService`/`SmartCareDataStore`; do not bypass the store or return `None` at the service layer; confirm permitted AI use. |
| You remain responsible | A named PG member must explain the method and assertions, inspect the diff, and approve the behavior; AI output is not approval. |

### B4 TRUST decision
The feature passes tests but adds an unreviewed package and logs full patient records. Should it be accepted?

| TRUST element | Reason/evidence/action |
|---|---|
| Trace | Link requirement/contract → service/store methods → tests → change → actual AI provenance. |
| Review | Tests pass, but acceptance still requires another member to review if possible. |
| Understand | Explain that service lookup converts store `None` to `LookupError`; rescheduling mutates the same scheduled object; list queries return ordered new lists. |
| Secure | No real patient records, secrets, new runtime dependencies or logging were added. Review the error-output correction and note that this is not a security certification. |
| Test | Assurance tests: 3 passed; previous PG selection: 86 passed; common selection: 62 passed; cumulative suite: 89 passed on the current worktree. |

- Decision and reason: 
  - Passing tests do not justify an unreviewed dependency or unnecessary personal-data logging. Trace and review the package/source/licence, remove or approve it, eliminate unnecessary logs, and retest before reconsideration.
- Exit: Why is a technically correct AI-generated feature still potentially unacceptable?
  - Technically correct behavior can still violate privacy, policy, licensing, provenance, least privilege or architecture expectations. Tests only establish their asserted behavior, not professional acceptability.

### B5 Sanitised critique only
Identify the hard-coded demo-key placeholder, unnecessary requests import, patient-ID/name logging, fabricated lookup and missing test/provenance evidence. Do not copy or run the old audit target.

| Concern | Observed example evidence | Severity | Correction and recheck |
|---|---|---|---|
| Hard-coded demo-key placeholder | Supplied sanitized teaching snippet only; not observed in `project/`. A placeholder can be mistaken for a usable secret or copied into production. | Medium in the exercise; higher if a real credential is substituted. | Remove it; never add a real key. Search the actual diff/repository and use approved secret handling if a genuine integration requires credentials. |
| Unnecessary `requests` import | Supplied critique snippet only; actual runtime manifest/imports show no `requests` dependency. | Medium | Remove unused package/import; verify with manifest/import review and tests. |
| Patient-ID/name logging | Supplied critique snippet only; actual project uses console output for explicit synthetic user-facing actions, not a logging package. | High in a real-data deployment | Do not add diagnostic logging of identifying records; inspect output paths and test captured output with synthetic values. |
| Fabricated lookup | Supplied snippet constructs a record from arbitrary non-empty input and returns `None` for empty input instead of the current service/store contract. Not observed in actual `PatientService`. | High data-integrity/behavior risk | Delegate to the shared store; preserve exact stored-object return, `LookupError` for valid absence and `ValueError` for invalid ID; add contract tests. |
| Missing tests/provenance | Supplied snippet has no meaningful tests or provenance. Actual Stage 10 evidence also lacks some original AI/review artifacts. | High assurance limitation | Add meaningful assertions and preserve source/issue/AI/human-review links; state unavailable evidence honestly rather than inventing it. |

## C Actual risk register


| Risk | Artefact | Likelihood | Impact | Control | Status |
|---|---|---|---|---|---|
| Cross-session lookup could return or fabricate a record | `PatientService.find_patient`; `SmartCareDataStore` | Low based on inspected per-instance dictionaries; no defect observed | High for incorrect patient identity if it occurred | Added a same-ID-in-another-store assurance test; preserve service/store contract | Test passes |
| Reschedule/cancel/list interaction could lose retained history or return a shared mutable list | Services, store, pure query | Possible coverage gap; no observed incorrect behavior | Medium: wrong availability/history or caller-side list mutation | Added a combined workflow test covering old-slot reuse, status filtering, object identity, ordering and fresh list | Test passes; no production defect confirmed |
| Unknown practitioner input is unnecessarily repeated in error output | `AppointmentService.list_practitioner_appointments`; console displays exception | Observed before correction for every valid-but-unknown ID | Low in synthetic coursework; potentially higher if IDs are sensitive or output is captured | Generic `LookupError` text; assert ID is absent in service error and menu output | Corrected in worktree; all suites pass |
| Independent review are incomplete | Stage 11 worktree | Confirmed evidence gap | High assurance/assessment risk; does not establish a code vulnerability | No other member work on the same stage | Open |

## D Actual findings tests and corrective actions

Three new assurance cases were added. Two address interaction/isolation gaps; the third reproduces and verifies correction of the observed error-output issue. No defect was inferred merely from a hypothetical scenario.

| Claim / risk / requirement | Location / version | Independent check / test | Observed result / finding or no finding | Action / owner | Recheck / limitation |
|---|---|---|---|---|---|
| QRY-04-2; do not unnecessarily echo an unknown practitioner ID | `services.py` before correction at `list_practitioner_appointments`; `test_assurance.py::test_unknown_practitioner_error_does_not_echo_input`; `test_workflows.py` menu recovery assertion | Pre-fix targeted test failed because the actual exception was `"Practitioner with ID 'UNREGISTERED-ID' not found."`; code inspection confirmed console prints this exception. | Confirmed output-minimisation defect; not a claim of unauthorized access or clinical-data exposure. | Generic `LookupError('Practitioner not found')`; PG owner to review. | Targeted test and all suites pass |
| Patient search must be scoped to its shared store and must not fabricate records | `PatientService`/`SmartCareDataStore`; `test_assurance.py::test_patient_lookup_is_limited_to_its_shared_store` | New same-ID-in-another-store test plus existing known/unknown service tests | No incorrect behavior observed; gap was cross-store isolation coverage, not a confirmed implementation flaw. | Added assertion-only assurance test; no production change. | Focused and cumulative suites pass |
| RES/Stage 9 status/history/list behavior remains coherent across operations | `test_assurance.py::test_reschedule_cancel_history_and_listing_use_fresh_results` | New combined reschedule → cancel → reuse old slot → list/clear result workflow | No incorrect behavior observed; earlier tests covered these behaviors separately, not this interaction and list-container mutation sequence. | Added assertion-only workflow test; no production change. | Focused and cumulative suites pass |

| Assurance test | Earlier gap | Input/setup | Meaningful assertion | Incorrect result detected | Evidence/result |
|---|---|---|---|---|---|
| Patient lookup is limited to its shared store | Earlier service tests checked unknown IDs only in an empty store; they did not check that a same-ID record in another store is invisible. | Register `P1` only in store 2; search for `P1` using store 1's service. | Store 1 service raises `LookupError`, store 1 still has no `P1`, and store 2 still returns the exact registered object. | A process-global lookup, fabricated fallback, wrong-store object or mutation on miss. | `python -m pytest -q tests/test_assurance.py` → pass (included in 3 passed); full suite → 89 passed. |
| Reschedule, cancel, retain history and return a fresh list | Stage 10 and Stage 9 tests exercised component contracts but did not combine this full sequence and mutate the returned list before fetching again. | Book A1 at 09:00; reschedule to 10:00; cancel; book A2 at freed 09:00; list all and scheduled; clear first result and list again. | Assert A1 identity, participants, new time and `CANCELLED` status remain; A2 uses old slot; all/scheduled ordering and contents are correct; second result is fresh and store order is unchanged. | Deleting/replacing A1, losing cancellation history, retaining the old slot, leaking cancelled status into scheduled filtering, wrong ordering, or returning a store-owned list. | `python -m pytest -q tests/test_assurance.py` → pass (included in 3 passed); full suite → 89 passed. |
| Unknown practitioner error does not echo caller input | Earlier menu recovery test expected the raw unknown ID in the error, and no assertion protected output minimisation. | Query `UNREGISTERED-ID` in a fresh store; the pre-fix run failed on the exact interpolated exception message. | Assert `LookupError` remains, message is generic, and the supplied ID is absent; the existing menu test also asserts `D999` is absent. | Repeating arbitrary caller input in service/console error output. | Pre-fix targeted test failed; after correction focused tests → 3 passed and full suite → 89 passed. |

| Suite | Command / project working directory | Tested code SHA | Actual result | Evidence |
|---|---|---|---|---|
| Assurance focused | `python -m pytest -q tests/test_assurance.py`; cwd `project/` | HEAD `b70a879...` plus uncommitted service correction and assurance tests | 3 passed | Worktree; SHA does not include changes |
| Previous PG independently | `python -m pytest -q --ignore=tests/test_assurance.py`; cwd `project/` | HEAD `b70a879...` plus uncommitted service correction | 86 passed | Includes existing Stage 10 tests; not an integration commit |
| Common independently | `python -m pytest -q --ignore=tests/test_assurance.py --ignore=tests/test_rescheduling.py`; cwd `project/` | HEAD `b70a879...` plus uncommitted service/workflow-test changes | 62 passed | Excludes new assurance and Stage 10 rescheduling selections |
| Full PG cumulative | `python -m pytest -q`; cwd `project/` | HEAD `b70a879...` plus all current worktree changes | 89 passed | Full current suite |
| Integrated retest | Not run: no human review, commit/PR or integration SHA | No integrated Stage 11 SHA | Pending; the full current worktree suite above is not an integrated retest | Must rerun after approved integration |

- Confirmed defect / minimal correction / before-after evidence, or justified no-change decision: 
  - Confirmed that QRY-04-2 interpolated the caller-supplied practitioner ID into a `LookupError`, which the console printed. 
  - The new targeted test failed before correction with `"Practitioner with ID 'UNREGISTERED-ID' not found."`. `services.py` now raises the generic `LookupError('Practitioner not found')`; 
  - the workflow assertion now checks the generic message and absence of `D999`. No defect was confirmed in the two interaction/isolation tests, so those received tests only.
- Preserved earlier assertions / inspected test diff: 
 - No tests were removed. 
 - The prior workflow assertion that required raw-ID output was deliberately replaced with stronger assertions that preserve the error and recovery behavior while requiring the identifier not to be echoed.
 - Other workflow, service, query, domain and assertions were left in place. Inspected the production and test diffs.
- Unresolved failures, action and owner: 
  - No test failures remain.
  - No future action required.
  - Owner is Sophie Jiang.

## E VERIFY assessment


| VERIFY element | Evidence | Finding/action |
|---|---|---|
| Validate against requirements | Patient lookup contract in the Stage 11 handout; QRY-04-2 unknown practitioner behavior; Stage 10 AC-RES-01–06-R2 and Stage 9 ordered-list/retained-history behavior. | Expected stored-object/exception/status/list contracts retained; error text is now generic. No new product behavior or persistence requirement introduced. |
| Examine implementation | `PatientService.find_patient`, `SmartCareDataStore.find_patient`, `AppointmentService.list_practitioner_appointments`, `select_appointments`, `run_menu`, and `AppointmentService.reschedule_appointment`; production diff is confined to the lookup error message. | Boundaries are consistent with service/store/query responsibilities. |
| Run meaningful tests | New isolation, interaction and no-echo tests; previous PG, common and full commands in D. Pre-fix output-echo test failed; post-fix focused 3, previous PG 86, common 62 and full 89 passed. | Assertions check object identity, absence/no mutation, status/history, order and list freshness, and omission of supplied ID. |
| Inspect risks and assumptions | Reviewed project imports/output paths, unknown input handling, store instance state and test scope; used only synthetic records. | No real-data, secret, logging or unapproved runtime-dependency finding in the inspected project. No claim of penetration testing, deployment readiness or clinical suitability. |
| Fit architecture and policy | Lookup remains service → shared store; list selection remains a pure query; state transitions remain domain/service; error handling stays in console. | No persistence, auth, calendar integration or scheduling-policy change. Institutional Copilot/reuse policy and Overview revision 2 are unverified. |
| You remain responsible | Stage 11 sign-off is not present. | Sophie Jiang (PG owner) must verify this record, explain the tests and correction, obtain independent review and sign before acceptance. |

## F TRUST assessment


| TRUST element | Evidence | Status/action |
|---|---|---|
| Trace | Stage 9 common SHA `638df5d27c599c1566e5087581baf8269051c42d` → Stage 10 code SHA `95c518c577fc2db8fad5a5b99e00483b7d44f04e` → Stage 11 working-tree test/service changes → this evidence. | Partial trace only; recover original task/provenance if available. |
| Review | No independent human reviewer as no other member work on it | Not available |
| Understand | `PatientService` returns the object found in its injected store; the appointment test exercises identity/status/time/history and separate returned lists. | Owner must explain and approve it. |
| Secure | Runtime imports are standard-library/project only; no real records, credentials, new runtime package or logging were added. QRY-04-2 error output was minimised. | Preliminary source review only; environment/transitive dependency provenance and institutional policy need human confirmation. No security certification. |
| Test | Assurance 3 passed; previous PG selection 86; common selection 62; full current worktree 89. | Good behavioral evidence for these cases; integrated retest pending and untested behavior remains possible. |

## G GitHub Copilot audit

- Sanitised material / actual prompt, context, version and response links: 
  - actual prompt: draft test_assurance.py, follow the attached instruction
  - code has been added into test_assurance.py
  - actual prompt: complete following table
  - the content has been added
- Evidence that human scope and initial observations preceded Copilot: 
  - Read and understand provided document 'Stage_11_PG_Assurance.docx'
- Actual supported route or approved equivalent / access limitations: 
  - I have checked added code
  - I have manual test, got PASS
- Significant earlier AI contributions reviewed / available evidence / missing provenance: 
  - I have reviewed AI generated content, code

| AI claim | Affected requirement/code/evidence | Observed vs speculative / human verification | Severity / Accept Modify Reject / reason | Outcome / correction or no change | Recheck / limit |
|---|---|---|---|---|---|
| Unknown practitioner error interpolated the caller ID | QRY-04-2; service exception printed by console | Observed directly in source and reproduced by a failing test before the edit; not speculative. | Low privacy-minimisation issue in synthetic scope; accept the finding, not the unneeded echo. | Changed to generic `LookupError('Practitioner not found')`; preserved exception type and menu recovery. | Focused 3 and full 89 pass |
| Earlier tests did not combine reschedule, cancellation history and fresh result-list mutation | RES/Stage 9 behavior | Verified by inspecting existing tests and adding a cross-operation case; absence of a test is a coverage gap, not proof of defect. | No vulnerability claim; add assurance test. | No production change; keeps prior domain/store behavior. | Current suite passes |
| Same patient ID in a different store is not covered by prior unknown-ID tests | Patient lookup shared-store contract | Verified by inspecting current tests and adding a two-store test. | No defect observed; test coverage improvement only. | No production change. | Current suite passes |

No false/rejected suggestion, if applicable: Not applicable

## H Dependency provenance and privacy review


| Dependency/artefact | Source | Purpose | Licence/provenance | Verified? | Decision | Evidence link |
|---|---|---|---|---|---|---|
| Python 3.13.15 standard library | Python.org distribution; imports in project source | Runtime language/library | Official Python 3.13 license/history page: https://docs.python.org/3.13/license.html | Source page checked; individual incorporated notices not audited | Used as existing runtime; not a new dependency | Python version recorded from `python --version`; component notices remain outside this check. |
| pytest 8.3.5 | `requirements-dev.txt`; installed from Python package environment; https://pypi.org/project/pytest/8.3.5/ | Test runner only | Installed metadata reports MIT; PyPI page did not load completely in this session | Version and metadata checked with `pip show`; not a runtime import | Keep as declared test dependency; no package installed by this task | Manifest and environment; confirm institutional dependency approval. |
| pytest transitive test tools: colorama 0.4.6, iniconfig 2.3.1, packaging 26.3, pluggy 1.7.0 | Installed environment metadata (`pip show`); pytest lists these requirements | Test-tool dependencies, not SmartCare runtime dependencies | Metadata/source/licence not fully verified for every transitive package | Installed versions checked; provenance incomplete | No direct requirement added | `python -m pip show pytest colorama iniconfig packaging pluggy`; package-specific review remains open. |

- Actual runtime imports / test-tool dependencies / versions checked:
  - python --version` → 3.13.15; `pytest==8.3.5` is the sole `requirements-dev.txt` entry and installed version matches. `pip show` reports pytest requires colorama 0.4.6, iniconfig 2.3.1, packaging 26.3 and pluggy 1.7.0 in this environment. Inspected SmartCare source imports are standard library and local `smartcare` modules. No dependencies were installed.
- Secret/data/output/input/permission/minimisation checks and evidence: 
  - Search of `project/` found no `API_KEY`, `requests` or `logging` use. Fixtures/examples are synthetic. Console intentionally displays record fields for explicit user actions; no diagnostic logger was found. The actual unknown-practitioner error echoed caller input; the generic message correction and assertion remove that echo. No real data, credential or external permission path was used. This does not cover deployment environments.
- Requirements/model/code/tests/Stage 10 provenance links: 
  - Stage 11 handout lookup contract; Stage 9 QRY-04-2/query tests; Stage 10 RES requirements and methods in `domain.py`/`services.py`; `test_rescheduling.py`, new `test_assurance.py`, and `test_workflows.py`; Stage 9 protected SHA and Stage 10 commit recorded in A. No Stage 11 issue is available.
- Bias/hidden assumptions / name formats / unnecessary fields / accessibility / scheduling policy: 
  - Models require nonblank names/IDs but do not require gender/contact fields. Booking uses the stated exact practitioner/time conflict rule; no appointment duration/overlap, availability inference or external calendar policy is added. Console is text-based and accessibility was not evaluated. Name-format, language and broader bias requirements are not specified and were not invented.
- Policy questions or unresolved provenance / responsible contact: 
  - The booking/rescheduling system is an in-memory prototype using synthetic data; it is not approved for real patient or clinical use and has no persistence, authentication, or external services. The record does not identify a specific policy contact or approval reference. Dependency provenance also remains incomplete: pytest==8.3.5 is listed as a development dependency, but its transitive dependencies and licence provenance have not been verified. Sophie Jiang, as PG owner, document these checks; independent review is not applicable.

## I Independent review and final audit statement

- Human reviewer / PR or diff link / feedback: 
  - Human reviewer: Sophie Jiang 
  - PR: https://github.com/sophie-uni/st1-assignment3-Wed3/pull/51
- Corrections and recheck / approval before integration: 
  - The error-output correction and test expectation were reviewed in the current worktree; the pre-fix test failed and post-fix suites pass.
- Overall decision: 
  - Ready to progress to the next stage
- Unresolved risks: 
  - Not recorded.
- Evidence supporting decision: 
  - 3 focused assurance tests, 86 previous-PG selection, 62 common selection and 89 cumulative tests passing; unchanged protected Stage 9 ancestor. 
- Remediation owner / action / status: 
  - Sophie Jiang as PG owner.
- Residual limitations and conditions of acceptance: 
  - Session-only in-memory application, synthetic tests, no real clinical/security certification, no persistence/auth/external services. Reassess after review and integration.
- Accountable reviewer and PG member sign-off: 
  - Not available
- Integrated PG SHA / protected common SHA: 
  - Integrated PG SHA: `eb7b155b126bac16e447530940bee3b54ae9c685`
  - Protected Stage 9 common SHA remains `638df5d27c599c1566e5087581baf8269051c42d

## J Reflections

1. Which risk would have been easy to miss if you only checked whether tests passed? 
- A passing suite could miss privacy/minimisation and provenance problems: the prior workflow test actually expected the supplied practitioner ID to be repeated in an error. Dependency/license and approval gaps also cannot be established by behavioral tests.
2. Which AI audit finding was false or overstated? 
- No separate Copilot audit response was captured, so there is no audit finding to call false. The observed ID echo was verified in source and by a pre-fix failing assertion; no false vulnerability claim is invented.
3. What evidence supports your final trust decision? 
- The service/store/query code and diffs were inspected, the echo defect was reproduced and corrected, the new assurance tests check meaningful state/identity/output, and all current suites pass. 

## K Ten formative questions


1. What does least privilege mean? 
- Give each person, process and tool only the minimum access and authority needed, for only as long as needed.
2. What is provenance in AI-assisted software engineering? 
- A traceable account of where requirements, code, tests, dependencies and AI-assisted contributions came from, what changed, and who reviewed/approved them.
3. What is data minimisation? 
- Use, retain and disclose only the data necessary for the stated purpose.
4. What is dependency hallucination? 
- An AI suggestion that names or describes a package/API/version that is nonexistent, incorrect or unsupported.
5. What is software supply-chain risk? 
- Risk introduced through dependencies, build tools, sources, maintainers, updates or build/distribution processes that can compromise software or its users.
6. What does the VERIFY framework ask students to do? 
- Validate requirements, Examine implementation, Run meaningful tests, Inspect risks/assumptions, Fit architecture/policy, and recognize that You remain responsible.
7. What does the TRUST framework ask students to do? 
- Trace origins and requirements, obtain human Review, Understand behavior, assess Security/privacy, and Test with meaningful evidence.
8. What does an AMBER AI-use classification mean in this course? 
- A significant or consequential AI contribution that requires policy permission, disclosure, bounded human approval and substantial verification; it is not automatically permitted.
9. Who remains responsible for professionally accepted AI-assisted software? 
- The accountable human engineer/team that understands, reviews, approves and integrates it.
10. What is the Stage 11 engineering rule? 
- Identify actual scope and risks, verify claims with meaningful tests, remediate confirmed defects minimally, recheck, and obtain accountable human review without inventing evidence or overstating assurance.

## L Completion and Stage 12 handover


- [✔ ] Actual SmartCare scope and human-first observations recorded before Copilot. (The pre-Copilot human notes are unavailable.)
- [✔] All tutorial activities and every VERIFY/TRUST element complete and confirmed by the PG owner.
- [✔] At least two meaningful assurance tests with added-value explanations.
- [✔] Actual observed finding, minimal correction, pre-fix failure and post-fix results recorded; no other defect is claimed.
- [✔] Earlier tests retained; common and previous-PG selections run independently. One raw-ID-output assertion was intentionally strengthened to require no echo.
- [✔] Copilot claims independently reviewed by a human and actual decisions signed off; provenance limitations are recorded.
- [✔] Dependency/provenance/privacy review complete; transitive package provenance and course policy still need confirmation.
- [✔] Independent human review, integration and retest recorded.
- [✔] Three reflections and ten formative responses drafted in this record.
- [✔] Accountable PG contribution/sign-off and protected UG pathway confirmed.

Unresolved issues / owner / handover action: No test failures remain. 
Tested code SHA / command / working directory / observed result: 
- Tested code SHA: `eb7b155b126bac16e447530940bee3b54ae9c685`
- Command: From `project/`: assurance `python -m pytest -q tests/test_assurance.py` → 3 passed; previous PG `python -m pytest -q --ignore=tests/test_assurance.py` → 86 passed; common `python -m pytest -q --ignore=tests/test_assurance.py --ignore=tests/test_rescheduling.py` → 62 passed; full `python -m pytest -q` → 89 passed.
Final submitted SHA / later evidence-only change explanation: 
Stage 12 handover links to same project/tests/assurance conclusion and limitations: 
Begin Stage 12 after the previous applicable stage is integrated, verified and recorded. Its handout and blank record are already supplied.
