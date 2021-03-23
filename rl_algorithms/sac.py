""" This file is based on https://github.com/philtabor/Actor-Critic-Methods-Paper-To-Code/blob/master/SAC """

import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Normal

from .continuous_replay_memory import ReplayBuffer
from .interface import AlgInterface


class SACAgent(AlgInterface):
    def __init__(self, alpha, beta, gamma, batch_size, tau, reward_scale, layer1_size, layer2_size, input_dims,
                 n_actions, action_space_high=1.0, mem_size=1_000_000):
        self.gamma = gamma
        self.tau = tau
        self.memory = ReplayBuffer(mem_size, input_dims, n_actions)
        self.batch_size = batch_size
        self.n_actions = n_actions

        self.actor = ActorNetwork(alpha, input_dims, layer1_size, layer2_size, n_actions=n_actions,
                                  max_action=action_space_high)

        self.critic_1 = CriticNetwork(beta, input_dims, layer1_size, layer2_size, n_actions)

        self.critic_2 = CriticNetwork(beta, input_dims, layer1_size, layer2_size, n_actions)

        self.value = ValueNetwork(beta, input_dims, layer1_size, layer2_size)

        self.target_value = ValueNetwork(beta, input_dims, layer1_size, layer2_size)

        self.scale = reward_scale
        self._update_network_parameters(tau=1)

    def choose_action(self, observation):
        self.actor.eval()
        observation = T.tensor([observation], dtype=T.float).to(self.actor.device)
        actions, _ = self.actor.sample_normal(observation, reparameterize=False)

        return actions.cpu().detach().numpy()[0]

    def remember(self, state, action, reward, state_, done):
        self.memory.store_transition(state, action, reward, state_, done)

    def learn(self):
        self.actor.train()

        if self.memory.mem_cntr < self.batch_size:
            return

        states, actions, rewards, states_, done = self.memory.sample_buffer(self.batch_size)

        states = T.tensor(states, dtype=T.float).to(self.actor.device)
        states_ = T.tensor(states_, dtype=T.float).to(self.actor.device)
        actions = T.tensor(actions, dtype=T.float).to(self.actor.device)
        rewards = T.tensor(rewards, dtype=T.float).to(self.actor.device)
        done = T.tensor(done).to(self.actor.device)

        value = self.value(states)
        value = value.view(-1)

        value_ = self.target_value(states_)
        value_ = value_.view(-1)

        value_[done] = 0.0

        """ Value Network Loss """

        predicted_actions, log_probs_sums = self.actor.sample_normal(states, reparameterize=False)

        log_probs_sums = log_probs_sums.view(-1)

        q_1_critic_values = self.critic_1.forward(states, predicted_actions)
        q_2_critic_values = self.critic_2.forward(states, predicted_actions)
        critic_values = T.min(q_1_critic_values, q_2_critic_values)
        critic_values = critic_values.view(-1)

        self.value.optimizer.zero_grad()
        value_target = critic_values - log_probs_sums
        value_loss = 0.5 * F.mse_loss(value, value_target)
        value_loss.backward(retain_graph=True)
        self.value.optimizer.step()

        """ Actor Network Loss """

        predicted_actions, log_probs_sums = self.actor.sample_normal(states, reparameterize=True)
        log_probs_sums = log_probs_sums.view(-1)

        q_1_critic_values = self.critic_1.forward(states, predicted_actions)
        q_2_critic_values = self.critic_2.forward(states, predicted_actions)
        critic_values = T.min(q_1_critic_values, q_2_critic_values)
        critic_values = critic_values.view(-1)

        actor_loss = log_probs_sums - critic_values
        actor_loss = T.mean(actor_loss)
        self.actor.optimizer.zero_grad()
        actor_loss.backward(retain_graph=True)
        self.actor.optimizer.step()

        """ Critic Network Loss"""

        q_hat = self.scale * rewards + self.gamma * value_
        q1_critic_values = self.critic_1.forward(states, actions).view(-1)
        q2_critic_values = self.critic_2.forward(states, actions).view(-1)
        critic_1_loss = 0.5 * F.mse_loss(q1_critic_values, q_hat)
        critic_2_loss = 0.5 * F.mse_loss(q2_critic_values, q_hat)

        self.critic_1.optimizer.zero_grad()
        self.critic_2.optimizer.zero_grad()
        critic_loss = critic_1_loss + critic_2_loss
        critic_loss.backward()
        self.critic_1.optimizer.step()
        self.critic_2.optimizer.step()

        self._update_network_parameters()

    def _update_network_parameters(self, tau=None):
        if tau is None:
            tau = self.tau

        target_value_params = self.target_value.named_parameters()
        value_params = self.value.named_parameters()

        target_value_state_dict = dict(target_value_params)
        value_state_dict = dict(value_params)

        for name in value_state_dict:
            value_state_dict[name] = tau * value_state_dict[name].clone() + (1 - tau) * \
                                     target_value_state_dict[name].clone()

        self.target_value.load_state_dict(value_state_dict, strict=False)


class CriticNetwork(nn.Module):
    def __init__(self, beta, input_dims, fc1_dims, fc2_dims, n_actions):
        super(CriticNetwork, self).__init__()
        self.input_dims = input_dims
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims

        self.fc1 = nn.Linear(self.input_dims + n_actions, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)

        self.q1 = nn.Linear(self.fc2_dims, 1)

        self.optimizer = optim.Adam(self.parameters(), lr=beta)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')

        self.to(self.device)

    def forward(self, x, action):
        x = T.cat([x, action], dim=1)

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        q1 = self.q1(x)

        return q1


class ActorNetwork(nn.Module):
    def __init__(self, alpha, input_dims, fc1_dims, fc2_dims, max_action, n_actions):
        super(ActorNetwork, self).__init__()
        self.input_dims = input_dims
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.n_actions = n_actions
        self.max_action = max_action

        self.reparam_noise = 1e-6

        self.fc1 = nn.Linear(self.input_dims, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)

        self.mu = nn.Linear(self.fc2_dims, self.n_actions)
        self.sigma = nn.Linear(self.fc2_dims, self.n_actions)

        self.optimizer = optim.Adam(self.parameters(), lr=alpha)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')

        self.to(self.device)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        mu = self.mu(x)

        sigma = self.sigma(x)
        sigma = T.clamp(sigma, min=self.reparam_noise, max=1)

        return mu, sigma

    def sample_normal(self, x, reparameterize=True):
        mu, sigma = self.forward(x)
        probabilities = Normal(mu, sigma)

        if reparameterize:
            action = probabilities.rsample()
        else:
            action = probabilities.sample()

        bounded_action = T.tanh(action) * T.tensor(self.max_action).to(self.device)

        log_probs = probabilities.log_prob(action)

        log_probs -= T.log(1 - bounded_action.pow(2) + self.reparam_noise)

        log_probs_sum = log_probs.sum(1, keepdim=True)

        return bounded_action, log_probs_sum


class ValueNetwork(nn.Module):
    def __init__(self, beta, input_dims, fc1_dims, fc2_dims):
        super(ValueNetwork, self).__init__()
        self.input_dims = input_dims
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims

        self.fc1 = nn.Linear(self.input_dims, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)

        self.v = nn.Linear(self.fc2_dims, 1)

        self.optimizer = optim.Adam(self.parameters(), lr=beta)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')

        self.to(self.device)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        v = self.v(x)

        return v
