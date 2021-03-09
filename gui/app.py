import time
import random
import numpy as np

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThreadPool, QRunnable, QTimer, QObject, QMutex
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene

from envs.breakout_env import BreakoutEnv
from envs.pong_env import PongEnv
from envs.snake_env import SnakeEnv, Action
from gui.mainwindow import Ui_GUI
from rl_algorithms.dqn import DQNAgent

ENV_NAME_TO_OBJECT = {"Snake": SnakeEnv, "Breakout": BreakoutEnv, "Pong": PongEnv}
ENV_ZOOM = {"SnakeEnv": 30, "BreakoutEnv": 10, "PongEnv": 25}

ALG_NAME_TO_OBJECT = {"DQN": DQNAgent}


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_GUI()
        self.ui.setupUi(self)

        self.thread_pool = QThreadPool()
        print("Detected %d cores" % self.thread_pool.maxThreadCount())

        self.ui.mplWidget.canvas.ax.set_ylabel('score')
        self.ui.mplWidget.canvas.ax.set_xlabel('steps')

        # https://www.learnpyqt.com/tutorials/plotting-matplotlib/
        # self.timer = QTimer()
        # self.timer.setInterval(1000)
        # self.timer.timeout.connect(self.update_learning_curve_canvas)
        # self.timer.start()

        # initialize environment
        self.env = None  # TODO: init interface
        env_selection = self.ui.envComboBox.currentText()
        self.env_changed(env_selection)

        # setup triggers
        self.ui.envComboBox.currentTextChanged.connect(self.env_changed)

        self.ui.gridSizeComboBox.currentIndexChanged.connect(self.update_snake_vision_selections)
        self.ui.gridSizeComboBox.currentIndexChanged.connect(self.snake_env_config_changed)

        self.ui.snakeVisionComboBox.currentIndexChanged.connect(self.snake_env_config_changed)

        self.ui.algComboBox.currentTextChanged.connect(self.alg_changed)

        self.ui.startButton.clicked.connect(self.start_training)

    def init_env(self, env_name):
        config = None

        if env_name == "Snake":
            config = self.get_snake_env_config()
        elif env_name == "Breakout":
            config = self.get_breakout_env_config()
        elif env_name == "Pong":
            config = self.get_pong_env_config()

        self.env = ENV_NAME_TO_OBJECT[env_name](*config)
        self.env.reset()

    def swap_env_configs(self, env_name):
        env_stacked_widget = self.ui.envStackedWidget

        if env_name == "Snake":
            env_stacked_widget.setCurrentIndex(0)
        elif env_name == "Breakout":
            env_stacked_widget.setCurrentIndex(1)
        elif env_name == "Pong":
            env_stacked_widget.setCurrentIndex(2)

    def get_snake_env_config(self):
        grid_size_index = self.ui.gridSizeComboBox.currentIndex()
        grid_size = [5, 7, 9][grid_size_index]

        snake_vision_index = self.ui.snakeVisionComboBox.currentIndex()
        snake_vision = [1, 2, 3, 4][snake_vision_index]

        return grid_size, snake_vision

    def get_breakout_env_config(self):
        return []

    def get_pong_env_config(self):
        return []

    @pyqtSlot(str)
    def env_changed(self, env_name):
        self.init_env(env_name)
        self.swap_env_configs(env_name)
        self.update_env_canvas()

    @pyqtSlot(str)
    def alg_changed(self, alg_name):
        self.swap_alg_configs(alg_name)

    def swap_alg_configs(self, alg_name):
        alg_stacked_widget = self.ui.algStackedWidget

        if alg_name == "DQN":
            alg_stacked_widget.setCurrentIndex(0)
        else:
            alg_stacked_widget.setCurrentIndex(1)

    @pyqtSlot(int)
    def update_snake_vision_selections(self, index):
        self.ui.snakeVisionComboBox.clear()
        items = ["1", "2", "3", "4"]
        for i in range(index + 2):
            self.ui.snakeVisionComboBox.addItem(items[i])

    @pyqtSlot()
    def snake_env_config_changed(self):
        config = self.get_snake_env_config()
        self.env = SnakeEnv(*config)
        self.env.reset()
        self.update_env_canvas()

    @pyqtSlot()
    def breakout_env_config_changed(self):
        config = self.get_breakout_env_config()
        self.env = BreakoutEnv()
        self.env.reset()
        self.update_env_canvas()

    @pyqtSlot()
    def pong_env_config_changed(self):
        config = self.get_pong_env_config()
        self.env = PongEnv()
        self.env.reset()
        self.update_env_canvas()

    @pyqtSlot()
    def start_training(self):
        self.disable_config()

        alg = self.ui.algComboBox.currentText()
        alg_config = ()
        if alg == "DQN":
            alg_config = self.get_alg_config()

        worker = Worker(self, alg, alg_config)

        # noinspection PyUnresolvedReferences
        worker.signals.update_env.connect(self.update_env_canvas)
        # noinspection PyUnresolvedReferences
        worker.signals.update_learning_graph.connect(self.update_learning_curve_canvas)

        self.thread_pool.start(worker)

    def get_alg_config(self):
        lr = self.ui.learningRateDoubleSpinBox.value()
        gamma = self.ui.gammaDoubleSpinBox.value()
        batch_size = self.ui.batchSizeSpinBox.value()
        epsilon = self.ui.epsilonDoubleSpinBox.value()
        eps_dec = self.ui.epsilonDecDoubleSpinBox.value()
        eps_min = self.ui.epsilonMinSpinBox.value()
        n_layer_1 = self.ui.layer1SpinBox.value()
        n_layer_2 = self.ui.layer2SpinBox.value()

        return lr, gamma, batch_size, epsilon, eps_dec, eps_min, n_layer_1, n_layer_2

    def disable_config(self):
        self.ui.envComboBox.setEnabled(False)
        self.ui.gridSizeComboBox.setEnabled(False)
        self.ui.snakeVisionComboBox.setEnabled(False)
        self.ui.algComboBox.setEnabled(False)
        self.ui.learningRateDoubleSpinBox.setEnabled(False)
        self.ui.gammaDoubleSpinBox.setEnabled(False)
        self.ui.batchSizeSpinBox.setEnabled(False)
        self.ui.epsilonDoubleSpinBox.setEnabled(False)
        self.ui.epsilonDecDoubleSpinBox.setEnabled(False)
        self.ui.epsilonMinSpinBox.setEnabled(False)
        self.ui.layer1SpinBox.setEnabled(False)
        self.ui.layer2SpinBox.setEnabled(False)
        self.ui.startButton.setEnabled(False)

    def update_learning_curve_canvas(self, data):
        score_history = data[0]
        x = data[1]

        running_avg = np.zeros(len(score_history))
        for i in range(len(running_avg)):
            running_avg[i] = np.mean(score_history[max(0, i - 100):(i + 1)])

        self.ui.mplWidget.canvas.ax.cla()
        self.ui.mplWidget.canvas.ax.set_ylabel('score')
        self.ui.mplWidget.canvas.ax.set_xlabel('steps')
        self.ui.mplWidget.canvas.ax.plot(x, running_avg, '#3399FF')
        self.ui.mplWidget.canvas.draw()

    def update_env_canvas(self):
        zoom = ENV_ZOOM[self.env.__class__.__name__]

        img = self.env.screenshot().repeat(zoom, axis=0).repeat(zoom, axis=1)

        q_img = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
        q_pix = QPixmap.fromImage(q_img)

        scene = QGraphicsScene(self)
        scene.addPixmap(q_pix)
        self.ui.envView.setScene(scene)


class Worker(QRunnable):
    def __init__(self, window, alg, alg_config):
        super(QRunnable, self).__init__()
        self.window = window
        self.alg = alg
        self.alg_config = alg_config

        self.signals = WorkerSignals()

    def run(self):
        rl_agent = ALG_NAME_TO_OBJECT[self.alg](*self.alg_config)

        scores, score_history = [], []

        for i in range(1_000_000):
            done = False
            score = 0
            state = self.window.env.reset()

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

                state_, reward, done, score = self.window.env.step(converted_action)
                score += reward

                rl_agent.store_transition(state, action, reward, state_, done)
                rl_agent.learn()

                state = state_

                # noinspection PyUnresolvedReferences
                self.signals.update_env.emit()

                QApplication.processEvents()
                time.sleep(0.01)

            score_history.append(score)
            x = [j + 1 for j in range(i + 1)]

            # noinspection PyUnresolvedReferences
            self.signals.update_learning_graph.emit((score_history, x))


class WorkerSignals(QObject):
    update_env = pyqtSignal()
    update_learning_graph = pyqtSignal(tuple)
