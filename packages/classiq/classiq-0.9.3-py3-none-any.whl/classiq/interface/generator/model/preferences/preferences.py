from typing import TYPE_CHECKING, List, Optional

import pydantic
from pydantic.utils import sequence_like

from classiq.interface.generator.model.preferences.randomness import create_random_seed
from classiq.interface.generator.result import QuantumFormat
from classiq.interface.generator.transpiler_basis_gates import (
    DEFAULT_BASIS_GATES,
    TranspilerBasisGates,
)

if TYPE_CHECKING:
    pydanticConstrainedQuantumFormatList = List[QuantumFormat]
else:
    pydanticConstrainedQuantumFormatList = pydantic.conlist(
        QuantumFormat, min_items=1, max_items=len(QuantumFormat)
    )


DEFAULT_DRAW_AT_LEVEL = 1


class HardwareSettings(pydantic.BaseModel):
    basis_gates: List[TranspilerBasisGates] = pydantic.Field(
        default=DEFAULT_BASIS_GATES,
        description="The basis gates of the hardware. "
        "This set will be used during the model optimization.",
    )


class Preferences(pydantic.BaseModel):

    hardware_settings: HardwareSettings = pydantic.Field(
        default_factory=HardwareSettings,
        description="Hardware settings which will be used during optimization",
    )

    output_format: pydanticConstrainedQuantumFormatList = pydantic.Field(
        default=[QuantumFormat.QASM],
        description="The quantum circuit output format(s). "
        "When multiple formats are requested, only the first one will be presented in "
        "the VSCode extension.",
    )

    pretty_qasm: bool = pydantic.Field(
        True,
        description="Prettify the OpenQASM2 outputs (use line breaks inside the gate "
        "declarations).",
    )

    qasm3: bool = pydantic.Field(
        False,
        description="Output OpenQASM 3.0 instead of OpenQASM 2.0. Relevant only for "
        "the `qasm` and `transpiled_qasm` attributes of `GeneratedCircuit`.",
    )

    draw_as_functions: Optional[bool] = pydantic.Field(
        default=None,
        description="If true, the generation output will be "
        "visualized as functions and not as an unrolled circuit",
    )

    draw_at_level: pydantic.PositiveInt = pydantic.Field(
        default=DEFAULT_DRAW_AT_LEVEL,
        description="If `draw_as_functions` is `True`, this specifies the hierarchy level of the functions that are "
        "shown in the visualization",
    )

    transpile_circuit: bool = pydantic.Field(
        default=True,
        description="If true, the returned result will contain a "
        "transpiled circuit and its depth",
    )

    timeout_seconds: pydantic.PositiveInt = pydantic.Field(
        default=300, description="Generation timeout in seconds"
    )

    random_seed: int = pydantic.Field(
        default_factory=create_random_seed,
        description="The random seed used for the generation",
    )

    class Config:
        extra = "forbid"

    @pydantic.validator("output_format", pre=True, always=True)
    def validate_output_format(cls, output_format):
        if not sequence_like(output_format):
            return [output_format]

        if len(output_format) == len(set(output_format)):
            return output_format

        raise ValueError(
            f"output_format={output_format}\n"
            "has at least one format that appears twice or more"
        )
