import sys
import numpy as np
import itertools
import mmap
import pdb
from environment import enviroment_class

train_input = sys.argv[1]
value_output=sys.argv[2]
q_value_output=sys.argv[3]
policy_output=sys.argv[4]
num_episodes=int(sys.argv[5])
max_episode_length=int(sys.argv[6])
learning_rate=float(sys.argv[7])
discount_factor=float(sys.argv[8])
epsilon=float(sys.argv[8])


def epsilon_greedy_policy():
    random_prob = np.random.rand()
    if random_prob < 1 - epsilon:
        do_greedy = False
    else:
        do_greedy = True

    return do_greedy


def greedy_policy(q_values):
    # Creating greedy policy for test time.
    action = np.argmax(q_values)
    return action

if __name__ == '__main__':
    env_class = enviroment_class(train_input)
    q_values = np.zeros(4)
    for episode in range(num_episodes):
        for idx in range(max_episode_length):
            do_greedy = epsilon_greedy_policy()
            if do_greedy:
                action = greedy_policy(q_values)
            else:
                action =



