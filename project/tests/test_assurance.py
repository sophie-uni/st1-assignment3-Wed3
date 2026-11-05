"""Stage 11 assurance tests for session isolation and workflow interactions."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


ORIGINAL_TIME = datetime(2026, 10, 1, 9, 0)
RESCHEDULED_TIME = datetime(2026, 10, 1, 10, 0)


def test_patient_lookup_is_limited_to_its_shared_store() -> None:
    first_store = SmartCareDataStore()
    second_store = SmartCareDataStore()
    first_service = PatientService(first_store)
    second_service = PatientService(second_store)
    second_patient = second_service.register_patient('P1', 'Jordan Example')

    with pytest.raises(LookupError):
        first_service.find_patient('P1')

    assert first_store.find_patient('P1') is None
    assert first_store.list_patients() == []
    assert second_service.find_patient('P1') is second_patient


def test_reschedule_cancel_history_and_listing_use_fresh_results() -> None:
    store = SmartCareDataStore()
    patients = PatientService(store)
    patient_one = patients.register_patient('P1', 'Alex Example')
    patients.register_patient('P2', 'Jordan Example')
    practitioners = PractitionerService(store)
    practitioner = practitioners.register_practitioner(
        'D1',
        'Taylor Example',
        'General',
    )
    appointments = AppointmentService(store)
    moved = appointments.book_appointment(
        'A1',
        'P1',
        'D1',
        ORIGINAL_TIME,
    )

    appointments.reschedule_appointment('A1', RESCHEDULED_TIME)
    appointments.cancel_appointment('A1')
    replacement = appointments.book_appointment(
        'A2',
        'P2',
        'D1',
        ORIGINAL_TIME,
    )

    first_list = appointments.list_practitioner_appointments('D1')
    assert first_list == [replacement, moved]
    assert first_list[1] is moved
    assert moved.patient is patient_one
    assert moved.practitioner is practitioner
    assert moved.date_time == RESCHEDULED_TIME
    assert moved.status is AppointmentStatus.CANCELLED
    assert store.find_appointment('A1') is moved
    assert appointments.list_practitioner_appointments(
        'D1',
        AppointmentStatus.SCHEDULED,
    ) == [replacement]

    first_list.clear()
    second_list = appointments.list_practitioner_appointments('D1')

    assert second_list == [replacement, moved]
    assert second_list is not first_list
    assert store.list_appointments() == [moved, replacement]


def test_unknown_practitioner_error_does_not_echo_input() -> None:
    appointments = AppointmentService(SmartCareDataStore())

    with pytest.raises(LookupError) as error:
        appointments.list_practitioner_appointments('UNREGISTERED-ID')

    assert str(error.value) == 'Practitioner not found'
    assert 'UNREGISTERED-ID' not in str(error.value)
