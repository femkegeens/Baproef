import random
from typing import Optional
from numpy import ndarray
import numpy as np
from model import QModel
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
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.epsilon_max = epsilon_max
        self.epsilon = epsilon_max
        self.optimizer = torch.optim.Adam(self.nn.parameters(), lr=self.learning_rate)

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

        #PART 2 : decay epsilon at end of episode (aka when done = true)
        if done:
            self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

        # Compute the loss !
        greedy_action_val =  self.nn(obs)[self.greedy_action(obs)] #access expected qval of action
        taken_action_val = self.nn(obs)[act]
        loss = 0.5 * pow(rew + self.gamma * greedy_action_val - taken_action_val, 2) #formula applied, see 8.3 p. 21 in research training paper

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


