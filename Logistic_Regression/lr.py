# print("omsairam")
import csv
import time
import numpy as np
import math
import sys


def dict_constuct(dict_file):
    d = {}
    with open(dict_file) as file:
        for line in file:
            (key, val) = line.split(" ")
            d[int(val)] = key
    return d


def get_xi(attribute_input, d):
    location_list = [int(i.split(":")[0]) for i in attribute_input]
    final_list = [1] * len(location_list)
    # final_list = [1 if k in sparse_input else 0 for k in d.keys()]
    return final_list, location_list

def predict(input_file, theta,dict_file):
    d = dict_constuct(dict_file)
    labels=[]
    locations=[]
    xis=[]
    row_list=[]
    count = 0
    with open(input_file, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            label = int(row[0])
            attribute_input = row[1:]
            xi, lc = get_xi(attribute_input, d)
            # print (lc)
            xi.append(1)
            lc.append(l_len-1)
            #label.append(1)
            labels.append(label)

            locations.append(lc)
            # print(locations)
            xis.append(xi)


    for i in range(0, len(xis)):
        label = labels[i]

        xi = xis[i]
        location = locations[i]
        xi_new = get_final_xi(location, xi)
        #print(xi_new)
    # print (np.where(np.array(xi_new)==1))
        #print (theta)
        final_prod = probs(xi_new, theta)
        #print (final_prod)

        if final_prod > 0:
            row_list.append(1)
        else:
            row_list.append(0)
        #print(len(row_list))
    string_list = [str(i) for i in row_list]
        #print (string_list)
    formatted_labels=[str(i) for i in labels]
    #print(len(formatted_labels))
    #formatted_list = [string_list[0].split(" ")]
    #print (formatted_list)

    for j in range(len(labels)):

        if formatted_labels[j] == string_list[j]:
            count = count + 1
            misclassification = len(labels) - (count)
            error_rate = float(misclassification / (len(labels)))
            #print(error_rate)
    return row_list,error_rate


def regression(input_file, dict_file, epoch):
    row_list = []
    d = dict_constuct(dict_file)
    global l_len
    l_len = len(d) + 1
    theta = [0.0] * l_len

    theta = np.asarray(theta)
    labels = []
    xis = []
    locations = []
    theta_sparsed = []
    start_data = time.clock()
    with open(input_file, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            label = int(row[0])
            attribute_input = row[1:]
            xi, lc = get_xi(attribute_input, d)
            # print (lc)
            xi.append(1)
            lc.append(l_len-1)
            labels.append(label)
            locations.append(lc)
            # print(locations)
            xis.append(xi)
    print("Data Loaded")
    print(time.clock() - start_data)


    for j in range(epoch):
        for i in range(0, len(xis)):
            theta_sparsed = []
            label = labels[i]
            xi = xis[i]
            xi = np.asarray(xi)
            # print(xi)
            lc = locations[i]
            # print(lc)
            for k in lc:
                theta_sparsed.append(theta[k])
            # print(theta_sparsed)

            #theta_sparsed.insert(0, 0)
            theta_sparsed = np.asarray(theta_sparsed)
            theta += np.asarray(calculate_updates(label, xi, theta_sparsed, lc))
        #print (theta[-1])
    return  theta


def get_final_xi(lc, xi):
    xi_new = [0.0] * l_len
    for k in lc:
        xi_new[k] = 1
    xi_new[-1]=1
    return xi_new


def probs(xi, theta_j):
    prod = np.dot(xi, theta_j)
    return prod


def calculate_updates(label, xi, theta, lc):
    eta = 0.1
    sgd_val = sgd(xi, theta, label)
    valid_ind = []
    theta_update = [(eta * 1.0 * sgd_val) for i in range(0, len(xi))]
    theta_prime = [0.0] * l_len
    for i, k in enumerate(lc):
        theta_prime[k] = theta_update[i]
    # for i in range(0,len(xi)):
    # 	#if xi[i]!=0:
    # 	theta_update[i] = eta*xi[i]*sgd_val
    return theta_prime


def sgd(xi, theta_sparsed, y):
    multiply_result = np.dot(xi, theta_sparsed)
    sum_result = multiply_result
    exp_value = math.exp(sum_result)
    g = float((exp_value) / (1 + exp_value))
    y = float(y)
    sgd_value = (y - g)
    return sgd_value


def write_file(file, row_list):
    f = open(file, "w")
    for i in row_list:
        f.write(str(i))
        f.write("\n")
    f.close()


if __name__ == '__main__':
    start = time.clock()
    input_files = []
    input_files.append(sys.argv[1])
    input_files.append(sys.argv[2])
    input_files.append(sys.argv[3])
    dict_input = sys.argv[4]
    train_out_file = sys.argv[5]
    test_out_file = sys.argv[6]
    metrics = sys.argv[7]
    num_epoch = sys.argv[8]
    ## print("calling for train")
    theta = regression(input_files[0], dict_input, int(num_epoch))
    train_labels, train_error = predict(input_files[0], theta, dict_input)
    test_labels, test_error = predict(input_files[2], theta, dict_input)


    write_file(train_out_file, train_labels)
    write_file(test_out_file, test_labels)

    train_string = "error(train): {0}".format(train_error)
    test_string = "error(test): {0}".format(test_error)
    f = open(metrics, "w")
    f.write(train_string)
    f.write("\n")
    f.write(test_string)
    f.close()



