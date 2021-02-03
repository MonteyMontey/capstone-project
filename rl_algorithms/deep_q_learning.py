"""This file is based on https://github.com/philtabor/Deep-Q-Learning-Paper-To-Code/tree/master/DQN"""

import random
import numpy as np
from collections import deque
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam


def create_model(input_dim, fc1_dim, fc2_dim, output_dim):
    model = tf.keras.Sequential()
    model.add(Dense(fc1_dim, input_dim=input_dim))
    model.add(Dense(fc2_dim, activation='relu'))
    model.add(Dense(output_dim, activation='linear'))
    model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=['accuracy'])

    return model


class DQNAgent:
    def __init__(self, input_dim, fc1_dim, fc2_dim, output_dim):
        self.model = create_model(input_dim, fc1_dim, fc2_dim, output_dim)

        self.target_model = create_model(input_dim, fc1_dim, fc2_dim, output_dim)
        self.target_model.set_weights(self.model.get_weights())

        self.discount = 0.999
        self.replay_memory_size = 1_000_000
        self.min_replay_memory_size = 1_000
        self.mini_batch_size = 32
        self.update_target_every = 20  # Terminal states (end of episodes)

        self.replay_memory = deque(maxlen=self.replay_memory_size)

        self.target_update_counter = 0

    def set_config(self, discount, replay_memory_size, min_replay_memory_size, mini_batch_size, update_target_every):
        self.discount = discount
        self.replay_memory_size = replay_memory_size
        self.min_replay_memory_size = min_replay_memory_size
        self.mini_batch_size = mini_batch_size
        self.update_target_every = update_target_every

    def update_replay_memory(self, observation):
        self.replay_memory.append(observation)

    def get_action(self, observation):
        action_index = np.argmax(self.model.predict(np.expand_dims(observation, axis=0))[0])
        return action_index

    def train(self, terminal_state):
        if len(self.replay_memory) < self.min_replay_memory_size:
            return

        mini_batch = random.sample(self.replay_memory, self.mini_batch_size)

        current_observations = np.array([step[0] for step in mini_batch])
        current_qs_list = self.model.predict(current_observations)

        new_current_observations = np.array([step[3] for step in mini_batch])
        future_qs_list = self.target_model.predict(new_current_observations)

        x = []
        y = []

        for index, (current_observation, action, reward, new_current_observation, done) in enumerate(mini_batch):
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + self.discount * max_future_q
            else:
                new_q = reward

            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            x.append(current_observation)
            y.append(current_qs)

        self.model.fit(np.array(x), np.array(y), batch_size=self.mini_batch_size, verbose=0, shuffle=False)

        if terminal_state:
            self.target_update_counter += 1

        if self.target_update_counter > self.update_target_every:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0
