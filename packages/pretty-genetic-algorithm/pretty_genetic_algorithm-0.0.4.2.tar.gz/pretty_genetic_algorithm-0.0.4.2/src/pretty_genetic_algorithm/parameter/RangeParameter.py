from .BaseParameter import BaseParameter


class RangeParameter(BaseParameter):
    def __init__(
        self, start: float, end: float, step: float, alias: str, label: str = None
    ) -> None:
        """A range parameter for the genetic algorithm

        Args:
            start (float): Start of the range.
            stop (float): End of the range.
            step (float): Step to take for the range.
            alias (str): Attribute on creatures to set this parameter to.
            label (str, optional): Label of this parameter to display when printing. Defaults to the value of alias.
        """
        super().__init__(
            [start + i * step for i in range(int((end - start) / step))],
            alias,
            label,
        )
