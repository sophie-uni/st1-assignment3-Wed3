"""Stage 8 regression tests for the two diagnosed store defects."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


BOOKING_TIME = datetime(2026, 10, 1, 9, 0)


def fresh_session() -> tuple[SmartCareDataStore, AppointmentService]:
    """Return a new store with P1, P2, D1 and D2 registered through services."""
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)
    patient_service.register_patient('P1', 'Alex Example')
    patient_service.register_patient('P2', 'Jordan Example')
    practitioner_service = PractitionerService(data_store)
    practitioner_service.register_practitioner('D1', 'Taylor Example', 'General')
    practitioner_service.register_practitioner('D2', 'Morgan Example', 'General')
    return data_store, AppointmentService(data_store)


def test_f8_01_same_practitioner_same_time_conflict_is_rejected() -> None:
    """F8-01: FR-05 / AC-04.1 rejection with unchanged state; AC-04.2 still allowed."""
    data_store, appointment_service = fresh_session()
    first = appointment_service.book_appointment('A1', 'P1', 'D1', BOOKING_TIME)

    with pytest.raises(ValueError):
        appointment_service.book_appointment('A2', 'P2', 'D1', BOOKING_TIME)

    assert data_store.find_appointment('A2') is None
    assert data_store.list_appointments() == [first]
    assert first.status is AppointmentStatus.SCHEDULED
    other = appointment_service.book_appointment('A3', 'P2', 'D2', BOOKING_TIME)
    assert data_store.find_appointment('A3') is other
    assert other.status is AppointmentStatus.SCHEDULED


def test_f8_02_cancelled_appointment_remains_retrievable() -> None:
    """F8-02: FR-06/07, AC-05.2 retained history; AC-05.3 repeat still rejected."""
    data_store, appointment_service = fresh_session()
    booked = appointment_service.book_appointment('A1', 'P1', 'D1', BOOKING_TIME)

    cancelled = appointment_service.cancel_appointment('A1')

    assert cancelled is booked
    assert cancelled.status is AppointmentStatus.CANCELLED
    assert data_store.find_appointment('A1') is booked
    assert appointment_service.find_appointment('A1') is booked
    assert data_store.list_appointments() == [booked]
    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')
    assert booked.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [booked]
