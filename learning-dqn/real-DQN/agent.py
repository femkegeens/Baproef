import random
from typing import Optional
from numpy import ndarray
import numpy as np
from model import QModel
from replay_buffer import ReplayBuffer
import torch

class DQNAgent:
    """
    The agent class for exercise 1.
    """

    def __init__(self,
                 obs_dim: int,
                 num_actions: int,
                 learning_rate: float,
                 gamma: float,
                 epsilon_max: Optional[float] = None,
                 epsilon_min: Optional[float] = None,
                 epsilon_decay: Optional[float] = None):
        """
        :param num_states: Number of states.
        :param num_actions: Number of actions.
        :param learning_rate: The learning rate.
        :param gamma: The discount factor.
        :param epsilon_max: The maximum epsilon of epsilon-greedy.
        :param epsilon_min: The minimum epsilon of epsilon-greedy.
        :param epsilon_decay: The decay factor of epsilon-greedy.
        """
        self.obs_dim = obs_dim
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.nn = QModel(obs_dim, num_actions)
        self.target_nn = QModel(obs_dim, num_actions) #ADDED
        self.replay_buffer= ReplayBuffer(100, 4) #ADDED
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.epsilon_max = epsilon_max
        self.epsilon = epsilon_max
        self.optimizer = torch.optim.Adam(self.nn.parameters(), lr=self.learning_rate)
        self.target_optimizer = torch.optim.Adam(self.target_nn.parameters(), lr=self.learning_rate)

    def greedy_action(self, observation) -> int:
        """
        Return the greedy action.

        :param observation: The observation.
        :return: The action.
        """
        vals = self.nn(observation) #gives array of 2 values:  expected q-val when action 0 is taken, and expected q-val if action 1 is taken
        if vals[0] > vals[1]:
            return 0
        else:
            return 1

    def act(self, observation, training: bool = True) -> int:
        """
        Return the action.

        :param observation: The observation.
        :param training: Boolean flag for training, when not training agent
        should act greedily.
        :return: The action.
        """

        if training:
            if random.random() > self.epsilon:  # select greedy with 1-eps chance
                return self.greedy_action(observation)
            else:  # select random
                return random.choice([0,1])
        # if not training, act greedily
        else:
            return self.greedy_action(observation)

    def learn(self, obs, act, rew, done, next_obs) -> None:
        """
        Update the Q-Value.

        :param obs: The observation.
        :param act: The action.
        :param rew: The reward.
        :param done: Done flag.
        :param next_obs: The next observation.
        """

        #add to replay buffer
        self.replay_buffer.add_transition(obs, act, rew, done, next_obs)

        #PART 2 : decay epsilon at end of episode (aka when done = true)
        if done:
            self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

        # Compute the loss --> over batch!
        batchsize = 5
        samples=self.replay_buffer.sample(batchsize)
        samples_states = samples[0]
        samples_actions = samples[1]
        samples_rewards = samples[2]
        samples_dones = samples[3]
        samples_next_states = samples[4]

        for i in range(0, batchsize):

            #approach without target NN
            #q_current = self.nn(samples_states[i])
            #q_target = samples_rewards[i]
            #if not samples_dones[i]:
            #    q_target = q_target + self.gamma * max(self.nn(samples_next_states[i]))

            q_current = self.nn(samples_states[i])
            q_target = samples_rewards[i]
             if not samples_dones[i]:
                q_target = q_target + self.gamma * max(self.target_nn(samples_next_states[i]))

          loss = 0.5 * pow(q_target - q_current) #formula applied, see 8.3 p. 21 in research training paper

          self.optimizer.zero_grad()
          loss.backward()
          self.optimizer.step()

#ADD: switch networks every now and then


