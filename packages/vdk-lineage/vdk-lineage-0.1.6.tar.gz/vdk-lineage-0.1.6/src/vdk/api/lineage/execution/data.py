from dataclasses import dataclass


@dataclass(frozen=True)
class DataJobLineageData:
    """
    Defines the LineageData contract

    """

    op_id: str
    execution_id: str
    source_version: str
    team: str
