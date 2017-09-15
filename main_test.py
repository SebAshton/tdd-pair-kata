from main import Gate
import os

def test_can_create_a_gate():
    gate = Gate()
    assert gate.current_state() == "locked"

def test_can_unlock_with_a_coin():
    gate = Gate()
    gate.coin()

    assert gate.current_state() == "unlocked"

def test_can_unlock_and_pass_through_a_gate():
    gate = Gate()
    gate.coin()
    gate.through()

    assert gate.current_state() == "locked"

def test_adding_listener_for_an_action(mocker):
    stub = mocker.stub(name='on_locked_coin')
    gate = Gate()
    gate.listen(state="locked", event="coin", action=stub)
    gate.coin()

    stub.assert_called_once_with(gate)

def test_will_alarm_when_passing_through_a_locked_gate(mocker):
    gate = Gate()
    mocker.spy(gate, 'alarm')

    gate.through()

    assert gate.alarm.call_count == 1

def test_will_thank_you_when_pay_twice(mocker):
    gate = Gate(current_state="unlocked")
    mocker.spy(gate, 'thank_you')

    gate.coin()

    assert gate.thank_you.call_count == 1

def test_will_forbid_entry_when_unlocked_and_powering_off():
    gate = Gate(current_state="unlocked")
    gate.power()

    assert gate.current_state() == "no_entry"

def test_will_forbid_entry_when_locked_and_powering_off():
    gate = Gate()
    gate.power()

    assert gate.current_state() == "no_entry"

def test_will_lock_when_powering_on():
    gate = Gate(current_state="no_entry")
    gate.power()

    assert gate.current_state() == "locked"

def test_will_alarm_when_entering_and_powered_off(mocker):
    gate = Gate(current_state="no_entry")
    mocker.spy(gate, 'alarm')

    gate.through()

    assert gate.alarm.call_count == 1
