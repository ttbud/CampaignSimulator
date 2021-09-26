from dataclasses import dataclass
from typing import List, Union, Tuple

from strictyaml import load, Map, Str, Seq, Optional, MapPattern, EmptyDict

from src.config.time_range import TimeRange, OTHERWISE
from src.structures import Location, NonPlayerCharacter, Schedule, LocationType

location_schema = Map(
    {Optional("type"): Str(), Optional("sublocations"): Seq(Str())}
) | EmptyDict()
character_schema = MapPattern(TimeRange(), Str())
schema = Map({"locations": MapPattern(Str(), location_schema), "characters": MapPattern(Str(), character_schema)})


@dataclass
class Config:
    locations: List[Location]
    non_player_characters: List[NonPlayerCharacter]


def parse(path: str) -> Config:
    with open(path, 'r') as config_file:
        config_contents = config_file.read()

    raw_config = load(config_contents, schema)
    locations = {}
    for name, location in raw_config.data['locations'].items():
        raw_type = location.get('type')
        typ = None if raw_type is None else LocationType(raw_type)
        locations[name] = Location(name, [], typ)

    for name, raw_location in raw_config.data['locations'].items():
        if 'sublocations' not in raw_location:
            continue
        for sublocation_name in raw_location['sublocations']:
            locations[name].sublocations.append(locations[sublocation_name])

    characters = []
    for name, raw_character in raw_config.data['characters'].items():
        timeslots: List[Tuple[Tuple[int, int], Union[Location, LocationType]]] = []
        available_numbers = list(range(24))
        otherwise_location = None
        for time_range, location_name in raw_character.items():
            location = locations.get(location_name, LocationType(location_name))
            if time_range == OTHERWISE:
                otherwise_location = location
                continue
            start, end = time_range
            for time in range(start, end):
                available_numbers.remove(time)
            timeslots.append(((start, end), location))

        timeslots.sort(key=lambda x: x[0][0])
        current = 0
        for (i, ((start, end), _)) in enumerate(list(timeslots)):
            if start > current:
                if not otherwise_location:
                    raise ValueError("No slots and no otherwise location specified")
                timeslots.insert(i, ((current, start), otherwise_location))
            if start < current:
                raise ValueError("Overlapping time ranges")
            current = end
        if current != 24:
            if not otherwise_location:
                raise ValueError("No slots and no otherwise location specified")
            timeslots.append(((current, 24), otherwise_location))

        real_timeslots: List[Tuple[range, LocationType]] = []
        for ((start, end), location_type) in timeslots:
            real_timeslots.append((range(start, end), location_type))
        characters.append(NonPlayerCharacter(name, Schedule(real_timeslots)))

    return Config(list(locations.values()), characters)
