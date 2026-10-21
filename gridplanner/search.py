"""Dijkstra, A*, and weighted A* with reproducible grid generation."""

from dataclasses import dataclass
import heapq
import itertools
import math
import random

Cell = tuple[int, int]
SQRT2 = math.sqrt(2)


@dataclass(frozen=True)
class Grid:
    width: int
    height: int
    walls: frozenset[Cell]

    def __post_init__(self):
        if self.width < 2 or self.height < 2:
            raise ValueError("grid must be at least 2 by 2")
        if any(not (0 <= x < self.width and 0 <= y < self.height)
               for x, y in self.walls):
            raise ValueError("wall outside grid")

    @classmethod
    def random(cls, width: int, height: int, density: float, seed: int) -> "Grid":
        if not 0.2 <= density <= 0.4:
            raise ValueError("density must be between 0.20 and 0.40")
        rng = random.Random(seed)
        candidates = [(x, y) for y in range(height) for x in range(width)
                      if (x, y) not in ((0, 0), (width - 1, height - 1))]
        walls = frozenset(rng.sample(candidates, round(len(candidates) * density)))
        return cls(width, height, walls)

    def neighbors(self, cell: Cell, diagonal: bool):
        x, y = cell
        moves = ((1, 0), (-1, 0), (0, 1), (0, -1))
        if diagonal:
            moves += ((1, 1), (1, -1), (-1, 1), (-1, -1))
        for dx, dy in moves:
            next_cell = (x + dx, y + dy)
            if not (0 <= next_cell[0] < self.width and
                    0 <= next_cell[1] < self.height) or next_cell in self.walls:
                continue
            if dx and dy and ((x + dx, y) in self.walls or
                              (x, y + dy) in self.walls):
                continue
            yield next_cell, SQRT2 if dx and dy else 1.0


def heuristic(a: Cell, b: Cell, kind: str) -> float:
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    if kind == "manhattan":
        return dx + dy
    if kind == "euclidean":
        return math.hypot(dx, dy)
    if kind == "octile":
        return max(dx, dy) + (SQRT2 - 1) * min(dx, dy)
    raise ValueError(f"unknown heuristic: {kind}")


@dataclass
class Result:
    path: list[Cell]
    cost: float
    expanded: list[Cell]
    frontiers: list[frozenset[Cell]]


def search(
    grid: Grid,
    start: Cell = (0, 0),
    goal: Cell | None = None,
    algorithm: str = "astar",
    heuristic_kind: str = "octile",
    diagonal: bool = False,
    weight: float = 1.0,
    record_frontiers: bool = False,
) -> Result:
    goal = goal if goal is not None else (grid.width - 1, grid.height - 1)
    if start in grid.walls or goal in grid.walls:
        raise ValueError("start or goal blocked")
    if not all(0 <= p[0] < grid.width and 0 <= p[1] < grid.height
               for p in (start, goal)):
        raise ValueError("start or goal outside grid")
    if algorithm not in ("dijkstra", "astar", "weighted"):
        raise ValueError("unknown algorithm")
    if weight < 1 or not math.isfinite(weight):
        raise ValueError("weight must be finite and at least one")
    if diagonal and heuristic_kind == "manhattan" and algorithm != "dijkstra":
        raise ValueError("Manhattan is not admissible for diagonal movement")
    heuristic(start, goal, heuristic_kind)
    factor = 0 if algorithm == "dijkstra" else (
        weight if algorithm == "weighted" else 1.0)
    serial = itertools.count()
    queue = [(factor * heuristic(start, goal, heuristic_kind),
              next(serial), 0.0, start)]
    distances = {start: 0.0}
    parents: dict[Cell, Cell] = {}
    expanded: list[Cell] = []
    frontiers: list[frozenset[Cell]] = []
    settled: set[Cell] = set()
    while queue:
        _, _, cost, cell = heapq.heappop(queue)
        if cell in settled or cost > distances[cell] + 1e-12:
            continue
        settled.add(cell)
        expanded.append(cell)
        if record_frontiers:
            frontiers.append(frozenset(
                item[3] for item in queue if item[3] not in settled))
        if cell == goal:
            path = [goal]
            while path[-1] != start:
                path.append(parents[path[-1]])
            return Result(list(reversed(path)), cost, expanded, frontiers)
        for neighbor, step_cost in grid.neighbors(cell, diagonal):
            new_cost = cost + step_cost
            if neighbor not in settled and new_cost < distances.get(
                neighbor, math.inf) - 1e-12:
                distances[neighbor] = new_cost
                parents[neighbor] = cell
                priority = new_cost + factor * heuristic(
                    neighbor, goal, heuristic_kind)
                heapq.heappush(queue, (priority, next(serial),
                                       new_cost, neighbor))
    return Result([], math.inf, expanded, frontiers)

