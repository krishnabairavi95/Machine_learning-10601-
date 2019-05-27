import csv
import random
import numpy as np
import math
import sys



def forward_prop(input_file,test_file,hidden_count, init_flag,sigmoid,softmax,epoch):
    label = []
    xi = []

    with open(input_file, 'r') as csvin:
        csvin = csv.reader(csvin, delimiter='\n')

        for row in csvin:
            q = row[0].split(',')

            w = []
            for i in range(len(q)):
                tmp = int(q[i])
                w.append(tmp)
            y = w[0]
            label.append(y)
            x = w[1:]
            x = [1]+x
            s = len(x)
            xi.append(x)
            l = len(label)


       # print (label)
        input_length=len(xi)

        xi = np.asarray(xi)
        #print (init_flag.type)

       # print (s)
        #print (hidden_count)

        if init_flag== 2:
            alpha = np.zeros((s, hidden_count), dtype=float)
            beta = np.zeros((hidden_count + 1, 10), dtype=float)

        elif init_flag == 1:
            alpha = np.random.uniform(low=-0.1, high=0.1, size=(s, hidden_count))
            beta = np.random.uniform(low=-0.1, high=0.1, size=(hidden_count + 1, 10))

            # print (beta.shape)

        J_train_loss=[]
        J_test_loss=[]
        predict_label=[]
        #print (len(xi))
        #print (epoch)
        for k in range(epoch):
            one_hot_matrix = []
            ycap_whole = []
            ycap_matrix = []
            for j in range(len(xi)):
                #lab = label[j]
                # print(lab)

                #print ('hpp')
              # count=count+1
               # print (count)
                first_prod = np.dot(xi[j], alpha)
                #print(xi[j].shape)
                #print (first_prod)
                z = sigmoid(first_prod)
                #print (z)
                z = [1]+z.tolist()
                zi = np.transpose(np.expand_dims(np.array(z), axis=1))
                #zi=np.insert(z,0,1)
                #print (zi.shape)
                #print (beta)

                second_prod = np.dot(zi, beta)
                #print (second_prod)
                # print (np.exp(second_prod)/np.sum(np.exp(second_prod)))
                # print(second_prod.shape)
                ycap = softmax(second_prod)
                #print (ycap)

                result = np.array(ycap).flatten()
                result=result.tolist()
                ycap_matrix = ycap


                # ycap_matrix.append(ycap)
                # print(ycap_matrix)
                ycap_length = len(ycap)

                one_hot_y = [0] * 10
                x=label[j]
                one_hot_y[x] = 1
                #print (one_hot_y)
                #one_hot_label = one_hot(input_length, label)
                one_hot_label = np.transpose(np.expand_dims(np.array(one_hot_y),axis=1))

                g_ycap = -(one_hot_label / ycap_matrix)
                #print(g_ycap)

                g_b = ycap_matrix - one_hot_label

                #print (g_b.shape)
                g_b_t = np.transpose(g_b)
                #print (g_b_t.shape)
                #zi = np.asmatrix(zi)
                #print (zi)
                #print (zi.shape)

                g_beta = np.dot(g_b_t, zi)
                g_beta = np.transpose(g_beta)


                #print(g_b_t.shape)
                g_z = np.dot(beta, g_b_t)
                g_z=np.transpose(g_z)
                #print(g_z.shape)
                #g_z=np.delete(g_z,0)
                #print(zi.shape)
                #zi=np.delete(zi,0)
                #print (zi)
                g_a = g_z * zi * (1-zi)
                #print(g_a)

                #g_a_t = np.transpose(g_a)
                #print(g_a_t)

                #xi = np.asmatrix(xi)


                g_a = g_a[:,1:]
                g_a_t=np.transpose(g_a)
                #print (g_a_t.shape)

                g_alpha = np.dot(g_a_t, np.transpose(np.expand_dims(xi[j], axis=1)))
                g_alpha = np.transpose(g_alpha)
                #print (g_alpha)

                #print (alpha.shape)
                #print (g_alpha)

                #print (g_beta)
                #print (alpha)
                #print (gamma * g_beta)
                #print (g_alpha)
                #print (g_beta)
                alpha= alpha-(learning_rate * g_alpha)
                beta= beta-(learning_rate* g_beta)
                #print(alpha)
                #print(beta)

                one_hot_matrix.append(one_hot_y)
                ycap_whole.append(result)

            test_ycap,error_rate,one_hot_predict, ycap_total=predict(test_input,alpha,beta,sigmoid,softmax)
            train_ycap, train_error_rate, train_one_hot_predict, train_ycap_total = predict(train_input, alpha, beta, sigmoid, softmax)
            #print (one_hot_predict)
            #predict_label.append(ycap_total)
            #print (predict_label)

            predict_length=len(test_ycap)

            #print (len(one_hot_matrix[0]))
            #print (len(one_hot_predict[0]))

            #print (ycap_whole)
            #print ('##########################')
            #print (ycap_total)

            #print (predict_length)
            J_test=cross_entropy(one_hot_predict,ycap_total,predict_length)
            J_test_loss.append(J_test)


            J_train= cross_entropy(train_one_hot_predict,train_ycap_total,len(train_ycap))
            J_train_loss.append(J_train)
            #print (J_loss)

        return alpha, beta,J_train_loss,J_test_loss




def predict(input_file,alpha,beta,sigmoid,softmax):
    label = []
    xi = []
    ycap_test=[]
    ycap_label=[]
    ycap=[]
    one_hot_matrix = []
    ycap_whole = []
    ycap_matrix = []
    with open(input_file, 'r') as csvin:
        csvin = csv.reader(csvin, delimiter='\n')

        for row in csvin:
            q = row[0].split(',')

            w = []
            for i in range(len(q)):
                tmp = int(q[i])
                w.append(tmp)
            y = w[0]
            label.append(y)
            x = w[1:]
            x.insert(0, 1)
            s = len(x)
            xi.append(x)
            l = len(label)

        input_length = len(xi)
        #print(input_length)
        xi = np.asarray(xi)

        for j in range(len(xi)):
            one_hot_y = [0] * 10
            x = label[j]
            one_hot_y[x] = 1
            one_hot_label = np.array(one_hot_y)
            one_hot_matrix.append(one_hot_label)
            first_prod = np.dot(xi[j], alpha)
            print (first_prod.shape)
            z=sigmoid(first_prod)
            zi = np.insert(z, 0, 1)
            second_prod = np.dot(zi, beta)
            ycap = softmax(second_prod)

            result = np.array(ycap).flatten()
            result = result.tolist()
            ycap_matrix.append(result)

            ycap_test.append(result)
            ind=np.argmax(ycap)
            ycap_label.append(ind)


        ycap_length=len(ycap_label)

        #print(ycap_label)
        count = 0
        for j in range(len(label)):
            #print (ycap_label[j])
            if label[j] == ycap_label[j]:
                count = count + 1
                misclassification = len(label) - count
                #print(misclassification)
                error_rate = float(misclassification) / (len(label))

        #print(error_rate)


        #J_loss=cross_entropy(ycap,label)
        #print(J_loss)


      #  f = open(met, "w")
       # f.write(train_string)
        #f.write("\n")
       # f.write(test_string)
       # f.close()
    return ycap_label,error_rate,one_hot_matrix,ycap_test



def sigmoid(product):
    #print(product)
    sig=1/(1+(np.exp(-product)))
    return sig

def softmax(x):
    a=np.exp(x) / np.sum(np.exp(x))
    return a



def cross_entropy(y,ycap,input_length):

 #   print (ycap.shape)
  #  print(y.shape)
    objc_fn=0.0
    for n in range(input_length):
        for j in range(10):
            s = -(1 / input_length)
            #print (s)
            objc_fn += (y[n][j] * np.log(ycap[n][j]))
    obj_fn = objc_fn * s
    return obj_fn



def write_file(file, row_list):
    f = open(file, "w")
    for i in row_list:
        f.write(str(i))
        f.write("\n")
    f.close()





if __name__ == '__main__':


    train_input= sys.argv[1]
    test_input= sys.argv[2]
    train_output=sys.argv[3]
    test_output=sys.argv[4]
    metrics_out=sys.argv[5]
    epoch=int(sys.argv[6])
    hidden_count=int(sys.argv[7])

    init_flag=int(sys.argv[8])


    learning_rate=float(sys.argv[9])


    alpha_train, beta_train,J_train_loss,J_test_loss = forward_prop(train_input,test_input, hidden_count, init_flag, sigmoid, softmax, epoch)


    train_label, train_error_rate,one_hotted,ytt = predict(train_input, alpha_train, beta_train, sigmoid, softmax)
    test_label, test_error_rate,one_hotted,ytt = predict(test_input, alpha_train, beta_train, sigmoid, softmax)
    print(J_train_loss)
    print(J_test_loss)

    f = open(metrics_out, "w")
    train_string_3 = "error(train): {0}".format(train_error_rate)
    test_string_4 = "error(test): {0}".format(test_error_rate)

    f = open(metrics_out, "w")
    for i in range(len(J_train_loss)):
        #J_train_loss[int[i]] = i
        #a = np.array2string(J_train_loss[i])
        #a = a.replace("[ ", "")
        #a = a.replace(".]", "")
        a = str(i+1)
        print("epoch=" + a + " crossentropy(train): " + str(J_train_loss[i]))
        print("epoch=" + a + " crossentropy(train): " + str(J_test_loss[i]))

        f.write("epoch=" + a + " crossentropy(train): " + str(J_train_loss[i]))
        f.write("\n")
        f.write("epoch=" + a + " crossentropy(test): "+ str(J_test_loss[i]))
        f.write("\n")
    f.write(train_string_3)
    f.write("\n")
    f.write(test_string_4)
    f.close()

    #print("epoch=" + a + " crossentropy(train): " + str(J_train_loss[i]))
    #print("epoch=" + a + " crossentropy(test): "+ str(J_test_loss[i]))


    #train_string_3 = "error(train): {0}".format(train_error_rate)
    #test_string_4 = "error(test): {0}".format(test_error_rate)
    #f = open(metrics_out, "w")
    #f.write(train_string_1)
    #f.write("\n")
    #f.write(train_string_2)
    #f.write("\n")
    #f.write(train_string_3)
    #f.write("\n")
    #f.write(test_string_4)
    #f.close()


    write_file(train_output, train_label)
    write_file(test_output,test_label)

