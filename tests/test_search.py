import math
import unittest

from gridplanner import Grid, search


class SearchTests(unittest.TestCase):
    def test_known_four_way_path(self):
        grid = Grid(3, 3, frozenset({(1, 0), (1, 1)}))
        result = search(grid)
        self.assertEqual(result.cost, 4)
        self.assertEqual(result.path[0], (0, 0))
        self.assertEqual(result.path[-1], (2, 2))

    def test_admissible_heuristics_match_dijkstra(self):
        for seed in range(30):
            grid = Grid.random(20, 20, 0.30, seed)
            for diagonal in (False, True):
                baseline = search(grid, algorithm="dijkstra",
                                  diagonal=diagonal).cost
                kinds = ("euclidean", "octile") if diagonal else (
                    "manhattan", "euclidean", "octile")
                for kind in kinds:
                    with self.subTest(seed=seed, diagonal=diagonal, kind=kind):
                        candidate = search(grid, algorithm="astar",
                                           heuristic_kind=kind,
                                           diagonal=diagonal).cost
                        if math.isinf(baseline):
                            self.assertTrue(math.isinf(candidate))
                        else:
                            self.assertAlmostEqual(candidate, baseline)

    def test_corner_cutting_is_blocked(self):
        grid = Grid(2, 2, frozenset({(1, 0), (0, 1)}))
        self.assertTrue(math.isinf(search(grid, diagonal=True).cost))

    def test_weighted_search_and_input_validation(self):
        grid = Grid.random(20, 20, 0.2, 4)
        result = search(grid, algorithm="weighted", weight=1.5)
        self.assertTrue(result.path or math.isinf(result.cost))
        with self.assertRaises(ValueError):
            search(grid, diagonal=True, heuristic_kind="manhattan")


if __name__ == "__main__":
    unittest.main()

