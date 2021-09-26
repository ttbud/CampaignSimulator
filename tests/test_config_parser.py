from src.config.parse import parse, Config

# language=yaml
from src.structures import Location, LocationType, NonPlayerCharacter, Schedule


def test_a_thing():
    result = parse("./example.yml")
    deli_aisle = Location('deli aisle', sublocations=[], type=LocationType("store"))
    gun_section = Location('inexplicably large gun section', sublocations=[])
    walmart = Location('walmart', sublocations=[deli_aisle, gun_section],
                       type=LocationType("store"))
    steves_home = Location('steve\'s home', sublocations=[], type=LocationType('house'))
    assert result == Config(
        locations=[walmart, deli_aisle, gun_section, steves_home],
        non_player_characters=[
            NonPlayerCharacter('steve', schedule=Schedule([
                (range(0, 1), steves_home),
                (range(1, 2), deli_aisle),
                (range(2, 5), walmart),
                (range(5, 6), gun_section),
                (range(6, 24), steves_home),
            ]))
        ])
