from collections import defaultdict
from typing import Callable, Dict, Iterator, List, Tuple, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def countby(elements: Iterator[T], key: Callable[[T], U]) -> Dict[U, int]:
    groups = groupby(elements, key)
    counts = {k: len(v) for k, v in groups.items()}
    return counts


def groupby(elements: Iterator[T], key: Callable[[T], U]) -> Dict[U, List[T]]:
    groups: Dict[U, List[T]] = defaultdict(list)
    for el in elements:
        groups[key(el)].append(el)
    return dict(groups)


def groupby_pairs(
    pairs: List[Tuple[T, T]], key: Callable[[T], U]
) -> Dict[U, List[Tuple[T, T]]]:
    groups: Dict[U, List[Tuple[T, T]]] = defaultdict(list)
    for a, b in pairs:
        ka, kb = key(a), key(b)
        if ka == kb:
            groups[ka].append((a, b))
    return dict(groups)


def groupby_stream(
    elements: Iterator[T], key: Callable[[T], U], size: int
) -> Iterator[Tuple[U, List[T]]]:
    groups: Dict[U, List[T]] = defaultdict(list)
    for i, el in enumerate(elements):
        groups[key(el)].append(el)
        if (i + 1) % size == 0:
            for item in groups.items():
                yield item
            groups = defaultdict(list)
    for item in groups.items():
        yield item
