import numpy as np

from PyQt5.QtCore import pyqtSlot, QThreadPool
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QApplication

from envs.breakout_env import BreakoutEnv
from envs.pong_env import PongEnv
from envs.snake_env import SnakeEnv
from envs.interface import EnvInterface

from .utils import RenderMode
from .utils import get_dddqn_config, get_ddpg_config, get_sac_config
from .utils import get_snake_env_config
from .rl_thread import RLThread

from gui.mainwindow import Ui_GUI

ENV_NAME_TO_OBJECT = {"Snake": SnakeEnv, "Breakout": BreakoutEnv, "Pong": PongEnv}
ENV_NAME_TO_ZOOM = {"SnakeEnv": 34, "BreakoutEnv": 12, "PongEnv": 32}


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_GUI()
        self.ui.setupUi(self)

        self.thread_pool = QThreadPool()

        self.render_mode = RenderMode.SLOW_RENDER

        self.env = EnvInterface()
        self.env_changed(self.ui.envComboBox.currentText())

        self._setup_triggers()

    @pyqtSlot(str)
    def env_changed(self, env_name):
        self.init_env(env_name)
        self._swap_env_configs(env_name)
        self._update_env_canvas()

    @pyqtSlot(str)
    def alg_changed(self, alg_name):
        self._swap_alg_configs(alg_name)

    @pyqtSlot(int)
    def update_snake_vision_selections(self, index):
        self.ui.snakeVisionComboBox.clear()
        for i in range(index + 2):
            self.ui.snakeVisionComboBox.addItem(["1", "2", "3", "4"][i])

    @pyqtSlot()
    def snake_env_config_changed(self):
        config = get_snake_env_config(self)
        self.env = SnakeEnv(*config)
        self.env.reset()
        self._update_env_canvas()

    @pyqtSlot()
    def breakout_env_config_changed(self):
        paddle_size = self.ui.paddleSizeSpinBox.value()
        self.env = BreakoutEnv(paddle_size)
        self.env.reset()
        self._update_env_canvas()

    @pyqtSlot()
    def start_training(self):
        self._gui_training_mode(True)

        self.ui.pauseButton.setEnabled(True)
        self.ui.stopButton.setEnabled(True)

        alg = self.ui.algComboBox.currentText()

        if alg == "DDDQN":
            alg_config = get_dddqn_config(self)
        elif alg == "DDPG":
            alg_config = get_ddpg_config(self)
        elif alg == "SAC":
            alg_config = get_sac_config(self)

        self.rl_thread = RLThread(self, alg, alg_config)
        self.rl_thread.signals.update_env.connect(self._update_env_canvas)
        self.rl_thread.signals.update_learning_graph.connect(self._update_learning_curve_canvas)

        self.thread_pool.start(self.rl_thread)

    @pyqtSlot()
    def pause_training(self):
        self.rl_thread.pause = not self.rl_thread.pause

        if self.ui.pauseButton.text() == "Pause":
            self.ui.pauseButton.setText("Continue")

        elif self.ui.pauseButton.text() == "Continue":
            self.ui.pauseButton.setText("Pause")

    @pyqtSlot()
    def stop_training(self):
        self.rl_thread.stop = True
        self._gui_training_mode(False)
        self.ui.pauseButton.setDisabled(True)
        self.ui.stopButton.setDisabled(True)

    @pyqtSlot()
    def slow_render(self):
        self.render_mode = RenderMode.SLOW_RENDER

    @pyqtSlot()
    def fast_render(self):
        self.render_mode = RenderMode.FAST_RENDER

    @pyqtSlot()
    def no_render(self):
        self.render_mode = RenderMode.NO_RENDER

    def init_env(self, name):
        if name == "Snake":
            config = get_snake_env_config(self)
            self.env = SnakeEnv(*config)
        elif name == "Breakout":
            paddle_size = self.ui.paddleSizeSpinBox.value()
            self.env = BreakoutEnv(paddle_size)
        elif name == "Pong":
            self.env = PongEnv()

        self.env.reset()

    def _gui_training_mode(self, on: bool):
        self.ui.envComboBox.setDisabled(on)
        self.ui.envStackedWidget.setDisabled(on)
        self.ui.algComboBox.setDisabled(on)
        self.ui.algStackedWidget.setDisabled(on)
        self.ui.startButton.setDisabled(on)

    def _update_learning_curve_canvas(self, data):
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

    def _update_env_canvas(self):
        zoom = ENV_NAME_TO_ZOOM[self.env.__class__.__name__]

        img = self.env.screenshot().repeat(zoom, axis=0).repeat(zoom, axis=1)

        q_img = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
        q_pix = QPixmap.fromImage(q_img)

        scene = QGraphicsScene(self)
        scene.addPixmap(q_pix)
        self.ui.envView.setScene(scene)

    def _setup_triggers(self):
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

    def _swap_env_configs(self, env_name):
        env_stacked_widget = self.ui.envStackedWidget

        if env_name == "Snake":
            env_stacked_widget.setCurrentIndex(0)
        elif env_name == "Breakout":
            env_stacked_widget.setCurrentIndex(1)
        elif env_name == "Pong":
            env_stacked_widget.setCurrentIndex(2)

    def _swap_alg_configs(self, alg_name):
        alg_stacked_widget = self.ui.algStackedWidget

        if alg_name == "DDDQN":
            alg_stacked_widget.setCurrentIndex(0)
        elif alg_name == "DDPG":
            alg_stacked_widget.setCurrentIndex(1)
        elif alg_name == "SAC":
            alg_stacked_widget.setCurrentIndex(2)
