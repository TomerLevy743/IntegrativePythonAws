def split_line_to_values(line, char):
        index = line.find(char)
        value1 = line[:index].strip()
        value2 = line[index+1:].strip()

        return [value1,value2]


def import_data(list_of_dicts, file):
    config_file = open(file,"r")
    i=-1
    for line in config_file:
        if not ":" in line:
            if line != "\n":
                i+=1

            continue

        key_value = list_of_dicts.split_line_to_values(line, ":")
        if "," in key_value[1]:
            key_value[1]= list_of_dicts.split_line_to_values(key_value[1], ",")

        if isinstance(key_value[1],str) and key_value[1].isdigit():
            key_value[1] = int(key_value[1])

        list_of_dicts[i][key_value[0]] = key_value[1]


    config_file.close()
    return False #return dict

