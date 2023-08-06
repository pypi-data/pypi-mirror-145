import copy
from typing import Any
from typing import Dict
from typing import List

from math_object.point2d import Point2D


def lists_compare(list1: List[Any], list2: List[Any]) -> bool:
    if len(list1) != len(list2):
        return False
    if len(list1) == 0:
        return True
    for index, item in enumerate(list1):
        if item != list2[index]:
            return False
    return True


def is_cyclic_permutation(list1: List[Any], list2: List[Any]) -> bool:
    if len(list1) != len(list2):
        return False
    if len(list1) == 0:
        return True
    tmp_list = copy.deepcopy(list1)
    for _ in range(len(list1)):
        tmp_list = tmp_list[1:] + [tmp_list[0]]
        if lists_compare(tmp_list, list2):
            return True
    return False


class Polygon2D:
    """Simple representation of convex 2D polygons"""

    def __init__(self, pts: List[Point2D]):
        self.vertices = pts

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        if "vertices" not in data:
            raise RuntimeError(
                f"Invalid json format. Need key 'vertices', but got {str(data)}"
            )
        vertices: List[Point2D] = [Point2D.from_json(item) for item in data["vertices"]]
        return cls(vertices)

    @property
    def area(self) -> float:
        n: int = len(self.vertices)
        area: float = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.vertices[i].x * self.vertices[j].y
            area -= self.vertices[j].x * self.vertices[i].y
        area = abs(area) / 2.0
        return area

    @property
    def circumference(self) -> float:
        verts_extended = copy.deepcopy(self.vertices)
        verts_extended = verts_extended + [verts_extended[0]]
        return sum(
            verts_extended[i].distance(verts_extended[i - 1])
            for i in range(1, len(verts_extended))
        )

    def scale(self, factor: float):
        return Polygon2D([v * factor for v in self.vertices])

    def __str__(self) -> str:
        return " -- ".join([str(p) for p in self.vertices])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polygon2D):
            raise NotImplementedError()
        return is_cyclic_permutation(self.vertices, other.vertices)
