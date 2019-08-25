import os
import re
"""
Library to unify the valence and arousal value into one format

"""



def clean_file(file_name, anno_type):
	"""
	to unify one annotation file
	Args: file_name: the name of annotation, anno_type: type of annotation

	"""
    # read the file
    file_path = "./annotation/" + anno_type + "/" + file_name

    line_data = []

    with open(file_path, 'r') as f:
        for line in f:
            line_data.append(line)
    f.closed

    old_line_data = []
    for line in line_data:
        old_line_data.append(line.replace(",", "."))

	# translate the format into the unified format
    new_line_data = []
    for line in old_line_data:
        print(line)
        data = re.split("\t", line)
        num = data[-1].split("\n")[0]
        num = float(num)/1000.0
        data[-1] = str(num) + "\n"
        data.insert(1, "\t")
        print(data)
        data = "".join(data)
        new_line_data.append(data)

    new_file_name = re.split("(-)", file_name)

    new_file_name.pop(0)
    new_file_name.pop(0)
    new_file_name.pop(-1)
    new_file_name.pop(-1)
    new_file_name.pop(-1)
    new_file_name.pop(-1)

    new_file_name = "".join(new_file_name) + ".txt"

    new_file_path = "./annotation/" + "clean_" + anno_type + "/" + new_file_name


	# write the cleaned representation into a new file
    with open(new_file_path, 'w+') as f:
        for line in new_line_data:
            f.write(line)
    f.closed


def clean_all():
    file_name_a = os.listdir("./annotation/arousal")
    file_name_v = os.listdir("./annotation/valence")

    for file in file_name_a:
        clean_file(file, "arousal")

    for file in file_name_v:
        clean_file(file, "valence")

clean_all()
