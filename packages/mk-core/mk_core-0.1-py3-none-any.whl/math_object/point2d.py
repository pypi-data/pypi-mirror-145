import math
from typing import Dict


class Point2D:
    """Simple representation of a point in 2D space"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @classmethod
    def from_json(cls, data: Dict[str, int]):
        if "x" not in data or "y" not in data:
            raise RuntimeError(
                f"Invalid json format. Need keys 'x' and 'y', but got {str(data)}"
            )
        return cls(data["x"], data["y"])

    def distance(self, other: object) -> float:
        if not isinstance(other, Point2D):
            raise NotImplementedError()
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __add__(self, p: object):
        if not isinstance(p, Point2D):
            raise NotImplementedError()
        return Point2D(self.x + p.x, self.y + p.y)

    def __sub__(self, p: object):
        if not isinstance(p, Point2D):
            raise NotImplementedError()
        return Point2D(self.x - p.x, self.y - p.y)

    def __mul__(self, s: float):
        return Point2D(self.x * s, self.y * s)

    def __rmul__(self, s: float):
        return Point2D(self.x * s, self.y * s)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point2D):
            raise NotImplementedError()
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash(str(self))
