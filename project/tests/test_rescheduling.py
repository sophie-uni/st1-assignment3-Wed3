"""Focused tests for Stage 10 appointment rescheduling requirements."""

from datetime import datetime, timezone

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


ORIGINAL_TIME = datetime(2026, 10, 1, 9, 0)
NEW_TIME = datetime(2026, 10, 1, 10, 0)


def build_system() -> tuple[
    SmartCareDataStore,
    Patient,
    Patient,
    Practitioner,
    Practitioner,
    AppointmentService,
]:
    """Create a fresh store with two patients and two practitioners."""
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    patient_one = patient_service.register_patient('P1', 'Alex Example')
    patient_two = patient_service.register_patient('P2', 'Jordan Example')
    practitioner_service = PractitionerService(store)
    practitioner_one = practitioner_service.register_practitioner(
        'D1',
        'Taylor Example',
        'General',
    )
    practitioner_two = practitioner_service.register_practitioner(
        'D2',
        'Morgan Example',
        'Cardiology',
    )
    return (
        store,
        patient_one,
        patient_two,
        practitioner_one,
        practitioner_two,
        AppointmentService(store),
    )


def snapshot(store: SmartCareDataStore) -> tuple[tuple, ...]:
    """Capture stored appointment identities, links, fields, and order."""
    return tuple(
        (
            id(appointment),
            appointment.appointment_id,
            appointment.patient,
            appointment.practitioner,
            appointment.date_time,
            appointment.status,
        )
        for appointment in store.list_appointments()
    )


@pytest.mark.parametrize(
    'invalid_date_time',
    [
        '2026-10-01 10:00',
        None,
        datetime(2026, 10, 1, 10, 0, tzinfo=timezone.utc),
        datetime(2026, 10, 1, 10, 0, 1),
        datetime(2026, 10, 1, 10, 0, 0, 1),
    ],
)
def test_domain_rejects_invalid_datetime_without_mutation(
    invalid_date_time,
) -> None:
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    appointment = Appointment(
        'A1',
        patient,
        practitioner,
        ORIGINAL_TIME,
    )

    with pytest.raises(ValueError):
        appointment.reschedule(invalid_date_time)

    assert appointment.appointment_id == 'A1'
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == ORIGINAL_TIME
    assert appointment.status is AppointmentStatus.SCHEDULED


@pytest.mark.parametrize(
    'status',
    [AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED],
)
def test_domain_rejects_rescheduling_terminal_status_without_mutation(
    status: AppointmentStatus,
) -> None:
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    appointment = Appointment(
        'A1',
        patient,
        practitioner,
        ORIGINAL_TIME,
        status,
    )

    with pytest.raises(ValueError, match='Only SCHEDULED'):
        appointment.reschedule(ORIGINAL_TIME)

    assert appointment.appointment_id == 'A1'
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == ORIGINAL_TIME
    assert appointment.status is status


def test_service_moves_same_stored_object_and_listing_uses_new_time() -> None:
    store, patient_one, _, practitioner_one, _, service = build_system()
    appointment = service.book_appointment(
        'A1',
        'P1',
        'D1',
        ORIGINAL_TIME,
    )
    later = service.book_appointment(
        'A2',
        'P1',
        'D1',
        datetime(2026, 10, 1, 11, 0),
    )

    result = service.reschedule_appointment('A1', NEW_TIME)

    assert result is appointment
    assert result.appointment_id == 'A1'
    assert result.patient is patient_one
    assert result.practitioner is practitioner_one
    assert result.date_time == NEW_TIME
    assert result.status is AppointmentStatus.SCHEDULED
    assert store.find_appointment('A1') is appointment
    assert store.list_appointments() == [appointment, later]
    assert service.list_practitioner_appointments('D1') == [
        appointment,
        later,
    ]


def test_valid_unknown_appointment_id_raises_lookup_error_without_mutation() -> None:
    store, _, _, _, _, service = build_system()
    appointment = service.book_appointment(
        'A1',
        'P1',
        'D1',
        ORIGINAL_TIME,
    )
    before = snapshot(store)

    with pytest.raises(LookupError):
        service.reschedule_appointment('A9', NEW_TIME)

    assert snapshot(store) == before
    assert store.find_appointment('A1') is appointment


@pytest.mark.parametrize('invalid_id', ['', '   ', None, 123])
def test_invalid_appointment_id_raises_value_error_without_mutation(
    invalid_id: object,
) -> None:
    store, _, _, _, _, service = build_system()
    service.book_appointment('A1', 'P1', 'D1', ORIGINAL_TIME)
    before = snapshot(store)

    with pytest.raises(ValueError):
        service.reschedule_appointment(invalid_id, NEW_TIME)

    assert snapshot(store) == before


@pytest.mark.parametrize(
    'invalid_date_time',
    [
        '2026-10-01 10:00',
        None,
        datetime(2026, 10, 1, 10, 0, tzinfo=timezone.utc),
        datetime(2026, 10, 1, 10, 0, 1),
        datetime(2026, 10, 1, 10, 0, 0, 1),
    ],
)
def test_service_rejects_invalid_datetime_without_mutating_store(
    invalid_date_time,
) -> None:
    store, _, _, _, _, service = build_system()
    service.book_appointment('A1', 'P1', 'D1', ORIGINAL_TIME)
    before = snapshot(store)

    with pytest.raises(ValueError):
        service.reschedule_appointment('A1', invalid_date_time)

    assert snapshot(store) == before


def test_same_practitioner_conflict_is_rejected_without_mutation() -> None:
    store, _, _, _, _, service = build_system()
    target = service.book_appointment('A1', 'P1', 'D1', ORIGINAL_TIME)
    conflicting = service.book_appointment(
        'A2',
        'P2',
        'D1',
        NEW_TIME,
    )
    before = snapshot(store)

    with pytest.raises(ValueError, match='Practitioner already has'):
        service.reschedule_appointment('A1', NEW_TIME)

    assert snapshot(store) == before
    assert store.find_appointment('A1') is target
    assert store.find_appointment('A2') is conflicting


def test_different_practitioner_at_new_time_is_allowed() -> None:
    store, _, _, _, practitioner_two, service = build_system()
    target = service.book_appointment('A1', 'P1', 'D1', ORIGINAL_TIME)
    other_practitioner = service.book_appointment(
        'A2',
        'P2',
        'D2',
        NEW_TIME,
    )

    result = service.reschedule_appointment('A1', NEW_TIME)

    assert result is target
    assert result.date_time == NEW_TIME
    assert other_practitioner.practitioner is practitioner_two
    assert other_practitioner.date_time == NEW_TIME
    assert store.list_appointments() == [target, other_practitioner]


def test_same_time_noop_excludes_target_from_conflict_check() -> None:
    store, _, _, _, _, service = build_system()
    appointment = service.book_appointment(
        'A1',
        'P1',
        'D1',
        ORIGINAL_TIME,
    )
    before = snapshot(store)

    result = service.reschedule_appointment('A1', ORIGINAL_TIME)

    assert result is appointment
    assert result.date_time == ORIGINAL_TIME
    assert snapshot(store) == before


@pytest.mark.parametrize(
    'status',
    [AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED],
)
def test_service_rejects_terminal_target_even_for_same_time(
    status: AppointmentStatus,
) -> None:
    store, patient, _, practitioner, _, service = build_system()
    appointment = Appointment(
        'A1',
        patient,
        practitioner,
        ORIGINAL_TIME,
        status,
    )
    store.add_appointment(appointment)
    before = snapshot(store)

    with pytest.raises(ValueError, match='Only SCHEDULED'):
        service.reschedule_appointment('A1', ORIGINAL_TIME)

    assert snapshot(store) == before


def test_successful_move_releases_old_slot() -> None:
    store, _, patient_two, _, _, service = build_system()
    moved = service.book_appointment('A1', 'P1', 'D1', ORIGINAL_TIME)

    service.reschedule_appointment('A1', NEW_TIME)
    replacement = service.book_appointment(
        'A2',
        'P2',
        'D1',
        ORIGINAL_TIME,
    )

    assert replacement.patient is patient_two
    assert replacement.date_time == ORIGINAL_TIME
    assert store.find_appointment('A1') is moved
    assert moved.date_time == NEW_TIME
    assert store.find_appointment('A2') is replacement
    assert service.list_practitioner_appointments('D1') == [
        replacement,
        moved,
    ]