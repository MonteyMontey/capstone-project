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

                update_display()
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
def change_env(selection):
    global env

    env = ENV_OBJECT_MAP[selection]()
    env.reset()

    update_display()
    change_env_configs(selection)


@Slot(str)
def change_alg(selection):
    change_alg_configs(selection)


def change_env_configs(selection):
    env_stacked_widget = window.ui.envStackedWidget

    if selection == "Breakout":
        env_stacked_widget.setCurrentIndex(1)
    elif selection == "Snake":
        env_stacked_widget.setCurrentIndex(0)


def change_alg_configs(selection):
    alg_stacked_widget = window.ui.algStackedWidget

    if selection == "DQN":
        alg_stacked_widget.setCurrentIndex(1)
    else:
        alg_stacked_widget.setCurrentIndex(0)


def update_display():
    global env

    zoom = ENV_ZOOM_MAP[env.__class__.__name__]

    img = env.screenshot().repeat(zoom, axis=0).repeat(zoom, axis=1)

    q_img = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
    q_pix = QPixmap.fromImage(q_img)

    scene = QGraphicsScene(window)
    scene.addPixmap(q_pix)
    window.ui.envView.setScene(scene)


ENV_OBJECT_MAP = {"Snake": SnakeEnv, "Breakout": BreakoutEnv, "Pong": PongEnv}
ENV_ZOOM_MAP = {"SnakeEnv": 30, "BreakoutEnv": 8, "PongEnv": 20}

ALG_OBJECT_MAP = {"DQN": DQNAgent}

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    thread_pool = QThreadPool()
    print("Multithreading with maximum %d threads" % thread_pool.maxThreadCount())

    env = SnakeEnv()

    env_selection = window.ui.envComboBox.currentText()
    change_env(env_selection)

    window.ui.envComboBox.currentTextChanged.connect(change_env)

    window.ui.algComboBox.currentTextChanged.connect(change_alg)

    window.ui.startButton.clicked.connect(start_training)

    window.show()

    sys.exit(app.exec_())
