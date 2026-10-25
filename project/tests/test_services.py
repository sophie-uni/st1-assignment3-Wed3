from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

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