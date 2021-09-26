from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Union


class InvalidScheduleError(BaseException):
    pass


class InvalidHourError(BaseException):
    pass


@dataclass
class LocationType:
    name: str


@dataclass
class Location:
    name: str
    sublocations: List[Location]
    type: LocationType


@dataclass
class Schedule:
    schedule: List[Tuple[range, Union[Location, LocationType]]]

    def __init__(self, schedule: List[Tuple[range, Union[Location, LocationType]]]):
        hours = list(range(24))
        scheduled_times: List[int] = []
        for time_range, _ in schedule:
            for hour in time_range:
                scheduled_times.append(hour)
        if scheduled_times != hours:
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
        if hour not in range(24):
            raise InvalidHourError()
        self.hour = hour
        self.player_locations = player_locations
