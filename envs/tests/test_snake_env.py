import numpy as np
import unittest
from envs.snake_env import SnakeEnv, Action


class TestSnakeEnv(unittest.TestCase):
    def test_env_init(self):
        self.assertRaises(ValueError, SnakeEnv, 2)
        self.assertRaises(ValueError, SnakeEnv, 4)

    def test_step(self):
        env = SnakeEnv()
        env.reset()
        spawn_pos = env._snake.cells[0]

        env.step(Action.UP)
        pos = env._snake.cells[0]
        self.assertTrue(spawn_pos[0] == pos[0] and spawn_pos[1] - 1 == pos[1])

        env.step(Action.RIGHT)
        pos = env._snake.cells[0]
        self.assertTrue(spawn_pos[0] + 1 == pos[0] and spawn_pos[1] - 1 == pos[1])

        env.step(Action.DOWN)
        pos = env._snake.cells[0]
        self.assertTrue(spawn_pos[0] + 1 == pos[0] and spawn_pos[1] == pos[1])

        env.step(Action.LEFT)
        pos = env._snake.cells[0]
        self.assertEqual(spawn_pos, pos)

    def test_is_wall(self):
        env = SnakeEnv(7)

        for cell in [(-1, 0), (0, -1), (7, 0), (0, 7)]:
            self.assertTrue(env._is_wall(cell))

        for cell in [(3, 3), (0, 0), (0, 6), (6, 6), (6, 0)]:
            self.assertFalse(env._is_wall(cell))

    def test_is_snake(self):
        env = SnakeEnv(7)
        env.reset()

        self.assertTrue(env._is_snake((3, 3)))
        self.assertTrue(env._is_snake((3, 4)))

        self.assertFalse(env._is_snake((3, 2)))
        env.step(Action.UP)
        self.assertTrue(env._is_snake((3, 2)))

    def test_surrounding_cell_state(self):
        env = SnakeEnv(7, 1)
        env.reset()
        surrounding_cell_state = env._surrounding_cell_state()
        self.assertCountEqual(surrounding_cell_state, [0, 0, 0, 0, 1, 0, 0, 1, 0])

        env = SnakeEnv(7, 2)
        env.reset()
        surrounding_cell_state = env._surrounding_cell_state()
        self.assertCountEqual(surrounding_cell_state,
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])


if __name__ == "__main__":
    unittest.main()
