import numpy as np
from copy import deepcopy
import unittest
from envs.breakout_env import BreakoutEnv, Action


class TestBreakoutEnv(unittest.TestCase):

    def test_step(self):
        env = BreakoutEnv(15)
        env.reset()

        ball_pos = deepcopy(env.ball.pos)
        ball_vel = deepcopy(env.ball.vel)
        paddle_y_pos = deepcopy(env.paddle.y_pos)
        paddle_x_start = env.paddle.x_start
        paddle_x_end = env.paddle.x_end

        action = Action.RIGHT
        env.step(action)

        # check ball pos
        self.assertTrue(env.ball.pos == [ball_pos[0] + ball_vel[0], ball_pos[1] + ball_vel[1]])

        # check paddle pos
        self.assertTrue(
            env.paddle.x_start == paddle_x_start + action.value[0] and
            env.paddle.x_end == paddle_x_end + action.value[0] and
            env.paddle.y_pos == paddle_y_pos)


if __name__ == "__main__":
    unittest.main()
