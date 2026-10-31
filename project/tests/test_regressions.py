"""Imported from pytest, datetime, and the existing smartcare modules"""
from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def foundation() -> tuple[
    SmartCareDataStore,
    Patient,
    Practitioner,
    AppointmentService,
]:
    """Create fresh registered participants and services for a supplied
    check.
    """
    data_store = SmartCareDataStore()
    patient = PatientService(data_store).register_patient('P1', 'Alex Example')
    practitioner = PractitionerService(
        data_store,
    ).register_practitioner('D1', 'Taylor Example', 'General')
    return (data_store, patient, practitioner, AppointmentService(data_store))

# -------------------------------------------------------------------------
# Regression Test 1: Defect F8-01 (Practitioner Conflict Behaviour)
# -------------------------------------------------------------------------
"""Issue 31, Sophie"""
def test_conflict_rule_and_different_practitioner() -> None:
    """Verify conflict rule and different practitioner."""
    data_store, _, _, appointment_service = foundation()
    PractitionerService(
        data_store,
    ).register_practitioner('D2', 'Morgan Example', 'General')
    when = datetime(2026, 10, 1, 9)
    appointment_service.book_appointment('A1', 'P1', 'D1', when)
    with pytest.raises(ValueError):
        appointment_service.book_appointment('A2', 'P1', 'D1', when)
    assert appointment_service.book_appointment(
        'A3',
        'P1',
        'D2',
        when,
    ).practitioner.practitioner_id == 'D2'

"""Issue 27, Sophie"""
def test_same_practitioner_same_time_is_rejected() -> None:
    """T-FR05-1: a second D1 booking at the exact SCHEDULED time is rejected."""
    data_store, appointment_service = conflict_setup()
    first = appointment_service.book_appointment('A1', 'P1', 'D1', CONFLICT_TIME)

    with pytest.raises(ValueError):
        appointment_service.book_appointment('A2', 'P2', 'D1', CONFLICT_TIME)

    assert data_store.find_appointment('A2') is None
    assert data_store.list_appointments() == [first]
    assert first.status is AppointmentStatus.SCHEDULED

"""Issue 28, Sophie"""
def test_different_practitioner_same_time_is_allowed() -> None:
    """T-FR05-2: D2 can be booked at the time D1 is already booked."""
    data_store, appointment_service = conflict_setup()
    first = appointment_service.book_appointment('A1', 'P1', 'D1', CONFLICT_TIME)

    second = appointment_service.book_appointment(
        'A2',
        'P2',
        'D2',
        CONFLICT_TIME,
    )

    assert data_store.find_appointment('A2') is second
    assert second.practitioner is data_store.find_practitioner('D2')
    assert second.status is AppointmentStatus.SCHEDULED
    assert first.status is AppointmentStatus.SCHEDULED
    stored = data_store.list_appointments()
    assert len(stored) == 2 and first in stored and second in stored


# -------------------------------------------------------------------------
# Regression Test 2: Defect F8-02 (Retained Cancelled Appointment Lookup)
# -------------------------------------------------------------------------
"""Issue 25, Sophie"""
def test_cancel_appointment_returns_and_retains_cancelled_appointment() -> None:
    store = SmartCareDataStore()
    PatientService(store).register_patient("P1", "Sophie Jiang")
    PractitionerService(store).register_practitioner(
        "D1", "Sophie Doctor", "General"
    )
    service = AppointmentService(store)
    appointment = service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 10, 1, 9)
    )

    cancelled = service.cancel_appointment("A1")

    assert cancelled is appointment
    assert cancelled.status is AppointmentStatus.CANCELLED
    assert store.find_appointment("A1") is appointment

"""Issue 26, Trung"""
def test_repeated_service_cancellation_is_rejected() -> None:
    """Issue 26: cancelling A1 twice raises ValueError and changes nothing."""
    store = SmartCareDataStore()
    PatientService(store).register_patient("P1", "Sophie Jiang")
    PractitionerService(store).register_practitioner("D1", "Sophie Doctor", "General")
    service = AppointmentService(store)

    appointment = service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 10, 1, 9)
    )

    cancelled = service.cancel_appointment("A1")

    assert cancelled is appointment
    assert appointment.status is AppointmentStatus.CANCELLED
    assert store.find_appointment("A1") is appointment

    with pytest.raises(ValueError, match="Only SCHEDULED appointments may be cancelled"):
        service.cancel_appointment("A1")

    assert appointment.status is AppointmentStatus.CANCELLED
    assert store.find_appointment("A1") is appointment
    assert store.list_appointments() == [appointment]


"""Issue 29, Trung"""
def test_cancelled_appointment_does_not_block_slot() -> None:
    def test_cancelled_appointment_does_not_block_slot() -> None:
        """Issue 29: a CANCELLED booking no longer occupies the D1 time slot."""
        store = SmartCareDataStore()
        PatientService(store).register_patient("P1", "Alice Example")
        PatientService(store).register_patient("P2", "Bob Example")
        PractitionerService(store).register_practitioner("D1", "Sophie Doctor", "General")
        service = AppointmentService(store)

        when = datetime(2026, 10, 1, 9)

        first = service.book_appointment("A1", "P1", "D1", when)
        cancelled = service.cancel_appointment("A1")

        assert cancelled is first
        assert first.status is AppointmentStatus.CANCELLED
        assert store.find_appointment("A1") is first

        second = service.book_appointment("A2", "P2", "D1", when)

        assert second.status is AppointmentStatus.SCHEDULED
        assert store.find_appointment("A2") is second
        assert second.date_time == when
        assert store.find_appointment("A1") is first
        assert first.status is AppointmentStatus.CANCELLED

"""Issue 24, Sophie"""
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

"""Issue 30, Sophie"""
def test_repeated_service_cancellation_is_rejected() -> None:
    """T-FR06-2: cancelling A1 twice raises ValueError and changes nothing."""
    data_store, appointment_service, appointment = cancellation_setup()
    appointment_service.cancel_appointment('A1')

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')

    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [appointment]