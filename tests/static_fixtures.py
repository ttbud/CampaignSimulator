from src.structures import NonPlayerCharacter, Schedule, Location, LocationType

TEST_LOCATION_TYPE_1 = LocationType('test type 1')
TEST_LOCATION_TYPE_2 = LocationType('test type 2')
TEST_LOCATION_1 = Location('test location', [], TEST_LOCATION_TYPE_1)
TEST_LOCATION_2 = Location('another test location', [], TEST_LOCATION_TYPE_2)
TEST_SCHEDULE = Schedule([(range(12), TEST_LOCATION_1), (range(12, 24), TEST_LOCATION_TYPE_2)])
TEST_CHARACTER = NonPlayerCharacter('test char', TEST_SCHEDULE)
