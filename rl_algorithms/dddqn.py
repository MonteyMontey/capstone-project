""" This file is based on https://github.com/philtabor/Deep-Q-Learning-Paper-To-Code/blob/master/DuelingDDQN """

import numpy as np

import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from rl_algorithms.replay_memory.discrete_replay_memory import ReplayBuffer
from .interface import AlgInterface


class DuelingDDQNAgent(AlgInterface):
    def __init__(self, lr, gamma, batch_size, epsilon, eps_dec, eps_min, tau, fc1_dim, fc2_dim, input_dim, output_dim,
                 mem_size=1_000_000):
        self.gamma = gamma
        self.epsilon = epsilon
        self.lr = lr
        self.batch_size = batch_size
        self.eps_min = eps_min
        self.eps_dec = eps_dec
        self.tau = tau
        self.action_space = [i for i in range(output_dim)]
        self.learn_step_counter = 0

        self.memory = ReplayBuffer(mem_size, input_dim)

        self.q_eval = DuelingDeepQNetwork(self.lr, input_dim, fc1_dim, fc2_dim, output_dim)
        self.q_next = DuelingDeepQNetwork(self.lr, input_dim, fc1_dim, fc2_dim, output_dim)

        self._update_network_parameters(tau=1)

    def choose_action(self, observation):
        if np.random.random() > self.epsilon:
            state = np.array([observation], copy=False, dtype=np.float32)
            state_tensor = T.tensor(state).to(self.q_eval.device)
            _, advantages = self.q_eval.forward(state_tensor)

            action = T.argmax(advantages).item()
        else:
            action = np.random.choice(self.action_space)

        return action

    def remember(self, state, action, reward, state_, done):
        self.memory.store_transition(state, action, reward, state_, done)

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return

        self.q_eval.optimizer.zero_grad()

        self._update_network_parameters()

        states, actions, rewards, states_, dones = self._sample_memory()
        indices = np.arange(self.batch_size)

        v_s, a_s = self.q_eval.forward(states)
        v_s_, a_s_ = self.q_next.forward(states_)

        v_s_eval, a_s_eval = self.q_eval.forward(states_)

        q_pred = T.add(v_s, (a_s - a_s.mean(dim=1, keepdim=True)))[indices, actions]

        q_next = T.add(v_s_, (a_s_ - a_s_.mean(dim=1, keepdim=True)))

        q_eval = T.add(v_s_eval, (a_s_eval - a_s_eval.mean(dim=1, keepdim=True)))

        max_actions = T.argmax(q_eval, dim=1)
        q_next[dones] = 0.0

        q_target = rewards + self.gamma * q_next[indices, max_actions]

        loss = self.q_eval.loss(q_target, q_pred).to(self.q_eval.device)
        loss.backward()
        self.q_eval.optimizer.step()
        self.learn_step_counter += 1

        self._decrement_epsilon()

    def _sample_memory(self):
        state, action, reward, new_state, done = self.memory.sample_buffer(self.batch_size)

        states = T.tensor(state).to(self.q_eval.device)
        rewards = T.tensor(reward).to(self.q_eval.device)
        dones = T.tensor(done).to(self.q_eval.device)
        actions = T.tensor(action).to(self.q_eval.device)
        states_ = T.tensor(new_state).to(self.q_eval.device)

        return states, actions, rewards, states_, dones

    def _update_network_parameters(self, tau=None):
        if tau is None:
            tau = self.tau

        target_value_params = self.q_eval.named_parameters()
        value_params = self.q_next.named_parameters()

        target_value_state_dict = dict(target_value_params)
        value_state_dict = dict(value_params)

        for name in value_state_dict:
            value_state_dict[name] = tau * value_state_dict[name].clone() + (1 - tau) * \
                                     target_value_state_dict[name].clone()

        self.q_next.load_state_dict(value_state_dict)

    def _decrement_epsilon(self):
        self.epsilon = self.epsilon - self.eps_dec \
            if self.epsilon > self.eps_min else self.eps_min


class DuelingDeepQNetwork(nn.Module):
    def __init__(self, lr, input_dim, output_dim, fc1_dim, fc2_dim):
        super(DuelingDeepQNetwork, self).__init__()

        self.fc1 = nn.Linear(input_dim, fc1_dim)
        self.fc2 = nn.Linear(fc1_dim, fc2_dim)
        self.V = nn.Linear(fc2_dim, 1)
        self.A = nn.Linear(fc2_dim, output_dim)

        self.optimizer = optim.RMSprop(self.parameters(), lr=lr)
        self.loss = nn.MSELoss()
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):
        flat1 = F.relu(self.fc1(state))
        flat2 = F.relu(self.fc2(flat1))
        v = self.V(flat2)
        a = self.A(flat2)

        return v, a
