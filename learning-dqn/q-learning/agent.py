from typing import Optional
from numpy import ndarray
from numpy import zeros
from numpy import argmax
from numpy import random

def create_q_table(num_states: int, num_actions: int) -> ndarray:
    """
    Function that returns a q_table as an array of shape (num_states, num_actions) filled with zeros.

    :param num_states: Number of states.
    :param num_actions: Number of actions.
    :return: q_table: Initial q_table.
    """
    return zeros((num_states, num_actions))

class QLearnerAgent:
    """
    The agent class for exercise 1.
    """

    def __init__(self,
                 num_states: int,
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
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.q_table = create_q_table(num_states, num_actions)
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.epsilon_max = epsilon_max
        self.epsilon = epsilon_max

    def greedy_action(self, observation: int) -> int:
        """
        Return the greedy action.

        :param observation: The observation.
        :return: The action.
        """
        #go to row "observation" in the q-table and find the highest value in that row --> index corresponds with greedy action
        row =  self.q_table[observation]
        return argmax(row)



    def act(self, observation: int, training: bool = True) -> int:
        """
        Return the action.

        :param observation: The observation. ;obs =  current_row * nrows + current_col
        :param training: Boolean flag for training, when not training agent
        should act greedily.
        :return: The action.
        """

        if training:
            if random.random() > self.epsilon: #select greedy with 1-eps chance
                return self.greedy_action(observation)
            else:  #select random
                return random.randint(0,4)
        #if not training, act greedily
        else: return self.greedy_action(observation)






    def learn(self, obs: int, act: int, rew: float, done: bool, next_obs: int) -> None:
        """
        Update the Q-Value.

        :param obs: The observation.
        :param act: The action.
        :param rew: The reward.
        :param done: Done flag.
        :param next_obs: The next observation.
        """
        #PART 1 : update Q-value
        curr_qval = self.q_table[obs, act]
        greedy_next_action = self.greedy_action(next_obs)
        target = rew + (self.gamma * (not done) * self.q_table[next_obs, greedy_next_action]) #for when the epsiode is not done, stopping mid-ep
        error = target - curr_qval
        self.q_table[obs,act] += self.learning_rate * error


        #PART 2 : decay epsilon at end of episode (aka when done = true)
        if done:
            self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)


