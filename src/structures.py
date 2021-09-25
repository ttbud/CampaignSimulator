from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Union


class InvalidScheduleError:
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
            raise InvalidScheduleError


@dataclass
class NonPlayerCharacter:
    name: str
    schedule: Schedule
