import time
import numpy as np

from PyQt5.QtCore import pyqtSignal, QRunnable, QObject, QTimer
from PyQt5.QtWidgets import QApplication

from envs.action import Action
from envs.snake_env import SNAKE_ACTION_POOL
from envs.pong_env import PONG_ACTION_POOL
from envs.breakout_env import BREAKOUT_ACTION_POOL

from gui.utils import RenderMode

from rl_algorithms.dddqn import DuelingDDQNAgent
from rl_algorithms.ddpg import DDPGAgent
from rl_algorithms.sac import SACAgent

ALG_NAME_TO_OBJECT = {"DDDQN": DuelingDDQNAgent, "DDPG": DDPGAgent, "SAC": SACAgent}


class RLThread(QRunnable):
    """The RLThread class represents the separate thread in which the agent learning takes place"""

    def __init__(self, window, alg_name, alg_config):
        super(QRunnable, self).__init__()
        self.window = window
        self.alg = alg_name
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
        """Performs the learning of the RL agent and sends signals back to the main thread"""
        input_dim = len(self.window.env.get_state())

        env_name = self.window.ui.envComboBox.currentText()

        rl_agent = ALG_NAME_TO_OBJECT[self.alg](*self.alg_config, input_dim, self.window.env.output_dim)

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

                    # translate index output of network to Action object
                    if env_name == "Snake":
                        converted_action = SNAKE_ACTION_POOL[action_index]
                    elif env_name == "Breakout":
                        converted_action = BREAKOUT_ACTION_POOL[action_index]
                    elif env_name == "Pong":
                        converted_action = PONG_ACTION_POOL[action_index]

                    state_, reward, done, _ = self.window.env.step(converted_action)
                    score += reward

                    # store observation in replay memory
                    rl_agent.remember(state, action, reward, state_, done)
                    rl_agent.learn()

                    state = state_

                    if self.window.render_mode != RenderMode.NO_RENDER:
                        self.signals.update_env.emit()

                    # wait a certain amount of time between each episode depending on setting in UI
                    if self.window.render_mode == RenderMode.SLOW_RENDER:
                        time.sleep(0.5)
                    elif self.window.render_mode == RenderMode.FAST_RENDER:
                        time.sleep(0.05)
                    elif self.window.render_mode == RenderMode.NO_RENDER:
                        time.sleep(0.001)

            # keep track of scores for learning graph
            self.score_history.append(score)
            self.x = [j + 1 for j in range(episode)]

            # end thread if user clicked "Stop"
            if self.stop:
                break

    def update_learning_curve(self):
        """Signals the main thread to update the learning graph"""
        self.signals.update_learning_graph.emit((self.score_history, self.x))


class RLThreadSignals(QObject):
    """The RLThreadSignal class defines the signals that are used for communication between main thread and RL thread"""
    update_env = pyqtSignal()
    update_learning_graph = pyqtSignal(tuple)
