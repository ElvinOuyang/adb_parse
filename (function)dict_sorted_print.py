def print_dict_sorted(dictionary):
    key_list = []
    for key in dictionary.keys():
        key_list.append(key)
    key_list.sort()
    for key in key_list:
        print(key + ":" + str(dictionary[key]))