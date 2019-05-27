import sys
import numpy as np
import pdb
def data_process(test_input):
    data_list = []
    with open(test_input) as file:
        for line in file:
            if len(line)==0:
                continue
            a=[]
            #print (line)
            data = line.strip("\n")
            value= data.split(" ")
            #print (value)
            a=' '.join(value)
            data_list.append(a)
        print (len(data_list))

    return data_list


def ind_word (ind_to_word,input_data):
    word_list=[]

    with open (ind_to_word) as file:
        for line in file:
            #print(line)
            data = line.strip("\n ")
            #print (data)       ####Strip blank spaces
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


def normalise_function(list1):

 ###### Check the dimensions and then do. IF it's a matrix, this condition won't work

    sum = np.sum(list1)
    for i in range(len(list1)):
        list1[i] = list1[i]/sum
    return list1


def normalise_function_matrix(list1):
    ###### Check the dimensions and then do. IF it's a matrix, this condition won't work

    sum = np.sum(list1)
    for i in range(len(list1)):
        list1[i] = list1[i] / sum
        return list1



if __name__ == '__main__':



    test_input = sys.argv[1]
    ind_to_word=sys.argv[2]
    ind_to_tag=sys.argv[3]
    hmmprior=sys.argv[4]
    hmmemit=sys.argv[5]
    hmmtrans=sys.argv[6]
    predicted_file=sys.argv[7]
    metric_file=sys.argv[8]

    input_data=data_process(test_input)
    word_list= ind_word (ind_to_word,input_data)
    tag_list = ind_tag(ind_to_tag, input_data)
    #print (word_list)
    #print (input_data)

    B_matrix=np.genfromtxt(hmmemit)
    #print (B_matrix.shape)
    #exit()
    A_matrix = np.genfromtxt(hmmtrans)
    pi_matrix=np.genfromtxt(hmmprior)


# Alpha matrix formation:

    length_list = []
    temp = []
    log_list = []
    count = 0
    total_length = len(input_data)
    with open(predicted_file, "w") as f:
        for idx,line in enumerate(input_data):
            # print (input_data)
            #print (line)

            line = line.split(" ")
            word_matrix=[]
            bi_matrix = []
            alpha_matrix=[]
            beta_matrix=[]
            predict_tag_list = []
            beta_matrix=[]
            #print(line)
            if idx == 0:
                length_list.append(len(line))
            else:
                length_list.append(length_list[idx - 1] + len(line))

            for i, word in enumerate(line):

                word,tag = word.split('_')
                #print (word)

                tag_index = tag_list.index(tag)
                #print (tag_index)

                word_index = word_list.index(word)
                #print (word_index)

                # Alpha Calculation

                if i==0:
                    #pdb.set_trace()
                    bi=B_matrix[:, word_index]                       ##### ( 9 cross 1)
                    #print (bi)

                    alpha_initial=pi_matrix*bi                       ##### ( 9 cross 1)
                    #print (alpha_initial)
                    alpha=alpha_initial
                    if len(line)==1:
                        pass
                    else:
                        normalise_function(alpha_initial)
                    alpha_matrix.append(alpha_initial)
                    bi_matrix.append(bi)

                else:

                    bi=(B_matrix[:, word_index])
                    #print (bi)
                    A_trans=np.transpose(A_matrix)
                    var=np.dot(A_trans,alpha)
                    alpha_t= np.multiply(bi,var)
                    if i < len(line)-1:
                        normalise_function(alpha_t)

                    alpha=alpha_t                                                                         ###Normalise both alpha and alpha-t
                    alpha_matrix.append(alpha_t)
                    #bi_matrix.append(bi)

    # Important
            alpha_matrix=np.asarray(alpha_matrix)
            # print(alpha_matrix)


            #Beta Calculation
            beta_final = np.ones(len(tag_list))
            beta = beta_final
            beta_matrix.append(beta_final)
            for i, word in enumerate(line[::-1]):
                #print (i)

                word,tag = word.split('_')
                tag_index = tag_list.index(tag)
                word_index = word_list.index(word)

                if i < len(line)-1:
                    bi=(B_matrix[:, word_index])
                    var=bi*beta
                    beta_t= np.dot(A_matrix,var)

                    beta=beta_t

                    beta_matrix.append(beta_t)
            beta_matrix=list(reversed(beta_matrix))
            beta_matrix=np.asarray(beta_matrix)
            # print (beta_matrix[::-1])



            for i, word  in enumerate(line):
                prod= alpha_matrix[i] * beta_matrix[i]
                predict_tag= np.argmax(prod)
                predict_tag_list.append(predict_tag)
                word, tag = word.split('_')
                #pdb.set_trace()
                predicted_tag_value = tag_list[predict_tag]
                #print (predicted_tag_value)'
                if predicted_tag_value == tag:
                    count +=1
                temp.append((word) + '_' + str(predicted_tag_value))
            # print(temp)


            if idx == 0:
                l2 = length_list[idx]
                l1 = 0
            else:
                l1 = length_list[idx-1]
                l2 = length_list[idx]
            curr_line = temp[l1:l2]
            #print (curr_line)
            for j in range(len(curr_line)):
                if j==0:
                    pass
                else:
                    f.write(' ')
                f.write(curr_line[j].rstrip())
                # print (curr_line[j])
            if idx < total_length-1:
                f.write('\n')

            log_list.append(np.log(np.sum(alpha_matrix[-1])))

        log_list = np.array(log_list)
        average_log = np.mean(log_list)
        accuracy = count/len(temp)

    with open (metric_file, "w") as files:
        value = "Average Log-Likelihood:" + str(average_log)
        files.write(value)
        files.write('\n')
        value = "Accuracy:"+ str(accuracy)
        files.write(value)
        files.close




        # print(predict_tag_list)








        #Prediction:

        #alpha_norm=normalise_function(alpha)
        #prod_alphabeta= np.multiply(alpha_matrix,beta_matrix)
        #predicted_tag=np.argmax(prod_alphabeta)



        #Log-Likelihood

            #print (alpha_t)
            #log_likelihood = sum(np.log(np.sum(alpha_t)))

        #print (log_likelihood)
        # log_list.append(log_likelihood)



                #average = sum(log_list) / float(len(log_list))


            # Writing/Structuring test output


        # for i in range(len(temp)):
        #    f = open(predicted_file, "w")
        #    f.write(temp)
        #    f.write(" ")
        #    f.close()

    ##### Log likelihood

    # sum=np.sum(alpha_matrix[:,0],axis=0)
    # print (sum)
    # log_calc=np.log(sum)
    # print (log_calc)
    # log_likelihood=np.sum(log_calc)
    # print(log_likelihood)

0.8592352741878994, 0.8312727388767162, 0.7270215331001525, 0.7865678076778487, 0.7847476837218063, 0.912119612662637, 0.67057942542617, 0.7194679508342702, 0.9277139992135912, 0.8071893721280601, 0.7609701433798587, 0.8519416054179478, 0.9122038444839401, 0.6801368586574706, 0.45766525609972564, 0.8857992723928138, 0.8827048069391623, 0.82136910827925, 0.7901325779136708, 0.8329231754435648

