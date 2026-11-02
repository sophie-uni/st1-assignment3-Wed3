# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Wednesday 14:30-16:30 Group 3 (st1-assignment3-Wed3)
Members and UG/PG applicability: Sophie Jiang (PG), Hassan Ahmad (UG), Trung Hieu (UG)


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare A3 2026 revision 2. Python 3.13 and pytest 8.3.5 verified.
Common starting SHA / branch / applicable members: [response]
PG starting SHA / branch / applicable members or not applicable: [response]
Working-state review and approved integration: [response]
Protected common candidate and PG differences: [response]
Feature freeze / owner / verifier: [response]


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: [response]

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action | Who |
|---|---|---|---|---|---|---|
| Cancellation history works | [response] | [response] | [response] | [response] | [response] | Trung |
| Architecture responsibilities are appropriate | [response] | [response] | [response] | [response] | [response] | Trung |
| Rescheduling is safe — PG only | [response] | [response] | [response] | [response] | [response] | Sophie |
| AI use is responsible — common recheck / PG assurance | [response] | [response] | [response] | [response] | [response] | Sophie |
| System is maintainable | [response] | [response] | [response] | [response] | [response] | Hassan |
| FR-01–03 register/find and validation | [response] | [response] | [response] | [response] | [response] | Hassan |
| FR-04–05 booking/conflict rules | [response] | [response] | [response] | [response] | [response] | Hassan |
| FR-06–08 cancellation/history/find | [response] | [response] | [response] | [response] | [response] | Trung |
| FR-09 and QRY/FP listing/filter/order/purity | [response] | [response] | [response] | [response] | [response] | Sophie |
| UI full console sequence and error recovery | [response] | [response] | [response] | [response] | [response] | Sophie |
| Session-only scope / FR-10 retired | [response] | [response] | [response] | [response] | [response] | Hassan |
| PG RES and assurance integration | [response] | [response] | [response] | [response] | [response] | Sophie|


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link | Who | 
|---|---|---|---|---|---|---|
| Complete common | [response] | [response] | [response] | [response] | [response] | Trung |
| Complete PG if applicable | [response] | [response] | [response] | [response] | [response] | Sophie |
| Affected focused checks after correction | [response] | [response] | [response] | [response] | [response] | Hassan |
| Full integrated recheck | [response] | [response] | [response] | [response] | [response] | Sophie |

Prior assertions preserved / reviewed test diff (Hassan): [response] 
Remaining failure / limitation (Trung): [response]


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link | Who |
|---|---|---|---|---|---|
| Problem and stakeholders | [response] | [response] | [response] | [response] | Hassan |
| Register and find Patient and two Practitioners | [response] | [response] | [response] | [response] | Hassan |
| Valid booking | [response] | [response] | [response] | [response] | Hassan |
| Same practitioner exact-time conflict rejected | [response] | [response] | [response] | [response] | Hassan |
| Different practitioner same time allowed | [response] | [response] | [response] | [response] | Hassan |
| Cancel SCHEDULED and retain/find CANCELLED object | [response] | [response] | [response] | [response] | Hassan |
| Invalid/repeated cancellation rejected | [response] | [response] | [response] | [response] | Hassan |
| Default all-status listing | [response] | [response] | [response] | [response] | Trung |
| Explicit filtering / empty vs unknown / deterministic order | [response] | [response] | [response] | [response] | Trung |
| Invalid date/status/menu/lookup recovery and continued operation | [response] | [response] | [response] | [response] | Trung |
| Session-only limitation and normal exit | [response] | [response] | [response] | [response] | Trung |
| One meaningful requirement-linked pytest test explained | [response] | [response] | [response] | [response] | Trung |
| Architecture and one actual AI decision / known limitation | [response] | [response] | [response] | [response] | Trung |
| PG reschedule identity/participants/time and no-op | [response] | [response] | [response] | [response] | Sophie |
| PG conflict/invalid status/failure non-mutation | [response] | [response] | [response] | [response] | Sophie |
| PG old slot / current lookup/list ordering / assurance risks | [response] | [response] | [response] | [response] | Sophie |
Stable demo owner / fresh process / command: (Sophie)[response]
PG demonstrations through service/tests or not applicable: (Sophie)[response]


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck | Who |
|---|---|---|---|---|
| OOP responsibilities and pure-query boundaries | [response] | [response] | [response] | Hassan |
| PascalCase and snake_case naming | [response] | [response] | [response] | Hassan |
| Useful type hints and meaningful docstrings | [response] | [response] | [response] | Hassan |
| Four-space indentation and imports/layout | [response] | [response] | [response] | Hassan |
| Focused methods / duplication / dead or commented code | [response] | [response] | [response] | Trung |
| Globals / leakage / unnecessary inheritance or frameworks | [response] | [response] | [response] | Trung |
| No SQLite/persistence/repository ABCs/speculative features | [response] | [response] | [response] | Trung |
| Synthetic data / secrets / dependencies / provenance | [response] | [response] | [response] | Trung |
| Significant common Copilot contributions and human verification | [response] | [response] | [response] | Sophie |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | [response] | [response] | [response] | Sophie |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] |
Access route or approved equivalent / limitations: [response]
Available AI evidence and missing evidence honestly disclosed: [response]


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | [response] | [response] | [response] |
| Out-of-scope capabilities and known limitations | [response] | [response] | [response] |
| Confirmed teaching Python version and dependency installation | [response] | [response] | [response] |
| Working directory / demo / interactive / test commands | [response] | [response] | [response] |
| Repository structure and architecture responsibilities | [response] | [response] | [response] |
| Responsible AI summary / synthetic-data rule | [response] | [response] | [response] |
| Release label/version and SHA links | [response] | [response] | [response] |
Root README index and project/README verified: [response]
Fresh clone or extracted ZIP / candidate identity: [response]
Verifier and clean environment / actual version: [response]
Setup/run/test commands and observed results: [response]
Missing local file or setup gap / remedy and recheck: [response]


## G Known limitations debt and release notes

Delivered features: [response]
Important fixes: [response]
Architecture/quality improvements: [response]
Known limitations: [response]
AI-assisted development note: [response]

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] |
Session-only synthetic data and minute-precision local time: [response]
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: [response]
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: [response]
Difference between accepted scope limit and unresolved required behaviour: [response]
PG assurance residual risks / owner / status or not applicable: [response]


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] | [response] | [response] |
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

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: [response]
Approver / date / rationale and evidence: [response]
What risks remain / conditions / owners: [response]
Can the team explain the system: [response]
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

1. What is a release candidate? (Trung) [response] 

2. What is feature freeze and why is it used? (Trung) [response]

3. What is regression testing in a release context? (Trung) [response]

4. What is a known limitation? (Trung) [response]

5. What is technical debt? (Trung) [response]

6. What are release notes? (Hassan) [response]

7. What is software maintenance? (Hassan) [response]

8. What is the purpose of the individual demonstration/viva? (Hassan) [response]

9. What should the final responsible-AI check establish before release? (Hassan) [response]

10. What is the main course conclusion about AI and the role of the software engineer? (Hassan) [response]


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
| Problem and stakeholders | [response] | Hassan |
| Two requirements and acceptance criteria | [response] | Hassan |
| Domain model and architecture | [response] | Hassan |
| Design trade-off | [response] | Hassan |
| Meaningful test and its limits / 100 percent coverage | [response] | Hassan |
| Diagnosed defect and verification | [response] | Hassan |
| Shared store and session-state/query responsibilities | [response] | Trung |
| What would break if session-state lookup/query responsibilities changed? | [response] | Trung |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | [response] | Trung |
| FR-07 retained history test | [response] | Trung |
| Actual AI change rejected/modified or honestly accepted with verification | [response] | Trung |
| Unresolved limitation / future production work | [response] | Trung |
| Personal implementation contribution | [response] | Sophie |
| Personal test/review/design/integration contribution | [response] | Sophie |
| PG agentic change and rescheduling verification | [response] | Sophie |
| PG responsible-AI risk/remediation or supported no finding | [response] | Sophie |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: [response or not undertaken]
Separate reflection / peer / common team viva evidence links and routing: [response]
No further coding stage. Later corrections use the published assessment process.