from datetime import datetime, timezone

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)

BOOKING_TIME = datetime(2026, 10, 1, 9, 0)



"""Stage06 TODO service tests"""
def test_find_patient_returns_registered_patient() -> None:
    store = SmartCareDataStore()
    service = PatientService(store)
    patient = service.register_patient("P1", "Sophie Jiang")

    assert service.find_patient("P1") is patient


def test_find_patient_raises_for_unknown_id() -> None:
    service = PatientService(SmartCareDataStore())

    with pytest.raises(LookupError):
        service.find_patient("missing")


def test_find_practitioner_returns_registered_practitioner() -> None:
    store = SmartCareDataStore()
    service = PractitionerService(store)
    practitioner = service.register_practitioner(
        "D1", "Sophie Doctor", "General"
    )

    assert service.find_practitioner("D1") is practitioner


def test_find_practitioner_raises_for_unknown_id() -> None:
    service = PractitionerService(SmartCareDataStore())

    with pytest.raises(LookupError):
        service.find_practitioner("missing")


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


def test_cancel_unknown_appointment_raises() -> None:
    service = AppointmentService(SmartCareDataStore())

    with pytest.raises(LookupError):
        service.cancel_appointment("missing")


def test_cancelling_appointment_twice_raises_without_changing_state() -> None:
    store = SmartCareDataStore()
    PatientService(store).register_patient("P1", "Alex Example")
    PractitionerService(store).register_practitioner(
        "D1", "Taylor Example", "General"
    )
    service = AppointmentService(store)
    appointment = service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 10, 1, 9)
    )
    service.cancel_appointment("A1")

    with pytest.raises(ValueError):
        service.cancel_appointment("A1")

    assert appointment.status is AppointmentStatus.CANCELLED
    assert store.find_appointment("A1") is appointment

"""Stage07 service tests"""
"""T-FR01-1"""
"""AC-01.1 - Valid required patient data with an unused ID is stored."""
def test_register_patient_stores_valid_patient() -> None:
    store = SmartCareDataStore()
    service = PatientService(store)

    patient = service.register_patient("P1", "Sophie Jiang")

    assert patient.patient_id == "P1"
    assert patient.name == "Sophie Jiang"
    assert store.find_patient("P1") is patient
    assert store.list_patients() == [patient]

"""T-FR01-2"""
"""AC-01.2 - Registration with an existing patient ID is rejected."""
def test_register_patient_rejects_duplicate_id() -> None:
    store = SmartCareDataStore()
    service = PatientService(store)
    original = service.register_patient("P1", "Sophie Jiang")

    with pytest.raises(ValueError):
        service.register_patient("P1", "David Jiang")

    assert store.find_patient("P1") is original
    assert original.name == "Sophie Jiang"
    assert store.list_patients() == [original]


"""T-FR07"""
    # T-FR07-3
def test_blank_patient_id_rejected_by_service() -> None:
    store = SmartCareDataStore()
    service = PatientService(store)

    with pytest.raises(ValueError):
        service.register_patient("", "Alex Example")

    assert store.list_patients() == []

    # T-FR07-4
def test_new_appointment_starts_scheduled_by_service() -> None:
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P1", "Alex Example")
    practitioner_service.register_practitioner(
        "D1",
        "Taylor Example",
        "General",
    )

    appointment = appointment_service.book_appointment(
        "A1",
        "P1",
        "D1",
        datetime(2026, 10, 1, 9, 0),
    )

    assert appointment.status is AppointmentStatus.SCHEDULED
    assert store.find_appointment("A1") is appointment



# Hassan: FR-05 Prevent practitioner conflict

CONFLICT_TIME = datetime(2026, 10, 1, 9, 0)


def conflict_setup() -> tuple[SmartCareDataStore, AppointmentService]:
    """Create a fresh store with patients P1, P2 and practitioners D1, D2."""
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)
    patient_service.register_patient('P1', 'Alex Example')
    patient_service.register_patient('P2', 'Jordan Example')
    practitioner_service = PractitionerService(data_store)
    practitioner_service.register_practitioner('D1', 'Taylor Example', 'General')
    practitioner_service.register_practitioner('D2', 'Morgan Example', 'General')
    return data_store, AppointmentService(data_store)


def test_same_practitioner_same_time_is_rejected() -> None:
    """T-FR05-1: a second D1 booking at the exact SCHEDULED time is rejected."""
    data_store, appointment_service = conflict_setup()
    first = appointment_service.book_appointment('A1', 'P1', 'D1', CONFLICT_TIME)

    with pytest.raises(ValueError):
        appointment_service.book_appointment('A2', 'P2', 'D1', CONFLICT_TIME)

    assert data_store.find_appointment('A2') is None
    assert data_store.list_appointments() == [first]
    assert first.status is AppointmentStatus.SCHEDULED


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


@pytest.mark.parametrize(
    'nearby_time',
    [datetime(2026, 10, 1, 8, 59), datetime(2026, 10, 1, 9, 1)],
)
def test_same_practitioner_one_minute_apart_is_allowed(
    nearby_time: datetime,
) -> None:
    """T-FR05-3: only the exact time conflicts; one minute either side is free."""
    data_store, appointment_service = conflict_setup()
    first = appointment_service.book_appointment('A1', 'P1', 'D1', CONFLICT_TIME)

    second = appointment_service.book_appointment('A2', 'P2', 'D1', nearby_time)

    assert data_store.find_appointment('A2') is second
    assert second.date_time == nearby_time
    assert second.status is AppointmentStatus.SCHEDULED
    assert first.status is AppointmentStatus.SCHEDULED


def test_cancelled_appointment_does_not_block_slot() -> None:
    """T-FR05-4: a CANCELLED booking no longer occupies the D1 time slot."""
    data_store, appointment_service = conflict_setup()
    first = appointment_service.book_appointment('A1', 'P1', 'D1', CONFLICT_TIME)
    appointment_service.cancel_appointment('A1')

    second = appointment_service.book_appointment(
        'A2',
        'P2',
        'D1',
        CONFLICT_TIME,
    )

    assert data_store.find_appointment('A2') is second
    assert second.status is AppointmentStatus.SCHEDULED
    assert data_store.find_appointment('A1') is first
    assert first.status is AppointmentStatus.CANCELLED


# Devam: FR-06 Cancel appointment


def cancellation_setup() -> tuple[
    SmartCareDataStore,
    AppointmentService,
    Appointment,
]:
    """Create a fresh store holding one SCHEDULED appointment A1."""
    data_store = SmartCareDataStore()
    PatientService(data_store).register_patient('P1', 'Alex Example')
    PractitionerService(data_store).register_practitioner(
        'D1',
        'Taylor Example',
        'General',
    )
    appointment_service = AppointmentService(data_store)
    appointment = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9, 0),
    )
    return data_store, appointment_service, appointment


def test_cancel_appointment_returns_same_cancelled_object() -> None:
    """T-FR06-1: the service returns the booked object, now CANCELLED."""
    _, appointment_service, appointment = cancellation_setup()

    cancelled = appointment_service.cancel_appointment('A1')

    assert cancelled is appointment
    assert cancelled.status is AppointmentStatus.CANCELLED


def test_repeated_service_cancellation_is_rejected() -> None:
    """T-FR06-2: cancelling A1 twice raises ValueError and changes nothing."""
    data_store, appointment_service, appointment = cancellation_setup()
    appointment_service.cancel_appointment('A1')

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')

    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [appointment]


def test_cancel_unknown_appointment_raises_lookup_error() -> None:
    """T-FR06-3: a valid but unknown ID raises LookupError; A1 is untouched."""
    data_store, appointment_service, appointment = cancellation_setup()

    with pytest.raises(LookupError):
        appointment_service.cancel_appointment('A9')

    assert appointment.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [appointment]


def test_cancel_completed_appointment_through_service_is_rejected() -> None:
    """T-FR06-4: the service cannot cancel a COMPLETED appointment."""
    data_store = SmartCareDataStore()
    patient = PatientService(data_store).register_patient('P1', 'Alex Example')
    practitioner = PractitionerService(data_store).register_practitioner(
        'D1',
        'Taylor Example',
        'General',
    )
    completed = Appointment(
        'A1',
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.COMPLETED,
    )
    data_store.add_appointment(completed)

    with pytest.raises(ValueError):
        AppointmentService(data_store).cancel_appointment('A1')

    assert completed.status is AppointmentStatus.COMPLETED
    assert data_store.find_appointment('A1') is completed


    # Stage 8 refactor guard: booking participant lookup behaviour

    def test_book_unknown_practitioner_is_rejected() -> None:
        """R8-1: an unknown practitioner raises LookupError and nothing is stored."""
        data_store = SmartCareDataStore()
        PatientService(data_store).register_patient('P1', 'Alex Example')
        appointment_service = AppointmentService(data_store)

        with pytest.raises(LookupError):
            appointment_service.book_appointment(
                'A1',
                'P1',
                'D9',
                datetime(2026, 10, 1, 9, 0),
            )

        assert data_store.list_appointments() == []

    def test_book_blank_practitioner_id_is_rejected() -> None:
        """R8-2: a blank practitioner ID raises ValueError and nothing is stored."""
        data_store = SmartCareDataStore()
        PatientService(data_store).register_patient('P1', 'Alex Example')
        appointment_service = AppointmentService(data_store)

        with pytest.raises(ValueError):
            appointment_service.book_appointment(
                'A1',
                'P1',
                '   ',
                datetime(2026, 10, 1, 9, 0),
            )

        assert data_store.list_appointments() == []