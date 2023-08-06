""" Creature class definition """

import random
from typing import Any, Callable, Tuple, List, Type

from .parameter.BaseParameter import BaseParameter


class Creature:
    def __init__(
        self,
        dna_config: List[Type[BaseParameter]],
        dna: Tuple[Any] = None,
    ):
        """Creature class which holds a specific DNA sequence.

        Args:
            dna_config (List[Type[BaseParameter]]): Set of DNA to use for mutations
            dna (Tuple[Any], optional): Initial DNA to set. Defaults to None.
        """
        self.__dna_config = dna_config

        self.fitness = None
        if dna is not None:
            self.dna = dna
        else:
            self.dna = tuple(map(lambda parameter: parameter.new(), self.__dna_config))
        for i, parameter in enumerate(dna_config):
            setattr(self, parameter.alias, self.dna[i])

    def set_dna(self, dna: List[Any]) -> None:
        self.dna = dna

    def get_similarity(self, other: "Creature") -> float:
        """Measures how similar another creature is to this one"""
        return sum(abs(self.dna[i] - other.dna[i]) for i in range(len(self.dna)))

    def mate(self, other, self_bias: float = 0.5) -> "Creature":
        """Combines this creature's dna with another's"""
        return Creature(
            self.__dna_config,
            dna=tuple(
                self.dna[i] if random.random() < self_bias else other.dna[i]
                for i in range(len(self.dna))
            ),
        )

    def mutate(self, mutation_rate: float) -> "Creature":
        """Has a chance (mutation rate) to randomly change each dna unit and returns it"""
        return Creature(
            self.__dna_config,
            dna=tuple(
                param.new(old_val) if random.random() < mutation_rate else old_val
                for old_val, param in zip(self.dna, self.__dna_config)
            ),
        )

    def __str__(self):
        return (
            "[Creature "
            + " ".join(
                f"{parameter.label}:{val}"
                for val, parameter in zip(self.dna, self.__dna_config)
            )
            + "]"
        )

    def __eq__(self, other: object) -> bool:
        return other.__dna_config == self.__dna_config and other.dna == self.dna
