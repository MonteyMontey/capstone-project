import numpy as np
import random

RED = (255, 51, 51)
ORANGE = (255, 153, 51)
YELLOW = (255, 255, 51)
GREEN = (51, 255, 51)
LIGHT_BLUE = (51, 255, 255)
BLUE = (51, 153, 255)

WIDTH = 40
HEIGHT = 25
PADDLE_SIZE = 30
SPACE_TOP = 4

N_LAYERS = 6
COLORS = [RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE]


class Ball:
    def __init__(self):
        self.pos = [random.choice(range(0, WIDTH)), SPACE_TOP + N_LAYERS + 1]
        self.vel = random.choice([[-1, 1], [1, 1]])

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]


class Paddle:
    def __init__(self):
        self.y_pos = HEIGHT - 1
        self.x_start = WIDTH // 2 - PADDLE_SIZE // 2
        self.x_end = self.x_start + PADDLE_SIZE - 1

    def right(self):
        if self.x_end != WIDTH - 1:
            self.x_end += 1
            self.x_start += 1

    def left(self):
        if self.x_start != 0:
            self.x_start -= 1
            self.x_end -= 1


class BreakoutEnv:
    def __init__(self):
        self.paddle = None
        self.ball = None
        self.blocks = None

    def reset(self):
        self.blocks = np.zeros(shape=(N_LAYERS, WIDTH))
        self.ball = Ball()
        self.paddle = Paddle()

        return self._get_state()

    def _get_state(self):
        return [self.paddle.x_start / (WIDTH - 1), self.paddle.x_end / (WIDTH - 1),
                self.ball.pos[0] / (WIDTH - 1), self.ball.pos[1] / (HEIGHT - 1)]

    def step(self, action):
        reward = 0

        if action:
            self.paddle.right()
        else:
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
                if self.ball.pos[0] <= self.paddle.x_end - PADDLE_SIZE // 2:
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
        return self._get_state(), reward, done

    def screenshot(self):
        arr = np.zeros([HEIGHT, WIDTH, 3], dtype=np.uint8)

        for row_idx, row in enumerate(self.blocks):
            for block_idx, block in enumerate(row):
                if block == 0:
                    arr[row_idx + SPACE_TOP][block_idx] = COLORS[row_idx]

        arr[self.ball.pos[1], self.ball.pos[0]] = RED

        for i in range(self.paddle.x_start, self.paddle.x_end + 1):
            arr[self.paddle.y_pos][i] = RED

        return arr
