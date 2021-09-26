import random
from typing import List, Optional

from src.structures import NonPlayerCharacter, Location, LocationType, PlayerLocations, PlayerLocation

DEFAULT_LOCATION = Location('Wandering the streets', [], LocationType('default'))


class Simulator:
    def __init__(self, npcs: List[NonPlayerCharacter], locations: List[Location], starting_hour: int):
        self.npcs = npcs
        self.locations = locations
        self.hour = starting_hour
        self._player_locations: PlayerLocations = self._determine_player_locations()

    def advance_time(self, num_hours: Optional[int] = None) -> int:
        if num_hours is not None:
            self.hour += num_hours
        else:
            self.hour += 1
        if self.hour > 23:
            self.hour = self.hour - 24
        self._determine_player_locations()
        return self.hour

    def get_npc_location(self, npc: NonPlayerCharacter) -> Location:
        for player_location in self._player_locations.player_locations:
            if player_location.npc == npc:
                return player_location.location
        return DEFAULT_LOCATION

    def get_npcs_at_location(self, target_location: Location) -> List[NonPlayerCharacter]:
        npcs: List[NonPlayerCharacter] = []
        for player_location in self._player_locations.player_locations:
            if player_location.location == target_location:
                npcs.append(player_location.npc)
        return npcs

    def _determine_player_locations(self) -> PlayerLocations:
        self._player_locations = PlayerLocations(self.hour, [])
        for npc in self.npcs:
            for hour_range, location in npc.schedule.schedule:
                if self.hour in hour_range:
                    if isinstance(location, LocationType):
                        try:
                            location = random.choice(list(filter(lambda loc: loc.type == location, self.locations)))
                        except IndexError:
                            # There are no locations of the type the character wants
                            location = DEFAULT_LOCATION
                    self._player_locations.player_locations.append(PlayerLocation(npc, location))
        return self._player_locations
