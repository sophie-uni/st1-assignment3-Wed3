"""Stage 9 select_appointments tests: QRY-01 to QRY-03, FP-01 and FP-02."""

from datetime import datetime

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import select_appointments


TIE_TIME = datetime(2026, 10, 1, 9, 0)


def build_source() -> list[Appointment]:
    """Return a deliberately unsorted list for practitioners D1 and D2."""
    p1 = Patient('P1', 'Alex Example')
    p2 = Patient('P2', 'Jordan Example')
    d1 = Practitioner('D1', 'Taylor Example', 'General practice')
    d2 = Practitioner('D2', 'Morgan Example', 'Cardiology')
    return [
        Appointment('A3', p1, d1, datetime(2026, 10, 2, 10, 0)),
        Appointment('B1', p2, d2, datetime(2026, 10, 1, 8, 0)),
        Appointment(
            'A4', p2, d1, TIE_TIME, AppointmentStatus.COMPLETED,
        ),
        Appointment('A2', p1, d1, TIE_TIME),
        Appointment('A9', p2, d1, datetime(2026, 9, 30, 8, 0)),
        Appointment(
            'B2', p1, d2, TIE_TIME, AppointmentStatus.CANCELLED,
        ),
        Appointment(
            'A1', p2, d1, TIE_TIME, AppointmentStatus.CANCELLED,
        ),
    ]


def ids(appointments: list[Appointment]) -> list[str]:
    """Return appointment IDs in list order."""
    return [appointment.appointment_id for appointment in appointments]


def snapshot(appointments: list[Appointment]) -> list[tuple]:
    """Record list order, object identity and every relevant field."""
    return [
        (
            id(appointment),
            appointment.appointment_id,
            appointment.patient,
            appointment.practitioner,
            appointment.date_time,
            appointment.status,
        )
        for appointment in appointments
    ]


# QRY-01 practitioner isolation


def test_qry01_selects_only_requested_practitioner() -> None:
    """T-QRY01-1: D1 results exclude D2, and D2 is a working control."""
    source = build_source()

    d1_result = select_appointments(source, 'D1')
    d2_result = select_appointments(source, 'D2')

    assert ids(d1_result) == ['A9', 'A1', 'A2', 'A4', 'A3']
    assert all(a.practitioner.practitioner_id == 'D1' for a in d1_result)
    assert ids(d2_result) == ['B1', 'B2']
    assert set(ids(d1_result)).isdisjoint(ids(d2_result))


def test_qry01_practitioner_without_appointments_gives_empty_list() -> None:
    """T-QRY01-2: the pure query does not validate; no match is []."""
    assert select_appointments(build_source(), 'D9') == []


# QRY-02 status filtering


def test_qry02_default_includes_every_status() -> None:
    """T-QRY02-1: omitted status keeps SCHEDULED, CANCELLED and COMPLETED."""
    source = build_source()

    result = select_appointments(source, 'D1')

    assert {a.status for a in result} == set(AppointmentStatus)
    assert select_appointments(source, 'D1', None) == result


@pytest.mark.parametrize(
    ('status', 'expected_ids'),
    [
        (AppointmentStatus.SCHEDULED, ['A9', 'A2', 'A3']),
        (AppointmentStatus.CANCELLED, ['A1']),
        (AppointmentStatus.COMPLETED, ['A4']),
    ],
)
def test_qry02_each_explicit_status(
    status: AppointmentStatus,
    expected_ids: list[str],
) -> None:
    """T-QRY02-2: each enum status keeps only that status for D1."""
    result = select_appointments(build_source(), 'D1', status)

    assert ids(result) == expected_ids
    assert all(appointment.status is status for appointment in result)


def test_qry02_status_with_no_match_gives_empty_list() -> None:
    """T-QRY02-3: D2 has no COMPLETED appointment, so the result is []."""
    result = select_appointments(
        build_source(), 'D2', AppointmentStatus.COMPLETED,
    )

    assert result == []


# QRY-03 ordering, tie-break and unchanged source


def test_qry03_orders_by_date_time_then_id_without_changing_source() -> None:
    """T-QRY03-1: earlier date wins; equal 09:00 times sort A1, A2, A4."""
    source = build_source()
    before = snapshot(source)

    result = select_appointments(source, 'D1')

    assert ids(result) == ['A9', 'A1', 'A2', 'A4', 'A3']
    times = [appointment.date_time for appointment in result]
    assert times == sorted(times)
    assert snapshot(source) == before
    assert ids(source) == ['A3', 'B1', 'A4', 'A2', 'A9', 'B2', 'A1']


def test_qry03_date_time_outranks_appointment_id() -> None:
    """T-QRY03-2: A9 is first despite its ID because its date is earliest."""
    result = select_appointments(build_source(), 'D1')

    assert result[0].appointment_id == 'A9'
    assert result[-1].appointment_id == 'A3'


# FP-01 repeatable, no hidden state or I/O


def test_fp01_repeated_calls_give_equal_results_and_fresh_lists() -> None:
    """T-FP01-1: unchanged inputs give the same answer every time."""
    source = build_source()
    before = snapshot(source)

    first = select_appointments(source, 'D1', AppointmentStatus.SCHEDULED)
    second = select_appointments(source, 'D1', AppointmentStatus.SCHEDULED)
    third = select_appointments(source, 'D1', AppointmentStatus.SCHEDULED)

    assert ids(first) == ids(second) == ids(third) == ['A9', 'A2', 'A3']
    assert first is not second and second is not third
    assert snapshot(source) == before


def test_fp01_query_performs_no_input_or_output(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """T-FP01-2: the query neither prints nor asks for input."""
    def fail_input(*_: object) -> str:
        raise AssertionError('query must not read input')

    monkeypatch.setattr('builtins.input', fail_input)

    select_appointments(build_source(), 'D1')

    captured = capsys.readouterr()
    assert captured.out == '' and captured.err == ''


# FP-02 distinct returned lists, shared unchanged objects


def test_fp02_empty_source_returns_new_empty_list() -> None:
    """T-FP02-1: an empty source gives a different empty list."""
    source: list[Appointment] = []

    result = select_appointments(source, 'D1')

    assert result == []
    assert result is not source


def test_fp02_already_sorted_source_returns_new_list() -> None:
    """T-FP02-2: sorted D1-only input is not returned as the same list."""
    already_sorted = select_appointments(build_source(), 'D1')
    before = snapshot(already_sorted)

    result = select_appointments(already_sorted, 'D1')

    assert result is not already_sorted
    assert ids(result) == ids(already_sorted)
    assert snapshot(already_sorted) == before


def test_fp02_unsorted_source_reuses_same_unchanged_objects() -> None:
    """T-FP02-3: the new list holds the source objects, not copies."""
    source = build_source()
    before = snapshot(source)

    result = select_appointments(source, 'D1')

    assert result is not source
    for appointment in result:
        assert any(appointment is original for original in source)
    assert snapshot(source) == before