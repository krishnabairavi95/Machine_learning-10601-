import sys
import numpy as np
import itertools
import mmap
import pdb


filename= sys.argv[1]
output_file = sys.argv[2]
action_file = sys.argv[3]


action_list = []
with open(action_file) as file:
    for line in file:
        data = line.strip("\n ")
        data = data.split(' ')
        action_list.append(data)
file.close()
action_list = action_list[0]
for i in range((len(action_list))):
    action_list[i] = int(action_list[i])

class enviroment_class(object):
    def __init__(self, filename):
        f1 = open(filename, "r")
        l1 = f1.readlines()
        l2 = []
        for i in l1:
            # print (i[:-1])
            l2.append(i[:-1])

            rows = l2
            # print(rows)
            self.row_len = len(rows)

            self.final_dict = dict()
            for i in range(self.row_len):
                x = i
                sentence = rows[i]
                self.col_len = len(sentence)
                for j in range(self.col_len):
                    tuple_1 = (x,)
                    y = j
                    dict_value = sentence[j]
                    tuple_1 = tuple_1 + (y,)
                    self.final_dict[tuple_1] = dict_value
                    if dict_value == 'S':
                        self.initial_state = tuple_1

        self.reward = -1

    def step(self, j):
        row = self.initial_state[0]
        col = self.initial_state[1]
        is_terminal = 0
        if j == 0:
            if col == 0:
                next_state = self.initial_state
            else:
                next_state = (row, col - 1)
                if self.final_dict[next_state][0] == '*':
                    next_state = self.initial_state
                if self.final_dict[next_state][0] == 'G':
                    is_terminal = 1

        elif j == 1:
            if row == 0:
                next_state = self.initial_state
            else:
                next_state = (row - 1, col)
                if self.final_dict[next_state][0] == '*':
                    next_state = self.initial_state
                if self.final_dict[next_state][0] == 'G':
                    is_terminal = 1

        elif j == 2:
            if col == self.col_len - 1:
                next_state = self.initial_state
            else:
                next_state = (row, col + 1)
                if self.final_dict[next_state][0] == '*':
                    next_state = self.initial_state
                if self.final_dict[next_state][0] == 'G':
                    is_terminal = 1
        else:
            # if A[i]==3:
            if row == self.row_len - 1:
                next_state = self.initial_state
            else:
                next_state = (row + 1, col)
                if self.final_dict[next_state][0] == '*':
                    next_state = self.initial_state
                if self.final_dict[next_state][0] == 'G':
                    is_terminal = 1

        self.initial_state = next_state
        return next_state, self.reward, is_terminal

    def reset(self):
        state = self.initial_state
        return state


if __name__ == '__main__':

    env_class = enviroment_class(filename)

    with open(output_file, 'w') as f:
        for i in range(len(action_list)):
            nS, rewards, is_terminal = env_class.step(action_list[i])
            #pdb.set_trace()
            string= str(nS[0]) + ' '+ str(nS[1]) + ' '+ str(rewards) + ' ' + str(is_terminal)
            print (string)
            f.write(string)
            if i < len(action_list) :
                f.write('\n')

    f.close






