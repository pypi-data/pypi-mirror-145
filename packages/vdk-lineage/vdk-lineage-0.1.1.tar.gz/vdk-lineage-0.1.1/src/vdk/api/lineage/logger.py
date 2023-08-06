from abc import ABC

from vdk.api.lineage.sql.data import LineageData


class LineageLogger(ABC):
    """
    This interface describes what behaviour a lineage logger must possess to interact with the lineage logging
    functionality afforded by different plugins.
    """

    def send(self, lineage_data: LineageData) -> None:
        """
        This method sends the collected lineage data to some lineage data processing application.

        :param lineage_data: The collected lineage data.
        """
        pass
