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
    patient = service.register_patient("P1", "Alex Example")

    assert service.find_patient("P1") is patient


def test_find_patient_raises_for_unknown_id() -> None:
    service = PatientService(SmartCareDataStore())

    with pytest.raises(LookupError):
        service.find_patient("missing")


def test_find_practitioner_returns_registered_practitioner() -> None:
    store = SmartCareDataStore()
    service = PractitionerService(store)
    practitioner = service.register_practitioner(
        "D1", "Taylor Example", "General"
    )

    assert service.find_practitioner("D1") is practitioner


def test_find_practitioner_raises_for_unknown_id() -> None:
    service = PractitionerService(SmartCareDataStore())

    with pytest.raises(LookupError):
        service.find_practitioner("missing")


def test_cancel_appointment_returns_and_retains_cancelled_appointment() -> None:
    store = SmartCareDataStore()
    PatientService(store).register_patient("P1", "Alex Example")
    PractitionerService(store).register_practitioner(
        "D1", "Taylor Example", "General"
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

"""Extend the Stage06 service tests"""
"""check patient and practitioner lookup; 
valid booking and appointment lookup; 
practitioner conflicts and valid alternatives; 
cancellation and retained history. 
Check duplicate patient, practitioner and appointment IDs do not overwrite the original records. 
Check unknown participants, invalid values and rejected operations leave the existing state unchanged."""