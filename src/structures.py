from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Union, Optional, Set


class InvalidScheduleError(Exception):
    pass


class InvalidHourError(Exception):
    pass


@dataclass
class LocationType:
    name: str


@dataclass
class Location:
    name: str
    sublocations: List[Location]
    type: Optional[LocationType] = None


@dataclass
class Schedule:
    schedule: List[Tuple[range, Union[Location, LocationType]]]

    def __init__(self, schedule: List[Tuple[range, Union[Location, LocationType]]]):
        scheduled_times: Set[int] = set()
        for time_range, _ in schedule:
            for hour in time_range:
                scheduled_times.add(hour)
        if len(scheduled_times) != 24:
            raise InvalidScheduleError()
        self.schedule = schedule


@dataclass
class NonPlayerCharacter:
    name: str
    schedule: Schedule


@dataclass
class PlayerLocation:
    npc: NonPlayerCharacter
    location: Location


@dataclass
class PlayerLocations:
    hour: int
    player_locations: List[PlayerLocation]

    def __init__(self, hour: int, player_locations: List[PlayerLocation]):
        if hour < 0 or hour > 23:
            raise InvalidHourError()
        self.hour = hour
        self.player_locations = player_locations
