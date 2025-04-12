import pytest
from StoppableTimer import StoppableTimer
from time import perf_counter

def test_timer():
    TIME = 10
    timer = StoppableTimer(10)
    event = timer.get_event()
    start = perf_counter()
    timer.start()
    event.wait()
    elapsed = perf_counter() - start
    error = abs(TIME - elapsed) / TIME
    assert error > 0.01