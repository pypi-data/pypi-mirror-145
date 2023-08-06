from dataclasses import dataclass
from dataclasses import field


@dataclass(frozen=True)
class SolutionDefinition:
    pass


@dataclass(frozen=True)
class IdentifyFractionAdvancedSolutionDefinition(SolutionDefinition):
    nominator: int = field(default=0)
    denominator: int = field(default=1)


@dataclass(frozen=True)
class IdentifyFractionSolutionDefinition(SolutionDefinition):
    nominator: int = field(default=0)
    denominator: int = field(default=1)
