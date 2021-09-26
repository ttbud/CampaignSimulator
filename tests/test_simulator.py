import pytest

from src.simulator import Simulator
from tests.static_fixtures import TEST_CHARACTER, TEST_LOCATION_1, TEST_LOCATION_2


@pytest.fixture
def simulator() -> Simulator:
    return Simulator([TEST_CHARACTER], [TEST_LOCATION_1, TEST_LOCATION_2], 0)


def test_advance_time(simulator: Simulator) -> None:
    start_time = simulator.hour
    simulator.advance_time()
    assert simulator.hour == (start_time + 1) % 24
    start_time = simulator.hour
    simulator.advance_time(num_hours=4)
    assert simulator.hour == (start_time + 4) % 24


def test_get_npc_location(simulator: Simulator) -> None:
    assert simulator.get_npc_location(TEST_CHARACTER) == TEST_LOCATION_1
    simulator.advance_time(12)
    assert simulator.get_npc_location(TEST_CHARACTER) == TEST_LOCATION_2
