import argparse
import math

from .search import Grid, search


def main():
    parser = argparse.ArgumentParser(description="Grid path planner")
    parser.add_argument("--size", type=int, default=30)
    parser.add_argument("--density", type=float, default=0.30)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--algorithm", choices=("dijkstra", "astar", "weighted"),
                        default="astar")
    parser.add_argument("--heuristic", choices=("manhattan", "euclidean", "octile"),
                        default="octile")
    parser.add_argument("--diagonal", action="store_true")
    parser.add_argument("--weight", type=float, default=1.5)
    parser.add_argument("--plot")
    parser.add_argument("--animate")
    args = parser.parse_args()
    grid = Grid.random(args.size, args.size, args.density, args.seed)
    result = search(grid, algorithm=args.algorithm,
                    heuristic_kind=args.heuristic, diagonal=args.diagonal,
                    weight=args.weight, record_frontiers=bool(args.animate))
    print(f"cost={result.cost:.4f}" if math.isfinite(result.cost) else "no path")
    print(f"expanded={len(result.expanded)} path_cells={len(result.path)}")
    if args.plot or args.animate:
        from .visualize import plot_result, animate_result
        if args.plot:
            plot_result(grid, result, args.plot)
        if args.animate:
            animate_result(grid, result, args.animate)


if __name__ == "__main__":
    main()

