from typing import TYPE_CHECKING, Callable, Dict, Generic, Iterable, Iterator, List, Optional, Set, Tuple, TypeVar

if TYPE_CHECKING:
    from graphviz import Digraph

T = TypeVar("T")


class BKNode(Generic[T]):  # should be smaller than a pair-tuple

    __slots__ = ["value", "leaves"]

    def __init__(self, value: T, leaves: Dict[int, "BKNode"]) -> None:

        self.value = value
        self.leaves = leaves

    def __str__(self) -> str:
        return str(self.value) + ": " + str(self.leaves)

    def __repr__(self) -> str:
        return repr(self.value) + ": " + repr(self.leaves)


class BKTree(Generic[T]):

    """BK-tree. Used for nearest neighbor queries according to a discrete metric.
    Examples for the metric are the Manhattan distance or the Levenshtein distance.

    from polyleven import levenshtein  # pip install polyleven

    words = ["laptop", "security", "microsoft", "computer", "software", "tree", "algorithm", "desktop"]

    tree = BKTree(levenshtein)
    tree.update(words)
    tree.saveimage("bk-tree.gv")
    """

    def __init__(self, distance_func: Callable[[T, T], int]) -> None:

        self.distance_func = distance_func
        self.root: Optional[BKNode[T]] = None

    def add(self, value: T) -> None:

        if self.root is None:
            self.root = BKNode(value, {})
            return

        node = self.root
        while True:
            distance = self.distance_func(value, node.value)
            try:
                node = node.leaves[distance]
            except KeyError:
                node.leaves[distance] = BKNode(value, {})
                break

    def update(self, values: Iterable[T]) -> None:

        for value in values:
            self.add(value)

    def find(self, value: T, max_distance: int) -> List[Tuple[int, T]]:

        """Returns all values from tree where the metric distance
        is less or equal to `max_distance`.
        """

        node = self.root
        ret: List[Tuple[int, T]] = []

        if node is None:
            return ret

        candidates = [node]  # is a deque better here?

        while candidates:
            candidate = candidates.pop()
            distance = self.distance_func(value, candidate.value)

            if distance <= max_distance:
                ret.append((distance, candidate.value))

            # instead of looking for candidates by searching,
            # one could also directly access the necessary keys in the dict
            for d, bknode in candidate.leaves.items():
                lower = distance - max_distance
                upper = distance + max_distance
                if lower <= d <= upper:
                    candidates.append(bknode)

        return ret

    @staticmethod
    def _find_by_distance(node: BKNode[T], distance: int) -> Iterator[Set[T]]:

        for d, bknode in node.leaves.items():
            if d == distance:
                nodeset = set(BKTree._values(bknode))
                nodeset.add(node.value)
                yield nodeset
            yield from BKTree._find_by_distance(bknode, distance)

    def find_by_distance(self, distance: int) -> Iterator[Set[T]]:

        """Find all sets of values where the distance between each other equals `distance`."""

        if self.root is None:
            return iter([])
        else:
            return self._find_by_distance(self.root, distance)

    @staticmethod
    def _dot(dot: "Digraph", node: BKNode[T]) -> None:

        for distance, childnode in node.leaves.items():
            dot.node(str(childnode.value))
            dot.edge(str(node.value), str(childnode.value), label=str(distance))
            BKTree._dot(dot, childnode)

    def saveimage(self, filename: str, format: str = "png") -> None:
        from graphviz import Digraph

        if self.root is None:
            raise ValueError("Tree is empty")

        dot = Digraph(format=format)
        dot.node(str(self.root.value))
        self._dot(dot, self.root)
        dot.render(filename)

    @staticmethod
    def _values(node: BKNode[T]) -> Iterator[T]:

        yield node.value
        for leaf in node.leaves.values():
            yield from BKTree._values(leaf)

    def values(self) -> Iterator[T]:

        """Returns all values in arbitrary order."""

        if self.root is None:
            return iter([])
        else:
            return self._values(self.root)

    def __iter__(self) -> Iterator[T]:

        return self.values()
