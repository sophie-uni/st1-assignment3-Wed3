'''Patient and Practitioner construction and required-field validation,
and Appointment construction,
initial status and guarded cancellation.
Preserve the four original reference-test intentions: blank patient ID rejected;
a new appointment starts SCHEDULED;
cancellation changes status;
repeated cancellation is rejected.
Implement your own tests using the current imports and ValueError contract.'''

from datetime import datetime, timezone

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)

BOOKING_TIME = datetime(2026, 10, 1, 9, 0)


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


    # Hassan: Appointment construction (FR-04 supporting domain evidence)

    def test_new_appointment_starts_scheduled() -> None:
        """T-FR04-D1: a new appointment keeps its participants and is SCHEDULED."""
        patient = Patient('P1', 'Alex Example')
        practitioner = Practitioner('D1', 'Taylor Example', 'General')

        appointment = Appointment('A1', patient, practitioner, BOOKING_TIME)

        assert appointment.status is AppointmentStatus.SCHEDULED
        assert appointment.appointment_id == 'A1'
        assert appointment.patient is patient
        assert appointment.practitioner is practitioner
        assert appointment.date_time == BOOKING_TIME

    @pytest.mark.parametrize(
        'invalid_time',
        [
            datetime(2026, 10, 1, 9, 0, 1),
            datetime(2026, 10, 1, 9, 0, 0, 1),
            datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc),
            '2026-10-01 09:00',
        ],
    )
    def test_appointment_rejects_time_not_local_minute_precision(
            invalid_time: object,
    ) -> None:
        """T-FR04-D2: only a naive, minute-precision datetime is accepted."""
        patient = Patient('P1', 'Alex Example')
        practitioner = Practitioner('D1', 'Taylor Example', 'General')

        with pytest.raises(ValueError):
            Appointment('A1', patient, practitioner, invalid_time)

    # Devam: Appointment cancellation guard (FR-06 domain evidence)

    def scheduled_appointment() -> Appointment:
        """Return a fresh SCHEDULED appointment."""
        patient = Patient('P1', 'Alex Example')
        practitioner = Practitioner('D1', 'Taylor Example', 'General')
        return Appointment('A1', patient, practitioner, BOOKING_TIME)

    def test_cancel_changes_status() -> None:
        """T-FR06-D1: cancel() moves a SCHEDULED appointment to CANCELLED."""
        appointment = scheduled_appointment()

        appointment.cancel()

        assert appointment.status is AppointmentStatus.CANCELLED
        assert appointment.appointment_id == 'A1'
        assert appointment.date_time == BOOKING_TIME

    def test_repeated_cancel_is_rejected() -> None:
        """T-FR06-D2: a second cancel() raises ValueError and keeps CANCELLED."""
        appointment = scheduled_appointment()
        appointment.cancel()

        with pytest.raises(ValueError):
            appointment.cancel()

        assert appointment.status is AppointmentStatus.CANCELLED