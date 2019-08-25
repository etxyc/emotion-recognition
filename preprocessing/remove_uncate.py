import os
import subprocess

UNCATE = 15
HEAD = 99

"""
Library to remove the images without any category label
"""


def clean_one_dire(dir_name):
	"""
	to remove the images without any category label
	Args: the name of video directory

	"""
	# read cate annotation
	name = dir_name.split(".mp4")[0]
	anno_name = "AU_" + name + ".txt"
	anno_path = "./annotation/" + anno_name

	emotion = [HEAD]

	with open(anno_path) as f:
		for line in f:
			first_process = line.split(":")
			if first_process[1] == " N/A\n":
				emotion.append(UNCATE)
			else:

				second_process = first_process[1].split(",")
				third_process = [value for value in second_process if value != "1"]
				third_process = [value for value in third_process if value != "1\n"]

				for i in range(0, 8):
					if third_process[i] == "true" or third_process[i] == " true":
						emotion.append(i)


	# list all image file name
	image_name = os.listdir("./image/" + dir_name)
	image_name.sort()
	# if has  _0, reformat the name
	image_path = "./image/" + dir_name
	for img in image_name:
		if "_0.jpg" in img:
			new_name = img.split("_0.jpg")[0] + ".jpg"
			subprocess.check_output("mv " + image_path + "/" + img + " " + image_path + "/" + new_name, shell=True)

	# list updated image name
	image_name = os.listdir(image_path)
	image_name.sort()

	# check annotation, if no category, mv to proper dir
	uncate_name = dir_name + "_uncate"
	uncate_path = "./image/" + uncate_name
	if not os.path.exists(uncate_path):
		os.makedirs(uncate_path)

	for img in image_name:
		num = img.split(".jpg")[0]
		num = int(num)

#		print(len(emotion))
#		print(num)
		if num >= len(emotion):
			print("Out of Range?")
			print("mv " + "./image/" + dir_name + "/" + img + " " + uncate_path + "/" + img)
			subprocess.check_output("mv " + "./image/" + dir_name + "/" + img + " " + uncate_path + "/" + img, shell=True)

		elif emotion[num] == UNCATE:
			print("uncate")
			print("mv " + "./image/" + dir_name + "/" + img + " " + uncate_path + "/" + img)
			subprocess.check_output("mv " + "./image/" + dir_name + "/" + img + " " + uncate_path + "/" + img, shell=True)



def main():
	# for all directory
	# list all directory
	dir_list = os.listdir("./image")
	print(dir_list)

	for dire in dir_list:
		print(dire + " Starting")
		clean_one_dire(dire)
		print(dire + " Done")

	print("All Done")

if __name__ == "__main__":
	main()
