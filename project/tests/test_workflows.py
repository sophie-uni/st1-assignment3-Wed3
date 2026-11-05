"""End-to-end interactive menu workflow tests."""

import builtins

from smartcare.console import run_menu


def provide_menu_inputs(monkeypatch, responses: list[str]) -> None:
    """Replace console input with a fixed, reproducible response sequence."""
    remaining = iter(responses)
    monkeypatch.setattr(
        builtins,
        'input',
        lambda _prompt='': next(remaining),
    )


def test_menu_completes_register_book_cancel_list_and_exit(
    monkeypatch,
    capsys,
) -> None:
    provide_menu_inputs(
        monkeypatch,
        [
            '1', 'P1', 'Alex Example',
            '2', 'D1', 'Taylor Example', 'General',
            '1', 'P2', 'Jordan Example',
            '2', 'D2', 'Morgan Example', 'Cardiology',
            '3', 'P1',
            '4', 'D2',
            '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
            '5', 'A2', 'P2', 'D1', '2026-10-01 09:00',
            '5', 'A2', 'P2', 'D2', '2026-10-01 09:00',
            '6', 'A1',
            '8', 'D1', '',
            '7', 'A1',
            '6', 'A1',
            '8', 'D1', 'cancelled',
            '5', 'A3', 'P2', 'D1', '2026-10-01 09:00',
            '8', 'D1', '',
            '9',
        ],
    )

    run_menu()

    output = capsys.readouterr().out
    assert 'Registered patient P1.' in output
    assert 'Registered practitioner D2.' in output
    assert 'P1: Alex Example' in output
    assert 'D2: Morgan Example, Cardiology' in output
    assert 'Practitioner already has a SCHEDULED appointment' in output
    assert 'Booked A2: P2 with D2, 2026-10-01 09:00, scheduled' in output
    assert 'Cancelled A1: P1 with D1, 2026-10-01 09:00, cancelled' in output
    assert 'A1: P1 with D1, 2026-10-01 09:00, scheduled' in output
    assert 'A1: P1 with D1, 2026-10-01 09:00, cancelled' in output
    assert 'A3: P2 with D1, 2026-10-01 09:00, scheduled' in output
    assert 'Exiting. Session-only data will be lost.' in output


def test_menu_recovers_from_invalid_input_without_losing_session(
    monkeypatch,
    capsys,
) -> None:
    provide_menu_inputs(
        monkeypatch,
        [
            'unknown',
            '1', '', 'Blank ID',
            '1', 'P1', 'Alex Example',
            '1', 'P1', 'Replacement Name',
            '2', 'D1', 'Taylor Example', 'General',
            '3', 'missing',
            '4', 'D999',
            '5', 'A9', 'missing', 'D1', '2026-10-01 09:00',
            '5', 'A9', 'P1', 'D1', 'not-a-date',
            '5', 'A9', 'P1', 'D1', '2026-02-30 09:00',
            '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
            '5', 'A1', 'P1', 'D1', '2026-10-01 10:00',
            '8', 'D1', 'unknown',
            '8', 'D999', '',
            '6', 'A1',
            '7', 'A1',
            '7', 'A1',
            '6', 'A1',
            '9',
        ],
    )

    run_menu()

    output = capsys.readouterr().out
    assert 'Invalid choice. Select a number from 1 to 9.' in output
    assert 'Patient ID cannot be blank' in output
    assert 'Patient ID already exists' in output
    assert 'Patient not found' in output
    assert 'Practitioner not found' in output
    assert 'D999' not in output
    assert 'Use date/time format YYYY-MM-DD HH:MM' in output
    assert 'Invalid calendar date/time' in output
    assert 'Appointment ID already exists' in output
    assert 'Status must be scheduled, cancelled, completed' in output
    assert output.count('Only SCHEDULED appointments may be cancelled') == 1
    assert 'A1: P1 with D1, 2026-10-01 09:00, scheduled' in output
    assert 'A1: P1 with D1, 2026-10-01 09:00, cancelled' in output
    assert 'Exiting. Session-only data will be lost.' in output