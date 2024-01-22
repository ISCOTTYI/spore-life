import unittest
import numpy as np
from gol import GameOfLife, DormantLife, ALIVE, DORM, DEAD
from lifetime_distribution import lifetime_distribution

class TestDormantLife(unittest.TestCase):
    def test_ALIVE_DORM_conversion(self):
        test_grid = np.array([
            [DEAD, ALIVE, DEAD],
            [DEAD, ALIVE, DEAD],
            [DEAD, DEAD, DEAD]
        ])
        gol = DormantLife(test_grid)
        grid_step = gol.step()
        res = np.array([
            [DEAD, DORM, DEAD],
            [DEAD, DORM, DEAD],
            [DEAD, DEAD, DEAD]
        ])
        np.testing.assert_array_equal(res, grid_step)
    
    def test_periodic_boundary(self):
        test_grid = np.array([
            [ALIVE, DEAD, ALIVE],
            [DEAD, ALIVE, DEAD],
            [DEAD, DEAD, ALIVE]
        ])
        gol = DormantLife(test_grid)
        grid_step = gol.step()
        np.testing.assert_array_equal(test_grid, grid_step)
    
    def test_limit_cases_stochasticity(self):
        test_grid = np.array([
            [DEAD, ALIVE, DEAD],
            [DEAD, DORM, DEAD],
            [DEAD, ALIVE, DEAD]
        ])
        # alpha = 0 should get us GameOfLife step with DEAD == DORM.
        gol = DormantLife(test_grid, alpha=0)
        gol_grid_step = gol.step()
        gol_res = np.array([
            [DEAD, DORM, DEAD],
            [DEAD, DORM, DEAD],
            [DEAD, DORM, DEAD]
        ])
        np.testing.assert_array_equal(gol_res, gol_grid_step)
        # alpha = 1 should get us determinstic DormantLife step.
        dl = DormantLife(test_grid, alpha=1)
        dl_grid_step = dl.step()
        dl_res = np.array([
            [DEAD, DORM, DEAD],
            [DEAD, ALIVE, DEAD],
            [DEAD, DORM, DEAD]
        ])
        np.testing.assert_array_equal(dl_res, dl_grid_step)

    def test_p_grid_decay(self):
        gol = DormantLife(np.full((3, 3), DEAD), alpha=0.5)
        gol.step()
        np.testing.assert_array_equal(gol.p_grid, np.full((3, 3), 0.5))
    
    def test_p_grid_reset(self):
        test_grid = np.array([
            [ALIVE, ALIVE, DEAD],
            [DEAD, DEAD, DEAD],
            [DEAD, DEAD, DEAD]
        ])
        gol = DormantLife(test_grid, alpha=0.5)
        gol.step()
        res_p_grid = np.full((3, 3), 0.5); res_p_grid[0, 0:2] = 1
        np.testing.assert_array_equal(gol.p_grid, res_p_grid)
    
    def test_stochastic_update(self):
        test_grid = np.array([
            [DORM, ALIVE, DEAD],
            [DORM, ALIVE, DEAD],
            [DEAD, DEAD, DEAD]
        ])
        gol = DormantLife(test_grid, seed=1, alpha=0.6)
        grid_step = gol.step()
        res = np.array([
            [ALIVE, DORM, DEAD],
            [DORM, DORM, DEAD],
            [DEAD, DEAD, DEAD]
        ])
        np.testing.assert_array_equal(grid_step, res)
    
    # def test_transitions(self):
    #     test_grid = np.array([
    #         [DEAD, ALIVE, DORM],
    #         [DEAD, ALIVE, DORM],
    #         [DEAD, DEAD, DEAD]
    #     ])
    #     gol = DormantLife(test_grid)
    #     grid_step = gol.step()
    #     self.assertEqual(gol.transitions_from(test_grid, ALIVE, DORM), 2)
    #     self.assertEqual(gol.transitions_from(test_grid, DORM, ALIVE), 2)
    #     self.assertEqual(gol.transitions_from(test_grid, ALIVE, DEAD), 0)
    #     self.assertEqual(gol.transitions_from(test_grid, DEAD, ALIVE), 0)
        

class TestLifetimeDistribution(unittest.TestCase):
    def test_lifetime_measuring(self):
        test_grid = np.array([
                [DEAD, ALIVE, DEAD],
                [DEAD, ALIVE, ALIVE],
                [DEAD, DEAD, DEAD]
        ])
        dl = DormantLife(test_grid)
        self.assertDictEqual(
            lifetime_distribution(ALIVE, dl, 3, 0, exclude_alive_after_trans=0),
            {0: 6, 1: 3})
    
    def test_exclude_alive_after_trans(self):
        test_grid = np.array([
                [DEAD, ALIVE, DEAD],
                [DEAD, ALIVE, ALIVE],
                [DEAD, DEAD, DEAD]
        ])
        dl = DormantLife(test_grid)
        self.assertDictEqual(
            lifetime_distribution(ALIVE, dl, 3, 0, exclude_alive_after_trans=1),
            {0: 6})


if __name__ == '__main__':
    unittest.main()
