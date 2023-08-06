import pydantic

from classiq.interface.helpers.custom_pydantic_types import pydanticNonEmptyString


class AnalysisParams(pydantic.BaseModel):
    qasm: pydanticNonEmptyString
