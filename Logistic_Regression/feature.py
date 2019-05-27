import csv
import sys

def count_word(process_string):
    total_count = dict()
    words = process_string.split(" ")
    for word in words:
    	if word in total_count.keys():
    		total_count[word] += 1
    	else:
    		total_count[word] = 1
    return total_count

def process_row_1(label, process_string, d):
	new_dict = dict(zip(d.values(), d.keys()))
	words_list = process_string.split(" ")
	final_list = ['{0}:1'.format(new_dict[k]) for k in words_list if k in new_dict]
	final_list.insert(0, label)
	return final_list

def process_row_2(label, process_string, d):
	final_list = []
	new_dict = dict(zip(d.values(), d.keys()))
	count_dict = count_word(process_string)
	words_list = process_string.split(" ")
	final_list = ['{0}:1'.format(new_dict[k]) for k in words_list if (k in new_dict and count_dict.get(k, 4)<4)]
	final_list.insert(0, label)
	return final_list

def dict_constuct(dict_file):
	d = {}
	with open(dict_file) as file:
		for line in file:
			(key, val) = line.split(" ")
			d[int(val)] = key
	return d


def method_1(input_file, dict_file):
	row_list = []
	tsv_output_list = []
	d = dict_constuct(dict_file)
	with open(input_file,'r') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		for row in tsvin:
			if row != []:
				label = row[0]
				process_string = row[1].strip()
				final_string = process_row_1(label, process_string, d)
				final_list = remove_duplicate(final_string)
				tsv_output_list.append(final_list)
	print("\n\n")
	print(tsv_output_list)
	return tsv_output_list

def method_2(input_file, dict_file):
	row_list = []
	tsv_output_list = []
	d = dict_constuct(dict_file)
	with open(input_file,'r') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		for row in tsvin:
			row_list.append(row)
		for row in row_list:
			if row != []:
				label = row[0]
				process_string = row[1].strip()
				final_string = process_row_2(label, process_string, d)
				final_list = remove_duplicate(final_string)
				tsv_output_list.append(final_list)
	print("\n\n")
	print(tsv_output_list)
	return tsv_output_list

			


def remove_duplicate(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 
      


if __name__ == '__main__':
	input_files = []
	output_files = []
	input_files.append(sys.argv[1])
	input_files.append(sys.argv[2])
	input_files.append(sys.argv[3])
	dict_input = sys.argv[4]
	output_files.append(sys.argv[5])
	output_files.append(sys.argv[6])
	output_files.append(sys.argv[7])
	feature_flag = int(sys.argv[8])
	if feature_flag == 1:
		for i in range(len(input_files)):
			tsv_output_list = method_1(input_files[i], dict_input)
			output_file = output_files[i]
			with open(output_file, 'wt') as out_file:
				tsv_writer = csv.writer(out_file, delimiter='\t', lineterminator='\n')
				tsv_writer.writerows(tsv_output_list)
	elif feature_flag == 2:
		for i in range(len(input_files)):
			tsv_output_list = method_2(input_files[i], dict_input)
			output_file = output_files[i]
			with open(output_file, 'wt') as out_file:
				tsv_writer = csv.writer(out_file, delimiter='\t', lineterminator='\n')
				tsv_writer.writerows(tsv_output_list)
	else:
		print("invalid method type")


# single input 
# Method 1 : 21 secs
# Method 2 : 11 secs

# all 3 files 
# Method 1 : 30 secs 
# Method 2 : 14 secs
