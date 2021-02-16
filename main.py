import sys
import time

from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Slot, QThreadPool, QRunnable

from gui import Ui_GUI

from envs.snake_env import SnakeEnv, Action
from envs.pong_env import PongEnv
from envs.breakout_env import BreakoutEnv

from rl_algorithms.dqn import DQNAgent


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_GUI()
        self.ui.setupUi(self)


class Worker(QRunnable):
    @Slot()
    def run(self):
        global env

        rl_algo = window.ui.algComboBox.currentText()
        rl_agent = ALG_OBJECT_MAP[rl_algo](27, 64, 32, 4, 0.001, 0.999, 1, 1_000_000, 32)

        for i in range(100):
            done = False
            state = env.reset()

            while not done:
                action = rl_agent.choose_action(state)

                if action == 0:
                    converted_action = Action.UP
                elif action == 1:
                    converted_action = Action.RIGHT
                elif action == 2:
                    converted_action = Action.DOWN
                else:
                    converted_action = Action.LEFT

                state_, reward, done, score = env.step(converted_action)
                score += reward

                rl_agent.store_transition(state, action, reward, state_, done)
                rl_agent.learn()

                state = state_

                update_env_canvas()
                QApplication.processEvents()
                time.sleep(0.2)


@Slot()
def start_training():
    window.ui.startButton.setEnabled(False)
    window.ui.envComboBox.setEnabled(False)
    window.ui.algComboBox.setEnabled(False)

    worker = Worker()
    thread_pool.start(worker)


@Slot(str)
def env_changed(selection):
    init_env(selection)
    update_env_canvas()
    swap_env_configs(selection)


@Slot()
def env_config_changed():
    global env
    env_name = env.__class__.__name__

    config = get_env_config(env_name)

    env = ENV_NAME_TO_OBJECT_MAP[env_name](*config)
    env.reset()

    update_env_canvas()


def get_env_config(env_name):
    global env

    if env_name == "SnakeEnv":
        config = get_snake_env_config()
    else:
        config = []

    return config


@Slot(str)
def alg_changed(selection):
    change_alg_configs(selection)


def alg_config_changed(selection):
    pass


def get_snake_env_config():
    grid_size_index = window.ui.gridSizeComboBox.currentIndex()
    grid_size = [3, 5, 7, 9][grid_size_index]

    snake_vision_index = window.ui.snakeVisionComboBox.currentIndex()
    snake_vision = [1, 2, 3, 4, 5][snake_vision_index]

    return grid_size, snake_vision


def change_alg_configs(selection):
    alg_stacked_widget = window.ui.algStackedWidget

    if selection == "DQN":
        alg_stacked_widget.setCurrentIndex(1)
    else:
        alg_stacked_widget.setCurrentIndex(0)


def init_env(env_name):
    global env

    env_config = get_env_config(env_name)
    env = ENV_SELECTION_TO_OBJECT_MAP[env_name](*env_config)
    env.reset()


def update_env_canvas():
    global env

    zoom = ENV_ZOOM_MAP[env.__class__.__name__]

    img = env.screenshot().repeat(zoom, axis=0).repeat(zoom, axis=1)

    q_img = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
    q_pix = QPixmap.fromImage(q_img)

    scene = QGraphicsScene(window)
    scene.addPixmap(q_pix)
    window.ui.envView.setScene(scene)


def swap_env_configs(selection):
    env_stacked_widget = window.ui.envStackedWidget

    if selection == "Breakout":
        env_stacked_widget.setCurrentIndex(1)
    elif selection == "Snake":
        env_stacked_widget.setCurrentIndex(0)


ENV_SELECTION_TO_OBJECT_MAP = {"Snake": SnakeEnv, "Breakout": BreakoutEnv, "Pong": PongEnv}
ENV_NAME_TO_OBJECT_MAP = {"SnakeEnv": SnakeEnv, "BreakoutEnv": BreakoutEnv, "PongEnv": PongEnv}

ENV_ZOOM_MAP = {"SnakeEnv": 30, "BreakoutEnv": 8, "PongEnv": 20}

ALG_OBJECT_MAP = {"DQN": DQNAgent}

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    thread_pool = QThreadPool()
    print("Multithreading with maximum %d threads" % thread_pool.maxThreadCount())

    env = SnakeEnv()

    env_selection = window.ui.envComboBox.currentText()
    env_changed(env_selection)

    window.ui.envComboBox.currentTextChanged.connect(env_changed)

    window.ui.gridSizeComboBox.currentIndexChanged.connect(env_config_changed)
    window.ui.snakeVisionComboBox.currentIndexChanged.connect(env_config_changed)

    window.ui.algComboBox.currentTextChanged.connect(alg_changed)

    window.ui.startButton.clicked.connect(start_training)

    window.show()

    sys.exit(app.exec_())
