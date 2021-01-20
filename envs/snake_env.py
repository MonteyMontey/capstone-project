import numpy as np
from enum import Enum
from typing import List, Tuple


class Action(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


class SnakeVision(Enum):
    UP = (0, -1)
    DIAG_UP_RIGHT = (1, -1)
    RIGHT = (1, 0)
    DIAG_DOWN_RIGHT = (1, 1)
    DOWN = (0, 1)
    DIAG_DOWN_LEFT = (-1, 1)
    LEFT = (-1, 0)
    DIAG_UP_LEFT = (-1, -1)


class Snake:
    def __init__(self, cells: List[Tuple], vel: Action = Action.UP):
        self.cells = cells
        self._last_action = vel

        self.cell_lookup = set()
        self.cell_lookup.update(cells)

    def move(self, action: Action):
        self.grow(action)
        self.cell_lookup.remove(self.cells.pop())

    def grow(self, action: Action):
        next_cell = self.next_cell(action)

        self.cells.insert(0, next_cell)
        self.cell_lookup.add(next_cell)

        if not self._is_180_turn(action):
            self._last_action = action

    def next_cell(self, action: Action):
        if self._is_180_turn(action):
            action = self._last_action

        snake_head = self.cells[0]
        next_cell = snake_head[0] + action.value[0], snake_head[1] + action.value[1]

        return next_cell

    def _is_180_turn(self, action: Action):
        return (action == Action.UP and self._last_action == Action.DOWN) or \
               (action == Action.DOWN and self._last_action == Action.UP) or \
               (action == Action.LEFT and self._last_action == Action.RIGHT) or \
               (action == Action.RIGHT and self._last_action == Action.LEFT)


class SnakeEnv:
    def __init__(self, grid_size: int = 7):
        if grid_size % 2 == 0 or grid_size < 3:
            raise ValueError("grid_size must be odd and greater than or equal to 3")

        self.grid_size = grid_size
        self._grid = self._make_grid()

        self._score = None
        self._snake = None
        self._food_cell = None

    def reset(self):
        self._score = 0
        self._spawn_snake()
        self._spawn_food()

        return self._get_state()

    def step(self, action: Action):
        next_cell = self._snake.next_cell(action)

        if self._is_snake(next_cell) or self._is_wall(next_cell):
            done = True
            reward = -1
        else:
            done = False
            if next_cell == self._food_cell:
                self._snake.grow(action)
                self._score += 1
                self._spawn_food()
                reward = 1
            else:
                self._snake.move(action)
                reward = -0.1

        return self._get_state(), reward, done, self._score

    def _get_state(self):
        snake_head = self._snake.cells[0]

        food_distance_x, food_distance_y = np.subtract(snake_head, self._food_cell)
        food_data = [food_distance_x / self.grid_size, food_distance_y / self.grid_size]

        snake_pos_x = (snake_head[1] + 1) / self.grid_size
        snake_pos_y = (snake_head[0] + 1) / self.grid_size
        wall_data = [snake_pos_x, snake_pos_y]

        snake_data = []
        for vision in SnakeVision:
            snake_data.append(self._dist_to_snake(snake_head, vision))

        return np.array(food_data + wall_data + snake_data, dtype=np.float32)

    def screenshot(self):
        arr = np.zeros([self.grid_size, self.grid_size, 3], dtype=np.uint8)
        arr[:] = (0, 0, 0)

        arr[self._food_cell[1]][self._food_cell[0]] = (0, 255, 127)

        for idx, snake_grid in enumerate(self._snake.cells):
            if idx == 0:
                arr[snake_grid[1]][snake_grid[0]] = (0, 191, 255)
            else:
                arr[snake_grid[1]][snake_grid[0]] = (65, 105, 225)

        return arr

    def _is_wall(self, cell: Tuple):
        return True if cell[0] >= self.grid_size or cell[1] >= self.grid_size or cell[0] < 0 or cell[1] < 0 else False

    def _is_snake(self, cell: Tuple):
        return True if cell in self._snake.cell_lookup else False

    def _spawn_snake(self):
        snake_cells = []
        snake_x = self.grid_size // 2
        for i in range(2):
            snake_cells.append((snake_x, self.grid_size // 2 + i))

        self._snake = Snake(snake_cells)

    def _spawn_food(self):
        available_cells = list(self._grid.difference(self._snake.cell_lookup))
        self._food_cell = available_cells[np.random.choice(len(available_cells))]

    def _dist_to_snake(self, pos, direction):
        dist = 0
        while True:
            pos = pos[0] + direction.value[0], pos[1] + direction.value[1]
            dist += 1
            if self._is_snake(pos):
                return dist / self.grid_size
            if self._is_wall(pos):
                return 1

    def _make_grid(self):
        grid = set()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                grid.add((i, j))
        return grid
