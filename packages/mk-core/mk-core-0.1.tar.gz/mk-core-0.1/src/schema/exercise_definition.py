from dataclasses import dataclass
from dataclasses import field


@dataclass(frozen=True)
class ExerciseDefinition:

    type: str = field(default="not-implemented")
    layout: str = field(default="default")

    @classmethod
    def from_json(cls, data):
        """Reads data from JSON file"""
        pass
