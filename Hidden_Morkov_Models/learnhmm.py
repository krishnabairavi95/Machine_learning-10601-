import csv
import sys
import numpy as np
import itertools
import mmap


def data_process(train_input):
    data_list = []
    with open(train_input) as file:
        for line in file:
            a=[]
            #print (line)
            data = line.strip("\n")
            value= data.split(" ")
            #print (value)
            a=' '.join(value)
            data_list.append(a)
        #print(data_list)

    return data_list

def ind_word (ind_to_word,input_data):
    word_list=[]

    with open (ind_to_word) as file:
        for line in file:
            #print(line)
            data = line.strip("\n ")
            #print (data)
            word_list.append(data)


    return word_list



def ind_tag(ind_to_tag,input_data):
    tag_list=[]
    with open(ind_to_tag) as file:
        for line in file:
            #print (line)
            data = line.strip("\n ")
            #print (data)
            tag_list.append(data)
    return tag_list


def temp_func (input_data,word_list,tag_list):

    word_matrix = []
    tag_matrix = []

    for line in input_data:
        line=line.replace("_", " ")
        line=line.split(" ")
        #print(line)
        #len(line)
        tag_conv = []
        word_conv=[]
        for i in range(len(line)):
            if (i%2)==0:
                x=word_list.index(line[i])
                word_conv.append(x)
            else:
                x=tag_list.index(line[i])
                tag_conv.append(x)

        #print (word_conv)
    return word_conv,tag_conv


def normalise_function(matrix):
    if matrix.ndim == 1:

        return matrix/np.sum(matrix)

    else:

        sum = np.sum(matrix, axis=1)
        for i in range(matrix.shape[0]):
            matrix[i,:] = matrix[i,:]/sum[i]
        return matrix



def intitialisation_matrix(pi_matrix,yt):

    pi_matrix[yt] += 1

def transition_matrix(A_matrix,yt, yt_1):

    A_matrix[yt_1][yt] += 1

def emmission_matrix(B_matrix,yt,xt):
    B_matrix[yt][xt] += 1








if __name__ == '__main__':


    train_input = sys.argv[1]
    #test_input=sys.argv[2]
    ind_to_word=sys.argv[2]
    ind_to_tag=sys.argv[3]
    hmmprior=sys.argv[4]
    hmmtrans=sys.argv[5]
    hmmemit=sys.argv[6]


    #print(train_input)
    input_data = data_process(train_input)
    #print(len(input_data))
    word_list = ind_word(ind_to_word, input_data)
    tag_list= ind_tag(ind_to_tag,input_data)


    pi_matrix = np.zeros(len(tag_list))
    A_matrix = np.zeros((len(tag_list), len(tag_list)))
    B_matrix = np.zeros((len(tag_list), len(word_list)))
    #print (B_matrix)

    for line in input_data:
        #line = line.replace("_", " ")
        line = line.split(" ")
        #print(line)
    # len(line)
        x=[]
        for i, word in enumerate(line):
            word,tag = word.split('_')
            xt = word_list.index(word)
            yt = tag_list.index(tag)

            #(B_matrix, tag_index, word_index)

            if i == 0:
                intitialisation_matrix(pi_matrix, yt)

                yt_1 = yt
            else:
                transition_matrix(A_matrix, yt, yt_1)
                yt_1 = yt
            emmission_matrix(B_matrix,yt,xt)

        pi=pi_matrix +1
        A=A_matrix + 1
        B=B_matrix + 1
        pi_normalised = normalise_function(pi)

        A_normalised = normalise_function(A)

        B_normalised = normalise_function(B)



    np.savetxt(hmmprior, pi_normalised)
    np.savetxt(hmmemit, A_normalised)
    np.savetxt(hmmtrans, B_normalised)
