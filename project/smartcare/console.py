"""Console helpers and a small runnable starting demonstration."""


import re
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM; raise ValueError for invalid input."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', text
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')
    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM',
        ) from None


def format_appointment(appointment: Appointment) -> str:
    """Return readable synthetic appointment details without changing
    state.
    """
    return (
        f'{appointment.appointment_id}: '
        f'{appointment.patient.patient_id} with '
        f'{appointment.practitioner.practitioner_id}, '
        f'{appointment.date_time:%Y-%m-%d %H:%M}, {appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate supplied registration and booking using synthetic
    records.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'DR1',
        'Taylor Example',
        'General practice',
    )
    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    print('Session-only data: records are lost on exit.')


def run_menu() -> None:
    """Stage 9: implement the register/find/book/cancel/list/exit menu.

    Call services, recover from expected input errors, and keep this
    session's data until exit. main.py reports the incomplete menu
    without crashing.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    actions = {
        '1': 'Register patient',
        '2': 'Register practitioner',
        '3': 'Find patient',
        '4': 'Find practitioner',
        '5': 'Book appointment',
        '6': 'Find appointment',
        '7': 'Cancel appointment',
        '8': 'List practitioner appointments',
        '9': 'Exit',
    }

    while True:
        print('\nSmartCare appointment menu')
        for choice, label in actions.items():
            print(f'{choice}. {label}')

        try:
            choice = input('Choice: ').strip()
            if choice == '1':
                patient = patients.register_patient(
                    input('Patient ID: '),
                    input('Patient name: '),
                )
                print(f'Registered patient {patient.patient_id}.')
            elif choice == '2':
                practitioner = practitioners.register_practitioner(
                    input('Practitioner ID: '),
                    input('Practitioner name: '),
                    input('Specialty: '),
                )
                print(f'Registered practitioner {practitioner.practitioner_id}.')
            elif choice == '3':
                patient = patients.find_patient(input('Patient ID: '))
                print(f'{patient.patient_id}: {patient.name}')
            elif choice == '4':
                practitioner = practitioners.find_practitioner(
                    input('Practitioner ID: ')
                )
                print(
                    f'{practitioner.practitioner_id}: {practitioner.name}, '
                    f'{practitioner.specialty}'
                )
            elif choice == '5':
                appointment = appointments.book_appointment(
                    input('Appointment ID: '),
                    input('Patient ID: '),
                    input('Practitioner ID: '),
                    parse_date_time(
                        input('Date/time (YYYY-MM-DD HH:MM): ')
                    ),
                )
                print(f'Booked {format_appointment(appointment)}')
            elif choice == '6':
                appointment = appointments.find_appointment(
                    input('Appointment ID: ')
                )
                print(format_appointment(appointment))
            elif choice == '7':
                appointment = appointments.cancel_appointment(
                    input('Appointment ID: ')
                )
                print(f'Cancelled {format_appointment(appointment)}')
            elif choice == '8':
                practitioner_id = input('Practitioner ID: ')
                status_text = input(
                    'Status (scheduled/cancelled/completed, or blank for all): '
                ).strip().lower()
                if status_text in ('', 'all'):
                    status = None
                else:
                    try:
                        status = AppointmentStatus(status_text)
                    except ValueError:
                        raise ValueError(
                            'Status must be scheduled, cancelled, completed, '
                            'or blank for all.'
                        ) from None
                listed = appointments.list_practitioner_appointments(
                    practitioner_id,
                    status,
                )
                if listed:
                    for appointment in listed:
                        print(format_appointment(appointment))
                else:
                    print('No appointments found.')
            elif choice == '9':
                print('Exiting. Session-only data will be lost.')
                return
            else:
                print('Invalid choice. Select a number from 1 to 9.')
        except (ValueError, LookupError) as error:
            print(f'Error: {error}')
        except EOFError:
            print('Input ended. Exiting. Session-only data will be lost.')
            return
