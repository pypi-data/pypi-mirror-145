from dataclasses import dataclass


@dataclass
class UpdateLoggableDataDTO:
    input: str
    output: str
    likelihood: float
