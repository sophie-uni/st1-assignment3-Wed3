'''Patient and Practitioner construction and required-field validation,
and Appointment construction,
initial status and guarded cancellation.
Preserve the four original reference-test intentions: blank patient ID rejected;
a new appointment starts SCHEDULED;
cancellation changes status;
repeated cancellation is rejected.
Implement your own tests using the current imports and ValueError contract.'''

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus, Patient, Practitioner


# T-FR07-1
def test_cancel_changes_status_and_keeps_appointment_in_store() -> None:
    """Cancelled appointments retain their history while transitioning state."""
    data_store = SmartCareDataStore()
    patient = Patient("P-001", "Alex Example")
    practitioner = Practitioner("D-001", "Taylor Example", "General")
    appointment = Appointment(
        "A-001",
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 30),
    )

    data_store.add_patient(patient)
    data_store.add_practitioner(practitioner)
    data_store.add_appointment(appointment)

    appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.find_appointment("A-001") is appointment
    assert data_store.list_appointments() == [appointment]
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner


# T-FR07-2
def test_repeated_cancellation_is_rejected_and_state_remains_cancelled() -> None:
    """A second cancellation attempt must fail without mutating the cancelled state."""
    patient = Patient("P-002", "Jamie Example")
    practitioner = Practitioner("D-002", "Morgan Example", "General")
    appointment = Appointment(
        "A-002",
        patient,
        practitioner,
        datetime(2026, 10, 2, 11, 0),
    )

    appointment.cancel()

    with pytest.raises(ValueError, match="Only SCHEDULED appointments may be cancelled"):
        appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED
    assert appointment.date_time == datetime(2026, 10, 2, 11, 0)