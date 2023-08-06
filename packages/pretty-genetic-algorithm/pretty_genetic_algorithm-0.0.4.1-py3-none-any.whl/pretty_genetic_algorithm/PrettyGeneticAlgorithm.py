from collections import OrderedDict
from typing import Any, Callable, List, Optional, Tuple, Type

from functools import reduce
from tqdm import notebook
import random
import json

from .parameter.BaseParameter import BaseParameter
from .Creature import Creature


class PrettyGeneticAlgorithm:
    def __init__(
        self,
        num_species: int,
        num_creatures_per_species: int,
        dna_config: List[Type[BaseParameter]],
        fitness_cache_size: int = 500,
        mutation_rate: float = 0.1,
        silent: bool = False,
    ):
        """A pretty printing genetic algorithm implementation

        Args:
            num_species (int): Number of species to create, all species will evolve separately.
            num_creatures_per_species (int): Number of creatures to have per species. All creatures within a species can mutate/evolve with eachother.
            dna_config (List[Type[BaseParameter]]): The set of parameters to search over.
            fitness_cache_size (int, optional): If the genetic has already calculated a creature's fitness, it will use the old value and not calculate again. Defaults to 500.
            mutation_rate (float, optional): How likely a single DNA piece will mutate. Defaults to 0.1.
            silent (bool): If true, it will mute the output of this genetic algorithm. Defaults to False.
        """
        self.__num_species = num_species
        self.__num_creatures_per_species = num_creatures_per_species
        self.species = [
            [Creature(dna_config) for _ in range(self.__num_creatures_per_species)]
            for _ in range(self.__num_species)
        ]
        self.__mutation_rate = mutation_rate
        self.__fitness_cache_size = fitness_cache_size
        self.__silent = silent

        self.__fitness_cache = OrderedDict()
        self.__best_fitness = None
        self.__best_creature = None
        self.fitness_history = []
        total_permutations = reduce(
            lambda acc, item: acc * len(item.values), dna_config, 1
        )
        if not self.__silent:
            print(
                f"Total DNA permutations: {' * '.join(str(len(item.values)) for item in dna_config)} = {total_permutations}"
            )

    __progress = None

    def __show_progress(
        self, progress: float, total: float, description: str = None
    ) -> None:
        if self.__progress is None:
            self.__progress = notebook.tqdm(total=total)
        if description is not None:
            self.__progress.set_description(description)
        self.__progress.n = progress
        self.__progress.refresh()

    def __measure_fitnesses(
        self,
        measure_fitness: Callable[[Creature], float],
        generation: int,
        generations: int,
    ) -> List[List[float]]:
        fitnesses = []
        for i, species in enumerate(self.species):
            fitnesses.append([])
            for j, creature in enumerate(species):
                fitness = measure_fitness(creature)

                if self.__best_fitness is None or self.__best_fitness < fitness:
                    self.__best_fitness = round(fitness, 4)
                    self.__best_creature = creature
                fitnesses[-1].append(fitness)
                if not self.__silent:
                    current_iteration = (
                        (
                            generation
                            * self.__num_species
                            * self.__num_creatures_per_species
                        )
                        + (i * self.__num_creatures_per_species)
                        + j
                        + 1
                    )
                    total_iterations = (
                        self.__num_species
                        * self.__num_creatures_per_species
                        * generations
                    )
                    self.__show_progress(
                        current_iteration,
                        total_iterations,
                        description=f"GA Progress | Best So Far: {round(self.__best_fitness, 4)}",
                    )
        return fitnesses

    def cache_fitness(self, measure_fitness: Callable[[Creature], float]):
        """Method decorator that caches the fitness of a creature's dna for reuse next time.
            The measure fitness method can optionally take a verbose argument, where if enabled, the fitness will be force calculated and returned immediately.

        Args:
            measure_fitness (Callable[[Creature], float]): Method that's being decorated.
        """

        def wrapper(creature: Creature, verbose: bool = False):
            if verbose:
                return measure_fitness(creature, verbose=verbose)
            if creature.dna not in self.__fitness_cache:
                self.__fitness_cache[creature.dna] = measure_fitness(creature)
                while len(self.__fitness_cache) > self.__fitness_cache_size:
                    self.__fitness_cache.popitem()
            return self.__fitness_cache[creature.dna]

        return wrapper

    def evolve(
        self,
        generations: int,
        measure_fitness: Callable[[Creature], float],
        choose_mate: Callable[["PrettyGeneticAlgorithm", List[Creature]], int] = None,
        choose_mate_args: Tuple[Any, ...] = (),
        mutate: Callable[
            ["PrettyGeneticAlgorithm", Creature, Creature, Callable[[Creature], float]],
            None,
        ] = None,
        mutate_args: Tuple[Any, ...] = (),
        creatures_to_keep: int = 1,
    ) -> List[List[List[float]]]:
        """Evolves the genetic algorithm based on parameters.

        Args:
            generations (int): Number of generations to run the genetic algorithm for.
            measure_fitness (Callable[[Creature], float]): The method used to determine how good a specific creature is. Must return a float corresponding to this value.
            choose_mate (Callable[[Self, List[Creature]], int, ...], optional): Chooses the next creature based on the index of the first. Only provide a custom function if you know what you're doing. Defaults to spatial area.
            choose_mate_args (Tuple[Any, ...], optional): Any extra arguments you would like to supply for the choose_mate method. Defaults to ().
            mutate (Callable[ [Self, Creature, Creature, Callable[[Creature], float], ...], None ], optional): Mutates one of the two passed creature's DNA, to progress the genetic algorithm. Only provide a custom function if you know what you're doing. Defaults to tournament.
            mutate_args (Tuple[Any, ...], optional): Any extra arguments you would like to supply for the mutate method. Defaults to ().
            creatures_to_keep (int, optional): Number of creatures to keep per species for the next generation. Only keeps the best creatures. Defaults to 1.

        Returns:
            List[List[List[float]]]: History of the fitnesses which is a 3 dimensional list, where the outer list is the generations, followed by the number of species, and then the creatures.
        """
        if choose_mate is None:
            choose_mate = self.spatial_area
        if mutate is None:
            mutate = self.tournament_mutation

        self.fitness_history.append(
            self.__measure_fitnesses(measure_fitness, 0, generations)
        )
        for i in range(1, generations):
            for j, species in enumerate(self.species):
                sorted_creatures = sorted(
                    enumerate(species),
                    key=lambda item: self.fitness_history[-1][j][item[0]],
                    reverse=True,
                )
                creatures_saved = sorted(
                    [item[0] for item in sorted_creatures[:creatures_to_keep]]
                )
                for _ in range(self.__num_creatures_per_species):
                    a = random.randint(
                        0, self.__num_creatures_per_species - 1 - creatures_to_keep
                    )
                    for index in creatures_saved:
                        if a >= index:
                            a += 1
                        else:
                            break
                    b = choose_mate(self, species, a, *choose_mate_args)
                    mutate(
                        self,
                        self.species[j][a],
                        self.species[j][b],
                        measure_fitness,
                        *mutate_args,
                    )
            self.fitness_history.append(
                self.__measure_fitnesses(measure_fitness, i, generations)
            )
        return self.fitness_history

    def best(self) -> Tuple[Optional[float], Optional[Creature]]:
        """Returns the best fitness and creature so far.

        Returns:
            Tuple[Optional[float], Optional[Creature]]: The fitness and the creature which are the best it's found.
        """
        return (self.__best_fitness, self.__best_creature)

    def serialise_dna_data(self) -> str:
        """Serialises all the dna from this genetic algorithm instance.

        Returns:
            str: Json string containing all of this instance's creature dna.
        """
        return json.dumps(
            [[creature.dna for creature in creatures] for creatures in self.species]
        )

    @staticmethod
    def deserialise_dna_data(dna_str: str, *args, **kwargs) -> "PrettyGeneticAlgorithm":
        """Creates a new PrettyGeneticAlgorithm instance from some passed in dna data.
            Accepts args and kwargs which are passed to the constructor of the created instance.

        Args:
            dna_str (str): Input dna data string.

        Returns:
            PrettyGeneticAlgorithm: Instance created from the dna data string.
        """
        dna_data = json.loads(dna_str)
        assert len(dna_data) > 0 and all(
            len(species) == len(dna_data[0]) for species in dna_data
        ), "Malformed DNA data when deserialising!"

        ga_kwargs = {}
        if len(args) < 2:
            ga_kwargs["num_species"] = len(dna_data)
        if len(args) < 3:
            ga_kwargs["num_creatures_per_species"] = len(dna_data[0])
        ga_kwargs.update(kwargs)

        ga = PrettyGeneticAlgorithm(*args, **ga_kwargs)
        for species_dna, species in zip(dna_data, ga.species):
            for creature_dna, creature in zip(species_dna, species):
                creature.set_dna(tuple(creature_dna))
        return ga

    # Mutation functions defined below

    @staticmethod
    def tournament_mutation(
        instance: "PrettyGeneticAlgorithm",
        a: Creature,
        b: Creature,
        measure_fitness: Callable[[Creature], float],
    ):
        """Overwrites the lesser of the fitnesses of a and b with a mutated version of the two.

        Args:
            instance (PrettyGeneticAlgorithm): Pretty genetic algorithm instance.
            a (Creature): First chosen creature.
            b (Creature): Creature chosen based on the choosing mate function.
            measure_fitness (Callable[[Creature], float]): Way to measure a creature's fitness.
        """
        if measure_fitness(a) > measure_fitness(b):
            b.set_dna(a.mutate(instance.__mutation_rate).dna)
        else:
            a.set_dna(b.mutate(instance.__mutation_rate).dna)

    @staticmethod
    def mating_mutation(
        instance: "PrettyGeneticAlgorithm",
        a: Creature,
        b: Creature,
        measure_fitness: Callable[[Creature], float],
    ):
        """Shares the dna between the creatures based on the ratio of their fitnesses squared.

        Args:
            instance (PrettyGeneticAlgorithm): Pretty genetic algorithm instance.
            a (Creature): First chosen creature.
            b (Creature): Creature chosen based on the choosing mate function.
            measure_fitness (Callable[[Creature], float]): Way to measure a creature's fitness.
        """
        a_fitness = measure_fitness(a)
        b_fitness = measure_fitness(b)
        offset = min(a_fitness, b_fitness) - 1
        a_fitness, b_fitness = (a_fitness - offset) ** 2, (b_fitness - offset) ** 2
        child = a.mate(b, self_bias=a_fitness / (a_fitness + b_fitness))
        a.set_dna(child.mutate(instance.__mutation_rate).dna)

    # Choosing mate functions below

    @staticmethod
    def simple_random(
        instance: "PrettyGeneticAlgorithm", species: List[Creature], creature_idx: int
    ) -> int:
        """Chooses a random index for the other creature.

        Args:
            instance (PrettyGeneticAlgorithm): Pretty genetic algorithm instance.
            species (List[Creature]): List of creatures in the current species.
            creature_idx (int): Index of the first creature in the species.

        Returns:
            int: Chosen index.
        """
        return random.randint(0, len(species) - 1)

    @staticmethod
    def spatial_area(
        instance: "PrettyGeneticAlgorithm",
        species: List[Creature],
        creature_idx: int,
        creature_window_size: int = 3,
    ) -> int:
        """Chooses a random creature from the creatures around the current one.

        Args:
            instance (PrettyGeneticAlgorithm): Pretty genetic algorithm instance.
            species (List[Creature]): List of creatures in the current species.
            creature_idx (int): Index of the first creature in the species.
            creature_window_size (int, optional): Window size to choose from. Defaults to 3.

        Returns:
            int: Chosen index.
        """
        return random.randint(
            creature_idx, creature_idx + creature_window_size - 1
        ) % len(species)

    @staticmethod
    def spatial_similarity(
        instance: "PrettyGeneticAlgorithm",
        species: List[Creature],
        creature_idx: int,
        num_creatures_per_species=3,
        invert: bool = False,
    ) -> int:
        """Sorts the creatures based on how similar they are to the current creature and chooses a random similar creature from the start.

        Args:
            instance (PrettyGeneticAlgorithm): Pretty genetic algorithm instance.
            species (List[Creature]): List of creatures in the current species.
            creature_idx (int): Index of the first creature in the species.
            num_creatures_per_species (int, optional): How many creatures to consider when choosing. Defaults to 3.
            invert (bool, optional): Inverts the sort, so it will choose the least similar creatures. Defaults to False.

        Returns:
            int: Chosen index.
        """
        similarities = zip(
            range(len(species)),
            [species[creature_idx].get_similarity(other) for other in species],
        )
        sorted_creatures = sorted(
            similarities, key=lambda item: item[1], reverse=invert
        )
        return random.choice(sorted_creatures[:num_creatures_per_species])[0]

    @staticmethod
    def weighted_random(
        instance: "PrettyGeneticAlgorithm",
        species: List[Creature],
        creature_idx: int,
        measure_fitness: Callable[[Creature], float],
    ) -> int:
        """Chooses a creature where the higher the fitness, the more likely it will be chosen.

        Args:
            instance (PrettyGeneticAlgorithm): Pretty genetic algorithm instance.
            species (List[Creature]): List of creatures in the current species.
            creature_idx (int): Index of the first creature in the species.
            measure_fitness (Callable[[Creature], float]): How to measure the fitness.

        Returns:
            int: Chosen index.
        """
        raw_weights = list(
            map(
                lambda creature: measure_fitness(creature),
                species,
            )
        )
        min_weight = min(raw_weights)
        weights = list(map(lambda weight: weight - min_weight, raw_weights))
        chosen_creature = round(random.random() * sum(weights))
        curr_weight = 0
        for i, weight in enumerate(weights):
            curr_weight += weight
            if curr_weight >= chosen_creature:
                return i

    @staticmethod
    def choose_next(
        instance: "PrettyGeneticAlgorithm", species: List[Creature], creature_idx: int
    ) -> int:
        """Chooses the very next creature.

        Args:
            instance (PrettyGeneticAlgorithm): Pretty genetic algorithm instance.
            species (List[Creature]): List of creatures in the current species.
            creature_idx (int): Index of the first creature in the species.

        Returns:
            int: Chosen Index.
        """
        return (creature_idx + 1) % len(species)
