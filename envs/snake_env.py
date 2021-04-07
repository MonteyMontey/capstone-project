import numpy as np
from typing import List, Tuple

from .interface import EnvInterface
from .action import Action

SNAKE_ACTION_POOL = [Action.UP, Action.RIGHT, Action.DOWN, Action.LEFT]


class Snake:
    """
    The Snake class is responsible for movement through the environment based on action input.

    Args:
        cells (List[Tuple]): The coordinates of the cells that the Snake is initiated in.
        vel (Action): Optional argument to set the last action of the snake, which is needed as fallback if the next
            action is invalid.
    """

    def __init__(self, cells: List[Tuple], vel: Action = Action.UP):
        self.cells = cells
        self._last_action = vel

        self.cell_lookup = set()
        self.cell_lookup.update(cells)

    def move(self, action: Action):
        """Moves the snake by one grid in the direction of the action"""
        self.grow(action)
        self.cell_lookup.remove(self.cells.pop())

    def grow(self, action: Action):
        """Extends the snake by one grid in the direction of the action"""
        next_cell = self.next_cell(action)

        self.cells.insert(0, next_cell)
        self.cell_lookup.add(next_cell)

        if not self._is_180_turn(action):
            self._last_action = action

    def next_cell(self, action: Action):
        """Returns the coordinates of the upcoming cell based on the action"""
        if self._is_180_turn(action):
            action = self._last_action

        snake_head = self.cells[0]
        next_cell = snake_head[0] + action.value[0], snake_head[1] + action.value[1]

        return next_cell

    def _is_180_turn(self, action: Action):
        """Checks whether the action is the opposite of the last action"""
        return (action == Action.UP and self._last_action == Action.DOWN) or \
               (action == Action.DOWN and self._last_action == Action.UP) or \
               (action == Action.LEFT and self._last_action == Action.RIGHT) or \
               (action == Action.RIGHT and self._last_action == Action.LEFT)


class SnakeEnv(EnvInterface):
    """
    The SnakeEnv class provides the logic of the snake environment as well as all necessary methods to connect with the
    reinforcement learning agents.

    Args:
        grid_size (int): The dimensions of the environment: Env dimension = grid_size x grid_size. Grid size must be odd
            and greater than or equal to 3.
        vision (int): The snake's vision aka. the area around the head of the snake which state is returned as input to
            the RL agent. Snake size must be greater than or equal to 1.
    """

    def __init__(self, grid_size: int = 7, vision: int = 2):
        if grid_size % 2 == 0 or grid_size < 3:
            raise ValueError("grid_size must be odd and greater than or equal to 3")
        if vision < 0:
            raise ValueError("vision must be greater than or equal to 1")

        self.grid_size = grid_size
        self._grid = self._make_grid()

        self.vision = vision

        self._score = None
        self._snake = None
        self._food_cell = None

        self.output_dim = 4

    def reset(self):
        """Resets the environment"""
        self._score = 0
        self._spawn_snake()
        self._spawn_food()

        return self.get_state()

    def step(self, action: Action):
        """Executes the action in the environment

        Returns:
            state: The new state of the environment after the action was executed.
            reward: The reward for the executed action.
            done: done = True if snake dies, else done = False.
            score: How many pieces of food the snake ate so far.
        """

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
                reward = 10
            else:
                self._snake.move(action)
                reward = -0.1

        return self.get_state(), reward, done, self._score

    def get_state(self):
        """Returns the state of the environment which consists of the state of the area around the snake's head and the
            position of the food"""
        snake_head = self._snake.cells[0]

        food_distance_x, food_distance_y = np.subtract(snake_head, self._food_cell)
        food_position = [food_distance_x / self.grid_size, food_distance_y / self.grid_size]

        return np.array(food_position + self._surrounding_cell_state(snake_head), dtype=np.float32)

    def screenshot(self):
        """Returns a screenshot of the environment as a numpy array"""
        arr = np.zeros([self.grid_size, self.grid_size, 3], dtype=np.uint8)
        arr[:] = (0, 0, 0)

        arr[self._food_cell[1]][self._food_cell[0]] = (0, 255, 127)

        for idx, snake_grid in enumerate(self._snake.cells):
            if idx == 0:
                arr[snake_grid[1]][snake_grid[0]] = (0, 191, 255)
            else:
                arr[snake_grid[1]][snake_grid[0]] = (65, 105, 225)

        for y in range(self.vision * 2 + 1):
            for x in range(self.vision * 2 + 1):
                cell = (self._snake.cells[0][0] - self.vision + x, self._snake.cells[0][1] - self.vision + y)
                if not self._is_wall(cell) and not self._is_snake(cell) and not cell == self._food_cell:
                    arr[cell[1]][cell[0]] = (10, 10, 10)

        return arr

    def _is_wall(self, cell: Tuple):
        """Checks whether a specific cell is a wall"""
        return True if cell[0] >= self.grid_size or cell[1] >= self.grid_size or cell[0] < 0 or cell[1] < 0 else False

    def _is_snake(self, cell: Tuple):
        """Checks whether a specific cell is part of the snake"""
        return True if cell in self._snake.cell_lookup else False

    def _surrounding_cell_state(self, snake_head):
        """Returns the state of each cell around the snake's head. State = 1 if the cell is either part of the snake or
            a wall, State = 0 if cell is free"""
        surrounding_cells_state = []
        for y in range(self.vision * 2 + 1):
            for x in range(self.vision * 2 + 1):
                cell = (snake_head[0] - self.vision + x, snake_head[1] - self.vision + y)
                surrounding_cells_state.append(self._is_snake(cell) or self._is_wall(cell))

        return surrounding_cells_state

    def _spawn_snake(self):
        """Spawns the snake in the environments"""
        snake_cells = []
        snake_x = self.grid_size // 2
        for i in range(2):
            snake_cells.append((snake_x, self.grid_size // 2 + i))

        self._snake = Snake(snake_cells)

    def _spawn_food(self):
        """Spawns the food in the environment"""
        available_cells = list(self._grid.difference(self._snake.cell_lookup))
        self._food_cell = available_cells[np.random.choice(len(available_cells))]

    def _make_grid(self):
        """Creates the environment grid"""
        grid = set()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                grid.add((i, j))
        return grid
