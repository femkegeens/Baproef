from typing import Tuple, Optional

import gym
import numpy as np
import matplotlib.pyplot as plt
from gym import Env
from numpy import ndarray

from agent import QLearnerAgent


def run_episode(env: Env, agent: QLearnerAgent, training: bool, gamma) -> float:
    """
    Interact with the environment for one episode using actions derived from the q_table and the action_selector.

    :param env: The gym environment.
    :param agent: The agent.
    :param training: If true the q_table will be updated using q-learning. The flag is also passed to the action selector.
    :param gamma: The discount factor.
    :return: The cumulative discounted reward.
    """
    done = False
    obs = env.reset()
    cum_reward = 0.
    t = 0
    while not done:
        action = agent.act(obs, training)
        new_obs, reward, done, _ = env.step(action)
        if training:
            agent.learn(obs, action, reward, done, new_obs)
        obs = new_obs
        cum_reward += gamma ** t * reward
        t += 1
    return cum_reward


def train(env: Env, gamma: float, num_episodes: int, evaluate_every: int, num_evaluation_episodes: int,
          alpha: float, epsilon_max: Optional[float] = None, epsilon_min: Optional[float] = None,
          epsilon_decay: Optional[float] = None) -> Tuple[QLearnerAgent, ndarray, ndarray]:
    """
    Training loop.

    :param env: The gym environment.
    :param gamma: The discount factor.
    :param num_episodes: Number of episodes to train.
    :param evaluate_every: Evaluation frequency.
    :param num_evaluation_episodes: Number of episodes for evaluation.
    :param alpha: Learning rate.
    :param epsilon_max: The maximum epsilon of epsilon-greedy.
    :param epsilon_min: The minimum epsilon of epsilon-greedy.
    :param epsilon_decay: The decay factor of epsilon-greedy.
    :return: Tuple containing the agent, the returns of all training episodes and averaged evaluation return of
            each evaluation.
    """
    digits = len(str(num_episodes))
    agent = QLearnerAgent(env.observation_space.n, env.action_space.n, alpha, gamma, epsilon_max,
                          epsilon_min, epsilon_decay)
    evaluation_returns = np.zeros(num_episodes // evaluate_every)
    returns = np.zeros(num_episodes)
    for episode in range(num_episodes):
        returns[episode] = run_episode(env, agent, True, gamma)

        if (episode + 1) % evaluate_every == 0:
            evaluation_step = episode // evaluate_every
            cum_rewards_eval = np.zeros(num_evaluation_episodes)
            for eval_episode in range(num_evaluation_episodes):
                cum_rewards_eval[eval_episode] = run_episode(env, agent, False, gamma)
            evaluation_returns[evaluation_step] = np.mean(cum_rewards_eval)
            print(f"Episode {(episode + 1): >{digits}}/{num_episodes:0{digits}}:\t"
                  f"Averaged evaluation return {evaluation_returns[evaluation_step]:0.3}")
    return agent, returns, evaluation_returns


if __name__ == '__main__':
    try:
        env = gym.make('FrozenLake-v0')
    except gym.error.Error:
        env = gym.make('FrozenLake-v1')
    # TODO: complete.

#every ret is, as seen in line 71, an array of the agent, the returns, and the evaluation of bins of evaluate_every returns. The second one is the one we need to process data.
    ret1 = train(env, 0.99, 30000, 1000, 32, 0.01, 1.0, 0.05, 0.999)
    ret2 = train(env, 0.99, 30000, 1000, 32, 0.01, 1.0, 0.05, 0.999)
    ret3 = train(env, 0.99, 30000, 1000, 32, 0.01, 1.0, 0.05, 0.999)
    ret4 = train(env, 0.99, 30000, 1000, 32, 0.01, 1.0, 0.05, 0.999)
    ret5 = train(env, 0.99, 30000, 1000, 32, 0.01, 1.0, 0.05, 0.999)



#Plotting the data--------------------------------------------------------------------------------------------------------------------------------------------
#making bins
bin_size = 100
nr_eps = len(ret1[1]) #have to calc since we don't have access to this info here
nr_of_bins = nr_eps / bin_size #needed for the array_split function
binned1 = np.array(np.array_split(ret1[1], nr_of_bins), dtype="object")
binned2 = np.array(np.array_split(ret2[1], nr_of_bins), dtype="object")
binned3 = np.array(np.array_split(ret3[1], nr_of_bins), dtype="object")
binned4 = np.array(np.array_split(ret3[1], nr_of_bins), dtype="object")
binned5 = np.array(np.array_split(ret3[1], nr_of_bins), dtype="object")

#calculating means from bins
mean1 = np.mean(binned1, axis = 1)
mean2 = np.mean(binned2, axis = 1)
mean3 = np.mean(binned3, axis = 1)
mean4 = np.mean(binned4, axis = 1)
mean5 = np.mean(binned5, axis = 1)
#Data to be plotted
x = np.arange(bin_size, nr_eps+bin_size, bin_size) #x is all the same

#standard deviation of the means
mean_array =  np.array([mean1, mean2, mean3, mean4, mean5])
std_array = np.std(mean_array, axis=0,dtype=np.float64)

# plotting
plt.title("Q-learning: FrozenLake")
plt.xlabel("number of episodes")
plt.ylabel("return")
plt.scatter(x, mean1, color="red", s=4)
plt.scatter(x, mean2, color="blue", s=4)
plt.scatter(x, mean3, color="green", s=4)
plt.scatter(x, mean4, color="gold", s=4)
plt.scatter(x, mean5, color="deeppink", s=4)
plt.plot(x, std_array, color="darkturquoise")
plt.show()