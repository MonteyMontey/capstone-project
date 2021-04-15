import random
import numpy as np

from .action import Action

PONG_ACTION_POOL = [(Action.UP, Action.UP), (Action.UP, Action.DOWN), (Action.DOWN, Action.UP),
                    (Action.DOWN, Action.DOWN)]


class Ball:
    """The Ball class is responsible for the ball movement based on action input"""

    def __init__(self):
        self.pos = [random.choice(range(3, 13)), random.choice(range(9))]
        if self.pos[0] < 8:
            self.vel = random.choice([[1, 1], [1, -1]])
        else:
            self.vel = random.choice([[-1, 1], [-1, -1]])

    def move(self):
        """Moves the ball in the direction of the velocity"""
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]


class Paddle:
    """The Paddle class is responsible for the paddle movement based on action input"""

    def __init__(self):
        self.pos = 4

    def up(self):
        """Moves the paddle one cell up"""
        if self.pos != 1:
            self.pos -= 1

    def down(self):
        """Moves the paddle one cell down"""
        if self.pos != 7:
            self.pos += 1


class PongEnv:
    """The PongEnv class provides the logic of the Pong environment as well as all necessary methods to connect
            with the reinforcement learning agents."""

    def __init__(self):
        self.output_dim = 4

        self.ball = None
        self.left_paddle = None
        self.right_paddle = None

    def reset(self):
        """Resets the environment"""
        self.ball = Ball()
        self.left_paddle = Paddle()
        self.right_paddle = Paddle()

        return self.get_state()

    def step(self, action):
        """Executes the action in the environment

        Returns:
            state (list[float]): The new state of the environment after the action was executed.
            reward (float): The reward for the executed action.
            done (bool): done = True if snake dies, else done = False.
        """
        left_action, right_action = action
        reward = 0

        if left_action == Action.UP:
            self.left_paddle.up()
        elif left_action == Action.DOWN:
            self.left_paddle.down()

        if right_action == Action.UP:
            self.right_paddle.up()
        elif right_action == Action.DOWN:
            self.right_paddle.down()

        if (self.ball.pos[1] == 0 and self.ball.vel[1] == -1) or (self.ball.pos[1] == 8 and self.ball.vel[1] == 1):
            self.ball.vel[1] *= -1

        if self.ball.pos[0] == 2:
            if self.ball.pos[1] in [self.left_paddle.pos - 1, self.left_paddle.pos, self.left_paddle.pos + 1]:
                self.ball.vel[0] *= -1
                reward += 1

        elif self.ball.pos[0] == 13:
            if self.ball.pos[1] in [self.right_paddle.pos - 1, self.right_paddle.pos, self.right_paddle.pos + 1]:
                self.ball.vel[0] *= -1
                reward += 1

        self.ball.move()

        if self.ball.pos[0] == 0 or self.ball.pos[0] == 15:
            reward -= 1
            done = True
        else:
            done = False

        return self.get_state(), reward, done, None

    def screenshot(self):
        """Returns a screenshot of the environment as a numpy array"""
        arr = np.zeros([9, 16, 3], dtype=np.uint8)
        arr[:] = (0, 0, 0)

        white = (255, 255, 255)

        arr[self.left_paddle.pos - 1][1] = white
        arr[self.left_paddle.pos][1] = white
        arr[self.left_paddle.pos + 1][1] = white

        arr[self.right_paddle.pos - 1][14] = white
        arr[self.right_paddle.pos][14] = white
        arr[self.right_paddle.pos + 1][14] = white

        arr[self.ball.pos[1], self.ball.pos[0]] = white

        return arr

    def get_state(self):
        """Returns the state of the environment which consists of the left paddle position, the ball position, and the
            right paddle position"""
        return [self.left_paddle.pos / 9, self.ball.pos[0] / 16, self.ball.pos[1] / 9, self.right_paddle.pos / 9]
