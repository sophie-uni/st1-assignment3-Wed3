# SmartCare Stage 6 starter

Requirements baseline: SmartCare A3 2026 revision 2. Python 3.13 and pytest 8.3.5 verified. Runtime uses only the standard library.

From this directory, using a Python environment with the development dependency installed:

```sh
python main.py
python main.py --interactive
python -m pytest
```

If needed in your approved environment: `python -m pip install -r requirements-dev.txt`.

The demo registers synthetic records and books/finds an appointment. The interactive menu supports patient/practitioner registration and lookup, booking, appointment lookup and cancellation, and practitioner appointment listing with an optional status filter. Menu data exists only for that run and is lost on exit; FR-10 restart persistence is retired. Use synthetic information only.

`domain.py` contains the entities, status and guarded cancellation/rescheduling. `data_store.py` holds three dictionaries through add/find/list methods. The services share that object. Registration, booking, appointment lookup, conflict checking and practitioner listing are available. IDs are trimmed, non-blank and case-sensitive. Properties provide read-only identity/appointment state; changes go through domain methods. No special architecture terminology is required.

Stage 6 service lookup and cancellation, Stage 9 practitioner listing and interactive menu, and the PG Stage 10 rescheduling methods are implemented. `Appointment.reschedule` validates the new local minute-precision datetime and only changes a scheduled appointment's time. `AppointmentService.reschedule_appointment` checks the stored target and practitioner conflict before updating that same object; successful moves appear in subsequent lookups/lists and free the old slot. No restart persistence, notifications, or external calendar integration is provided.

Service booking accepts IDs and a `datetime` (local, minute precision). Console parser accepts exactly `YYYY-MM-DD HH:MM`. Store lookups return None when absent; service lookups raise LookupError. Invalid values, duplicates, conflicts and illegal transitions raise ValueError. Lists are new containers holding the stored objects. No age, duration, patient-conflict or past-date rules apply.
