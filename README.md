# Grid Path Planner

Dijkstra, A*, and weighted A* on reproducible obstacle grids. Supports
four-way or eight-way movement, Manhattan, Euclidean, and octile heuristics,
and diagonal corner-cut prevention. The search result includes path cost,
expanded cells, and frontier snapshots.

## Run

```sh
python -m gridplanner --size 30 --density 0.30 --seed 7 --algorithm astar --diagonal
```

Add `--plot result.png` to save a Matplotlib image of explored cells and
the path. Add `--animate search.gif` for a frontier animation. Plotting
requires `pip install -r requirements.txt`; core search uses only the
standard library. Run `python -m unittest discover -s tests -v` for checks
against Dijkstra on reproducible grids.

Admissible heuristic choices:

| Movement | Manhattan | Euclidean | Octile |
| --- | --- | --- | --- |
| Four-way | Yes | Yes | Yes |
| Eight-way | No | Yes | Yes |

Weighted A* multiplies the heuristic by a weight above 1. It often expands
fewer cells but no longer guarantees the minimum-cost path.

