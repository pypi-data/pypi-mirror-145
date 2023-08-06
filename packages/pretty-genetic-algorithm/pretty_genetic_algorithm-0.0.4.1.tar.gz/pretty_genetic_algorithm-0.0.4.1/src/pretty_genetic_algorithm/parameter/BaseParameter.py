from typing import Any, List, Optional

import random


class BaseParameter:
    label: str = NotImplemented
    alias: str = NotImplemented
    values: List[Any] = NotImplemented

    def __init__(self, values: List[Any], alias: str, label: str = None) -> None:
        """Base genetic algorithm parameter class

        Args:
            values (List[Any]): List of values this parameter can be.
            alias (str): Attribute on creatures to set this parameter to.
            label (str, optional): Label of this parameter to display when printing. Defaults to the value of alias.
        """
        self.values = values
        self.alias = alias
        self.label = label if label is not None else alias

    def new(self, value_before: Any = None) -> Any:
        """Generates a new value, optionally based on the previous value.

        Args:
            value_before (Any, optional): The previous value if there is one. Defaults to None.

        Returns:
            Any: New value.
        """
        return random.choice(self.values)
