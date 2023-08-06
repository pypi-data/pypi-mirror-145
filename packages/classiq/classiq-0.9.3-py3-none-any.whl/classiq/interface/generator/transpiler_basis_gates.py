import enum
from typing import List, Optional

SINGLE_QUBIT_GATES: List[str] = [
    "u1",
    "u2",
    "u",
    "p",
    "x",
    "y",
    "z",
    "t",
    "tdg",
    "s",
    "sdg",
    "sx",
    "sxdg",
    "rx",
    "ry",
    "rz",
    "id",
    "h",
]


BASIC_TWO_QUBIT_GATES: List[str] = [
    "cx",
    "cy",
    "cz",
    "ch",
    "cp",
]

EXTRA_TWO_QUBIT_GATES: List[str] = [
    "swap",
    "rxx",
    "rzz",
    "crx",
    "cry",
    "crz",
    "csx",
    "cu1",
    "cu",
]

TWO_QUBIT_GATES = BASIC_TWO_QUBIT_GATES + EXTRA_TWO_QUBIT_GATES

THREE_QUBIT_GATES: List[str] = ["ccx", "cswap"]
DEFAULT_BASIS_GATES = SINGLE_QUBIT_GATES + BASIC_TWO_QUBIT_GATES
ALL_GATES: List[str] = SINGLE_QUBIT_GATES + TWO_QUBIT_GATES + THREE_QUBIT_GATES

# The Enum names are capitalized per recommendation in https://docs.python.org/3/library/enum.html#module-enum
# The Enum values are lowered to keep consistency
# The super class for the builtin gates ensures being a string subtype

ALL_GATES_DICT = {gate.upper(): gate.lower() for gate in ALL_GATES}


class LowerValsEnum(str, enum.Enum):
    @classmethod
    def _missing_(cls, value: str) -> Optional[str]:  # type: ignore[override]
        if not isinstance(value, str):
            return None
        lower = value.lower()
        if value == lower:
            return None
        return cls(lower)


TranspilerBasisGates = LowerValsEnum(  # type: ignore[call-overload]
    "TranspilerBasisGates", ALL_GATES_DICT
)
