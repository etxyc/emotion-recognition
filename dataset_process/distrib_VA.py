import numpy as np
import scipy.misc as misc
import os
import cv2
import bisect
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)
UNCATE = 15
HEAD = 99
SEQ_LEN = 60

"""
Library to load valence and arousal data and labels, and visualise the distribution

"""


def read_image(file_name):
	image = cv2.imread(file_name)
	image = cv2.resize(image, (72, 72))
	return image

# Function to load label to two lists, first list is time, second the corresponding value
def load_label(video_name, anno):
	"""
	Load VA labels of a video
	Args: video_name: the name of the video. anno: the annotation, i.e. valence or arousal
	return: time step and the label
	"""
	file_path = "./annotation/" + anno + "/" + video_name + ".txt"

	time = []
	labels = []
	with open(file_path) as f:
		for line in f:
			one_time = float(line.split("\t")[0])
			one_value = line.split("\t")[-1]
			one_value = float(one_value.split("\n")[0])
			time.append(one_time)
			labels.append(one_value)
	return time, labels

def get_closest_value_index(a_list, value):
	"""
	functin to get the index of the closest neighbour
	Args: the list to search, the value to search
	Return: the closest neighbour's index

	"""
	index = bisect.bisect_left(a_list, value)
	if index == 0:
		return 0
	if index == len(a_list):
		return index-1
	left_index = index - 1
	after = a_list[index]
	before = a_list[left_index]
	if before - value >= value - after:
		return left_index
	else:
		return index


def read_label(time, labels, frame_no):
	"""
	to read the V&A labels

	Args: time: the time i video, label: the labels list, frame_no: the frame number of the frame in video
	Return: the frame's label of valence arousal

	"""
	sec = frame_no / 30.0
	n_index = get_closest_value_index(time, sec)
	return labels[n_index]


def read_dir(dir_path):
	"""
	load the valence arousal labels in for all frames in one directory

	Args: the directory path

	Return: data and label

	"""

	# read annotation file into dict

	# get a list of all the image files
	images = os.listdir(dir_path)
	images.sort()

	# read image file, get ndarray
	img_list = []
	for image in images:
		image_path = dir_path + "/" + image
		img_arr = read_image(image_path)
		img_list.append(img_arr)


	# load labels

	print("Loading: " + dir_path)
	name = dir_path.split("/")[-1]
	name = name.split(".mp4")[0]

	a_time, a_labels = load_label(name, "arousal")
	v_time, v_labels = load_label(name, "valence")

	img_sample = []
	labels = []
	f = 0
#	print(images)
	while img_list:
		img_seq = []
		label_seq = []
		for i in range(0, SEQ_LEN):
			if not img_list:
				break
			else:
				img_seq.append(img_list.pop(0))



				frame_num = images[f].split(".jpg")[0]
				frame_num = int(frame_num.split("_0")[0])
				VA_label = []



				VA_label.append(read_label(a_time, a_labels, frame_num))
				VA_label.append(read_label(v_time, v_labels, frame_num))
				label_seq.append(VA_label)
				f += 1

		if len(img_seq) == SEQ_LEN:
			new_seq = np.array(img_seq)
			img_sample.append(new_seq)
			new_labels = np.array(label_seq)
			labels.append(new_labels)

	img_sample = np.array(img_sample)
	labels = np.array(labels)

#	print(img_sample.shape)
#	print(labels.shape)
	return img_sample, labels

def VA_distribution(labels):
	"""
	to get the distribution of valence and arousal
	Args: V, A labels
	Return: V, A distribution

	"""

	[rows, cols] = labels.shape
	A = []
	V = []
	for i in range(rows):
		for j in range(cols):
			if j == 0:
				A.append(labels[i, j])
			if j == 1:
				V.append(labels[i, j])
	return A, V

def read_all_dir():

	"""
	Load valence and arousal labels for all the videos in the directory
	Visualize the distribution

	Return: data and labels

	"""
	current_path = os.getcwd()
	print(current_path)
	dir_list = os.listdir("./dataset/training")

	samples, labels = read_dir(current_path + "/dataset/training/" + dir_list.pop(0))

	for dire in dir_list:
		dire = current_path + "/dataset/training/" + dire
		img_sample, label = read_dir(dire)
		if img_sample.shape[0] > 0:
			samples = np.append(samples, img_sample, axis=0)
			labels = np.append(labels, label, axis=0)

	print(samples.shape)
	print(labels.shape)


	labels = labels.reshape(-1, labels.shape[-1])

	print(labels.shape)
	A, V = VA_distribution(labels)

	figure = plt.hist(A, bins=30)
	plt.title("Arousal Annotation")
	plt.xlabel("arousal value")
	plt.show()

	figure = plt.hist(V, bins=30)
	plt.title("Valence Annotation")
	plt.xlabel("valence value")
	plt.show()


	return samples, labels


read_all_dir()
