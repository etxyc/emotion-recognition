import os
import re

"""
Library to translate the frame based valence arousal annotation file to second based
"""


def clean_file(file_name, anno_type):

	"""
	to translate the frame based valence arousal annotation file to second based
	Args: file_name: name of the annotation files, anno_type: valence or arousal

	"""
    # read the file
    file_path = "./annotation/" + anno_type + "/" + file_name

    line_data = []

    with open(file_path, 'r') as f:
        for line in f:
            line_data.append(line)
    f.closed


    new_line_data = []
    i = 1
    for line in line_data:
        num = line.split("\n")[0]
        print(num)
        f = i/30.000
        f = str(round(f, 3))
        print(f)

        one_line = []
        one_line.append(f)
        one_line.append("\t")
        one_line.append(num)
        one_line.append("\n")

        one_line = "".join(one_line)

        new_line_data.append(one_line)
        i += 1

# write file

    new_file_path = "./annotation/" + "clean_" + anno_type + "/" + file_name

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
