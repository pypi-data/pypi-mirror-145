from enum import Enum
from typing import List, Optional, Union

import pydantic

from classiq.interface.chemistry import molecule


class FermionMapping(str, Enum):
    JORDAN_WIGNER = "jordan_wigner"
    PARITY = "parity"
    BRAVYI_KITAEV = "bravyi_kitaev"
    FAST_BRAVYI_KITAEV = "fast_bravyi_kitaev"


class GroundStateProblem(pydantic.BaseModel):
    molecule: molecule.Molecule
    basis: str = pydantic.Field(default="sto3g", description="Molecular basis set")
    mapping: FermionMapping = pydantic.Field(
        default=FermionMapping.JORDAN_WIGNER, description="Fermionic mapping type"
    )
    freeze_core: Optional[bool] = pydantic.Field(default=False)
    remove_orbitals: Optional[List[int]] = pydantic.Field(
        default=None, description="list of orbitals to remove"
    )
    two_qubit_reduction: Optional[bool] = pydantic.Field(default=False)
    z2_symmetries: Union[str, List[int], None] = pydantic.Field(
        default=None,
        description="possible values are: None, 'auto' or a list of 1 and -1",
    )
