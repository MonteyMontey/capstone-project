import numpy as np
from copy import deepcopy
import unittest
from envs.pong_env import PongEnv, Action


class TestPongEnv(unittest.TestCase):

    def test_step_up(self):
        env = PongEnv()
        env.reset()

        left_paddle_pos = env.left_paddle.pos
        right_paddle_pos = env.right_paddle.pos

        for i in range(3):
            env.step((Action.UP, Action.UP))
            self.assertTrue(
                env.left_paddle.pos == left_paddle_pos - (i + 1) and env.right_paddle.pos == right_paddle_pos - (i + 1))

        # Paddle should hit the ceiling and not move up further
        left_paddle_pos = env.left_paddle.pos
        right_paddle_pos = env.right_paddle.pos
        env.step((Action.UP, Action.UP))
        self.assertTrue(left_paddle_pos == env.left_paddle.pos and right_paddle_pos == env.right_paddle.pos)

    def test_step_down(self):
        env = PongEnv()
        env.reset()

        left_paddle_pos = env.left_paddle.pos
        right_paddle_pos = env.right_paddle.pos

        for i in range(3):
            env.step((Action.DOWN, Action.DOWN))
            self.assertTrue(
                env.left_paddle.pos == left_paddle_pos + (i + 1) and env.right_paddle.pos == right_paddle_pos + (i + 1))

        # Paddle should hit the floor and not move down further
        left_paddle_pos = env.left_paddle.pos
        right_paddle_pos = env.right_paddle.pos
        env.step((Action.DOWN, Action.DOWN))
        self.assertTrue(left_paddle_pos == env.left_paddle.pos and right_paddle_pos == env.right_paddle.pos)

    def test_get_state(self):
        env = PongEnv()
        env.reset()

        left_paddle_pos = env.left_paddle.pos
        right_paddle_pos = env.right_paddle.pos
        ball_pos = deepcopy(env.ball.pos)
        ball_vel = deepcopy(env.ball.vel)

        new_state = env.step((Action.UP, Action.DOWN))

        self.assertTrue(
            new_state[0] == [(left_paddle_pos - 1) / 9, (ball_pos[0] + ball_vel[0]) / 16,
                             (ball_pos[1] + ball_vel[1]) / 9, (right_paddle_pos + 1) / 9])


if __name__ == "__main__":
    unittest.main()
