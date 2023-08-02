import unittest
import numpy as np
from routeml.utils import get_logit_mask, get_logit_mask_vector


class TestGetLogitMask(unittest.TestCase):
    def test_get_logit_mask_1(self):
        sol = [0, 1, 2, 0, 3, 4]
        demands = np.array([0, 5, 8, 3, 6])
        demands = {i: demands[i] for i in range(len(demands))}
        capacity = 15
        expected_mask = np.array([[-np.inf, 0., 0., 0., 0.],
                                  [0., -np.inf, 0., 0., 0.],
                                  [0., -np.inf, -np.inf, -np.inf, -np.inf],
                                  [-np.inf, -np.inf, -np.inf, 0., 0.],
                                  [0., -np.inf, -np.inf, -np.inf, 0.]])

        result_mask = get_logit_mask(sol, demands, capacity)

        np.testing.assert_array_equal(result_mask, expected_mask)

    def test_get_logit_mask_2(self):
        sol = [0, 1, 2, 0, 3, 4, 0]
        demands = np.array([0, 5, 8, 3, 6])
        demands = {i: demands[i] for i in range(len(demands))}
        capacity = 15
        expected_mask = np.array([[-np.inf, 0., 0., 0., 0.],
                                  [0., -np.inf, 0., 0., 0.],
                                  [0., -np.inf, -np.inf, -np.inf, -np.inf],
                                  [-np.inf, -np.inf, -np.inf, 0., 0.],
                                  [0., -np.inf, -np.inf, -np.inf, 0.],
                                  [0., -np.inf, -np.inf, -np.inf, -np.inf],])

        result_mask = get_logit_mask(sol, demands, capacity)

        np.testing.assert_array_equal(result_mask, expected_mask)

    def test_get_logit_mask_3(self):
        sol = [0, 1, 0, 3, 4, 0]
        demands = np.array([0, 5, 8, 3, 6])
        demands = {i: demands[i] for i in sorted(set(sol))}
        capacity = 15
        expected_mask = np.array([[-np.inf, 0., -np.inf, 0., 0.],
                                  [0., -np.inf, -np.inf, 0., 0.],
                                  [-np.inf, -np.inf, -np.inf, 0., 0.],
                                  [0., -np.inf, -np.inf, -np.inf, 0.],
                                  [0., -np.inf, -np.inf, -np.inf, -np.inf]])

        result_mask = get_logit_mask(sol, demands, capacity, city_size=5)

        np.testing.assert_array_equal(result_mask, expected_mask)

    def test_get_logit_mask_vector(self):
        prob = [0, 1, 3, 5, 6]
        sol = [0, 1, 3]
        demands = np.array([0, 5, 8, 3, 6])
        demands = {node: demands[i]
                   for i, node in enumerate(sorted(set(prob)))}
        capacity = 15
        mask = get_logit_mask_vector(
            prob, sol, demands, capacity, city_size=10)

        result_mask = get_logit_mask(
            [0, 1, 3, 0, 5, 6, 0], demands, capacity, city_size=10)

        np.testing.assert_array_equal(mask, result_mask[len(sol) - 1])

    def test_get_logit_mask_vector_2(self):
        prob = [0, 1, 3, 5, 6]
        sol = [0, 1, 3, 0, 5, 6]
        demands = np.array([0, 5, 8, 3, 6])
        demands = {node: demands[i]
                   for i, node in enumerate(sorted(set(prob)))}
        capacity = 15
        mask = get_logit_mask_vector(
            prob, sol, demands, capacity, city_size=10)

        result_mask = get_logit_mask(
            [0, 1, 3, 0, 5, 6, 0], demands, capacity, city_size=10)

        # -2 as the last position is invalid, the final node is always 0.
        np.testing.assert_array_equal(mask, result_mask[len(sol) - 1])


if __name__ == '__main__':
    unittest.main()
