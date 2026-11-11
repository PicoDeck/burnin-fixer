"""Burn-In Fixer in the PicoDeck simulator, through the real main.lua.

The pad tests drive it from the simulator's test gamepad (sim.pad), the path
a Bluetooth controller takes: it reaches picocalc.gamepad only, never
picocalc.input. A drawText spy put before main.lua logs the status bar's two
labels when they change: MODE:<name - detail> (left) and HINT:<hint> (right,
without the running time).
"""
import time

import pytest

from conftest import APP, stage

_SPY = r"""
local dt, last = picocalc.display.drawText, {}
picocalc.display.drawText = function(x, y, t, ...)
  if y == 306 then
    local key, text = 'MODE', t
    if x ~= 2 then key, text = 'HINT', (t:gsub('^%d+:%d+%s*', '')) end
    if last[key] ~= text then last[key] = text; picocalc.sys.log(key .. ':' .. text) end
  end
  return dt(x, y, t, ...)
end
"""


def _launch(sim, rebind=None):
    """Stage with the spy, connect the test pad (nothing held), launch, and
    wait for the first mode. Returns the log seq the launch started at."""
    stage(sim, rebind=rebind, prepend=_SPY)
    sim.pad("none")
    seq = sim.get_log_buffer(tail=1).get("next_seq", 0)
    sim.launch_app(APP)
    sim.wait_for_log(r"^MODE:Solid Colors", timeout=10, since_seq=seq)
    return seq


def _exited(sim):
    assert sim.wait_for_exit(timeout=10)["result"] == "returned"


def _modes(sim, since):
    return [e["text"] for e in sim.get_log_lines(since) if e["text"].startswith("MODE:")]


def test_burnin_fixer_enter_and_esc_still_work(simulator):
    sim = simulator
    seq = _launch(sim)
    sim.keypress("enter")
    sim.wait_for_log(r"^MODE:Gradients", timeout=5, since_seq=seq)
    sim.keypress("esc")
    _exited(sim)


def test_burnin_fixer_a_skips_a_mode_and_b_quits(simulator):
    sim = simulator
    seq = _launch(sim)
    sim.pad("a", 100)
    sim.wait_for_log(r"^MODE:Gradients", timeout=5, since_seq=seq)
    sim.pad("b", 100)
    _exited(sim)


def test_burnin_fixer_a_held_skips_once(simulator):
    """A held does not repeat: one skip, however long it is held."""
    sim = simulator
    seq = _launch(sim)
    sim.pad("a")
    sim.wait_for_log(r"^MODE:Gradients", timeout=5, since_seq=seq)
    time.sleep(1.0)
    sim.pad("none")
    time.sleep(0.3)
    assert not any(m.startswith("MODE:Scan Line") for m in _modes(sim, seq)), _modes(sim, seq)
    sim.keypress("esc")
    _exited(sim)


def test_burnin_fixer_launcher_a_still_held_does_not_skip(simulator):
    """The launcher opens the app on A and A is still held: that press must
    not skip the first pattern, releasing it does nothing, a fresh press skips."""
    sim = simulator
    _launch(sim)
    sim.keypress("esc")
    _exited(sim)
    time.sleep(1.0)                      # back in the launcher, app selected
    seq = sim.get_log_buffer(tail=1).get("next_seq", 0)
    sim.pad("a")                         # open the app, and keep holding
    sim.wait_for_log(r"^MODE:Solid Colors", timeout=10, since_seq=seq)
    time.sleep(0.8)
    sim.pad("none")
    time.sleep(0.3)
    assert all(m.startswith("MODE:Solid Colors") for m in _modes(sim, seq)), _modes(sim, seq)
    sim.pad("a", 100)
    sim.wait_for_log(r"^MODE:Gradients", timeout=5, since_seq=seq)
    sim.keypress("esc")
    _exited(sim)


def test_burnin_fixer_f4_skips_and_f5_quits(simulator):
    """F4 and F5 are A and B's default keys."""
    sim = simulator
    seq = _launch(sim)
    sim.keypress("f4")
    sim.wait_for_log(r"^MODE:Gradients", timeout=5, since_seq=seq)
    sim.keypress("f5")
    _exited(sim)


@pytest.mark.parametrize("rebind,hint", [
    (None, "F4:Next  Esc:Exit"),
    ({"a": ["Z"]}, "Z:Next  Esc:Exit"),
    ({"a": []}, "?:Next  Esc:Exit"),       # A left unbound
])
def test_burnin_fixer_hint_names_a_by_its_key(simulator, rebind, hint):
    sim = simulator
    seq = _launch(sim, rebind=rebind)
    assert sim.wait_for_log(r"^HINT:", timeout=5, since_seq=seq) == "HINT:" + hint
    sim.keypress("esc")
    _exited(sim)


def test_burnin_fixer_follows_a_rebound_a(simulator):
    sim = simulator
    seq = _launch(sim, rebind={"a": ["Z"]})
    sim.keypress("f4")                   # no longer A
    time.sleep(0.5)
    assert all(m.startswith("MODE:Solid Colors") for m in _modes(sim, seq)), _modes(sim, seq)
    sim.keypress("z")                    # A is Z now
    sim.wait_for_log(r"^MODE:Gradients", timeout=5, since_seq=seq)
    sim.keypress("esc")
    _exited(sim)
