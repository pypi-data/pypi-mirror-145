from .BaseParameter import BaseParameter


class BoolParameter(BaseParameter):
    def __init__(self, alias: str, label: str = None) -> None:
        """A boolean parameter for the genetic algorithm

        Args:
            alias (str): Attribute on creatures to set this parameter to.
            label (str, optional): Label of this parameter to display when printing. Defaults to the value of alias.
        """
        super().__init__(
            [True, False],
            alias,
            label,
        )
