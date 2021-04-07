import numpy as np
import random

from .interface import EnvInterface
from .action import Action

RED = (255, 51, 51)
ORANGE = (255, 153, 51)
YELLOW = (255, 255, 51)
GREEN = (51, 255, 51)
LIGHT_BLUE = (51, 255, 255)
BLUE = (51, 153, 255)

WIDTH = 40
HEIGHT = 25
SPACE_TOP = 4

N_LAYERS = 6
COLORS = [RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE]

BREAKOUT_ACTION_POOL = [Action.LEFT, Action.RIGHT]


class Ball:
    """The Ball class is responsible for the ball movement"""

    def __init__(self):
        self.pos = [random.choice(range(0, WIDTH)), SPACE_TOP + N_LAYERS + 1]
        self.vel = random.choice([[-1, 1], [1, 1]])

    def move(self):
        """Moves the ball in the direction of the velocity"""
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]


class Paddle:
    """The Paddle class is responsible for the paddle movement"""

    def __init__(self, size):
        self.y_pos = HEIGHT - 1
        self.x_start = WIDTH // 2 - size // 2
        self.x_end = self.x_start + size - 1

    def right(self):
        """Moves the paddle on cell to the right"""
        if self.x_end != WIDTH - 1:
            self.x_end += 1
            self.x_start += 1

    def left(self):
        """Moves the paddle on cell to the left"""
        if self.x_start != 0:
            self.x_start -= 1
            self.x_end -= 1


class BreakoutEnv(EnvInterface):
    """The BreakoutEnv class provides the logic of the Breakout environment as well as all necessary methods to connect
    with the reinforcement learning agents."""

    def __init__(self, paddle_size):
        self.paddle_size = paddle_size

        self.output_dim = 2

        self.paddle = None
        self.ball = None
        self.blocks = None

    def reset(self):
        """Resets the environment"""
        self.blocks = np.zeros(shape=(N_LAYERS, WIDTH))
        self.ball = Ball()
        self.paddle = Paddle(self.paddle_size)

        return self.get_state()

    def get_state(self):
        """Returns the state of the environment which consists of the paddle position and the ball position"""
        return [self.paddle.x_start / (WIDTH - 1), self.paddle.x_end / (WIDTH - 1),
                self.ball.pos[0] / (WIDTH - 1), self.ball.pos[1] / (HEIGHT - 1)]

    def step(self, action: Action):
        """Executes the action in the environment

        Returns:
            state: The new state of the environment after the action was executed.
            reward: The reward for the executed action.
            done: done = True if snake dies, else done = False.
        """
        reward = 0

        if action == Action.RIGHT:
            self.paddle.right()
        elif action == Action.LEFT:
            self.paddle.left()

        # left right walls
        if self.ball.pos[0] == 0 and self.ball.vel[0] == -1 or self.ball.pos[0] == WIDTH - 1 and self.ball.vel[0] == 1:
            self.ball.vel[0] *= -1

        # roof
        if self.ball.pos[1] == 0:
            self.ball.vel[1] *= -1

        # paddle
        if self.ball.pos[1] == HEIGHT - 2:
            if self.paddle.x_start <= self.ball.pos[0] <= self.paddle.x_end:
                reward += 1
                if self.ball.pos[0] <= self.paddle.x_end - self.paddle_size // 2:
                    self.ball.vel = [-1, -1]
                else:
                    self.ball.vel = [1, -1]

        # blocks
        ball_pos_ = [self.ball.pos[0] + self.ball.vel[0], self.ball.pos[1] + self.ball.vel[1]]

        if SPACE_TOP + N_LAYERS > ball_pos_[1] >= SPACE_TOP:

            # straight
            if self.blocks[ball_pos_[1] - SPACE_TOP, self.ball.pos[0]] == 0:
                self.blocks[ball_pos_[1] - SPACE_TOP, self.ball.pos[0]] = 1
                self.ball.vel[1] *= -1

            # diagonal
            elif self.blocks[ball_pos_[1] - SPACE_TOP, ball_pos_[0]] == 0:
                self.blocks[ball_pos_[1] - SPACE_TOP, ball_pos_[0]] = 1
                self.ball.vel[0] *= -1
                self.ball.vel[1] *= -1

        # check for walls again
        if self.ball.pos[0] == 0 and self.ball.vel[0] == -1 or self.ball.pos[0] == WIDTH - 1 and self.ball.vel[0] == 1:
            self.ball.vel[0] *= -1

        # only move when there's no block in the way
        ball_pos_ = [self.ball.pos[0] + self.ball.vel[0], self.ball.pos[1] + self.ball.vel[1]]
        if SPACE_TOP + N_LAYERS > ball_pos_[1] >= SPACE_TOP:
            if self.blocks[ball_pos_[1] - SPACE_TOP, ball_pos_[0]] == 1:
                self.ball.move()
        else:
            self.ball.move()

        if self.ball.pos[1] == HEIGHT - 1:
            done = True
            reward -= 10
        else:
            done = False

        # state, reward, done
        return self.get_state(), reward, done, None

    def screenshot(self):
        """Returns a screenshot of the environment as a numpy array"""
        arr = np.zeros([HEIGHT, WIDTH, 3], dtype=np.uint8)

        for row_idx, row in enumerate(self.blocks):
            for block_idx, block in enumerate(row):
                if block == 0:
                    arr[row_idx + SPACE_TOP][block_idx] = COLORS[row_idx]

        arr[self.ball.pos[1], self.ball.pos[0]] = RED

        for i in range(self.paddle.x_start, self.paddle.x_end + 1):
            arr[self.paddle.y_pos][i] = RED

        return arr
