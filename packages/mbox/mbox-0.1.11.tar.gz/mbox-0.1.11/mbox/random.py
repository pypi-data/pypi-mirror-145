import random
from typing import List, TypeVar, Union

T = TypeVar("T")


def sample_groups(population: List[List[T]], k: Union[float, int]) -> List[List[T]]:
    if isinstance(k, float) and (k < 0.0 or k > 1.0):
        raise ValueError("Ratio must be between 0.0 and 1.0")
    if isinstance(k, float):
        sizes = [int(len(group) * k) for group in population]
    else:
        sizes = [min(len(group), k) for group in population]
    return [random.sample(group, size) for group, size in zip(population, sizes)]
