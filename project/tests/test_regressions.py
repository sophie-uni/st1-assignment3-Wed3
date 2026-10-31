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
    data_store, _, _, appointment_service = foundation()
    practitioner_d2 = PractitionerService(data_store).register_practitioner(
        "D2", "Morgan Example", "General"
    )
    when = datetime(2026, 10, 1, 9)

    first = appointment_service.book_appointment("A1", "P1", "D1", when)

    with pytest.raises(ValueError):
        appointment_service.book_appointment("A2", "P1", "D1", when)

    assert first.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [first]

    second = appointment_service.book_appointment("A3", "P1", "D2", when)

    assert second.practitioner is practitioner_d2
    assert second.date_time == when
    assert second.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [first, second]


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

# -------------------------------------------------------------------------
# Regression Test 2: Defect F8-02 (Retained Cancelled Appointment Lookup)
# -------------------------------------------------------------------------
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