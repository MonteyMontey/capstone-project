import numpy as np

from PyQt5.QtCore import pyqtSlot, QThreadPool
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene

from envs.breakout_env import BreakoutEnv
from envs.pong_env import PongEnv
from envs.snake_env import SnakeEnv
from envs.interface import EnvInterface

from gui.mainwindow import Ui_GUI

from .rl_thread import Worker

ENV_NAME_TO_OBJECT = {"Snake": SnakeEnv, "Breakout": BreakoutEnv, "Pong": PongEnv}
ENV_NAME_TO_ZOOM = {"SnakeEnv": 30, "BreakoutEnv": 10, "PongEnv": 25}


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_GUI()
        self.ui.setupUi(self)

        self.thread_pool = QThreadPool()
        self.worker = None

        self.render_mode = 1

        self.ui.mplWidget.canvas.ax.set_ylabel('score')
        self.ui.mplWidget.canvas.ax.set_xlabel('episodes')

        # initialize environment
        self.env = EnvInterface()
        self.env_changed(self.ui.envComboBox.currentText())

        # setup triggers
        self.ui.envComboBox.currentTextChanged.connect(self.env_changed)

        self.ui.gridSizeComboBox.currentIndexChanged.connect(self.update_snake_vision_selections)
        self.ui.gridSizeComboBox.currentIndexChanged.connect(self.snake_env_config_changed)
        self.ui.snakeVisionComboBox.currentIndexChanged.connect(self.snake_env_config_changed)

        self.ui.paddleSizeSpinBox.valueChanged.connect(self.breakout_env_config_changed)

        self.ui.algComboBox.currentTextChanged.connect(self.alg_changed)

        self.ui.startButton.clicked.connect(self.start_training)
        self.ui.pauseButton.clicked.connect(self.pause_training)
        self.ui.stopButton.clicked.connect(self.stop_training)

        self.ui.slowRenderingCheckBox.clicked.connect(self.slow_render)
        self.ui.fastRenderingCheckBox.clicked.connect(self.fast_render)
        self.ui.noRenderingCheckBox.clicked.connect(self.no_render)

    def init_env(self, env_name):
        if env_name == "Snake":
            config = self.get_snake_env_config()
            self.env = SnakeEnv(*config)
        elif env_name == "Breakout":
            paddle_size = self.ui.paddleSizeSpinBox.value()
            self.env = BreakoutEnv(paddle_size)
        elif env_name == "Pong":
            self.env = PongEnv()

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

        if alg_name == "DDDQN":
            alg_stacked_widget.setCurrentIndex(0)
        elif alg_name == "DDPG":
            alg_stacked_widget.setCurrentIndex(1)
        elif alg_name == "SAC":
            alg_stacked_widget.setCurrentIndex(2)

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
        paddle_size = self.ui.paddleSizeSpinBox.value()
        self.env = BreakoutEnv(paddle_size)
        self.env.reset()
        self.update_env_canvas()

    @pyqtSlot()
    def start_training(self):
        self.set_gui_training(True)

        self.ui.pauseButton.setEnabled(True)
        self.ui.stopButton.setEnabled(True)

        alg = self.ui.algComboBox.currentText()
        alg_config = ()
        if alg == "DDDQN":
            alg_config = self.get_dddqn_config()
        elif alg == "DDPG":
            alg_config = self.get_ddpg_config()
        elif alg == "SAC":
            alg_config = self.get_sac_config()

        self.worker = Worker(self, alg, alg_config)

        # noinspection PyUnresolvedReferences
        self.worker.signals.update_env.connect(self.update_env_canvas)
        # noinspection PyUnresolvedReferences
        self.worker.signals.update_learning_graph.connect(self.update_learning_curve_canvas)

        self.thread_pool.start(self.worker)

    @pyqtSlot()
    def pause_training(self):
        self.worker.pause = not self.worker.pause

        if self.ui.pauseButton.text() == "Pause":
            self.ui.pauseButton.setText("Continue")
        elif self.ui.pauseButton.text() == "Continue":
            self.ui.pauseButton.setText("Pause")

    @pyqtSlot()
    def stop_training(self):
        self.worker.stop = True
        self.set_gui_training(False)
        self.ui.pauseButton.setDisabled(True)
        self.ui.stopButton.setDisabled(True)

    @pyqtSlot()
    def slow_render(self):
        self.render_mode = 1

    @pyqtSlot()
    def fast_render(self):
        self.render_mode = 2

    @pyqtSlot()
    def no_render(self):
        self.render_mode = 3

    def get_dddqn_config(self):
        return [self.ui.learningRateDoubleSpinBoxDDDQN.value(),
                self.ui.gammaDoubleSpinBoxDDDQN.value(),
                self.ui.batchSizeSpinBoxDDDQN.value(),
                self.ui.epsilonDoubleSpinBoxDDDQN.value(),
                self.ui.epsilonDecDoubleSpinBoxDDDQN.value(),
                self.ui.epsilonMinSpinBoxDDDQN.value(),
                self.ui.tauDoubleSpinBoxDDDQN.value(),
                self.ui.layer1SpinBoxDDDQN.value(),
                self.ui.layer2SpinBoxDDDQN.value()]

    def get_ddpg_config(self):
        return [self.ui.learningRateAlphaDoubleSpinBoxDDPG.value(),
                self.ui.learningRateBetaDoubleSpinBoxDDPG.value(),
                self.ui.gammaDoubleSpinBoxDDPG.value(),
                self.ui.batchSizeSpinBoxDDPG.value(),
                self.ui.tauDoubleSpinBoxDDPG.value(),
                self.ui.layer1SpinBoxDDPG.value(),
                self.ui.layer2SpinBoxDDPG.value()]

    def get_sac_config(self):
        return [self.ui.learningRateAlphaDoubleSpinBoxSAC.value(),
                self.ui.learningRateBetaDoubleSpinBoxSAC.value(),
                self.ui.gammaDoubleSpinBoxSAC.value(),
                self.ui.batchSizeSpinBoxSAC.value(),
                self.ui.tauDoubleSpinBoxSAC.value(),
                self.ui.rewardScaleSpinBoxSAC.value(),
                self.ui.layer1SpinBoxSAC.value(),
                self.ui.layer2spinBoxSAC.value()]

    def set_gui_training(self, mode: bool):
        self.ui.envComboBox.setDisabled(mode)
        self.ui.envStackedWidget.setDisabled(mode)
        self.ui.algComboBox.setDisabled(mode)
        self.ui.algStackedWidget.setDisabled(mode)
        self.ui.startButton.setDisabled(mode)

    def update_learning_curve_canvas(self, data):
        score_history = data[0]
        x = data[1]

        running_avg = np.zeros(len(score_history))
        for i in range(len(running_avg)):
            running_avg[i] = np.mean(score_history[max(0, i - 100):(i + 1)])

        self.ui.mplWidget.canvas.ax.cla()
        self.ui.mplWidget.canvas.ax.set_ylabel('score')
        self.ui.mplWidget.canvas.ax.set_xlabel('episodes')
        self.ui.mplWidget.canvas.ax.plot(x, running_avg, '#3399FF')
        self.ui.mplWidget.canvas.draw()

    def update_env_canvas(self):
        zoom = ENV_NAME_TO_ZOOM[self.env.__class__.__name__]

        img = self.env.screenshot().repeat(zoom, axis=0).repeat(zoom, axis=1)

        q_img = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
        q_pix = QPixmap.fromImage(q_img)

        scene = QGraphicsScene(self)
        scene.addPixmap(q_pix)
        self.ui.envView.setScene(scene)
