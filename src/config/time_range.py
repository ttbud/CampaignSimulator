import re

from strictyaml import ScalarValidator
from strictyaml.yamllocation import YAMLChunk


class TimeRange(ScalarValidator):
    def validate_scalar(self, chunk: YAMLChunk):
        if chunk.contents == "otherwise":
            return OTHERWISE
        elif match := time_range_pattern.match(chunk.contents):
            start_time, end_time = match.groups()
            start_time, end_time = int(start_time), int(end_time)
            if start_time >= end_time:
                chunk.expecting_but_found("Start time must be before end time")
            elif not (0 <= start_time <= 24 and 0 <= end_time <= 24):
                chunk.expecting_but_found("Times must be between 0 and 24, inclusive")
            return start_time, end_time
        else:
            chunk.expecting_but_found("Something like 13-15")

    def to_yaml(self, data):
        raise NotImplementedError()


time_range_pattern = re.compile(r"(\d{1,2})-(\d{1,2})")
OTHERWISE = object()