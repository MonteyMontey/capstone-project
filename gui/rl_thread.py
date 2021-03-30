import time
import numpy as np

from PyQt5.QtCore import pyqtSignal, QRunnable, QObject, QTimer
from PyQt5.QtWidgets import QApplication

from envs.action import Action

from .utils import RenderMode

from rl_algorithms.dddqn import DuelingDDQNAgent
from rl_algorithms.ddpg import DDPGAgent
from rl_algorithms.sac import SACAgent

ALG_NAME_TO_OBJECT = {"DDDQN": DuelingDDQNAgent, "DDPG": DDPGAgent, "SAC": SACAgent}

ENV_OUTPUT_DIMS = {"Snake": 4, "Breakout": 2, "Pong": 2}

SNAKE_OUTPUT_TO_ACTION = [Action.UP, Action.RIGHT, Action.DOWN, Action.LEFT]
BREAKOUT_OUTPUT_TO_ACTION = [Action.LEFT, Action.RIGHT]
PONG_OUTPUT_TO_ACTION = [Action.UP, Action.DOWN]


class RLThread(QRunnable):
    def __init__(self, window, alg, alg_config):
        super(QRunnable, self).__init__()
        self.window = window
        self.alg = alg
        self.alg_config = alg_config

        self.pause = False
        self.stop = False

        self.score_history = []
        self.x = []

        self.signals = RLThreadSignals()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_learning_curve)
        self.timer.start()

    def run(self):
        input_dim = len(self.window.env.get_state())

        env_name = self.window.ui.envComboBox.currentText()
        output_dim = ENV_OUTPUT_DIMS[env_name]

        rl_agent = ALG_NAME_TO_OBJECT[self.alg](*self.alg_config, input_dim, output_dim)

        episode = 0

        while True:
            episode += 1

            done = False
            score = 0

            if self.alg == "DDPG":
                rl_agent.noise.reset()

            state = self.window.env.reset()
            while not done:
                if self.stop:
                    break
                elif self.pause:
                    QApplication.processEvents()
                else:
                    action = rl_agent.choose_action(state)

                    if self.alg == "DDDQN":
                        action_index = action
                    elif self.alg == "DDPG" or self.alg == "SAC":
                        action_index = np.argmax(action)

                    if env_name == "Snake":
                        converted_action = SNAKE_OUTPUT_TO_ACTION[action_index]
                    elif env_name == "Breakout":
                        converted_action = BREAKOUT_OUTPUT_TO_ACTION[action_index]
                    elif env_name == "Pong":
                        converted_action = PONG_OUTPUT_TO_ACTION[action_index]

                    state_, reward, done, _ = self.window.env.step(converted_action)
                    score += reward

                    rl_agent.remember(state, action, reward, state_, done)
                    rl_agent.learn()

                    state = state_

                    if self.window.render_mode != RenderMode.NO_RENDER:
                        self.signals.update_env.emit()

                    if self.window.render_mode == RenderMode.SLOW_RENDER:
                        time.sleep(0.5)
                    elif self.window.render_mode == RenderMode.FAST_RENDER:
                        time.sleep(0.05)
                    elif self.window.render_mode == RenderMode.NO_RENDER:
                        time.sleep(0.001)

            self.score_history.append(score)
            self.x = [j + 1 for j in range(episode)]

            if self.stop:
                break

    def update_learning_curve(self):
        self.signals.update_learning_graph.emit((self.score_history, self.x))


class RLThreadSignals(QObject):
    update_env = pyqtSignal()
    update_learning_graph = pyqtSignal(tuple)
