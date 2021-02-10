import sys
import random
import time

from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Slot, QThreadPool, QRunnable

from gui import Ui_GUI

from envs.snake_env import SnakeEnv, Action
from envs.pong_env import PongEnv
from envs.breakout_env import BreakoutEnv


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_GUI()
        self.ui.setupUi(self)


class Worker(QRunnable):
    @Slot()
    def run(self):
        global env

        done = False
        while not done:
            _, _, done, _ = env.step(random.choice(list(Action)))
            update_display()
            QApplication.processEvents()
            time.sleep(1)


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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    thread_pool = QThreadPool()
    print("Multithreading with maximum %d threads" % thread_pool.maxThreadCount())

    env = SnakeEnv()

    env_selection = window.ui.envComboBox.currentText()
    change_env(env_selection)

    window.ui.envComboBox.currentTextChanged.connect(change_env)

    window.ui.startButton.clicked.connect(start_training)

    window.show()

    sys.exit(app.exec_())
